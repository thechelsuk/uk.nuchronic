from __future__ import annotations

from html import unescape
import json
from pathlib import Path
import re
from urllib.parse import urlencode
from urllib.request import Request, urlopen

import yaml


ROOT = Path(__file__).resolve().parent.parent
CONFIG_FILE = ROOT / "_config.yml"
POSTS_DIR = ROOT / "_posts"
OUTPUT_FILE = ROOT / "_data" / "webmentions.yml"
COUNT_API = "https://webmention.io/api/count"
MENTIONS_API = "https://webmention.io/api/mentions.jf2"
USER_AGENT = "nuchronic-webmention-sync/1.0"
SLUG_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}-(.+)$")
TAG_PATTERN = re.compile(r"<[^>]+>")


def load_site_url() -> str:
    payload = yaml.safe_load(CONFIG_FILE.read_text(encoding="utf-8")) or {}
    site_url = str(payload.get("url", "")).strip().rstrip("/")
    if not site_url:
        raise ValueError("The Jekyll config must define a non-empty url.")
    return site_url


def derive_slug(post_path: Path) -> str:
    match = SLUG_PATTERN.match(post_path.stem)
    if match:
        return match.group(1)
    return post_path.stem


def fetch_json(base_url: str, params: dict[str, object]) -> dict[str, object]:
    url = f"{base_url}?{urlencode(params)}"
    request = Request(url, headers={"User-Agent": USER_AGENT})
    with urlopen(request, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def strip_html(value: str) -> str:
    return unescape(TAG_PATTERN.sub("", value)).strip()


def extract_content_text(entry: dict[str, object]) -> str:
    content = entry.get("content")
    if isinstance(content, dict):
        text_value = str(content.get("text", "")).strip()
        if text_value:
            return text_value

        html_value = str(content.get("html", "")).strip()
        if html_value:
            return strip_html(html_value)

    if isinstance(content, str) and content.strip():
        return content.strip()

    summary = str(entry.get("summary", "")).strip()
    return strip_html(summary) if summary else ""


def normalize_author(entry: dict[str, object]) -> dict[str, str]:
    author = entry.get("author")
    if not isinstance(author, dict):
        author = {}

    author_url = str(author.get("url", "")).strip()
    author_name = str(author.get("name", "")).strip() or author_url or "Someone"
    author_photo = str(author.get("photo", "")).strip()
    return {
        "author_name": author_name,
        "author_url": author_url,
        "author_photo": author_photo,
    }


def classify_mention(property_name: str) -> str:
    if property_name == "in-reply-to":
        return "replies"
    if property_name in {"like-of", "favorite-of", "bookmark-of", "rsvp-yes", "rsvp-no", "rsvp-maybe", "rsvp-interested", "emoji-react-of"}:
        return "likes"
    if property_name in {"repost-of", "share-of"}:
        return "reposts"
    return "mentions"


def normalize_mention(entry: dict[str, object]) -> dict[str, str]:
    property_name = str(entry.get("wm-property", "mention-of")).strip().lower()
    normalized = normalize_author(entry)
    normalized.update(
        {
            "url": str(entry.get("url", "")).strip(),
            "published": str(entry.get("published", "")).strip() or str(entry.get("wm-received", "")).strip(),
            "property": property_name,
            "content_text": extract_content_text(entry),
        }
    )
    return normalized


def sort_mentions(items: list[dict[str, str]]) -> list[dict[str, str]]:
    return sorted(items, key=lambda item: (item.get("published", ""), item.get("author_name", "")), reverse=True)


def load_existing_data() -> dict[str, object]:
    if not OUTPUT_FILE.exists():
        return {}
    payload = yaml.safe_load(OUTPUT_FILE.read_text(encoding="utf-8")) or {}
    return payload if isinstance(payload, dict) else {}


def build_default_record(target_url: str) -> dict[str, object]:
    return {
        "target": target_url,
        "count": 0,
        "types": {},
        "replies": [],
        "likes": [],
        "reposts": [],
        "mentions": [],
    }


def build_record(target_url: str) -> dict[str, object]:
    count_payload = fetch_json(COUNT_API, {"target": target_url})
    mentions_payload = fetch_json(MENTIONS_API, {"target": target_url, "per-page": 1000})

    replies: list[dict[str, str]] = []
    likes: list[dict[str, str]] = []
    reposts: list[dict[str, str]] = []
    mentions: list[dict[str, str]] = []

    for child in mentions_payload.get("children", []):
        if not isinstance(child, dict):
            continue

        normalized = normalize_mention(child)
        bucket = classify_mention(normalized["property"])
        if bucket == "replies":
            replies.append(normalized)
        elif bucket == "likes":
            likes.append(normalized)
        elif bucket == "reposts":
            reposts.append(normalized)
        else:
            mentions.append(normalized)

    record = build_default_record(target_url)
    record["count"] = int(count_payload.get("count", 0) or 0)
    raw_types = count_payload.get("type")
    if isinstance(raw_types, dict):
        record["types"] = {str(key): int(value or 0) for key, value in raw_types.items()}
    record["replies"] = sort_mentions(replies)
    record["likes"] = sort_mentions(likes)
    record["reposts"] = sort_mentions(reposts)
    record["mentions"] = sort_mentions(mentions)
    return record


def write_output(payload: dict[str, object]) -> None:
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    content = yaml.safe_dump(payload, sort_keys=False, allow_unicode=True).strip()
    OUTPUT_FILE.write_text(f"{content}\n", encoding="utf-8")


def main() -> int:
    site_url = load_site_url()
    existing_data = load_existing_data()
    results: dict[str, object] = {}

    for post_path in sorted(POSTS_DIR.glob("*.md")):
        slug = derive_slug(post_path)
        target_url = f"{site_url}/item/{slug}/"

        try:
            results[slug] = build_record(target_url)
        except Exception as exc:
            if slug in existing_data:
                print(f"Warning: failed to update {slug}: {exc}. Keeping existing data.")
                results[slug] = existing_data[slug]
            else:
                print(f"Warning: failed to update {slug}: {exc}. Falling back to an empty record.")
                results[slug] = build_default_record(target_url)

    write_output(results)
    print(f"Webmention sync complete: wrote {len(results)} record(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())