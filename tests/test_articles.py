from html.parser import HTMLParser
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
ARTICLE_SLUGS = (
    "3-tips-to-break-into-banking",
    "3-tips-to-succeed-in-business",
    "3-tips-to-succeed-in-dentistry",
    "3-tips-to-succeed-in-sports",
    "what-a-3-star-michelin-restaurant-taught-me-about-excellence",
    "from-public-service-to-private-practice-lessons-from-legal-veteran-stephen-kai-yi-wong",
    "seminar-with-mr-wong-kai-yi-breaking-barriers-in-law",
    "seminar-with-olympic-athlete-zachary-yuen",
    "internship-highlight-guardforce-hong-kong",
)


class ArticleAssets(HTMLParser):
    def __init__(self):
        super().__init__()
        self.stylesheets = []
        self.scripts = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "link" and attrs.get("rel") == "stylesheet":
            self.stylesheets.append(attrs.get("href"))
        if tag == "script":
            self.scripts.append(attrs.get("src"))


class ArticleTests(unittest.TestCase):
    def test_articles_use_shared_editorial_assets_without_squarespace_markup(self):
        for slug in ARTICLE_SLUGS:
            with self.subTest(article=slug):
                markup = (ROOT / "pages" / f"{slug}.html").read_text(encoding="utf-8")
                assets = ArticleAssets()
                assets.feed(markup)
                self.assertIn("../assets/css/editorial-pages.css", assets.stylesheets)
                self.assertEqual(["../assets/js/homepage.js"], assets.scripts)
                self.assertNotRegex(markup.lower(), r"squarespace|\bsqs(?:[-_]|rte)|\bsqsp[-_]|\byui_")
