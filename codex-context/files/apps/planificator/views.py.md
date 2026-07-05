# apps/planificator/views.py

Generated: `2026-07-05T21:21:12`

## Scope

- Real source file: `apps/planificator/views.py`
- App: `planificator`
- App guide: `codex-context/apps/planificator.md`
- Role: `backend`
- Size: 32362 bytes
- Source SHA-256: `620c0702c0f3909d77905a09dd1ba6540cf981a8d226bfef2fb3f9c261f28a46`

## Codex usage

Use this context only when the task directly touches this file or requires this file for routing. The real source file remains the source of truth before editing.

## Source

```python
import base64
import csv
import json
import logging
from io import StringIO
from pathlib import Path
from zipfile import BadZipFile

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import Http404, HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.utils import timezone
from django.views import View
from django.views.generic import ListView, TemplateView
from docx.opc.exceptions import PackageNotFoundError

from .constants import ROMANIAN_MONTH_NAMES
from .file_handlers import create_excel_export, read_tabular_rows
from .forms import (
    SafeCoursePreviewForm,
    ScheduleExportForm,
    ScheduleGeneratorForm,
    WordMatchGenerationForm,
    WordMatchUploadForm,
    XmlExportForm,
    normalize_schedule_initial,
)
from .presentation import build_preview_rows, build_source_preview, selected_month_headers
from .selectors import get_owned_generation, list_owned_generations
from .services import (
    GenerationSourceUnavailable,
    GenerationWorkflowError,
    create_schedule_generation,
)
from .settings_store import get_settings, save_settings
from .validators import (
    MAX_JSON_BYTES,
    ClientInputError,
    require_int,
    require_list,
    require_string,
)
from .word_matching import apply_word_matches, build_word_match_preview, read_schedule_rows
from .wp_course_updater import (
    WPCourseClient,
    WordPressRequestError,
    build_final_program,
    extract_slug_from_permalink,
    parse_effective_end_date,
    parse_excel_dates_from_row,
    valid_existing_program,
)
from .xml_export import create_xml_export, read_xml_schedule

logger = logging.getLogger(__name__)


class PlanificatorPermissionMixin(LoginRequiredMixin, PermissionRequiredMixin):
    permission_required = "planificator.use_course_planning"


class WordMatcherPermissionMixin(LoginRequiredMixin, PermissionRequiredMixin):
    permission_required = "planificator.use_word_matcher"


class XmlExportPermissionMixin(LoginRequiredMixin, PermissionRequiredMixin):
    permission_required = "planificator.use_xml_export"


def _form_error(form, fallback: str) -> str:
    for errors in form.errors.values():
        if errors:
            return str(errors[0])
    return fallback


def _json_error(message: str, *, status: int = 400) -> JsonResponse:
    return JsonResponse({"success": False, "error": message}, status=status)


def _json_request_data(request: HttpRequest) -> dict:
    if request.content_type != "application/json":
        raise ClientInputError("Cererea trebuie trimisă ca JSON.")
    if len(request.body) > MAX_JSON_BYTES:
        raise ClientInputError("Cererea este prea mare.", status=413)
    try:
        payload = json.loads(request.body.decode("utf-8") or "{}")
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ClientInputError("Cererea nu conține un obiect JSON valid.") from exc
    if not isinstance(payload, dict):
        raise ClientInputError("Cererea trebuie să conțină un obiect JSON.")
    return payload


def build_generator_form(user, *, source_generation_id=None) -> ScheduleGeneratorForm:
    settings = get_settings("schedule_generator", user)
    initial = normalize_schedule_initial(settings)
    if source_generation_id:
        initial["source_generation_id"] = source_generation_id
    return ScheduleGeneratorForm(initial=initial)


def generator_context(form: ScheduleGeneratorForm, **extra) -> dict:
    if form.is_bound and hasattr(form, "cleaned_data"):
        months = list(form.cleaned_data.get("months", []))
        holidays = list(form.cleaned_data.get("holidays", []))
    else:
        months = [int(month) for month in form.initial.get("months", []) if str(month).isdigit()]
        holidays_value = form.initial.get("holidays", "")
        holidays = [value.strip() for value in str(holidays_value).splitlines() if value.strip()]
    context = {
        "form": form,
        "selected_months": months,
        "selected_month_count": len(months),
        "selected_month_headers": selected_month_headers(months),
        "holiday_count": len(holidays),
        "working_days_label": "Luni – vineri",
        "page_messages": [],
        "preview_rows": [],
        "source_preview_rows": [],
        "unscheduled_courses": {},
    }
    context.update(extra)
    return context


class PeriodGeneratorView(PlanificatorPermissionMixin, TemplateView):
    template_name = "planificator/generator_perioade.html"

    def get_context_data(self, **kwargs):
        form = kwargs.pop("form", None) or build_generator_form(self.request.user)
        return generator_context(form, **super().get_context_data(**kwargs))

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        form = ScheduleGeneratorForm(request.POST, request.FILES)
        if not form.is_valid():
            context = generator_context(
                form,
                page_messages=[{
                    "level": "error",
                    "title": "Formularul este incomplet",
                    "body": "Corectează câmpurile marcate și încearcă din nou.",
                }],
            )
            return self.render_to_response(context, status=getattr(form, "upload_error_status", 400))

        try:
            workflow = create_schedule_generation(
                owner=request.user,
                upload=form.cleaned_data.get("input_file"),
                source_generation_id=form.cleaned_data.get("source_generation_id"),
                year=form.cleaned_data["year"],
                months=form.cleaned_data["months"],
                randomness=form.cleaned_data["randomness"],
                holidays=form.cleaned_data["holidays"],
            )
            if workflow.unscheduled_courses:
                context = generator_context(
                    form,
                    uploaded_file_name=workflow.source_file_name,
                    unscheduled_courses=workflow.unscheduled_courses,
                    generation_error="Programul nu poate fi salvat deoarece unele combinații curs/lună lipsesc.",
                    page_messages=[{
                        "level": "error",
                        "title": "Program incomplet",
                        "body": "Ajustează lunile sau zilele nelucrătoare și încearcă din nou.",
                    }],
                )
                return self.render_to_response(context, status=400)
            return redirect(
                "planificator:generator_perioade_result",
                generation_id=workflow.generation.pk,
            )
        except GenerationSourceUnavailable as exc:
            form.add_error("input_file", exc.message)
            return self.render_to_response(
                generator_context(
                    form,
                    page_messages=[{
                        "level": "warning",
                        "title": "Fișier necesar",
                        "body": exc.message,
                    }],
                ),
                status=exc.status,
            )
        except GenerationWorkflowError as exc:
            form.add_error(None, exc.message)
            context = generator_context(
                form,
                uploaded_file_name=exc.source_file_name,
                page_messages=[{
                    "level": "error",
                    "title": "Datele nu pot fi procesate",
                    "body": exc.message,
                }],
            )
            return self.render_to_response(context, status=exc.status)
        except ClientInputError as exc:
            form.add_error(None, exc.message)
            return self.render_to_response(
                generator_context(
                    form,
                    page_messages=[{
                        "level": "error",
                        "title": "Datele nu pot fi procesate",
                        "body": exc.message,
                    }],
                ),
                status=exc.status,
            )
        except Http404:
            raise
        except Exception:
            logger.exception("Unexpected schedule generation failure", extra={"user_id": request.user.pk})
            form.add_error(None, "Fișierul nu a putut fi procesat.")
            return self.render_to_response(
                generator_context(
                    form,
                    page_messages=[{
                        "level": "error",
                        "title": "Eroare la procesare",
                        "body": "Verifică structura fișierului și încearcă din nou.",
                    }],
                ),
                status=400,
            )


class ScheduleResultView(PlanificatorPermissionMixin, TemplateView):
    template_name = "planificator/generator_perioade.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        generation = get_owned_generation(
            generation_id=self.kwargs["generation_id"],
            user=self.request.user,
        )
        form = build_generator_form(self.request.user, source_generation_id=generation.pk)
        context.update(
            generator_context(
                form,
                generation=generation,
                schedule=generation.schedule,
                preview_rows=build_preview_rows(generation.schedule, generation.selected_months),
                source_preview_rows=build_source_preview(generation.schedule),
                source_course_count=generation.source_course_count,
                source_file_digest=generation.source_file_digest[:12],
                uploaded_file_name=generation.source_file_name,
                selected_months=generation.selected_months,
                selected_month_count=len(generation.selected_months),
                selected_month_headers=selected_month_headers(generation.selected_months),
                export_form=ScheduleExportForm(initial={"generation_id": generation.pk}),
            )
        )
        return context


class ScheduleHistoryDetailView(ScheduleResultView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["history_read_only"] = True
        return context


class CourseRefreshView(PlanificatorPermissionMixin, TemplateView):
    template_name = "planificator/actualizeaza_cursuri.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = SafeCoursePreviewForm()
        context["updater_settings"] = get_settings(
            "safe_course_date_updater",
            self.request.user,
        )
        return context


def _wp_client_from_payload(payload: dict) -> WPCourseClient:
    return WPCourseClient(
        payload["wp_base_url"],
        payload.get("wp_username", ""),
        payload.get("wp_app_password", ""),
    )


def _validate_wp_payload(
    payload: dict,
    *,
    allowed_fields: set[str],
    require_credentials: bool = True,
) -> dict:
    unknown = sorted(set(payload) - allowed_fields)
    if unknown:
        raise ClientInputError(f"Unknown request field: {unknown[0]}.")
    clean = {
        "wp_base_url": require_string(
            payload.get("wp_base_url"),
            "wp_base_url",
            allow_empty=False,
        )
    }
    if "wp_username" in allowed_fields:
        clean["wp_username"] = require_string(
            payload.get("wp_username", ""),
            "wp_username",
            allow_empty=not require_credentials,
            max_length=150,
        )
    if "wp_app_password" in allowed_fields:
        clean["wp_app_password"] = require_string(
            payload.get("wp_app_password", ""),
            "wp_app_password",
            allow_empty=not require_credentials,
            max_length=500,
        )
    for field in ("permalink", "slug"):
        if field in allowed_fields:
            clean[field] = require_string(
                payload.get(field, ""),
                field,
                max_length=2048 if field == "permalink" else 300,
            )
    if "post_id" in allowed_fields and payload.get("post_id") not in (None, ""):
        clean["post_id"] = require_int(
            payload["post_id"],
            "post_id",
            minimum=1,
            maximum=2_147_483_647,
        )
    for field in ("excel_dates", "final_dates"):
        if field in allowed_fields:
            dates = require_list(payload.get(field, []), field, max_items=1000)
            clean_dates = []
            for value in dates:
                date_value = require_string(value, field, allow_empty=False, max_length=50)
                if parse_effective_end_date(date_value) is None:
                    raise ClientInputError(f'Field "{field}" contains an invalid date.')
                clean_dates.append(date_value)
            clean[field] = clean_dates
    return clean


class CourseRefreshPreviewView(PlanificatorPermissionMixin, View):
    def post(self, request: HttpRequest, *args, **kwargs) -> JsonResponse:
        form = SafeCoursePreviewForm(request.POST, request.FILES)
        if not form.is_valid():
            return _json_error(
                _form_error(form, "Selectează un fișier CSV sau XLSX."),
                status=getattr(form, "upload_error_status", 400),
            )
        try:
            upload = form.cleaned_data["input_file"]
            raw_rows = read_tabular_rows(upload.read(), form.file_extension)
            if not raw_rows:
                raise ClientInputError("Input file must contain Title and Permalink columns.")
            header = [str(value or "").strip() for value in raw_rows[0]]
            normalized_columns = {
                name.lower(): index for index, name in enumerate(header) if name
            }
            missing = [
                name for name in ("title", "permalink") if name not in normalized_columns
            ]
            if missing:
                raise ClientInputError("Input file must contain Title and Permalink columns.")

            today = timezone.localdate()
            rows = []
            for row_index, values in enumerate(raw_rows[1:]):
                if not any(str(value or "").strip() for value in values):
                    continue
                row = {
                    header[index]: values[index] if index < len(values) else ""
                    for index in range(len(header))
                }
                title = str(row.get(header[normalized_columns["title"]], "") or "").strip()
                permalink = str(
                    row.get(header[normalized_columns["permalink"]], "") or ""
                ).strip()
                slug = extract_slug_from_permalink(permalink)
                excel_dates = parse_excel_dates_from_row(row)
                excel_only_program = build_final_program([], excel_dates, today)
                excel_only_dates = [item["data"] for item in excel_only_program]
                row_payload = {
                    "row_index": row_index,
                    "title": title,
                    "permalink": permalink,
                    "slug": slug,
                    "post_id": None,
                    "existing_valid_dates": [],
                    "excel_dates": excel_dates,
                    "final_dates": excel_only_dates,
                    "status": "preview ready",
                    "error": None,
                    "can_update": bool(slug and excel_only_dates),
                    "payload": {
                        "acf": {
                            "program": excel_only_program if excel_only_program else False
                        }
                    },
                }
                if not permalink:
                    row_payload["status"] = "error"
                    row_payload["error"] = "Missing permalink."
                elif not slug:
                    row_payload["status"] = "error"
                    row_payload["error"] = "Unable to extract slug from permalink."
                rows.append(row_payload)
            return JsonResponse({"success": True, "rows": rows})
        except ClientInputError as exc:
            return _json_error(exc.message, status=exc.status)
        except (ValueError, KeyError, TypeError, UnicodeError, BadZipFile, OSError):
            return _json_error("Unable to read the uploaded schedule file.")


class CourseRefreshConnectView(PlanificatorPermissionMixin, View):
    def post(self, request: HttpRequest, *args, **kwargs) -> JsonResponse:
        try:
            payload = _validate_wp_payload(
                _json_request_data(request),
                allowed_fields={"wp_base_url", "wp_username", "wp_app_password"},
            )
            user = _wp_client_from_payload(payload).test_connection()
            save_settings(
                "safe_course_date_updater",
                request.user,
                {
                    "wp_base_url": payload["wp_base_url"],
                    "wp_username": payload["wp_username"],
                },
            )
            return JsonResponse(
                {
                    "success": True,
                    "message": "Connected",
                    "user": {
                        "id": user.get("id"),
                        "name": user.get("name")
                        or user.get("slug")
                        or payload["wp_username"],
                    },
                }
            )
        except ClientInputError as exc:
            return _json_error(exc.message, status=exc.status)
        except WordPressRequestError as exc:
            return _json_error(str(exc), status=502)


class CourseRefreshResolveView(PlanificatorPermissionMixin, View):
    def post(self, request: HttpRequest, *args, **kwargs) -> JsonResponse:
        try:
            payload = _validate_wp_payload(
                _json_request_data(request),
                allowed_fields={
                    "wp_base_url",
                    "wp_username",
                    "wp_app_password",
                    "permalink",
                    "slug",
                },
                require_credentials=False,
            )
            permalink = payload.get("permalink", "")
            slug = payload.get("slug", "") or extract_slug_from_permalink(permalink)
            if not slug:
                raise ClientInputError("Missing slug/permalink.")
            post_id = _wp_client_from_payload(payload).resolve_course_post_id(
                slug=slug,
                permalink=permalink,
            )
            if not post_id:
                return _json_error(
                    "Could not resolve post ID from REST slug lookup.",
                    status=404,
                )
            return JsonResponse({"success": True, "post_id": int(post_id)})
        except ClientInputError as exc:
            return _json_error(exc.message, status=exc.status)
        except WordPressRequestError as exc:
            return _json_error(str(exc), status=502)


class CourseRefreshFetchDatesView(PlanificatorPermissionMixin, View):
    def post(self, request: HttpRequest, *args, **kwargs) -> JsonResponse:
        try:
            payload = _validate_wp_payload(
                _json_request_data(request),
                allowed_fields={
                    "wp_base_url",
                    "wp_username",
                    "wp_app_password",
                    "permalink",
                    "slug",
                    "post_id",
                    "excel_dates",
                },
            )
            permalink = payload.get("permalink", "")
            slug = payload.get("slug", "") or extract_slug_from_permalink(permalink)
            if not slug:
                raise ClientInputError("Missing slug/permalink.")
            client = _wp_client_from_payload(payload)
            post_id = client.resolve_course_post_id(
                slug=slug,
                permalink=permalink,
                fallback_post_id=payload.get("post_id"),
            )
            if not post_id:
                return _json_error(f"Course not found by slug: {slug}", status=404)
            existing_program = (
                client.get_course(int(post_id)).get("acf", {}).get("program") or []
            )
            today = timezone.localdate()
            current_valid = [
                item["data"] for item in valid_existing_program(existing_program, today)
            ]
            final_valid = [
                item["data"]
                for item in build_final_program(
                    existing_program,
                    payload.get("excel_dates", []),
                    today,
                )
            ]
            final_program = [{"data": value} for value in final_valid]
            return JsonResponse(
                {
                    "success": True,
                    "post_id": int(post_id),
                    "existing_valid_dates": current_valid,
                    "final_dates": final_valid,
                    "payload": {
                        "acf": {"program": final_program if final_program else False}
                    },
                    "can_update": bool(final_valid),
                }
            )
        except ClientInputError as exc:
            return _json_error(exc.message, status=exc.status)
        except WordPressRequestError as exc:
            return _json_error(str(exc), status=502)
        except (TypeError, ValueError, KeyError):
            return _json_error("WordPress returned invalid course data.")


class CourseRefreshUpdateRowView(PlanificatorPermissionMixin, View):
    def post(self, request: HttpRequest, *args, **kwargs) -> JsonResponse:
        try:
            payload = _validate_wp_payload(
                _json_request_data(request),
                allowed_fields={
                    "wp_base_url",
                    "wp_username",
                    "wp_app_password",
                    "permalink",
                    "slug",
                    "post_id",
                    "final_dates",
                },
            )
            permalink = payload.get("permalink", "")
            slug = payload.get("slug", "") or extract_slug_from_permalink(permalink)
            if not slug:
                raise ClientInputError("Missing slug/permalink.")
            client = _wp_client_from_payload(payload)
            post_id = client.resolve_course_post_id(
                slug=slug,
                permalink=permalink,
                fallback_post_id=payload.get("post_id"),
            )
            if not post_id:
                return _json_error(f"Course not found by slug: {slug}", status=404)
            today = timezone.localdate()
            existing_program = (
                client.get_course(int(post_id)).get("acf", {}).get("program") or []
            )
            current_valid = [
                item["data"] for item in valid_existing_program(existing_program, today)
            ]
            final_valid = [
                item["data"]
                for item in build_final_program(
                    existing_program,
                    payload.get("final_dates", []),
                    today,
                )
            ]
            if current_valid == final_valid:
                return JsonResponse(
                    {
                        "success": True,
                        "status": "no changes",
                        "updated": False,
                        "post_id": int(post_id),
                    }
                )
            client.update_course_program(
                int(post_id),
                [{"data": value} for value in final_valid],
                client.auth,
            )
            return JsonResponse(
                {
                    "success": True,
                    "status": "success",
                    "updated": True,
                    "post_id": int(post_id),
                    "final_dates": final_valid,
                }
            )
        except ClientInputError as exc:
            return _json_error(exc.message, status=exc.status)
        except WordPressRequestError as exc:
            return _json_error(str(exc), status=502)
        except (TypeError, ValueError, KeyError):
            return _json_error("WordPress returned invalid course data.")


class XmlFormatterView(XmlExportPermissionMixin, TemplateView):
    template_name = "planificator/xml_formatter.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        schedule_settings = get_settings("schedule_generator", self.request.user)
        context["form"] = XmlExportForm(
            initial={
                "start_post_id": schedule_settings.get("xml_start_post_id") or 20000
            }
        )
        return context


class XmlExportView(XmlExportPermissionMixin, View):
    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        form = XmlExportForm(request.POST, request.FILES)
        if not form.is_valid():
            return JsonResponse(
                {"error": _form_error(form, "Choose a CSV or XLSX file.")},
                status=getattr(form, "upload_error_status", 400),
            )

        upload = form.cleaned_data["input_file"]
        year = timezone.localdate().year
        try:
            schedule = read_xml_schedule(upload.read(), form.file_extension)
            xml_text = create_xml_export(
                schedule,
                year,
                start_post_id=form.cleaned_data["start_post_id"],
            )
        except ClientInputError as exc:
            return JsonResponse({"error": exc.message}, status=exc.status)
        except (ValueError, KeyError, TypeError, UnicodeError, BadZipFile, OSError):
            return JsonResponse(
                {"error": "Unable to read the uploaded schedule or create XML."},
                status=400,
            )
        except Exception:
            logger.exception(
                "Unexpected XML export failure", extra={"user_id": request.user.pk}
            )
            return JsonResponse(
                {"error": "Unable to read the uploaded schedule or create XML."},
                status=400,
            )

        response = HttpResponse(xml_text.encode("utf-8"), content_type="application/xml")
        response["Content-Disposition"] = (
            f'attachment; filename="formatted_courses_{year}.xml"'
        )
        return response


class WordConverterView(WordMatcherPermissionMixin, TemplateView):
    template_name = "planificator/word_converter.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = WordMatchUploadForm()
        return context


class WordMatchPreviewView(WordMatcherPermissionMixin, View):
    def post(self, request: HttpRequest, *args, **kwargs) -> JsonResponse:
        form = WordMatchUploadForm(request.POST, request.FILES)
        if not form.is_valid():
            return _json_error(
                _form_error(form, "Selectați documentul Word și programul generat."),
                status=getattr(form, "upload_error_status", 400),
            )

        word_file = form.cleaned_data["word_file"]
        schedule_file = form.cleaned_data["schedule_file"]
        try:
            word_file_bytes = word_file.read()
            schedule_rows = read_schedule_rows(
                schedule_file.read(),
                Path(schedule_file.name).suffix.lower(),
            )
            preview = build_word_match_preview(
                word_file_bytes,
                schedule_rows,
                get_settings("word_converter", request.user),
            )
        except ClientInputError as exc:
            return _json_error(exc.message, status=exc.status)
        except (BadZipFile, PackageNotFoundError, OSError, ValueError, KeyError):
            return _json_error("Documentul Word sau programul generat nu a putut fi citit.")
        except Exception:
            logger.exception("Unexpected Word match preview failure", extra={"user_id": request.user.pk})
            return _json_error("Previzualizarea potrivirilor nu a putut fi creată.")

        preview.update(
            {
                "success": True,
                "word_file_b64": base64.b64encode(word_file_bytes).decode("ascii"),
            }
        )
        return JsonResponse(preview)


class WordMatchGenerateView(WordMatcherPermissionMixin, View):
    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        try:
            payload = _json_request_data(request)
        except ClientInputError as exc:
            return _json_error(exc.message, status=exc.status)

        form = WordMatchGenerationForm(payload)
        if not form.is_valid():
            return _json_error(
                _form_error(form, "Datele pentru generarea documentului sunt invalide."),
                status=getattr(form, "validation_status", 400),
            )

        try:
            output_bytes, matched_count, skipped_count = apply_word_matches(
                form.cleaned_data["word_file_b64"],
                form.cleaned_data["schedule_options"],
                form.cleaned_data["matches"],
            )
        except ClientInputError as exc:
            return _json_error(exc.message, status=exc.status)
        except (BadZipFile, PackageNotFoundError, OSError, ValueError, KeyError):
            return _json_error("Documentul Word nu a putut fi generat.")
        except Exception:
            logger.exception("Unexpected Word generation failure", extra={"user_id": request.user.pk})
            return _json_error("Documentul Word nu a putut fi generat.")

        response = HttpResponse(
            output_bytes,
            content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        )
        response["Content-Disposition"] = (
            'attachment; filename="planificare_cursuri_actualizata.docx"'
        )
        response["X-Matched-Course-Rows"] = str(matched_count)
        response["X-Skipped-Course-Rows"] = str(skipped_count)
        return response


class ScheduleHistoryView(PlanificatorPermissionMixin, ListView):
    template_name = "planificator/istoric.html"
    context_object_name = "generations"
    paginate_by = 20

    def get_queryset(self):
        return list_owned_generations(user=self.request.user)


class ScheduleSampleCsvView(PlanificatorPermissionMixin, View):
    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        buffer = StringIO()
        writer = csv.writer(buffer)
        writer.writerow(["Title", "Durata Curs", "investitie", "Permalink"])
        writer.writerow(["Inspector stații ITP", "5 zile", "2500", "https://example.com/curs-itp"])
        response = HttpResponse(buffer.getvalue(), content_type="text/csv; charset=utf-8")
        response["Content-Disposition"] = 'attachment; filename="model_cursuri.csv"'
        return response


class ScheduleExportView(PlanificatorPermissionMixin, View):
    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        form = ScheduleExportForm(request.POST)
        if not form.is_valid():
            return JsonResponse({"success": False, "error": "Identificator de export invalid."}, status=400)
        generation = get_owned_generation(
            generation_id=form.cleaned_data["generation_id"],
            user=request.user,
        )
        try:
            excel_data = create_excel_export(generation.schedule, generation.year, generation.holidays)
        except Exception:
            logger.exception("Unexpected schedule export failure", extra={"generation_id": str(generation.pk)})
            return JsonResponse({"success": False, "error": "Exportul nu a putut fi creat."}, status=400)
        response = HttpResponse(
            excel_data,
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
        response["Content-Disposition"] = f'attachment; filename="program_cursuri_{generation.year}.xlsx"'
        return response
```
