# Source snapshot

## `apps/planificator/settings_store.py`

Size: 1.7 KB

```python
import logging

from django.db import DatabaseError

from .models import AppSetting

logger = logging.getLogger(__name__)


DEFAULT_SETTINGS = {
    "schedule_generator": {
        "year": 2026,
        "months": [],
        "randomness": 5,
        "holidays": [],
        "xml_start_post_id": 20000,
    },
    "word_converter": {
        "min_match_score": 88,
        "min_token_coverage": 70,
        "min_match_gap": 8,
    },
    "safe_course_date_updater": {
        "wp_base_url": "",
        "wp_username": "",
    },
}


def get_settings(scope: str, user) -> dict:
    defaults = DEFAULT_SETTINGS.get(scope, {})
    try:
        global_setting = AppSetting.objects.filter(scope=scope, user__isnull=True).first()
        user_setting = AppSetting.objects.filter(scope=scope, user=user).first()
    except DatabaseError:
        logger.exception("Unable to load settings", extra={"scope": scope, "user_id": user.pk})
        raise

    global_payload = global_setting.payload if global_setting and isinstance(global_setting.payload, dict) else {}
    user_payload = user_setting.payload if user_setting and isinstance(user_setting.payload, dict) else {}
    return {**defaults, **global_payload, **user_payload}


def save_settings(scope: str, user, payload: dict) -> dict:
    current = get_settings(scope, user)
    merged = {**DEFAULT_SETTINGS.get(scope, {}), **current, **payload}
    try:
        AppSetting.objects.update_or_create(
            scope=scope,
            user=user,
            defaults={"payload": merged},
        )
    except DatabaseError:
        logger.exception("Unable to save settings", extra={"scope": scope, "user_id": user.pk})
        raise
    return merged
```
