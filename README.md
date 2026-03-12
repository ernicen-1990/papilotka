# papilotka — WordPress REST API Client

Python client for [https://papilotka.com/papilotka-com](https://papilotka.com/papilotka-com).

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env
```

Edit `.env` and fill in your credentials:

```
WP_SITE_URL=https://papilotka.com/papilotka-com
WP_USERNAME=your_username
WP_APP_PASSWORD=xxxx xxxx xxxx xxxx xxxx xxxx
```

> **Application Password**: in WordPress go to
> *Users → Profile → Application Passwords*, enter a name and click **Add New**.

## Quick start

```bash
python example.py
```

## Usage

```python
from wp_client import WordPressClient

wp = WordPressClient()

# Public reads (no auth)
info  = wp.get_site_info()
posts = wp.get_posts(per_page=10)
pages = wp.get_pages()

# Authenticated writes
draft = wp.create_post("My Title", "<p>Content</p>", status="draft")
wp.update_post(draft["id"], status="publish")
wp.delete_post(draft["id"], force=True)
```

## API Reference

| Method | Description |
|---|---|
| `get_site_info()` | Site name, description, URL |
| `get_posts(**params)` | List posts |
| `get_post(id)` | Single post |
| `create_post(title, content, status, **kwargs)` | Create post |
| `update_post(id, **fields)` | Update post |
| `delete_post(id, force)` | Delete / trash post |
| `get_pages(**params)` | List pages |
| `get_page(id)` | Single page |
| `create_page(title, content, status, **kwargs)` | Create page |
| `update_page(id, **fields)` | Update page |
| `get_categories(**params)` | List categories |
| `get_tags(**params)` | List tags |
| `get_media(**params)` | List media |
| `upload_media(file_path, title)` | Upload a file |
| `get_users(**params)` | List users |
| `get_current_user()` | Authenticated user info |
