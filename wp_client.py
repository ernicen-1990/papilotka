"""WordPress REST API client for https://papilotka.com/papilotka-com"""

import os
from typing import Any
import requests
from dotenv import load_dotenv

load_dotenv()

SITE_URL = os.getenv("WP_SITE_URL", "https://papilotka.com/papilotka-com")
API_BASE = f"{SITE_URL.rstrip('/')}/wp-json/wp/v2"


class WordPressClient:
    def __init__(self, username: str = None, app_password: str = None):
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json"})

        username = username or os.getenv("WP_USERNAME")
        app_password = app_password or os.getenv("WP_APP_PASSWORD")
        if username and app_password:
            self.session.auth = (username, app_password)

    # --- Posts ---

    def get_posts(self, **params) -> list[dict]:
        return self._get("/posts", params=params)

    def get_post(self, post_id: int) -> dict:
        return self._get(f"/posts/{post_id}")

    def create_post(self, title: str, content: str, status: str = "draft", **kwargs) -> dict:
        return self._post("/posts", {"title": title, "content": content, "status": status, **kwargs})

    def update_post(self, post_id: int, **fields) -> dict:
        return self._patch(f"/posts/{post_id}", fields)

    def delete_post(self, post_id: int, force: bool = False) -> dict:
        return self._delete(f"/posts/{post_id}", params={"force": force})

    # --- Pages ---

    def get_pages(self, **params) -> list[dict]:
        return self._get("/pages", params=params)

    def get_page(self, page_id: int) -> dict:
        return self._get(f"/pages/{page_id}")

    def create_page(self, title: str, content: str, status: str = "draft", **kwargs) -> dict:
        return self._post("/pages", {"title": title, "content": content, "status": status, **kwargs})

    def update_page(self, page_id: int, **fields) -> dict:
        return self._patch(f"/pages/{page_id}", fields)

    # --- Categories & Tags ---

    def get_categories(self, **params) -> list[dict]:
        return self._get("/categories", params=params)

    def get_tags(self, **params) -> list[dict]:
        return self._get("/tags", params=params)

    # --- Media ---

    def get_media(self, **params) -> list[dict]:
        return self._get("/media", params=params)

    def upload_media(self, file_path: str, title: str = None) -> dict:
        with open(file_path, "rb") as f:
            filename = os.path.basename(file_path)
            headers = {
                "Content-Disposition": f'attachment; filename="{filename}"',
                "Content-Type": "application/octet-stream",
            }
            if title:
                headers["Content-Disposition"] += f'; title="{title}"'
            resp = self.session.post(f"{API_BASE}/media", data=f, headers=headers)
        return self._handle(resp)

    # --- Users ---

    def get_users(self, **params) -> list[dict]:
        return self._get("/users", params=params)

    def get_current_user(self) -> dict:
        return self._get("/users/me")

    # --- Site info ---

    def get_site_info(self) -> dict:
        resp = self.session.get(f"{SITE_URL.rstrip('/')}/wp-json")
        return self._handle(resp)

    # --- Internal helpers ---

    def _get(self, path: str, params: dict = None) -> Any:
        return self._handle(self.session.get(f"{API_BASE}{path}", params=params))

    def _post(self, path: str, data: dict) -> Any:
        return self._handle(self.session.post(f"{API_BASE}{path}", json=data))

    def _patch(self, path: str, data: dict) -> Any:
        return self._handle(self.session.patch(f"{API_BASE}{path}", json=data))

    def _delete(self, path: str, params: dict = None) -> Any:
        return self._handle(self.session.delete(f"{API_BASE}{path}", params=params))

    @staticmethod
    def _handle(resp: requests.Response) -> Any:
        resp.raise_for_status()
        return resp.json()
