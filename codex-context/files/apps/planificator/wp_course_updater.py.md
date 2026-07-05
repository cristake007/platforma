# apps/planificator/wp_course_updater.py

Generated: `2026-07-05T21:21:12`

## Scope

- Real source file: `apps/planificator/wp_course_updater.py`
- App: `planificator`
- App guide: `codex-context/apps/planificator.md`
- Role: `backend`
- Size: 16904 bytes
- Source SHA-256: `f45ee6ad1a86bb3c43829b4e8fc4cae7d22ecbccebdbe2f24ab396215dcbaf6e`

## Codex usage

Use this context only when the task directly touches this file or requires this file for routing. The real source file remains the source of truth before editing.

## Source

```python
from __future__ import annotations

from datetime import date, datetime
import random
import re
import time
from typing import Any
from urllib.parse import urljoin, urlparse

import requests
from requests.auth import HTTPBasicAuth

from .validators import validate_http_url_syntax, validate_public_http_url


MONTH_COLUMNS = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
]
ROMANIAN_MONTH_COLUMNS = [
    "Ianuarie",
    "Februarie",
    "Martie",
    "Aprilie",
    "Mai",
    "Iunie",
    "Iulie",
    "August",
    "Septembrie",
    "Octombrie",
    "Noiembrie",
    "Decembrie",
]
MAX_RESPONSE_BYTES = 5 * 1024 * 1024
MAX_REDIRECTS = 3


class WordPressRequestError(RuntimeError):
    """A client-safe WordPress integration failure."""


class WPCourseClient:
    def __init__(self, base_url: str, username: str, app_password: str):
        raw_base_url = (base_url or "").strip().rstrip("/")
        self.base_url = validate_http_url_syntax(raw_base_url) if raw_base_url else ""

        clean_username = (username or "").strip()
        clean_password = (app_password or "").strip().replace(" ", "")
        self.auth = HTTPBasicAuth(clean_username, clean_password)
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": "insomnia/11.0.2",
                "Accept": "*/*",
                "Content-Type": "application/json",
                "Origin": self.base_url,
                "Referer": f"{self.base_url}/",
                "Cache-Control": "no-cache",
                "Pragma": "no-cache",
            }
        )
        self.timeout = (5, 30)
        self.min_interval_seconds = 0.85
        self.max_retries = 4
        self.base_backoff_seconds = 1.25
        self.last_request_ts = 0.0

    def _endpoint(self, path: str) -> str:
        normalized = path if path.startswith("/") else f"/{path}"
        return f"{self.base_url}{normalized}"

    def _rest_candidate_paths(self, path: str) -> list[str]:
        normalized = path if path.startswith("/") else f"/{path}"
        return [normalized]

    def _sleep_for_spacing(self) -> None:
        elapsed = time.monotonic() - self.last_request_ts
        if elapsed < self.min_interval_seconds:
            time.sleep(self.min_interval_seconds - elapsed)

    def _mark_request_complete(self) -> None:
        self.last_request_ts = time.monotonic()

    @staticmethod
    def _is_cloudflare_challenge(response: requests.Response) -> bool:
        return (
            response.headers.get("cf-mitigated", "").lower() == "challenge"
            or "just a moment" in (response.text or "").lower()
        )

    @staticmethod
    def _retry_after_seconds(response: requests.Response) -> float | None:
        value = (response.headers.get("Retry-After") or "").strip()
        if not value:
            return None
        try:
            return max(0.0, float(value))
        except ValueError:
            return None

    def _compute_backoff(
        self,
        attempt_index: int,
        response: requests.Response | None = None,
    ) -> float:
        retry_after = self._retry_after_seconds(response) if response is not None else None
        if retry_after is not None:
            return retry_after + random.uniform(0.1, 0.4)
        delay = min(self.base_backoff_seconds * (2**attempt_index), 12.0)
        return delay + random.uniform(0.1, 0.5)

    @staticmethod
    def _raise_for_response(response: requests.Response) -> None:
        if response.ok:
            return
        if WPCourseClient._is_cloudflare_challenge(response):
            raise WordPressRequestError("WordPress rejected the request with a browser challenge.")
        if response.status_code == 401:
            raise WordPressRequestError("WordPress authentication failed.")
        if response.status_code == 403:
            raise WordPressRequestError("WordPress denied this operation.")
        if response.status_code == 404:
            raise WordPressRequestError("The required WordPress endpoint was not found.")
        if response.status_code == 429:
            raise WordPressRequestError("WordPress is temporarily rate limiting requests.")
        if response.status_code >= 500:
            raise WordPressRequestError("WordPress is temporarily unavailable.")
        raise WordPressRequestError("WordPress rejected the request.")

    @staticmethod
    def _read_bounded_response(response: requests.Response) -> requests.Response:
        content_length = response.headers.get("Content-Length")
        if content_length:
            try:
                if int(content_length) > MAX_RESPONSE_BYTES:
                    response.close()
                    raise WordPressRequestError("WordPress returned a response that is too large.")
            except ValueError:
                pass
        chunks: list[bytes] = []
        total = 0
        for chunk in response.iter_content(chunk_size=64 * 1024):
            if not chunk:
                continue
            total += len(chunk)
            if total > MAX_RESPONSE_BYTES:
                response.close()
                raise WordPressRequestError("WordPress returned a response that is too large.")
            chunks.append(chunk)
        response._content = b"".join(chunks)
        response._content_consumed = True
        return response

    def _send_with_safe_redirects(
        self,
        method: str,
        url: str,
        *,
        auth=None,
        **kwargs,
    ) -> requests.Response:
        current_method = method.upper()
        current_url = url
        current_kwargs = dict(kwargs)

        for redirect_index in range(MAX_REDIRECTS + 1):
            current_url = validate_public_http_url(current_url)
            self._sleep_for_spacing()
            try:
                response = self.session.request(
                    method=current_method,
                    url=current_url,
                    auth=auth,
                    timeout=self.timeout,
                    allow_redirects=False,
                    stream=True,
                    **current_kwargs,
                )
            except (requests.Timeout, requests.ConnectionError) as exc:
                self._mark_request_complete()
                raise WordPressRequestError("Unable to reach WordPress.") from exc
            except requests.RequestException as exc:
                self._mark_request_complete()
                raise WordPressRequestError("WordPress request failed.") from exc
            self._mark_request_complete()
            response = self._read_bounded_response(response)

            if response.status_code not in {301, 302, 303, 307, 308}:
                return response
            location = response.headers.get("Location", "").strip()
            if not location:
                raise WordPressRequestError("WordPress returned an invalid redirect.")
            if redirect_index >= MAX_REDIRECTS:
                raise WordPressRequestError("WordPress returned too many redirects.")
            current_url = urljoin(current_url, location)
            validate_public_http_url(current_url)
            if response.status_code == 303 or (
                response.status_code in {301, 302} and current_method == "POST"
            ):
                current_method = "GET"
                current_kwargs.pop("json", None)
                current_kwargs.pop("data", None)
                current_kwargs.pop("files", None)
        raise WordPressRequestError("WordPress returned too many redirects.")

    def _request_with_retries(
        self,
        method: str,
        path: str,
        *,
        auth=None,
        retry_on_401_without_auth: bool = False,
        **kwargs,
    ) -> requests.Response:
        last_response: requests.Response | None = None
        for candidate_path in self._rest_candidate_paths(path):
            url = self._endpoint(candidate_path)
            for attempt in range(self.max_retries + 1):
                response = self._send_with_safe_redirects(method, url, auth=auth, **kwargs)
                if response.ok:
                    return response
                last_response = response
                if response.status_code == 401 and retry_on_401_without_auth and auth is not None:
                    fallback = self._send_with_safe_redirects(method, url, auth=None, **kwargs)
                    if fallback.ok:
                        return fallback
                    last_response = fallback
                if response.status_code in (403, 429, 500, 502, 503, 504) and attempt < self.max_retries:
                    time.sleep(self._compute_backoff(attempt, response))
                    continue
                break
        if last_response is not None:
            self._raise_for_response(last_response)
        raise WordPressRequestError("Unable to call the WordPress endpoint.")

    def _get_with_optional_auth(
        self,
        path: str,
        prefer_auth: bool = True,
        **kwargs,
    ) -> requests.Response:
        if prefer_auth:
            return self._request_with_retries(
                "GET",
                path,
                auth=self.auth,
                retry_on_401_without_auth=True,
                **kwargs,
            )
        return self._request_with_retries(
            "GET",
            path,
            auth=None,
            retry_on_401_without_auth=False,
            **kwargs,
        )

    @staticmethod
    def _response_json(response: requests.Response) -> Any:
        try:
            return response.json()
        except (requests.exceptions.JSONDecodeError, ValueError) as exc:
            raise WordPressRequestError("WordPress returned an invalid response.") from exc

    def get_course_by_slug(self, slug: str) -> dict[str, Any] | None:
        slug = str(slug or "").strip()
        if not slug:
            return None
        response = self._get_with_optional_auth(
            "/wp-json/wp/v2/cursuri",
            prefer_auth=True,
            params={"slug": slug},
        )
        data = self._response_json(response)
        if not isinstance(data, list):
            return None
        for item in data:
            if str((item or {}).get("slug", "")).strip() == slug:
                return item
        return None

    def test_connection(self) -> dict[str, Any]:
        response = self._request_with_retries(
            "GET",
            "/wp-json/wp/v2/users/me",
            auth=self.auth,
            retry_on_401_without_auth=False,
        )
        data = self._response_json(response)
        return data if isinstance(data, dict) else {}

    def resolve_course_post_id(
        self,
        slug: str | None = None,
        permalink: str | None = None,
        fallback_post_id: int | None = None,
    ) -> int | None:
        clean_slug = str(slug or "").strip()
        if not clean_slug and permalink:
            clean_slug = extract_slug_from_permalink(permalink)
        if not clean_slug:
            return None
        course = self.get_course_by_slug(clean_slug)
        if not course or course.get("id") is None:
            return None
        try:
            return int(course["id"])
        except (TypeError, ValueError):
            return None

    def get_course(self, post_id: int) -> dict[str, Any]:
        response = self._get_with_optional_auth(
            f"/wp-json/wp/v2/cursuri/{int(post_id)}",
            prefer_auth=True,
        )
        data = self._response_json(response)
        if not isinstance(data, dict):
            raise WordPressRequestError("WordPress returned an invalid response.")
        return data

    def update_course_program(
        self,
        post_id: int,
        final_program: list[dict],
        auth=None,
    ) -> dict[str, Any]:
        payload = {"acf": {"program": final_program if final_program else False}}
        response = self._request_with_retries(
            "POST",
            f"/wp-json/wp/v2/cursuri/{int(post_id)}",
            auth=auth or self.auth,
            retry_on_401_without_auth=False,
            json=payload,
        )
        data = self._response_json(response)
        if not isinstance(data, dict):
            raise WordPressRequestError("WordPress returned an invalid response.")
        return data


def extract_slug_from_permalink(url: str) -> str:
    parsed = urlparse((url or "").strip())
    parts = [part for part in (parsed.path or "").strip("/ ").split("/") if part]
    return parts[-1] if parts else ""


def parse_single_ro_date(value: str) -> date:
    return datetime.strptime(value.strip(), "%d.%m.%Y").date()


def parse_effective_end_date(text: str) -> date | None:
    text = str(text or "").strip()
    if not text:
        return None
    single = re.fullmatch(r"(\d{1,2})\.(\d{1,2})\.(\d{4})", text)
    if single:
        day, month, year = map(int, single.groups())
        try:
            return date(year, month, day)
        except ValueError:
            return None
    date_range = re.fullmatch(r"(\d{1,2})-(\d{1,2})\.(\d{1,2})\.(\d{4})", text)
    if date_range:
        _start_day, end_day, month, year = map(int, date_range.groups())
        try:
            return date(year, month, end_day)
        except ValueError:
            return None
    return None


def _normalize_excel_date_value(value: Any) -> str:
    if value is None:
        return ""
    if hasattr(value, "to_pydatetime"):
        value = value.to_pydatetime()
    if isinstance(value, datetime):
        return value.strftime("%d.%m.%Y")
    if isinstance(value, date):
        return value.strftime("%d.%m.%Y")
    return str(value).strip()


def expand_date_token(token: str) -> list[str]:
    token = _normalize_excel_date_value(token)
    if not token or token.lower() == "nan":
        return []
    token = token.replace("–", "-").replace("—", "-")
    if re.fullmatch(r"\d{1,2}\.\d{1,2}\.\d{4}", token):
        parsed = datetime.strptime(token, "%d.%m.%Y")
        return [parsed.strftime("%d.%m.%Y")]
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}(?:\s+\d{2}:\d{2}:\d{2})?", token):
        parsed = datetime.strptime(token[:10], "%Y-%m-%d")
        return [parsed.strftime("%d.%m.%Y")]
    match = re.fullmatch(r"(\d{1,2})-(\d{1,2})\.(\d{1,2})\.(\d{4})", token)
    if not match:
        return []
    start_day, end_day, month, year = map(int, match.groups())
    if end_day < start_day:
        return []
    out: list[str] = []
    for day in range(start_day, end_day + 1):
        normalized = f"{day:02d}.{month:02d}.{year}"
        try:
            parse_single_ro_date(normalized)
        except ValueError:
            return []
        out.append(normalized)
    return out


def split_cell_tokens(value: Any) -> list[str]:
    text = _normalize_excel_date_value(value)
    if not text or text.lower() == "nan":
        return []
    return [text]


def parse_excel_dates_from_row(row: dict) -> list[str]:
    dates: list[str] = []
    lowered_row = {str(key).strip().lower(): value for key, value in (row or {}).items()}
    for english_column, romanian_column in zip(MONTH_COLUMNS, ROMANIAN_MONTH_COLUMNS):
        raw_value = lowered_row.get(english_column.lower())
        if raw_value in (None, ""):
            raw_value = lowered_row.get(romanian_column.lower())
        for token in split_cell_tokens(raw_value):
            normalized = str(token).strip()
            if normalized:
                dates.append(normalized)
    return dates


def _filter_existing_non_expired_rows(
    program: list[dict],
    today: date,
) -> list[dict[str, str]]:
    normalized: list[dict[str, str]] = []
    seen: set[str] = set()
    for row in program or []:
        raw = str((row or {}).get("data", "")).strip()
        if not raw:
            continue
        end_date = parse_effective_end_date(raw)
        if end_date is not None and end_date >= today and raw not in seen:
            normalized.append({"data": raw})
            seen.add(raw)
    return normalized


def build_final_program(
    existing_program: list,
    excel_dates: list[str],
    today: date,
) -> list[dict]:
    seen: set[str] = set()
    result: list[dict[str, str]] = []
    for row in _filter_existing_non_expired_rows(existing_program, today):
        raw = row["data"]
        if raw not in seen:
            result.append({"data": raw})
            seen.add(raw)
    for raw in excel_dates:
        normalized = str(raw).strip()
        if normalized and normalized not in seen:
            result.append({"data": normalized})
            seen.add(normalized)
    return result


def valid_existing_program(existing_program: list, today: date) -> list[dict[str, str]]:
    return _filter_existing_non_expired_rows(existing_program, today)
```
