import uuid

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q

from .validators import validate_layout_json


def generated_diploma_upload_to(instance, _filename: str) -> str:
    if instance.batch_id:
        return f"{instance.batch.output_folder}/{_filename}"
    return (
        f"diplomas/{instance.owner_id}/{instance.participant_list_id}/"
        f"{instance.pk}.pdf"
    )


class DiplomaTemplate(models.Model):
    DEFAULT_CATEGORY = "General"

    class PageSize(models.TextChoices):
        A4 = "A4", "A4"

    class Orientation(models.TextChoices):
        LANDSCAPE = "landscape", "Peisaj"
        PORTRAIT = "portrait", "Portret"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="diploma_templates",
    )
    name = models.CharField(max_length=160)
    category = models.CharField(max_length=80, default=DEFAULT_CATEGORY)
    description = models.TextField(blank=True)
    page_size = models.CharField(max_length=16, choices=PageSize.choices, default=PageSize.A4)
    orientation = models.CharField(
        max_length=16,
        choices=Orientation.choices,
        default=Orientation.LANDSCAPE,
    )
    page_width_mm = models.PositiveSmallIntegerField(default=297)
    page_height_mm = models.PositiveSmallIntegerField(default=210)
    grid_size_mm = models.PositiveSmallIntegerField(default=1)
    major_grid_size_mm = models.PositiveSmallIntegerField(default=10)
    layout_json = models.JSONField(default=dict)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-updated_at", "name")
        indexes = [
            models.Index(fields=("owner", "name"), name="dipl_tmpl_owner_name"),
            models.Index(
                fields=("owner", "is_active", "-updated_at"),
                name="dipl_tmpl_owner_act_upd",
            ),
            models.Index(
                fields=("owner", "category", "-updated_at"),
                name="dipl_tmpl_owner_cat_upd",
            ),
        ]
        constraints = [
            models.CheckConstraint(condition=Q(page_width_mm__gt=0), name="dipl_tmpl_width_mm_gt_0"),
            models.CheckConstraint(condition=Q(page_height_mm__gt=0), name="dipl_tmpl_height_mm_gt_0"),
            models.CheckConstraint(condition=Q(grid_size_mm__gt=0), name="dipl_tmpl_grid_mm_gt_0"),
            models.CheckConstraint(condition=Q(major_grid_size_mm__gt=0), name="dipl_tmpl_major_grid_gt_0"),
        ]

    def clean(self):
        super().clean()
        normalized_category = " ".join((self.category or "").split())
        if not normalized_category:
            raise ValidationError({"category": "Categoria este obligatorie."})
        self.category = normalized_category
        if not self.layout_json:
            return
        normalized = validate_layout_json(self.layout_json)
        page = normalized["page"]
        mismatches = (
            page["size"] != self.page_size,
            page["orientation"] != self.orientation,
            page["width_mm"] != self.page_width_mm,
            page["height_mm"] != self.page_height_mm,
            page["grid_mm"] != self.grid_size_mm,
            page["major_grid_mm"] != self.major_grid_size_mm,
        )
        if any(mismatches):
            raise ValidationError({"layout_json": "Metadatele paginii nu corespund template-ului."})
        self.layout_json = normalized

    def __str__(self) -> str:
        return f"{self.name} — {self.owner}"


class ParticipantList(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="participant_lists",
    )
    name = models.CharField(max_length=160)
    description = models.TextField(blank=True)
    course_name = models.CharField(max_length=200, blank=True)
    source_file_name = models.CharField(max_length=255)
    participant_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-updated_at", "name")
        indexes = [
            models.Index(
                fields=("owner", "-updated_at"),
                name="dipl_plist_owner_upd",
            ),
        ]

    def __str__(self) -> str:
        return self.name


class Participant(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="diploma_participants",
    )
    participant_list = models.ForeignKey(
        ParticipantList,
        on_delete=models.CASCADE,
        related_name="participants",
    )
    full_name = models.CharField(max_length=200)
    date_of_birth = models.DateField()
    place_of_birth = models.CharField(max_length=200)
    certificate_number = models.CharField(max_length=100)
    source_row = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("source_row", "full_name")
        indexes = [
            models.Index(
                fields=("participant_list", "source_row"),
                name="dipl_part_list_row",
            ),
            models.Index(
                fields=("owner", "certificate_number"),
                name="dipl_part_owner_cert",
            ),
        ]

    def clean(self):
        super().clean()
        if self.participant_list_id and self.owner_id != self.participant_list.owner_id:
            raise ValidationError(
                {"participant_list": "Lista de participanți trebuie să aparțină aceluiași utilizator."}
            )

    def __str__(self) -> str:
        return self.full_name


class ParticipantImportDraft(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="participant_import_drafts",
    )
    list_name = models.CharField(max_length=160)
    description = models.TextField(blank=True)
    course_name = models.CharField(max_length=200, blank=True)
    source_file_name = models.CharField(max_length=255)
    source_sheets_json = models.JSONField(default=list)
    source_columns_json = models.JSONField(default=list)
    source_rows_json = models.JSONField(default=list)
    column_mapping_json = models.JSONField(default=dict)
    mapping_confirmed = models.BooleanField(default=False)
    valid_rows_json = models.JSONField(default=list)
    invalid_rows_json = models.JSONField(default=list)
    warnings_json = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(db_index=True)

    class Meta:
        ordering = ("-created_at",)
        indexes = [
            models.Index(
                fields=("owner", "expires_at"),
                name="dipl_pdraft_owner_exp",
            ),
        ]

    def __str__(self) -> str:
        return self.list_name


class DiplomaGenerationBatch(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "În așteptare"
        RUNNING = "running", "În curs"
        COMPLETED = "completed", "Finalizat"
        COMPLETED_WITH_ERRORS = "completed_with_errors", "Finalizat cu erori"
        FAILED = "failed", "Eșuat"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="diploma_generation_batches",
    )
    participant_list = models.ForeignKey(
        ParticipantList,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="diploma_generation_batches",
    )
    template = models.ForeignKey(
        DiplomaTemplate,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="diploma_generation_batches",
    )
    participant_list_name = models.CharField(max_length=160, default="")
    template_name = models.CharField(max_length=160, default="")
    status = models.CharField(
        max_length=24,
        choices=Status.choices,
        default=Status.PENDING,
    )
    total_count = models.PositiveIntegerField(default=0)
    success_count = models.PositiveIntegerField(default=0)
    failed_count = models.PositiveIntegerField(default=0)
    output_folder = models.CharField(max_length=500)
    error_summary = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ("-created_at",)
        indexes = [
            models.Index(
                fields=("owner", "-created_at"),
                name="dipl_batch_owner_created",
            ),
            models.Index(
                fields=("participant_list", "-created_at"),
                name="dipl_batch_list_created",
            ),
            models.Index(
                fields=("template", "-created_at"),
                name="dipl_batch_tmpl_created",
            ),
            models.Index(
                fields=("owner", "status", "-created_at"),
                name="dipl_batch_owner_st_created",
            ),
        ]

    def clean(self):
        super().clean()
        errors = {}
        if self.participant_list_id:
            if self.owner_id != self.participant_list.owner_id:
                errors["participant_list"] = "Lista trebuie să aparțină aceluiași utilizator."
            self.participant_list_name = self.participant_list_name or self.participant_list.name
        if self.template_id:
            if self.owner_id != self.template.owner_id:
                errors["template"] = "Template-ul trebuie să aparțină aceluiași utilizator."
            self.template_name = self.template_name or self.template.name
        if errors:
            raise ValidationError(errors)

    def __str__(self) -> str:
        return f"{self.participant_list_display_name} — {self.get_status_display()}"

    @property
    def participant_list_display_name(self) -> str:
        return self.participant_list_name or getattr(self.participant_list, "name", "Listă ștearsă")

    @property
    def template_display_name(self) -> str:
        return self.template_name or getattr(self.template, "name", "Template șters")


class GeneratedDiploma(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="generated_diplomas",
    )
    participant_list = models.ForeignKey(
        ParticipantList,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="generated_diplomas",
    )
    participant = models.ForeignKey(
        Participant,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="generated_diplomas",
    )
    template = models.ForeignKey(
        DiplomaTemplate,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="generated_diplomas",
    )
    batch = models.ForeignKey(
        DiplomaGenerationBatch,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="generated_diplomas",
    )
    certificate_number = models.CharField(max_length=100)
    participant_name = models.CharField(max_length=200)
    participant_list_name = models.CharField(max_length=160, default="")
    template_name = models.CharField(max_length=160, default="")
    pdf_file = models.FileField(upload_to=generated_diploma_upload_to, max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)
        indexes = [
            models.Index(
                fields=("owner", "-created_at"),
                name="dipl_gen_owner_created",
            ),
            models.Index(
                fields=("batch", "participant_name"),
                name="dipl_gen_batch_name",
            ),
            models.Index(
                fields=("participant_list", "participant_name"),
                name="dipl_gen_list_name",
            ),
            models.Index(
                fields=("participant", "-created_at"),
                name="dipl_gen_part_created",
            ),
            models.Index(
                fields=("template", "created_at"),
                name="dipl_gen_tmpl_created",
            ),
        ]

    def clean(self):
        super().clean()
        errors = {}
        if self.participant_list_id:
            if self.owner_id != self.participant_list.owner_id:
                errors["participant_list"] = "Lista trebuie să aparțină aceluiași utilizator."
            self.participant_list_name = self.participant_list_name or self.participant_list.name
        if self.participant_id:
            if self.owner_id != self.participant.owner_id:
                errors["participant"] = "Participantul trebuie să aparțină aceluiași utilizator."
            elif (
                self.participant_list_id
                and self.participant.participant_list_id != self.participant_list_id
            ):
                errors["participant"] = "Participantul nu aparține listei selectate."
        if self.template_id:
            if self.owner_id != self.template.owner_id:
                errors["template"] = "Template-ul trebuie să aparțină aceluiași utilizator."
            self.template_name = self.template_name or self.template.name
        if self.batch_id:
            if self.owner_id != self.batch.owner_id:
                errors["batch"] = "Lotul trebuie să aparțină aceluiași utilizator."
            elif (
                self.participant_list_id
                and self.batch.participant_list_id != self.participant_list_id
            ):
                errors["batch"] = "Lotul nu corespunde listei selectate."
            elif self.template_id and self.batch.template_id != self.template_id:
                errors["batch"] = "Lotul nu corespunde template-ului selectat."
        if errors:
            raise ValidationError(errors)

    def __str__(self) -> str:
        return f"{self.participant_name} — {self.certificate_number}"

    @property
    def participant_list_display_name(self) -> str:
        return self.participant_list_name or getattr(self.participant_list, "name", "Listă ștearsă")

    @property
    def template_display_name(self) -> str:
        return self.template_name or getattr(self.template, "name", "Template șters")
