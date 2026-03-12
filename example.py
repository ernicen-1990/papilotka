"""Example usage of the WordPress REST API client."""

from wp_client import WordPressClient

wp = WordPressClient()

# Fetch site info (no auth required)
info = wp.get_site_info()
print(f"Site: {info.get('name')} — {info.get('description')}")
print(f"URL:  {info.get('url')}")
print()

# List recent posts (no auth required)
posts = wp.get_posts(per_page=5, orderby="date", order="desc")
print(f"Latest {len(posts)} post(s):")
for p in posts:
    print(f"  [{p['id']}] {p['title']['rendered']}")
print()

# Authenticated actions — requires WP_USERNAME + WP_APP_PASSWORD in .env
# draft = wp.create_post("Hello from API", "<p>Created via REST API</p>")
# print(f"Created draft post: {draft['link']}")
