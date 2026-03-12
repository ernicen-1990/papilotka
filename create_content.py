"""
Content creation (posts already deleted by rebuild_content.py):
1. Create portfolio category
2. Create 4 portfolio posts
3. Create 5 pages
4. Create navigation
5. Configure settings
"""

import json
from wp_client import WordPressClient, SITE_URL
from dotenv import load_dotenv

load_dotenv()
wp = WordPressClient()
session = wp.session
base = SITE_URL.rstrip("/")


def api(method, path, **kwargs):
    r = getattr(session, method)(f"{base}/wp-json/wp/v2{path}", **kwargs)
    return r


# ── 1. CREATE PORTFOLIO CATEGORY ──────────────────────────────────────────────
print("=== CREATING PORTFOLIO CATEGORY ===")
r = api("post", "/categories", json={"name": "Portfolio", "slug": "portfolio", "description": "Nasze realizacje filmowe"})
if r.status_code == 201:
    portfolio_cat_id = r.json()["id"]
    print(f"  ✓ Created category 'portfolio' id={portfolio_cat_id}")
elif r.status_code == 400 and "term_exists" in r.text:
    r2 = api("get", "/categories", params={"slug": "portfolio"})
    cats = r2.json()
    portfolio_cat_id = cats[0]["id"] if cats else None
    print(f"  ~ Category already exists id={portfolio_cat_id}")
else:
    print(f"  ✗ Category error: {r.status_code} {r.text[:200]}")
    portfolio_cat_id = None

# ── 2. CREATE PORTFOLIO POSTS ─────────────────────────────────────────────────
print("\n=== CREATING PORTFOLIO POSTS ===")

portfolio_posts = [
    {
        "title": "Kampania reklamowa dla branży FMCG",
        "slug":  "kampania-reklamowa-fmcg",
        "excerpt": "Kompleksowa produkcja spotu TV i materiałów online dla wiodącej marki z sektora dóbr szybkozbywalnych.",
        "content": """<!-- wp:group {"style":{"spacing":{"blockGap":"var(--wp--preset--spacing--40)"}},"layout":{"type":"constrained","contentSize":"780px"}} -->
<div class="wp-block-group">
<!-- wp:heading {"level":6} -->
<h6 class="wp-block-heading">Filmy reklamowe</h6>
<!-- /wp:heading -->
<!-- wp:heading {"level":1} -->
<h1 class="wp-block-heading">Kampania reklamowa dla branży FMCG</h1>
<!-- /wp:heading -->
<!-- wp:paragraph {"style":{"color":{"text":"var(--wp--preset--color--muted)"},"typography":{"fontSize":"var(--wp--preset--font-size--lg)"}}} -->
<p style="color:var(--wp--preset--color--muted);font-size:var(--wp--preset--font-size--lg)">Spot TV, materiały online i content do social media — całościowa produkcja dla wiodącej marki FMCG.</p>
<!-- /wp:paragraph -->
<!-- wp:separator {"className":"is-style-wide","style":{"border":{"color":"var(--wp--preset--color--surface-2)","width":"1px"}}} -->
<hr class="wp-block-separator is-style-wide" style="border-color:var(--wp--preset--color--surface-2)"/>
<!-- /wp:separator -->
<!-- wp:columns -->
<div class="wp-block-columns">
<!-- wp:column -->
<div class="wp-block-column">
<!-- wp:heading {"level":6} -->
<h6 class="wp-block-heading">Zakres</h6>
<!-- /wp:heading -->
<!-- wp:paragraph {"style":{"color":{"text":"var(--wp--preset--color--muted)"}}} --><p style="color:var(--wp--preset--color--muted)">Spot TV 30s, film 60s online, 6 formatów social media</p><!-- /wp:paragraph -->
</div><!-- /wp:column -->
<!-- wp:column -->
<div class="wp-block-column">
<!-- wp:heading {"level":6} -->
<h6 class="wp-block-heading">Czas realizacji</h6>
<!-- /wp:heading -->
<!-- wp:paragraph {"style":{"color":{"text":"var(--wp--preset--color--muted)"}}} --><p style="color:var(--wp--preset--color--muted)">3 tygodnie od briefa do deliverables</p><!-- /wp:paragraph -->
</div><!-- /wp:column -->
<!-- wp:column -->
<div class="wp-block-column">
<!-- wp:heading {"level":6} -->
<h6 class="wp-block-heading">Klient</h6>
<!-- /wp:heading -->
<!-- wp:paragraph {"style":{"color":{"text":"var(--wp--preset--color--muted)"}}} --><p style="color:var(--wp--preset--color--muted)">Branża FMCG, dystrybucja ogólnopolska</p><!-- /wp:paragraph -->
</div><!-- /wp:column -->
</div><!-- /wp:columns -->
</div><!-- /wp:group -->""",
    },
    {
        "title": "Film eventowy – Gala Biznesu 2024",
        "slug":  "film-eventowy-gala-biznesu-2024",
        "excerpt": "Dynamiczny film relacyjny z prestiżowej gali biznesowej — atmosfera, emocje i kluczowe momenty wieczoru.",
        "content": """<!-- wp:group {"layout":{"type":"constrained","contentSize":"780px"}} -->
<div class="wp-block-group">
<!-- wp:heading {"level":6} -->
<h6 class="wp-block-heading">Filmy eventowe</h6>
<!-- /wp:heading -->
<!-- wp:heading {"level":1} -->
<h1 class="wp-block-heading">Film eventowy – Gala Biznesu 2024</h1>
<!-- /wp:heading -->
<!-- wp:paragraph {"style":{"color":{"text":"var(--wp--preset--color--muted)"},"typography":{"fontSize":"var(--wp--preset--font-size--lg)"}}} -->
<p style="color:var(--wp--preset--color--muted);font-size:var(--wp--preset--font-size--lg)">Prestiżowa gala dla 500 gości — uchwyciliśmy każdy ważny moment tego wyjątkowego wieczoru.</p>
<!-- /wp:paragraph -->
<!-- wp:separator {"className":"is-style-wide","style":{"border":{"color":"var(--wp--preset--color--surface-2)","width":"1px"}}} -->
<hr class="wp-block-separator is-style-wide" style="border-color:var(--wp--preset--color--surface-2)"/>
<!-- /wp:separator -->
<!-- wp:paragraph {"style":{"color":{"text":"var(--wp--preset--color--muted)"}}} -->
<p style="color:var(--wp--preset--color--muted)">Realizacja wielokamerowa, transmisja live, aftermovie 3 minutowy i skróty do social media. Całość zmontowana i dostarczona w ciągu 48 godzin od eventu.</p>
<!-- /wp:paragraph -->
</div><!-- /wp:group -->""",
    },
    {
        "title": "Brand story – Startup technologiczny",
        "slug":  "brand-story-startup-technologiczny",
        "excerpt": "Historia marki opowiedziana obrazem — skąd pochodzi, dokąd zmierza i co ją wyróżnia na rynku.",
        "content": """<!-- wp:group {"layout":{"type":"constrained","contentSize":"780px"}} -->
<div class="wp-block-group">
<!-- wp:heading {"level":6} -->
<h6 class="wp-block-heading">Brand storytelling</h6>
<!-- /wp:heading -->
<!-- wp:heading {"level":1} -->
<h1 class="wp-block-heading">Brand story – Startup technologiczny</h1>
<!-- /wp:heading -->
<!-- wp:paragraph {"style":{"color":{"text":"var(--wp--preset--color--muted)"},"typography":{"fontSize":"var(--wp--preset--font-size--lg)"}}} -->
<p style="color:var(--wp--preset--color--muted);font-size:var(--wp--preset--font-size--lg)">Tworzenie historii marki, która angażuje inwestorów, klientów i pracowników.</p>
<!-- /wp:paragraph -->
<!-- wp:separator {"className":"is-style-wide","style":{"border":{"color":"var(--wp--preset--color--surface-2)","width":"1px"}}} -->
<hr class="wp-block-separator is-style-wide" style="border-color:var(--wp--preset--color--surface-2)"/>
<!-- /wp:separator -->
<!-- wp:paragraph {"style":{"color":{"text":"var(--wp--preset--color--muted)"}}} -->
<p style="color:var(--wp--preset--color--muted)">Film 90-sekundowy opowiadający historię założycieli, produkt i misję firmy. Stworzony na potrzeby rundy inwestycyjnej serii A.</p>
<!-- /wp:paragraph -->
</div><!-- /wp:group -->""",
    },
    {
        "title": "Spot produktowy – Premium Cosmetics",
        "slug":  "spot-produktowy-premium-cosmetics",
        "excerpt": "Elegancki spot produktowy w stylu luxury — zmysłowe kadry, precyzyjne oświetlenie, pełna kontrola nad marką.",
        "content": """<!-- wp:group {"layout":{"type":"constrained","contentSize":"780px"}} -->
<div class="wp-block-group">
<!-- wp:heading {"level":6} -->
<h6 class="wp-block-heading">Filmy produktowe</h6>
<!-- /wp:heading -->
<!-- wp:heading {"level":1} -->
<h1 class="wp-block-heading">Spot produktowy – Premium Cosmetics</h1>
<!-- /wp:heading -->
<!-- wp:paragraph {"style":{"color":{"text":"var(--wp--preset--color--muted)"},"typography":{"fontSize":"var(--wp--preset--font-size--lg)"}}} -->
<p style="color:var(--wp--preset--color--muted);font-size:var(--wp--preset--font-size--lg)">Luxury production — slow motion, macro, profesjonalne oświetlenie studyjne.</p>
<!-- /wp:paragraph -->
<!-- wp:separator {"className":"is-style-wide","style":{"border":{"color":"var(--wp--preset--color--surface-2)","width":"1px"}}} -->
<hr class="wp-block-separator is-style-wide" style="border-color:var(--wp--preset--color--surface-2)"/>
<!-- /wp:separator -->
<!-- wp:paragraph {"style":{"color":{"text":"var(--wp--preset--color--muted)"}}} -->
<p style="color:var(--wp--preset--color--muted)">Film 20-sekundowy do kampanii Instagram Reels i TikTok, plus wersja 30s na YouTube. Realizacja w studio z kontrolowanym oświetleniem i tłem chroma key.</p>
<!-- /wp:paragraph -->
</div><!-- /wp:group -->""",
    },
]

for post_data in portfolio_posts:
    r = api("post", "/posts", json={
        "title":      post_data["title"],
        "slug":       post_data["slug"],
        "status":     "publish",
        "excerpt":    post_data["excerpt"],
        "content":    post_data["content"],
        "categories": [portfolio_cat_id] if portfolio_cat_id else [],
    })
    if r.status_code == 201:
        print(f"  ✓ Post: {post_data['title']}")
    else:
        print(f"  ✗ Failed: {post_data['title']} → {r.status_code}: {r.text[:150]}")

# ── 3. PAGES ───────────────────────────────────────────────────────────────────
print("\n=== CREATING PAGES ===")

about_content = open("/home/user/papilotka/page_about.html").read()
services_content = open("/home/user/papilotka/page_services.html").read()
contact_content = open("/home/user/papilotka/page_contact.html").read()

pages_to_create = [
    {"title": "Strona główna", "slug": "home",     "content": "<!-- front-page.html template handles this page -->", "template": "",          "menu_order": 0},
    {"title": "Portfolio",     "slug": "portfolio","content": "<!-- portfolio.html template handles this page -->",   "template": "portfolio", "menu_order": 1},
    {"title": "O nas",         "slug": "o-nas",    "content": about_content,                                         "template": "no-title",  "menu_order": 2},
    {"title": "Usługi",        "slug": "uslugi",   "content": services_content,                                      "template": "no-title",  "menu_order": 3},
    {"title": "Kontakt",       "slug": "kontakt",  "content": contact_content,                                       "template": "no-title",  "menu_order": 4},
]

page_ids = {}
for pg in pages_to_create:
    r = api("post", "/pages", json={
        "title":      pg["title"],
        "slug":       pg["slug"],
        "status":     "publish",
        "content":    pg["content"],
        "template":   pg["template"],
        "menu_order": pg["menu_order"],
    })
    if r.status_code == 201:
        pid = r.json()["id"]
        page_ids[pg["slug"]] = pid
        print(f"  ✓ Page '{pg['title']}' id={pid}")
    else:
        print(f"  ✗ Failed '{pg['title']}': {r.status_code} {r.text[:200]}")

# ── 4. NAVIGATION ──────────────────────────────────────────────────────────────
print("\n=== CREATING NAVIGATION ===")

port_id   = page_ids.get("portfolio", "")
onas_id   = page_ids.get("o-nas", "")
uslugi_id = page_ids.get("uslugi", "")
kontakt_id= page_ids.get("kontakt", "")

nav_content = f"""<!-- wp:navigation-link {{"label":"Portfolio","type":"page","id":{port_id},"url":"{base}/portfolio/","kind":"post-type"}} /-->
<!-- wp:navigation-link {{"label":"Usługi","type":"page","id":{uslugi_id},"url":"{base}/uslugi/","kind":"post-type"}} /-->
<!-- wp:navigation-link {{"label":"O nas","type":"page","id":{onas_id},"url":"{base}/o-nas/","kind":"post-type"}} /-->"""

r = api("post", "/navigation", json={
    "title":   "Menu główne",
    "slug":    "menu-glowne",
    "status":  "publish",
    "content": nav_content,
})
if r.status_code == 201:
    nav_id = r.json()["id"]
    print(f"  ✓ Navigation created id={nav_id}")
else:
    # try to find existing
    r2 = api("get", "/navigation", params={"slug": "menu-glowne"})
    navs = r2.json()
    nav_id = navs[0]["id"] if navs else None
    print(f"  ~ Nav id={nav_id}: {r.status_code} {r.text[:100]}")

# ── 5. SETTINGS ────────────────────────────────────────────────────────────────
print("\n=== CONFIGURING SETTINGS ===")

home_page_id = page_ids.get("home")
if home_page_id:
    r = api("post", "/settings", json={
        "title":         "Papilotka.com | Dom produkcyjny",
        "description":   "Filmy reklamowe · Brand storytelling · Filmy eventowe",
        "show_on_front": "page",
        "page_on_front": home_page_id,
        "page_for_posts": 0,
    })
    if r.status_code == 200:
        print(f"  ✓ Front page = Home (id={home_page_id}), title + tagline updated")
    else:
        print(f"  ✗ Settings: {r.status_code} {r.text[:200]}")

# ── SUMMARY ────────────────────────────────────────────────────────────────────
print("\n=== SUMMARY ===")
print(f"Navigation ID  : {nav_id}")
print(f"Page IDs       : {page_ids}")
print(f"Portfolio cat  : {portfolio_cat_id}")
print("Done! Update header.html with nav id:", nav_id)
