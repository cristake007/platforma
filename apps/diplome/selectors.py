from django.db.models import Count
from django.shortcuts import get_object_or_404
from django.utils import timezone

from .models import (
    DiplomaGenerationBatch,
    DiplomaTemplate,
    GeneratedDiploma,
    Participant,
    ParticipantImportDraft,
    ParticipantList,
)


def list_owned_templates(*, user, category=""):
    queryset = DiplomaTemplate.objects.filter(owner=user)
    if category:
        queryset = queryset.filter(category=category)
    return queryset.only(
        "id",
        "name",
        "category",
        "description",
        "page_size",
        "orientation",
        "is_active",
        "created_at",
        "updated_at",
    )


def list_owned_template_categories(*, user):
    return (
        DiplomaTemplate.objects.filter(owner=user)
        .exclude(category="")
        .order_by("category")
        .values_list("category", flat=True)
        .distinct()
    )


def get_owned_template(*, user, template_id) -> DiplomaTemplate:
    return get_object_or_404(DiplomaTemplate, pk=template_id, owner=user)


def get_owned_template_for_update(*, user, template_id) -> DiplomaTemplate:
    return get_object_or_404(
        DiplomaTemplate.objects.select_for_update(),
        pk=template_id,
        owner=user,
    )


def list_owned_participant_lists(*, user):
    return ParticipantList.objects.filter(owner=user).only(
        "id",
        "name",
        "description",
        "course_name",
        "source_file_name",
        "participant_count",
        "created_at",
        "updated_at",
    )


def get_owned_participant_list(*, user, participant_list_id) -> ParticipantList:
    return get_object_or_404(
        ParticipantList,
        pk=participant_list_id,
        owner=user,
    )


def list_owned_participants(*, user, participant_list):
    return participant_list.participants.filter(owner=user)


def list_owned_participants_for_list(*, user, participant_list_id):
    return Participant.objects.filter(
        owner=user,
        participant_list_id=participant_list_id,
        participant_list__owner=user,
    ).select_related("participant_list")


def get_owned_participant(*, user, participant_id) -> Participant:
    return get_object_or_404(
        Participant.objects.select_related("participant_list"),
        pk=participant_id,
        owner=user,
        participant_list__owner=user,
    )


def get_owned_participant_for_update(*, user, participant_id) -> Participant:
    return get_object_or_404(
        Participant.objects.select_for_update().select_related("participant_list"),
        pk=participant_id,
        owner=user,
        participant_list__owner=user,
    )


def get_owned_participant_list_for_update(*, user, participant_list_id) -> ParticipantList:
    return get_object_or_404(
        ParticipantList.objects.select_for_update(),
        pk=participant_list_id,
        owner=user,
    )


def get_owned_import_draft(*, user, draft_id) -> ParticipantImportDraft:
    return get_object_or_404(
        ParticipantImportDraft,
        pk=draft_id,
        owner=user,
        expires_at__gt=timezone.now(),
    )


def get_owned_import_draft_for_update(*, user, draft_id) -> ParticipantImportDraft:
    return get_object_or_404(
        ParticipantImportDraft.objects.select_for_update(),
        pk=draft_id,
        owner=user,
        expires_at__gt=timezone.now(),
    )


def get_owned_generated_diploma(*, user, generated_diploma_id) -> GeneratedDiploma:
    return get_object_or_404(
        GeneratedDiploma.objects.select_related(
            "batch",
            "participant_list",
            "participant",
            "template",
        ),
        pk=generated_diploma_id,
        owner=user,
    )


def list_owned_generation_batches(user):
    return DiplomaGenerationBatch.objects.filter(owner=user).select_related(
        "participant_list",
        "template",
    )


def get_owned_generation_batch(user, batch_id) -> DiplomaGenerationBatch:
    return get_object_or_404(
        DiplomaGenerationBatch.objects.select_related(
            "participant_list",
            "template",
        ),
        pk=batch_id,
        owner=user,
    )


def list_generated_diplomas_for_batch(user, batch_id):
    return GeneratedDiploma.objects.filter(
        owner=user,
        batch_id=batch_id,
        batch__owner=user,
    ).select_related(
        "participant",
        "participant_list",
        "template",
        "batch",
    ).order_by("participant_name", "certificate_number")


def list_owned_participant_lists_with_counts(user):
    return (
        ParticipantList.objects.filter(owner=user)
        .annotate(actual_participant_count=Count("participants"))
        .order_by("-updated_at", "name")
    )


def list_owned_templates_for_generation(user):
    return DiplomaTemplate.objects.filter(owner=user).order_by("name")
