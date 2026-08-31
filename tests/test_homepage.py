from html.parser import HTMLParser
from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]


class HomepageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.h1_count = 0
        self.ids = set()
        self.hrefs = []
        self.stylesheets = []
        self.scripts = []
        self.advisor_cards = 0
        self.body_classes = set()
        self.button_types = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        classes = set((attrs.get("class") or "").split())
        if tag == "body":
            self.body_classes = classes
        if tag == "h1":
            self.h1_count += 1
        if attrs.get("id"):
            self.ids.add(attrs["id"])
        if tag == "a" and attrs.get("href") is not None:
            self.hrefs.append(attrs["href"])
        if tag == "link" and attrs.get("rel") == "stylesheet":
            self.stylesheets.append(attrs.get("href"))
        if tag == "script" and attrs.get("src"):
            self.scripts.append(attrs["src"])
        if tag == "button":
            self.button_types.append(attrs.get("type"))
        if tag == "article" and "advisor-card" in classes:
            self.advisor_cards += 1


class ProductionHomepageTests(unittest.TestCase):
    def test_root_homepage_is_the_approved_production_experience(self):
        text = (ROOT / "index.html").read_text(encoding="utf-8")
        parser = HomepageParser()
        parser.feed(text)

        self.assertIn("homepage", parser.body_classes)
        self.assertEqual(1, parser.h1_count)
        self.assertIn("assets/css/homepage.css", parser.stylesheets)
        self.assertIn("assets/js/homepage.js", parser.scripts)
        self.assertNotIn("Prototype", text)
        self.assertNotIn('href="#"', text)
        self.assertNotIn('class="save"', text)
        self.assertTrue(parser.button_types)
        self.assertTrue(all(button_type == "button" for button_type in parser.button_types))
        self.assertIn("#main-content", parser.hrefs)
        self.assertIn("main-content", parser.ids)

        for section_id in (
            "company",
            "initiatives",
            "impact",
            "schools",
            "advisors",
            "opportunities",
        ):
            self.assertIn(section_id, parser.ids)

        for href in (
            "#initiatives",
            "pages/upcoming.html",
            "pages/student-ambassador.html",
            "pages/events-and-camps.html",
            "pages/internship-opportunities.html",
            "pages/alumni-network.html",
            "pages/about-us.html",
            "pages/contact.html",
        ):
            self.assertIn(href, parser.hrefs)

        self.assertEqual(5, parser.advisor_cards)

    def test_homepage_marquee_skips_clone_loop_for_reduced_motion(self):
        script = (ROOT / "assets" / "js" / "homepage.js").read_text(encoding="utf-8")
        self.assertIn("prefers-reduced-motion: reduce", script)
        self.assertIn("if (reduceMotion)", script)

    def test_homepage_accessibility_colours_have_explicit_high_contrast_overrides(self):
        stylesheet = (ROOT / "assets" / "css" / "homepage.css").read_text(encoding="utf-8")
        self.assertIn(".hero-message .eyebrow", stylesheet)
        self.assertIn("color: var(--ink)", stylesheet)
        self.assertIn("box-shadow: 0 0 0 6px var(--ink)", stylesheet)

    def test_impact_navigation_and_past_events_cta_target_the_right_places(self):
        text = (ROOT / "index.html").read_text(encoding="utf-8")
        self.assertRegex(text, r'<a href="#impact">\s*Our impact\s*</a>')

        impact = text[text.index('<section class="action" id="impact">') :]
        first_story = re.search(
            r'<article class="story">(.*?)</article>', impact, flags=re.S
        )
        if first_story is None:
            self.fail("The impact section should include at least one story card")
        first_story_html = first_story.group(1)
        self.assertIn('href="pages/events-and-camps.html"', first_story_html)
        self.assertIn('class="story-link"', first_story_html)
        self.assertIn("View past events", first_story_html)

        stylesheet = (ROOT / "assets" / "css" / "homepage.css").read_text(
            encoding="utf-8"
        )
        self.assertIn(".story-link", stylesheet)


if __name__ == "__main__":
    unittest.main()
