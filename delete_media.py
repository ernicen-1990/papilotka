"""Delete all media items concurrently using ThreadPoolExecutor."""
import concurrent.futures, requests
from wp_client import WordPressClient, SITE_URL
from dotenv import load_dotenv

load_dotenv()
wp = WordPressClient()
base = SITE_URL.rstrip("/")


def get_all_media_ids():
    ids = []
    page = 1
    while True:
        r = wp.session.get(f"{base}/wp-json/wp/v2/media", params={"per_page": 100, "page": page, "_fields": "id"})
        if r.status_code != 200:
            break
        items = r.json()
        if not items:
            break
        ids.extend(item["id"] for item in items)
        total_pages = int(r.headers.get("X-WP-TotalPages", 1))
        if page >= total_pages:
            break
        page += 1
    return ids


def delete_one(media_id):
    r = wp.session.post(
        f"{base}/wp-json/wp/v2/media/{media_id}",
        headers={"X-HTTP-Method-Override": "DELETE"},
        json={"force": True},
    )
    return media_id, r.status_code


print("Fetching all media IDs...")
ids = get_all_media_ids()
print(f"Found {len(ids)} media items. Deleting with 8 threads...")

deleted = 0
errors = 0
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:
    for mid, code in ex.map(delete_one, ids):
        if code in (200, 204, 410):
            deleted += 1
        else:
            errors += 1

print(f"Done. Deleted: {deleted}, Errors: {errors}")
