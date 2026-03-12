"""
Full site content rebuild.
1. Delete all posts, pages, media
2. Create portfolio category + 4 portfolio posts
3. Create 5 pages (Home, Portfolio, O nas, Usługi, Kontakt) with block content
4. Create navigation menu
5. Configure WordPress settings
"""

import json, time
from wp_client import WordPressClient, SITE_URL
from dotenv import load_dotenv

load_dotenv()
wp = WordPressClient()
session = wp.session
base = SITE_URL.rstrip("/")


def api(method, path, **kwargs):
    r = getattr(session, method)(f"{base}/wp-json/wp/v2{path}", **kwargs)
    return r


def force_delete(path):
    """Use X-HTTP-Method-Override because direct DELETE returns 405 on this host."""
    r = session.post(
        f"{base}/wp-json/wp/v2{path}",
        headers={"X-HTTP-Method-Override": "DELETE"},
        json={"force": True},
    )
    return r


def delete_all(post_type):
    page = 1
    deleted = 0
    while True:
        r = api("get", f"/{post_type}", params={"per_page": 100, "page": page, "status": "any"})
        if r.status_code != 200:
            break
        items = r.json()
        if not items:
            break
        for item in items:
            iid = item["id"]
            r2 = force_delete(f"/{post_type}/{iid}")
            if r2.status_code in (200, 204, 410):
                deleted += 1
            else:
                print(f"  WARN: could not force-delete {post_type}/{iid}: {r2.status_code} {r2.text[:80]}")
        page += 1
    print(f"  Deleted {deleted} {post_type}")


# ── 1. DELETE EXISTING CONTENT ────────────────────────────────────────────────
print("=== DELETING EXISTING CONTENT ===")
delete_all("posts")
delete_all("pages")
# delete media
page = 1
media_deleted = 0
while True:
    r = api("get", "/media", params={"per_page": 100, "page": page})
    if r.status_code != 200:
        break
    items = r.json()
    if not items:
        break
    for item in items:
        r2 = force_delete(f"/media/{item['id']}")
        if r2.status_code in (200, 204):
            media_deleted += 1
    page += 1
print(f"  Deleted {media_deleted} media items")

# ── 2. CREATE PORTFOLIO CATEGORY ──────────────────────────────────────────────
print("\n=== CREATING PORTFOLIO CATEGORY ===")
r = api("post", "/categories", json={"name": "Portfolio", "slug": "portfolio", "description": "Nasze realizacje filmowe"})
if r.status_code == 201:
    portfolio_cat_id = r.json()["id"]
    print(f"  Created category 'portfolio' id={portfolio_cat_id}")
else:
    # Already exists?
    r2 = api("get", "/categories", params={"slug": "portfolio"})
    cats = r2.json()
    portfolio_cat_id = cats[0]["id"] if cats else None
    print(f"  Category exists, id={portfolio_cat_id}")

# ── 3. CREATE PORTFOLIO POSTS ─────────────────────────────────────────────────
print("\n=== CREATING PORTFOLIO POSTS ===")

portfolio_posts = [
    {
        "title": "Kampania reklamowa dla branży FMCG",
        "slug": "kampania-reklamowa-fmcg",
        "excerpt": "Kompletna produkcja spotu TV i materiałów online dla wiodącej marki z sektora dóbr szybkozbywalnych.",
        "content": """<!-- wp:group {"style":{"spacing":{"blockGap":"var(--wp--preset--spacing--50)"}},"layout":{"type":"constrained"}} -->
<div class="wp-block-group">
<!-- wp:heading {"level":6} -->
<h6 class="wp-block-heading">Filmy reklamowe</h6>
<!-- /wp:heading -->
<!-- wp:heading {"level":1} -->
<h1 class="wp-block-heading">Kampania reklamowa dla branży FMCG</h1>
<!-- /wp:heading -->
<!-- wp:paragraph {"style":{"color":{"text":"var(--wp--preset--color--muted)"}}} -->
<p style="color:var(--wp--preset--color--muted)">Spot TV, materiały online i content do social media — całościowa produkcja dla wiodącej marki FMCG.</p>
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
<!-- wp:paragraph {"style":{"color":{"text":"var(--wp--preset--color--muted)"}}} -->
<p style="color:var(--wp--preset--color--muted)">Spot TV 30s, film 60s online, 6 formatów social media</p>
<!-- /wp:paragraph -->
</div>
<!-- /wp:column -->
<!-- wp:column -->
<div class="wp-block-column">
<!-- wp:heading {"level":6} -->
<h6 class="wp-block-heading">Czas realizacji</h6>
<!-- /wp:heading -->
<!-- wp:paragraph {"style":{"color":{"text":"var(--wp--preset--color--muted)"}}} -->
<p style="color:var(--wp--preset--color--muted)">3 tygodnie</p>
<!-- /wp:paragraph -->
</div>
<!-- /wp:column -->
</div>
<!-- /wp:columns -->
<!-- wp:embed {"url":"https://www.youtube.com/watch?v=dQw4w9WgXcQ","type":"video","providerNameSlug":"youtube","responsive":true,"className":"wp-embed-aspect-16-9 wp-has-aspect-ratio"} -->
<figure class="wp-block-embed is-type-video is-provider-youtube wp-block-embed-youtube wp-embed-aspect-16-9 wp-has-aspect-ratio"><div class="wp-block-embed__wrapper">
https://www.youtube.com/watch?v=dQw4w9WgXcQ
</div></figure>
<!-- /wp:embed -->
</div>
<!-- /wp:group -->""",
    },
    {
        "title": "Film eventowy – Gala Biznesu 2024",
        "slug": "film-eventowy-gala-biznesu-2024",
        "excerpt": "Dynamiczny film relacyjny z prestiżowej gali biznesowej — atmosfera, emocje i kluczowe momenty wieczoru.",
        "content": """<!-- wp:group {"layout":{"type":"constrained"}} -->
<div class="wp-block-group">
<!-- wp:heading {"level":6} -->
<h6 class="wp-block-heading">Filmy eventowe</h6>
<!-- /wp:heading -->
<!-- wp:heading {"level":1} -->
<h1 class="wp-block-heading">Film eventowy – Gala Biznesu 2024</h1>
<!-- /wp:heading -->
<!-- wp:paragraph {"style":{"color":{"text":"var(--wp--preset--color--muted)"}}} -->
<p style="color:var(--wp--preset--color--muted)">Prestiżowa gala dla 500 gości — uchwyciliśmy każdy ważny moment tego wyjątkowego wieczoru.</p>
<!-- /wp:paragraph -->
</div>
<!-- /wp:group -->""",
    },
    {
        "title": "Brand story – Startup technologiczny",
        "slug": "brand-story-startup-technologiczny",
        "excerpt": "Historia marki opowiedziana obrazem — skąd pochodzi, dokąd zmierza i co ją wyróżnia na rynku.",
        "content": """<!-- wp:group {"layout":{"type":"constrained"}} -->
<div class="wp-block-group">
<!-- wp:heading {"level":6} -->
<h6 class="wp-block-heading">Brand storytelling</h6>
<!-- /wp:heading -->
<!-- wp:heading {"level":1} -->
<h1 class="wp-block-heading">Brand story – Startup technologiczny</h1>
<!-- /wp:heading -->
<!-- wp:paragraph {"style":{"color":{"text":"var(--wp--preset--color--muted)"}}} -->
<p style="color:var(--wp--preset--color--muted)">Tworzenie historii marki, która angażuje i buduje zaufanie wśród inwestorów i klientów.</p>
<!-- /wp:paragraph -->
</div>
<!-- /wp:group -->""",
    },
    {
        "title": "Spot produktowy – Premium Cosmetics",
        "slug": "spot-produktowy-premium-cosmetics",
        "excerpt": "Elegancki spot produktowy w stylu luxury — zmysłowe kadry, precyzyjne oświetlenie, pełna kontrola nad marką.",
        "content": """<!-- wp:group {"layout":{"type":"constrained"}} -->
<div class="wp-block-group">
<!-- wp:heading {"level":6} -->
<h6 class="wp-block-heading">Filmy produktowe</h6>
<!-- /wp:heading -->
<!-- wp:heading {"level":1} -->
<h1 class="wp-block-heading">Spot produktowy – Premium Cosmetics</h1>
<!-- /wp:heading -->
<!-- wp:paragraph {"style":{"color":{"text":"var(--wp--preset--color--muted)"}}} -->
<p style="color:var(--wp--preset--color--muted)">Luxury production — slow motion, macro, profesjonalne oświetlenie studyjne.</p>
<!-- /wp:paragraph -->
</div>
<!-- /wp:group -->""",
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
        print(f"  ✗ Failed post: {post_data['title']} — {r.status_code}: {r.text[:120]}")

# ── 4. PAGE CONTENT ────────────────────────────────────────────────────────────
print("\n=== CREATING PAGES ===")

# About page content
about_content = """<!-- wp:group {"align":"full","style":{"color":{"background":"var(--wp--preset--color--surface)"},"spacing":{"padding":{"top":"var(--wp--preset--spacing--70)","bottom":"var(--wp--preset--spacing--60)","left":"var(--wp--preset--spacing--50)","right":"var(--wp--preset--spacing--50)"}}},"layout":{"type":"constrained"}} -->
<div class="wp-block-group alignfull" style="background-color:var(--wp--preset--color--surface);padding-top:var(--wp--preset--spacing--70);padding-bottom:var(--wp--preset--spacing--60);padding-left:var(--wp--preset--spacing--50);padding-right:var(--wp--preset--spacing--50)">
<!-- wp:group {"style":{"spacing":{"blockGap":"var(--wp--preset--spacing--20)"}},"layout":{"type":"constrained","contentSize":"780px"}} -->
<div class="wp-block-group">
<!-- wp:heading {"level":6} -->
<h6 class="wp-block-heading">O nas</h6>
<!-- /wp:heading -->
<!-- wp:heading {"level":1} -->
<h1 class="wp-block-heading">Tworzymy filmy z pasją do obrazu.</h1>
<!-- /wp:heading -->
<!-- wp:paragraph {"style":{"color":{"text":"var(--wp--preset--color--muted)"},"typography":{"fontSize":"var(--wp--preset--font-size--lg)"}}} -->
<p style="color:var(--wp--preset--color--muted);font-size:var(--wp--preset--font-size--lg)">Papilotka to dom produkcyjny z Łodzi — miejsce, w którym pomysły zamieniają się w filmy, które sprzedają, angażują i zostają w pamięci.</p>
<!-- /wp:paragraph -->
</div>
<!-- /wp:group -->
</div>
<!-- /wp:group -->

<!-- wp:group {"align":"full","style":{"color":{"background":"var(--wp--preset--color--base)"},"spacing":{"padding":{"top":"var(--wp--preset--spacing--70)","bottom":"var(--wp--preset--spacing--70)","left":"var(--wp--preset--spacing--50)","right":"var(--wp--preset--spacing--50)"}}},"layout":{"type":"constrained"}} -->
<div class="wp-block-group alignfull" style="padding-top:var(--wp--preset--spacing--70);padding-bottom:var(--wp--preset--spacing--70);padding-left:var(--wp--preset--spacing--50);padding-right:var(--wp--preset--spacing--50)">
<!-- wp:columns {"align":"wide","isStackedOnMobile":true,"style":{"spacing":{"blockGap":{"left":"var(--wp--preset--spacing--60)"}}}} -->
<div class="wp-block-columns alignwide">
<!-- wp:column -->
<div class="wp-block-column">
<!-- wp:heading {"level":2} -->
<h2 class="wp-block-heading">Kim jesteśmy</h2>
<!-- /wp:heading -->
<!-- wp:paragraph {"style":{"color":{"text":"var(--wp--preset--color--muted)"}}} -->
<p style="color:var(--wp--preset--color--muted)">Jesteśmy ekipą reżyserów, operatorów, montażystów i producentów z wieloletnim doświadczeniem w reklamie, filmie korporacyjnym i content marketingu. Rozumiemy biznes — i potrafimy go opowiedzieć obrazem.</p>
<!-- /wp:paragraph -->
<!-- wp:paragraph {"style":{"color":{"text":"var(--wp--preset--color--muted)"}}} -->
<p style="color:var(--wp--preset--color--muted)">Od 2016 roku pracujemy z markami z całej Polski — od startupów po duże korporacje. Każdy projekt traktujemy indywidualnie, bo każda marka ma swoją unikalną historię.</p>
<!-- /wp:paragraph -->
</div>
<!-- /wp:column -->
<!-- wp:column -->
<div class="wp-block-column">
<!-- wp:group {"style":{"spacing":{"blockGap":"var(--wp--preset--spacing--30)"}}} -->
<div class="wp-block-group">
<!-- wp:group {"style":{"spacing":{"padding":{"left":"var(--wp--preset--spacing--40)"},"blockGap":"var(--wp--preset--spacing--10)"}},"border":{"left":{"color":"var(--wp--preset--color--accent)","width":"3px"}}} -->
<div class="wp-block-group" style="padding-left:var(--wp--preset--spacing--40);border-left-color:var(--wp--preset--color--accent);border-left-width:3px;border-left-style:solid">
<!-- wp:heading {"level":4} -->
<h4 class="wp-block-heading">Kreatywność na każdym etapie</h4>
<!-- /wp:heading -->
<!-- wp:paragraph {"style":{"color":{"text":"var(--wp--preset--color--muted)"},"typography":{"fontSize":"var(--wp--preset--font-size--sm)"}}} -->
<p style="color:var(--wp--preset--color--muted);font-size:var(--wp--preset--font-size--sm)">Od scenariusza po ostateczny montaż — angażujemy się twórczo w każdy etap produkcji.</p>
<!-- /wp:paragraph -->
</div>
<!-- /wp:group -->
<!-- wp:group {"style":{"spacing":{"padding":{"left":"var(--wp--preset--spacing--40)"},"blockGap":"var(--wp--preset--spacing--10)"}},"border":{"left":{"color":"var(--wp--preset--color--surface-2)","width":"3px"}}} -->
<div class="wp-block-group" style="padding-left:var(--wp--preset--spacing--40);border-left-color:var(--wp--preset--color--surface-2);border-left-width:3px;border-left-style:solid">
<!-- wp:heading {"level":4} -->
<h4 class="wp-block-heading">Terminowość i przejrzystość</h4>
<!-- /wp:heading -->
<!-- wp:paragraph {"style":{"color":{"text":"var(--wp--preset--color--muted)"},"typography":{"fontSize":"var(--wp--preset--font-size--sm)"}}} -->
<p style="color:var(--wp--preset--color--muted);font-size:var(--wp--preset--font-size--sm)">Dotrzymujemy terminów i jesteśmy w stałym kontakcie przez cały czas trwania projektu.</p>
<!-- /wp:paragraph -->
</div>
<!-- /wp:group -->
<!-- wp:group {"style":{"spacing":{"padding":{"left":"var(--wp--preset--spacing--40)"},"blockGap":"var(--wp--preset--spacing--10)"}},"border":{"left":{"color":"var(--wp--preset--color--surface-2)","width":"3px"}}} -->
<div class="wp-block-group" style="padding-left:var(--wp--preset--spacing--40);border-left-color:var(--wp--preset--color--surface-2);border-left-width:3px;border-left-style:solid">
<!-- wp:heading {"level":4} -->
<h4 class="wp-block-heading">Rezultaty, które mówią same za siebie</h4>
<!-- /wp:heading -->
<!-- wp:paragraph {"style":{"color":{"text":"var(--wp--preset--color--muted)"},"typography":{"fontSize":"var(--wp--preset--font-size--sm)"}}} -->
<p style="color:var(--wp--preset--color--muted);font-size:var(--wp--preset--font-size--sm)">Tworzymy filmy, które osiągają cele — zasięgi, konwersje, zaangażowanie.</p>
<!-- /wp:paragraph -->
</div>
<!-- /wp:group -->
</div>
<!-- /wp:group -->
</div>
<!-- /wp:column -->
</div>
<!-- /wp:columns -->
</div>
<!-- /wp:group -->

<!-- wp:group {"align":"full","style":{"color":{"background":"var(--wp--preset--color--navy)"},"spacing":{"padding":{"top":"var(--wp--preset--spacing--70)","bottom":"var(--wp--preset--spacing--70)","left":"var(--wp--preset--spacing--50)","right":"var(--wp--preset--spacing--50)"}}},"layout":{"type":"constrained","contentSize":"680px"}} -->
<div class="wp-block-group alignfull" style="background-color:var(--wp--preset--color--navy);padding-top:var(--wp--preset--spacing--70);padding-bottom:var(--wp--preset--spacing--70);padding-left:var(--wp--preset--spacing--50);padding-right:var(--wp--preset--spacing--50)">
<!-- wp:heading {"level":6,"style":{"color":{"text":"rgba(255,255,255,0.45)"}}} -->
<h6 class="wp-block-heading" style="color:rgba(255,255,255,0.45)">Zacznijmy współpracę</h6>
<!-- /wp:heading -->
<!-- wp:heading {"level":2,"style":{"color":{"text":"#ffffff"}}} -->
<h2 class="wp-block-heading" style="color:#ffffff">Chętnie poznamy Twój projekt.</h2>
<!-- /wp:heading -->
<!-- wp:buttons -->
<div class="wp-block-buttons">
<!-- wp:button -->
<div class="wp-block-button"><a class="wp-block-button__link wp-element-button" href="/papilotka-com/kontakt">Napisz do nas</a></div>
<!-- /wp:button -->
</div>
<!-- /wp:buttons -->
</div>
<!-- /wp:group -->"""

# Services page content
services_content = """<!-- wp:group {"align":"full","style":{"color":{"background":"var(--wp--preset--color--surface)"},"spacing":{"padding":{"top":"var(--wp--preset--spacing--70)","bottom":"var(--wp--preset--spacing--60)","left":"var(--wp--preset--spacing--50)","right":"var(--wp--preset--spacing--50)"}}},"layout":{"type":"constrained"}} -->
<div class="wp-block-group alignfull" style="background-color:var(--wp--preset--color--surface);padding-top:var(--wp--preset--spacing--70);padding-bottom:var(--wp--preset--spacing--60);padding-left:var(--wp--preset--spacing--50);padding-right:var(--wp--preset--spacing--50)">
<!-- wp:group {"style":{"spacing":{"blockGap":"var(--wp--preset--spacing--20)"}},"layout":{"type":"constrained","contentSize":"680px"}} -->
<div class="wp-block-group">
<!-- wp:heading {"level":6} -->
<h6 class="wp-block-heading">Nasze usługi</h6>
<!-- /wp:heading -->
<!-- wp:heading {"level":1} -->
<h1 class="wp-block-heading">Kompleksowa produkcja filmowa.</h1>
<!-- /wp:heading -->
<!-- wp:paragraph {"style":{"color":{"text":"var(--wp--preset--color--muted)"},"typography":{"fontSize":"var(--wp--preset--font-size--lg)"}}} -->
<p style="color:var(--wp--preset--color--muted);font-size:var(--wp--preset--font-size--lg)">Oferujemy pełen zakres usług produkcji filmowej — od koncepcji po gotowy materiał.</p>
<!-- /wp:paragraph -->
</div>
<!-- /wp:group -->
</div>
<!-- /wp:group -->

<!-- wp:group {"align":"full","style":{"color":{"background":"var(--wp--preset--color--base)"},"spacing":{"padding":{"top":"var(--wp--preset--spacing--70)","bottom":"var(--wp--preset--spacing--70)","left":"var(--wp--preset--spacing--50)","right":"var(--wp--preset--spacing--50)"}}},"layout":{"type":"constrained"}} -->
<div class="wp-block-group alignfull" style="padding-top:var(--wp--preset--spacing--70);padding-bottom:var(--wp--preset--spacing--70);padding-left:var(--wp--preset--spacing--50);padding-right:var(--wp--preset--spacing--50)">

<!-- wp:group {"align":"wide","style":{"spacing":{"blockGap":"var(--wp--preset--spacing--30)","padding":{"top":"var(--wp--preset--spacing--50)","bottom":"var(--wp--preset--spacing--50)","left":"var(--wp--preset--spacing--40)","right":"var(--wp--preset--spacing--40)"}},"color":{"background":"var(--wp--preset--color--surface)"},"border":{"top":{"color":"var(--wp--preset--color--accent)","width":"3px"}}},"layout":{"type":"constrained"}} -->
<div class="wp-block-group alignwide" style="background-color:var(--wp--preset--color--surface);padding:var(--wp--preset--spacing--50) var(--wp--preset--spacing--40);border-top-color:var(--wp--preset--color--accent);border-top-width:3px;border-top-style:solid">
<!-- wp:columns {"isStackedOnMobile":true} -->
<div class="wp-block-columns">
<!-- wp:column {"width":"280px"} -->
<div class="wp-block-column" style="flex-basis:280px">
<!-- wp:heading {"level":6} -->
<h6 class="wp-block-heading">01</h6>
<!-- /wp:heading -->
<!-- wp:heading {"level":2} -->
<h2 class="wp-block-heading">Filmy reklamowe</h2>
<!-- /wp:heading -->
</div>
<!-- /wp:column -->
<!-- wp:column -->
<div class="wp-block-column">
<!-- wp:paragraph {"style":{"color":{"text":"var(--wp--preset--color--muted)"}}} -->
<p style="color:var(--wp--preset--color--muted)">Spoty TV i online, filmy produktowe, kampanie wizerunkowe i performance marketing. Tworzymy materiały wideo, które budują świadomość marki i bezpośrednio napędzają sprzedaż.</p>
<!-- /wp:paragraph -->
<!-- wp:list {"style":{"color":{"text":"var(--wp--preset--color--muted)"},"typography":{"fontSize":"var(--wp--preset--font-size--sm)"}}} -->
<ul class="wp-block-list" style="color:var(--wp--preset--color--muted);font-size:var(--wp--preset--font-size--sm)"><li>Spoty TV (15s, 30s, 60s)</li><li>Filmy na YouTube i social media</li><li>Filmy produktowe i e-commerce</li><li>Kampanie wizerunkowe</li></ul>
<!-- /wp:list -->
</div>
<!-- /wp:column -->
</div>
<!-- /wp:columns -->
</div>
<!-- /wp:group -->

<!-- wp:group {"align":"wide","style":{"spacing":{"blockGap":"var(--wp--preset--spacing--30)","padding":{"top":"var(--wp--preset--spacing--50)","bottom":"var(--wp--preset--spacing--50)","left":"var(--wp--preset--spacing--40)","right":"var(--wp--preset--spacing--40)"}},"color":{"background":"var(--wp--preset--color--surface)"},"border":{"top":{"color":"var(--wp--preset--color--surface-2)","width":"1px"}}},"layout":{"type":"constrained"}} -->
<div class="wp-block-group alignwide" style="background-color:var(--wp--preset--color--surface);padding:var(--wp--preset--spacing--50) var(--wp--preset--spacing--40);border-top-color:var(--wp--preset--color--surface-2);border-top-width:1px;border-top-style:solid">
<!-- wp:columns {"isStackedOnMobile":true} -->
<div class="wp-block-columns">
<!-- wp:column {"width":"280px"} -->
<div class="wp-block-column" style="flex-basis:280px">
<!-- wp:heading {"level":6} -->
<h6 class="wp-block-heading">02</h6>
<!-- /wp:heading -->
<!-- wp:heading {"level":2} -->
<h2 class="wp-block-heading">Brand storytelling</h2>
<!-- /wp:heading -->
</div>
<!-- /wp:column -->
<!-- wp:column -->
<div class="wp-block-column">
<!-- wp:paragraph {"style":{"color":{"text":"var(--wp--preset--color--muted)"}}} -->
<p style="color:var(--wp--preset--color--muted)">Filmy o firmie, dokumenty korporacyjne, employer branding i investor relations. Opowiadamy historię Twojej marki w sposób, który buduje zaufanie i angażuje odbiorców.</p>
<!-- /wp:paragraph -->
<!-- wp:list {"style":{"color":{"text":"var(--wp--preset--color--muted)"},"typography":{"fontSize":"var(--wp--preset--font-size--sm)"}}} -->
<ul class="wp-block-list" style="color:var(--wp--preset--color--muted);font-size:var(--wp--preset--font-size--sm)"><li>Filmy „o firmie" i korporacyjne</li><li>Employer branding i rekrutacja</li><li>Dokumenty wizerunkowe</li><li>Filmy dla inwestorów</li></ul>
<!-- /wp:list -->
</div>
<!-- /wp:column -->
</div>
<!-- /wp:columns -->
</div>
<!-- /wp:group -->

<!-- wp:group {"align":"wide","style":{"spacing":{"blockGap":"var(--wp--preset--spacing--30)","padding":{"top":"var(--wp--preset--spacing--50)","bottom":"var(--wp--preset--spacing--50)","left":"var(--wp--preset--spacing--40)","right":"var(--wp--preset--spacing--40)"}},"color":{"background":"var(--wp--preset--color--surface)"},"border":{"top":{"color":"var(--wp--preset--color--surface-2)","width":"1px"}}},"layout":{"type":"constrained"}} -->
<div class="wp-block-group alignwide" style="background-color:var(--wp--preset--color--surface);padding:var(--wp--preset--spacing--50) var(--wp--preset--spacing--40);border-top-color:var(--wp--preset--color--surface-2);border-top-width:1px;border-top-style:solid">
<!-- wp:columns {"isStackedOnMobile":true} -->
<div class="wp-block-columns">
<!-- wp:column {"width":"280px"} -->
<div class="wp-block-column" style="flex-basis:280px">
<!-- wp:heading {"level":6} -->
<h6 class="wp-block-heading">03</h6>
<!-- /wp:heading -->
<!-- wp:heading {"level":2} -->
<h2 class="wp-block-heading">Filmy eventowe</h2>
<!-- /wp:heading -->
</div>
<!-- /wp:column -->
<!-- wp:column -->
<div class="wp-block-column">
<!-- wp:paragraph {"style":{"color":{"text":"var(--wp--preset--color--muted)"}}} -->
<p style="color:var(--wp--preset--color--muted)">Konferencje, gale, targi, premiery produktów i imprezy firmowe. Tworzymy dynamiczne relacje, które oddają atmosferę i emocje Twojego wydarzenia.</p>
<!-- /wp:paragraph -->
<!-- wp:list {"style":{"color":{"text":"var(--wp--preset--color--muted)"},"typography":{"fontSize":"var(--wp--preset--font-size--sm)"}}} -->
<ul class="wp-block-list" style="color:var(--wp--preset--color--muted);font-size:var(--wp--preset--font-size--sm)"><li>Konferencje i targi branżowe</li><li>Gale i uroczystości firmowe</li><li>Premiery produktów</li><li>Transmisje live i aftermovie</li></ul>
<!-- /wp:list -->
</div>
<!-- /wp:column -->
</div>
<!-- /wp:columns -->
</div>
<!-- /wp:group -->

</div>
<!-- /wp:group -->

<!-- wp:group {"align":"full","style":{"color":{"background":"var(--wp--preset--color--navy)"},"spacing":{"padding":{"top":"var(--wp--preset--spacing--70)","bottom":"var(--wp--preset--spacing--70)","left":"var(--wp--preset--spacing--50)","right":"var(--wp--preset--spacing--50)"}}},"layout":{"type":"constrained","contentSize":"680px"}} -->
<div class="wp-block-group alignfull" style="background-color:var(--wp--preset--color--navy);padding-top:var(--wp--preset--spacing--70);padding-bottom:var(--wp--preset--spacing--70);padding-left:var(--wp--preset--spacing--50);padding-right:var(--wp--preset--spacing--50)">
<!-- wp:heading {"level":6,"style":{"color":{"text":"rgba(255,255,255,0.45)"}}} -->
<h6 class="wp-block-heading" style="color:rgba(255,255,255,0.45)">Zapytaj o wycenę</h6>
<!-- /wp:heading -->
<!-- wp:heading {"level":2,"style":{"color":{"text":"#ffffff"}}} -->
<h2 class="wp-block-heading" style="color:#ffffff">Opowiedz nam o swoim projekcie.</h2>
<!-- /wp:heading -->
<!-- wp:paragraph {"style":{"color":{"text":"rgba(255,255,255,0.6)"}}} -->
<p style="color:rgba(255,255,255,0.6)">Każdy projekt jest inny — skontaktuj się z nami, żebyśmy mogli przygotować indywidualną ofertę.</p>
<!-- /wp:paragraph -->
<!-- wp:buttons -->
<div class="wp-block-buttons">
<!-- wp:button -->
<div class="wp-block-button"><a class="wp-block-button__link wp-element-button" href="/papilotka-com/kontakt">Wyślij zapytanie →</a></div>
<!-- /wp:button -->
</div>
<!-- /wp:buttons -->
</div>
<!-- /wp:group -->"""

# Contact page content
contact_content = """<!-- wp:group {"align":"full","style":{"color":{"background":"var(--wp--preset--color--surface)"},"spacing":{"padding":{"top":"var(--wp--preset--spacing--70)","bottom":"var(--wp--preset--spacing--70)","left":"var(--wp--preset--spacing--50)","right":"var(--wp--preset--spacing--50)"}}},"layout":{"type":"constrained"}} -->
<div class="wp-block-group alignfull" style="background-color:var(--wp--preset--color--surface);padding-top:var(--wp--preset--spacing--70);padding-bottom:var(--wp--preset--spacing--70);padding-left:var(--wp--preset--spacing--50);padding-right:var(--wp--preset--spacing--50)">

<!-- wp:columns {"align":"wide","isStackedOnMobile":true,"style":{"spacing":{"blockGap":{"left":"var(--wp--preset--spacing--70)"}}}} -->
<div class="wp-block-columns alignwide">

<!-- wp:column -->
<div class="wp-block-column">
<!-- wp:heading {"level":6} -->
<h6 class="wp-block-heading">Skontaktuj się</h6>
<!-- /wp:heading -->
<!-- wp:heading {"level":1} -->
<h1 class="wp-block-heading">Napisz do nas.</h1>
<!-- /wp:heading -->
<!-- wp:paragraph {"style":{"color":{"text":"var(--wp--preset--color--muted)"}}} -->
<p style="color:var(--wp--preset--color--muted)">Chętnie porozmawiamy o Twoim projekcie. Odpiszemy w ciągu 24 godzin i zaproponujemy bezpłatną konsultację wstępną.</p>
<!-- /wp:paragraph -->

<!-- wp:separator {"className":"is-style-wide","style":{"border":{"color":"var(--wp--preset--color--surface-2)","width":"1px"}}} -->
<hr class="wp-block-separator is-style-wide" style="border-color:var(--wp--preset--color--surface-2)"/>
<!-- /wp:separator -->

<!-- wp:group {"style":{"spacing":{"blockGap":"var(--wp--preset--spacing--30)"}},"layout":{"type":"flex","orientation":"vertical"}} -->
<div class="wp-block-group">

<!-- wp:group {"style":{"spacing":{"blockGap":"var(--wp--preset--spacing--10)"}},"layout":{"type":"flex","orientation":"vertical"}} -->
<div class="wp-block-group">
<!-- wp:heading {"level":6} -->
<h6 class="wp-block-heading">Email</h6>
<!-- /wp:heading -->
<!-- wp:paragraph -->
<p><a href="mailto:kontakt@papilotka.com">kontakt@papilotka.com</a></p>
<!-- /wp:paragraph -->
</div>
<!-- /wp:group -->

<!-- wp:group {"style":{"spacing":{"blockGap":"var(--wp--preset--spacing--10)"}},"layout":{"type":"flex","orientation":"vertical"}} -->
<div class="wp-block-group">
<!-- wp:heading {"level":6} -->
<h6 class="wp-block-heading">Lokalizacja</h6>
<!-- /wp:heading -->
<!-- wp:paragraph {"style":{"color":{"text":"var(--wp--preset--color--muted)"}}} -->
<p style="color:var(--wp--preset--color--muted)">Łódź, Polska<br>Realizujemy projekty na terenie całego kraju</p>
<!-- /wp:paragraph -->
</div>
<!-- /wp:group -->

<!-- wp:group {"style":{"spacing":{"blockGap":"var(--wp--preset--spacing--10)"}},"layout":{"type":"flex","orientation":"vertical"}} -->
<div class="wp-block-group">
<!-- wp:heading {"level":6} -->
<h6 class="wp-block-heading">Czas realizacji zapytań</h6>
<!-- /wp:heading -->
<!-- wp:paragraph {"style":{"color":{"text":"var(--wp--preset--color--muted)"}}} -->
<p style="color:var(--wp--preset--color--muted)">Odpowiadamy w ciągu 24 godzin roboczych.</p>
<!-- /wp:paragraph -->
</div>
<!-- /wp:group -->

</div>
<!-- /wp:group -->

</div>
<!-- /wp:column -->

<!-- wp:column -->
<div class="wp-block-column">
<!-- wp:group {"style":{"color":{"background":"var(--wp--preset--color--surface-2)"},"spacing":{"padding":{"top":"var(--wp--preset--spacing--50)","bottom":"var(--wp--preset--spacing--50)","left":"var(--wp--preset--spacing--50)","right":"var(--wp--preset--spacing--50)"}},"border":{"radius":"4px"}},"layout":{"type":"flex","orientation":"vertical"}} -->
<div class="wp-block-group" style="background-color:var(--wp--preset--color--surface-2);padding:var(--wp--preset--spacing--50);border-radius:4px">
<!-- wp:heading {"level":4} -->
<h4 class="wp-block-heading">Wyślij wiadomość</h4>
<!-- /wp:heading -->
<!-- wp:paragraph {"style":{"color":{"text":"var(--wp--preset--color--muted)"},"typography":{"fontSize":"var(--wp--preset--font-size--sm)"}}} -->
<p style="color:var(--wp--preset--color--muted);font-size:var(--wp--preset--font-size--sm)">Opisz krótko swój projekt — rodzaj filmu, cel, termin i budżet. Im więcej szczegółów, tym szybciej przygotujemy ofertę.</p>
<!-- /wp:paragraph -->
<!-- wp:html -->
<form style="display:flex;flex-direction:column;gap:1rem" method="post" action="#">
  <input type="text" placeholder="Imię i nazwisko *" required style="background:#2a2a2a;border:1px solid rgba(255,255,255,0.1);color:#fff;padding:0.875rem 1rem;font-family:inherit;font-size:0.875rem;border-radius:4px;outline:none"/>
  <input type="email" placeholder="Adres e-mail *" required style="background:#2a2a2a;border:1px solid rgba(255,255,255,0.1);color:#fff;padding:0.875rem 1rem;font-family:inherit;font-size:0.875rem;border-radius:4px;outline:none"/>
  <input type="text" placeholder="Firma (opcjonalnie)" style="background:#2a2a2a;border:1px solid rgba(255,255,255,0.1);color:#fff;padding:0.875rem 1rem;font-family:inherit;font-size:0.875rem;border-radius:4px;outline:none"/>
  <select style="background:#2a2a2a;border:1px solid rgba(255,255,255,0.1);color:rgba(255,255,255,0.6);padding:0.875rem 1rem;font-family:inherit;font-size:0.875rem;border-radius:4px;outline:none">
    <option value="">Rodzaj projektu *</option>
    <option>Film reklamowy</option>
    <option>Brand storytelling</option>
    <option>Film eventowy</option>
    <option>Film produktowy</option>
    <option>Inne</option>
  </select>
  <textarea placeholder="Opisz swój projekt *" rows="5" required style="background:#2a2a2a;border:1px solid rgba(255,255,255,0.1);color:#fff;padding:0.875rem 1rem;font-family:inherit;font-size:0.875rem;border-radius:4px;outline:none;resize:vertical"></textarea>
  <button type="submit" style="background:#FF3C00;color:#fff;border:none;padding:0.875rem 2rem;font-family:inherit;font-size:0.8125rem;font-weight:600;letter-spacing:0.04em;text-transform:uppercase;border-radius:24px;cursor:pointer">Wyślij wiadomość →</button>
</form>
<!-- /wp:html -->
</div>
<!-- /wp:group -->
</div>
<!-- /wp:column -->

</div>
<!-- /wp:columns -->

</div>
<!-- /wp:group -->"""

pages_to_create = [
    {
        "title": "Strona główna",
        "slug": "home",
        "content": "<!-- front-page template handles this page -->",
        "template": "",
        "menu_order": 0,
    },
    {
        "title": "Portfolio",
        "slug": "portfolio",
        "content": "<!-- portfolio template handles this page -->",
        "template": "portfolio",
        "menu_order": 1,
    },
    {
        "title": "O nas",
        "slug": "o-nas",
        "content": about_content,
        "template": "no-title",
        "menu_order": 2,
    },
    {
        "title": "Usługi",
        "slug": "uslugi",
        "content": services_content,
        "template": "no-title",
        "menu_order": 3,
    },
    {
        "title": "Kontakt",
        "slug": "kontakt",
        "content": contact_content,
        "template": "no-title",
        "menu_order": 4,
    },
]

page_ids = {}
for pg in pages_to_create:
    payload = {
        "title":      pg["title"],
        "slug":       pg["slug"],
        "status":     "publish",
        "content":    pg["content"],
        "template":   pg["template"],
        "menu_order": pg["menu_order"],
    }
    r = api("post", "/pages", json=payload)
    if r.status_code == 201:
        pid = r.json()["id"]
        page_ids[pg["slug"]] = pid
        print(f"  ✓ Page: '{pg['title']}' id={pid} slug={pg['slug']}")
    else:
        print(f"  ✗ Failed page: {pg['title']} — {r.status_code}: {r.text[:200]}")

# ── 5. CREATE NAVIGATION ───────────────────────────────────────────────────────
print("\n=== CREATING NAVIGATION ===")

home_id  = page_ids.get("home", "")
port_id  = page_ids.get("portfolio", "")
onas_id  = page_ids.get("o-nas", "")
uslugi_id= page_ids.get("uslugi", "")
kontakt_id=page_ids.get("kontakt", "")

base_url = base

nav_content = f"""<!-- wp:navigation-link {{"label":"Portfolio","type":"page","id":{port_id},"url":"{base_url}/portfolio/","kind":"post-type"}} /-->
<!-- wp:navigation-link {{"label":"Usługi","type":"page","id":{uslugi_id},"url":"{base_url}/uslugi/","kind":"post-type"}} /-->
<!-- wp:navigation-link {{"label":"O nas","type":"page","id":{onas_id},"url":"{base_url}/o-nas/","kind":"post-type"}} /-->
<!-- wp:navigation-link {{"label":"Kontakt","type":"page","id":{kontakt_id},"url":"{base_url}/kontakt/","kind":"post-type"}} /-->"""

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
    print(f"  ✗ Navigation failed: {r.status_code}: {r.text[:200]}")
    nav_id = None

# ── 6. CONFIGURE WORDPRESS SETTINGS ──────────────────────────────────────────
print("\n=== CONFIGURING WORDPRESS SETTINGS ===")

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
        print(f"  ✓ Front page set to Home (id={home_page_id})")
    else:
        print(f"  ✗ Settings failed: {r.status_code}: {r.text[:200]}")

# ── SUMMARY ────────────────────────────────────────────────────────────────────
print("\n=== SUMMARY ===")
print(f"Navigation ID: {nav_id}")
print(f"Page IDs: {page_ids}")
print(f"Portfolio category ID: {portfolio_cat_id}")
print("Done!")
