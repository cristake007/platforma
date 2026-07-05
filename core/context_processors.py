import re

from .navigation import NAVIGATION


def _is_active(item: dict, current_url_name: str) -> bool:
    active_names = item.get("active_url_names", (item.get("url_name"),))
    return bool(current_url_name and current_url_name in active_names)


def _is_allowed(item: dict, request, permissions: set[str]) -> bool:
    permission = item.get("permission")
    return not permission or request.user.is_superuser or permission in permissions


def build_navigation(request, permissions: set[str] | None = None) -> list[dict]:
    resolver_match = request.resolver_match
    current_url_name = resolver_match.view_name if resolver_match else ""
    permissions = permissions if permissions is not None else getattr(
        request, "_application_shell_permissions", set()
    )
    navigation = []
    for section in NAVIGATION:
        items = []
        for item in section["items"]:
            children = [
                {**child, "is_active": _is_active(child, current_url_name)}
                for child in item.get("children", ())
                if _is_allowed(child, request, permissions)
            ]
            if item.get("children") and not children:
                continue
            if not _is_allowed(item, request, permissions):
                continue
            items.append(
                {
                    **item,
                    "children": children,
                    "is_active": _is_active(item, current_url_name)
                    or any(child["is_active"] for child in children),
                }
            )
        navigation.append({**section, "items": items})
    return navigation


def build_application_shell(request, profile=None, permissions: set[str] | None = None) -> dict:
    user_display_name = "Vizitator"
    user_initials = "VI"
    user_avatar_url = ""
    if request.user.is_authenticated:
        username = request.user.get_username()
        full_name = request.user.get_full_name()
        user_display_name = full_name or username
        full_name_parts = full_name.split()
        username_parts = [part for part in re.split(r"[\W_]+", username) if part]
        if len(full_name_parts) > 1:
            user_initials = f"{full_name_parts[0][0]}{full_name_parts[-1][0]}".upper()
        elif len(username_parts) > 1:
            user_initials = f"{username_parts[0][0]}{username_parts[-1][0]}".upper()
        else:
            user_initials = username[:2].upper() or "U"
        if profile and profile.avatar:
            user_avatar_url = profile.avatar.url
    return {
        "app_navigation": build_navigation(request, permissions),
        "app_name": "Platforma TUVTK",
        "app_tagline": "Operațiuni interne",
        "user_display_name": user_display_name,
        "user_initials": user_initials,
        "user_avatar_url": user_avatar_url,
    }


def application_shell(request):
    shell = getattr(request, "application_shell", None)
    return shell if shell is not None else build_application_shell(request)
