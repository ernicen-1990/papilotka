"""Explore current theme structure via REST API."""
import json
from wp_client import WordPressClient, SITE_URL
import requests
from dotenv import load_dotenv
import os

load_dotenv()
wp = WordPressClient()

session = wp.session
base = SITE_URL.rstrip("/")

def get(path, params=None):
    r = session.get(f"{base}/wp-json/wp/v2{path}", params=params)
    if r.status_code == 200:
        return r.json()
    return {"error": r.status_code, "text": r.text[:200]}

# Active theme
themes = get("/themes", {"status": "active"})
print("=== ACTIVE THEME ===")
print(json.dumps(themes, indent=2, ensure_ascii=False))

# Templates
print("\n=== TEMPLATES ===")
templates = get("/templates", {"per_page": 100})
print(json.dumps(templates, indent=2, ensure_ascii=False))

# Template parts
print("\n=== TEMPLATE PARTS ===")
parts = get("/template-parts", {"per_page": 100})
print(json.dumps(parts, indent=2, ensure_ascii=False))

# Global styles
print("\n=== GLOBAL STYLES ===")
gs = get("/global-styles/themes/" + (themes[0]["stylesheet"] if themes and isinstance(themes, list) else ""))
print(json.dumps(gs, indent=2, ensure_ascii=False))

# Menus / nav
print("\n=== MENUS ===")
menus = get("/menus", {"per_page": 100})
print(json.dumps(menus, indent=2, ensure_ascii=False))

# Pages (to understand site structure)
print("\n=== PAGES ===")
pages = get("/pages", {"per_page": 100, "_fields": "id,slug,title,parent,template,status"})
print(json.dumps(pages, indent=2, ensure_ascii=False))

# Posts
print("\n=== RECENT POSTS ===")
posts = get("/posts", {"per_page": 5, "_fields": "id,slug,title,categories,tags"})
print(json.dumps(posts, indent=2, ensure_ascii=False))

# Categories
print("\n=== CATEGORIES ===")
cats = get("/categories", {"per_page": 100})
print(json.dumps(cats, indent=2, ensure_ascii=False))
