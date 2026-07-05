# apps/diplome/views.py

Generated: `2026-07-05T22:50:42`

## Scope

- Real source file: `apps/diplome/views.py`
- App: `diplome`
- App guide: `codex-context/apps/diplome.md`
- Role: `backend`
- Size: 24389 bytes
- Source SHA-256: `2cbcd5d14769862287586dbe38935e0d95d03de08ffd88dcea3264b8aeeb5f3c`

## Codex usage

Use this context only when the task directly touches this file or requires this file for routing. The real source file remains the source of truth before editing.

## Source

```python
import logging
from urllib.parse import urlencode

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.http import FileResponse, Http404, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View
from django.views.generic import FormView, ListView, TemplateView

from apps.media_library.selectors import list_owned_media_assets
from apps.media_library.services import require_owned_layout_assets, serialize_media_assets

from .forms import (
    BulkDiplomaGenerationForm,
    DiplomaGenerationSelectionForm,
    DiplomaGenerationHistoryFilterForm,
    DiplomaTemplateCreateForm,
    DiplomaTemplateFilterForm,
    DiplomaTemplateLayoutForm,
    ParticipantColumnMappingForm,
    ParticipantListImportForm,
    ParticipantSheetSelectionForm,
)
from .selectors import (
    get_owned_generation_batch,
    get_owned_import_draft,
    get_owned_participant_list,
    get_owned_template,
    list_owned_participants,
    list_owned_participant_lists,
    list_generated_diplomas_for_batch,
    list_owned_template_categories,
    list_owned_templates,
)
from .services import (
    apply_participant_import_mapping,
    build_batch_zip_response,
    build_diploma_preview_context,
    build_generation_history_context,
    build_generated_diploma_filename,
    build_preview_data,
    confirm_participant_import,
    create_diploma_template,
    create_participant_import_draft,
    delete_diploma_template,
    delete_participant_list,
    generate_single_diploma,
    generate_diploma_batch,
    get_generated_diploma_download,
    resume_generation_batch,
    select_participant_import_sheet,
    update_diploma_template_layout,
)


logger = logging.getLogger(__name__)


DRAFT_TEMPLATE_IDS_SESSION_KEY = "diplome_draft_template_ids"


def _draft_template_ids(request) -> list[str]:
    return list(request.session.get(DRAFT_TEMPLATE_IDS_SESSION_KEY, []))


def _is_draft_template(request, template_id) -> bool:
    return str(template_id) in _draft_template_ids(request)


def _mark_draft_template(request, template_id) -> None:
    template_id = str(template_id)
    draft_ids = _draft_template_ids(request)
    if template_id not in draft_ids:
        draft_ids.append(template_id)
        request.session[DRAFT_TEMPLATE_IDS_SESSION_KEY] = draft_ids


def _clear_draft_template(request, template_id) -> None:
    template_id = str(template_id)
    draft_ids = [item for item in _draft_template_ids(request) if item != template_id]
    if draft_ids:
        request.session[DRAFT_TEMPLATE_IDS_SESSION_KEY] = draft_ids
    else:
        request.session.pop(DRAFT_TEMPLATE_IDS_SESSION_KEY, None)


class DiplomaTemplateListView(LoginRequiredMixin, ListView):
    template_name = "diplome/template_list.html"
    context_object_name = "templates"

    def get_filter_form(self):
        if not hasattr(self, "_filter_form"):
            categories = list_owned_template_categories(user=self.request.user)
            self._filter_form = DiplomaTemplateFilterForm(
                data=self.request.GET,
                categories=categories,
            )
        return self._filter_form

    def get_queryset(self):
        form = self.get_filter_form()
        category = form.cleaned_data["category"] if form.is_valid() else ""
        self.selected_category = category
        return list_owned_templates(user=self.request.user, category=category)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "filter_form": self.get_filter_form(),
            "selected_category": getattr(self, "selected_category", ""),
        })
        return context


def _generation_index_context(form, bulk_form):
    return {
        "form": form,
        "bulk_form": bulk_form,
        "selected_participant_id": str(form["participant"].value() or ""),
        "has_participant_lists": form.fields["participant_list"].queryset.exists(),
        "has_templates": form.fields["template"].queryset.exists(),
    }


def _add_batch_result_message(request, batch):
    message = (
        f"Lot finalizat: {batch.success_count} din {batch.total_count} "
        f"diplome generate, {batch.failed_count} eșuate."
    )
    if batch.status == batch.Status.COMPLETED:
        messages.success(request, message)
    elif batch.status == batch.Status.COMPLETED_WITH_ERRORS:
        messages.warning(request, message)
    else:
        messages.error(request, message)


class DiplomaGenerationIndexView(LoginRequiredMixin, FormView):
    template_name = "diplome/generation_index.html"
    form_class = DiplomaGenerationSelectionForm

    def get_initial(self):
        initial = super().get_initial()
        for field_name in ("participant_list", "participant", "template"):
            value = self.request.GET.get(field_name)
            if value:
                initial[field_name] = value
        return initial

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        bulk_form = kwargs.get("bulk_form") or BulkDiplomaGenerationForm(
            user=self.request.user
        )
        context.update(_generation_index_context(context["form"], bulk_form))
        return context

    def form_valid(self, form):
        query = urlencode(
            {
                "participant_list": form.cleaned_data["participant_list"].pk,
                "participant": form.cleaned_data["participant"].pk,
                "template": form.cleaned_data["template"].pk,
            }
        )
        return redirect(f"{reverse('diplome:generation_preview')}?{query}")


class DiplomaGenerationPreviewView(LoginRequiredMixin, TemplateView):
    template_name = "diplome/generation_preview.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        selection = {
            "participant_list_id": self.request.GET.get("participant_list"),
            "participant_id": self.request.GET.get("participant"),
            "template_id": self.request.GET.get("template"),
        }
        if not all(selection.values()):
            raise Http404("Selecția pentru previzualizare este incompletă.")
        context.update(
            build_diploma_preview_context(owner=self.request.user, **selection)
        )
        context["selection_query"] = urlencode(
            {
                "participant_list": context["participant_list"].pk,
                "participant": context["participant"].pk,
                "template": context["diploma_template"].pk,
            }
        )
        generated_id = self.request.GET.get("generated")
        if generated_id:
            generated = get_generated_diploma_download(
                owner=self.request.user,
                generated_diploma_id=generated_id,
            )
            if (
                generated.participant_list_id
                != context["participant_list"].pk
                or generated.participant_id != context["participant"].pk
                or generated.template_id != context["diploma_template"].pk
            ):
                raise Http404("Fișierul generat nu corespunde selecției curente.")
            context["generated_diploma"] = generated
        return context


class DiplomaGenerationCreateView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        form = DiplomaGenerationSelectionForm(request.POST, user=request.user)
        if not form.is_valid():
            return render(
                request,
                "diplome/generation_index.html",
                _generation_index_context(
                    form,
                    BulkDiplomaGenerationForm(user=request.user),
                ),
                status=400,
            )
        generated = generate_single_diploma(
            owner=request.user,
            participant_list_id=form.cleaned_data["participant_list"].pk,
            participant_id=form.cleaned_data["participant"].pk,
            template_id=form.cleaned_data["template"].pk,
        )
        query = urlencode(
            {
                "participant_list": generated.participant_list_id,
                "participant": generated.participant_id,
                "template": generated.template_id,
                "generated": generated.pk,
            }
        )
        return redirect(f"{reverse('diplome:generation_preview')}?{query}")


class DiplomaGenerationDownloadView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        generated = get_generated_diploma_download(
            owner=request.user,
            generated_diploma_id=kwargs["generated_diploma_id"],
        )
        try:
            if not generated.pdf_file.name or not generated.pdf_file.storage.exists(
                generated.pdf_file.name
            ):
                raise Http404("Fișierul PDF nu mai este disponibil.")
            pdf_file = generated.pdf_file.open("rb")
        except (OSError, ValueError) as exc:
            raise Http404("Fișierul PDF nu mai este disponibil.") from exc
        return FileResponse(
            pdf_file,
            as_attachment=True,
            filename=build_generated_diploma_filename(generated),
            content_type="application/pdf",
        )


class BulkDiplomaGenerationCreateView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        form = BulkDiplomaGenerationForm(request.POST, user=request.user)
        if not form.is_valid():
            return render(
                request,
                "diplome/generation_index.html",
                _generation_index_context(
                    DiplomaGenerationSelectionForm(user=request.user),
                    form,
                ),
                status=400,
            )
        try:
            batch = generate_diploma_batch(
                request.user,
                form.cleaned_data["participant_list"].pk,
                form.cleaned_data["template"].pk,
            )
        except ValidationError as exc:
            form.add_error(None, exc)
            return render(
                request,
                "diplome/generation_index.html",
                _generation_index_context(
                    DiplomaGenerationSelectionForm(user=request.user),
                    form,
                ),
                status=400,
            )
        _add_batch_result_message(request, batch)
        return redirect("diplome:batch_detail", batch_id=batch.pk)


class DiplomaGenerationHistoryView(LoginRequiredMixin, TemplateView):
    template_name = "diplome/history_index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        filter_form = DiplomaGenerationHistoryFilterForm(
            self.request.GET,
            user=self.request.user,
        )
        filters = filter_form.cleaned_data if filter_form.is_valid() else {}
        context.update(build_generation_history_context(self.request.user, filters))
        context["filter_form"] = filter_form
        return context


class DiplomaGenerationBatchDetailView(LoginRequiredMixin, TemplateView):
    template_name = "diplome/batch_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        batch = get_owned_generation_batch(
            self.request.user,
            kwargs["batch_id"],
        )
        context.update(
            {
                "batch": batch,
                "generated_diplomas": list_generated_diplomas_for_batch(
                    self.request.user,
                    batch.pk,
                ),
            }
        )
        return context


class DiplomaGenerationBatchResumeView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        batch_id = kwargs["batch_id"]
        try:
            batch = resume_generation_batch(request.user, batch_id)
        except Http404:
            raise
        except ValidationError as exc:
            messages.error(request, " ".join(exc.messages))
        except Exception:
            logger.exception(
                "Could not resume diploma generation batch %s",
                batch_id,
            )
            messages.error(
                request,
                "Generarea lotului nu a putut fi reluată.",
            )
        else:
            _add_batch_result_message(request, batch)
        return redirect("diplome:batch_detail", batch_id=batch_id)


class DiplomaGenerationBatchZipDownloadView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return build_batch_zip_response(request.user, kwargs["batch_id"])


class DiplomaTemplateCreateView(LoginRequiredMixin, FormView):
    template_name = "diplome/template_form.html"
    form_class = DiplomaTemplateCreateForm

    def form_valid(self, form):
        template = create_diploma_template(owner=self.request.user, data=form.cleaned_data)
        _mark_draft_template(self.request, template.pk)
        return redirect("diplome:template_editor", template_id=template.pk)


class DiplomaTemplateEditorView(LoginRequiredMixin, TemplateView):
    template_name = "diplome/template_editor.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        template = get_owned_template(
            user=self.request.user,
            template_id=self.kwargs["template_id"],
        )
        context.update({
            "diploma_template": template,
            "layout": template.layout_json,
            "media_assets": serialize_media_assets(
                list_owned_media_assets(user=self.request.user)
            ),
            "media_assets_api_url": reverse("media_library:api_assets"),
            "media_assets_upload_url": reverse("media_library:api_upload"),
            "is_draft_template": _is_draft_template(self.request, template.pk),
        })
        return context

    def post(self, request, *args, **kwargs):
        get_owned_template(user=request.user, template_id=kwargs["template_id"])
        form = DiplomaTemplateLayoutForm(request.POST)
        if not form.is_valid():
            return JsonResponse(
                {"success": False, "errors": form.errors.get_json_data()},
                status=400,
            )
        try:
            template = update_diploma_template_layout(
                owner=request.user,
                template_id=kwargs["template_id"],
                layout=form.cleaned_data["layout_json"],
            )
        except ValidationError as exc:
            return JsonResponse(
                {
                    "success": False,
                    "errors": {
                        "layout_json": [
                            {"message": message, "code": "invalid_asset"}
                            for message in exc.messages
                        ]
                    },
                },
                status=400,
            )
        if template.layout_json["elements"]:
            _clear_draft_template(request, template.pk)
        return JsonResponse({
            "success": True,
            "message": "Template salvat.",
            "updatedAt": template.updated_at.isoformat(),
            "isDraft": _is_draft_template(request, template.pk),
        })


class DiplomaTemplatePreviewView(LoginRequiredMixin, TemplateView):
    template_name = "diplome/template_preview.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        template = get_owned_template(
            user=self.request.user,
            template_id=self.kwargs["template_id"],
        )
        context.update({
            "diploma_template": template,
            "layout": template.layout_json,
            "sample_participant": build_preview_data(),
            "media_assets": serialize_media_assets(
                require_owned_layout_assets(
                    owner=self.request.user,
                    layout=template.layout_json,
                ).values()
            ),
        })
        return context


class DiplomaTemplateDeleteView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        template_id = kwargs["template_id"]
        delete_diploma_template(
            owner=request.user,
            template_id=template_id,
        )
        _clear_draft_template(request, template_id)
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return JsonResponse({"success": True})
        messages.success(request, "Template-ul a fost șters.")
        return redirect("diplome:template_list")


class ParticipantListView(LoginRequiredMixin, ListView):
    template_name = "diplome/participant_list.html"
    context_object_name = "participant_lists"
    paginate_by = 50

    def get_queryset(self):
        return list_owned_participant_lists(user=self.request.user)


class ParticipantImportView(LoginRequiredMixin, FormView):
    template_name = "diplome/participant_import.html"
    form_class = ParticipantListImportForm

    def form_valid(self, form):
        try:
            draft = create_participant_import_draft(
                owner=self.request.user,
                data=form.cleaned_data,
            )
        except ValidationError as exc:
            form.add_error("source_file", exc)
            return self.form_invalid(form)
        if draft.source_sheets_json:
            return redirect("diplome:participant_import_sheet", draft_id=draft.pk)
        return redirect("diplome:participant_import_mapping", draft_id=draft.pk)


class ParticipantImportSheetView(LoginRequiredMixin, FormView):
    template_name = "diplome/participant_import_sheet.html"
    form_class = ParticipantSheetSelectionForm

    def get_draft(self):
        if not hasattr(self, "_draft"):
            self._draft = get_owned_import_draft(
                user=self.request.user,
                draft_id=self.kwargs["draft_id"],
            )
        return self._draft

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["sheets"] = self.get_draft().source_sheets_json
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["draft"] = self.get_draft()
        return context

    def form_valid(self, form):
        try:
            draft = select_participant_import_sheet(
                owner=self.request.user,
                draft_id=self.kwargs["draft_id"],
                sheet_index=form.selected_index(),
            )
        except ValidationError as exc:
            form.add_error("sheet_index", exc)
            return self.form_invalid(form)
        return redirect("diplome:participant_import_mapping", draft_id=draft.pk)


class ParticipantImportMappingView(LoginRequiredMixin, FormView):
    template_name = "diplome/participant_import_mapping.html"
    form_class = ParticipantColumnMappingForm

    def get_draft(self):
        if not hasattr(self, "_draft"):
            self._draft = get_owned_import_draft(
                user=self.request.user,
                draft_id=self.kwargs["draft_id"],
            )
        return self._draft

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        draft = self.get_draft()
        kwargs.update(
            {
                "columns": draft.source_columns_json,
                "suggested_mapping": draft.column_mapping_json,
            }
        )
        return kwargs

    def get(self, request, *args, **kwargs):
        draft = self.get_draft()
        if draft.source_sheets_json and not draft.source_columns_json:
            return redirect("diplome:participant_import_sheet", draft_id=draft.pk)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        draft = self.get_draft()
        form = context["form"]
        context.update(
            {
                "draft": draft,
                "mapping_rows": [
                    {
                        "column": column,
                        "field": form[f"column_{column['index']}"],
                    }
                    for column in draft.source_columns_json
                ],
            }
        )
        return context

    def form_valid(self, form):
        try:
            draft = apply_participant_import_mapping(
                owner=self.request.user,
                draft_id=self.kwargs["draft_id"],
                column_mapping=form.get_column_mapping(),
            )
        except ValidationError as exc:
            form.add_error(None, exc)
            return self.form_invalid(form)
        return redirect("diplome:participant_import_preview", draft_id=draft.pk)


class ParticipantImportPreviewView(LoginRequiredMixin, TemplateView):
    template_name = "diplome/participant_import_preview.html"

    def get(self, request, *args, **kwargs):
        draft = get_owned_import_draft(
            user=request.user,
            draft_id=kwargs["draft_id"],
        )
        if not draft.mapping_confirmed:
            return redirect("diplome:participant_import_mapping", draft_id=draft.pk)
        self._draft = draft
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["draft"] = self._draft
        return context


class ParticipantImportConfirmView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        try:
            participant_list = confirm_participant_import(
                owner=request.user,
                draft_id=kwargs["draft_id"],
            )
        except ValidationError as exc:
            messages.error(request, "; ".join(exc.messages))
            return redirect(
                "diplome:participant_import_preview",
                draft_id=kwargs["draft_id"],
            )
        messages.success(request, "Lista de participanți a fost importată.")
        return redirect(
            "diplome:participant_list_detail",
            participant_list_id=participant_list.pk,
        )


class ParticipantListDetailView(LoginRequiredMixin, TemplateView):
    template_name = "diplome/participant_list_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        participant_list = get_owned_participant_list(
            user=self.request.user,
            participant_list_id=self.kwargs["participant_list_id"],
        )
        paginator = Paginator(
            list_owned_participants(
                user=self.request.user,
                participant_list=participant_list,
            ),
            100,
        )
        page_obj = paginator.get_page(self.request.GET.get("page"))
        context.update(
            {
                "participant_list": participant_list,
                "participants": page_obj.object_list,
                "page_obj": page_obj,
                "is_paginated": page_obj.has_other_pages(),
            }
        )
        return context


class ParticipantListDeleteView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        delete_participant_list(
            owner=request.user,
            participant_list_id=kwargs["participant_list_id"],
        )
        messages.success(request, "Lista de participanți a fost ștearsă.")
        return redirect("diplome:list_index")


class DiplomaPlaceholderView(LoginRequiredMixin, TemplateView):
    template_name = "diplome/placeholder.html"
    page_title = "Diplome"
    page_description = "Această secțiune va fi disponibilă într-o etapă viitoare."

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "page_title": self.page_title,
            "page_description": self.page_description,
        })
        return context
```
