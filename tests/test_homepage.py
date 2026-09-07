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

    def test_partner_and_school_logos_use_transparent_image_assets(self):
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        network = html[html.index('<section class="partner-network"'):html.index('<section class="advisors"')]
        sources = set(re.findall(r'<img src="([^"]+)"', network))

        self.assertEqual(13, len(sources))
        for source in sources:
            self.assertIn("/transparent/", source)
            self.assertTrue((ROOT / source).is_file(), source)

    def test_partner_and_school_logos_have_no_outer_logo_cards(self):
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        network = html[html.index('<section class="partner-network"'):html.index('<section class="advisors"')]
        self.assertIn('partner-logos/transparent/', network)
        self.assertIn('school-logos/transparent/', network)

    def test_advisor_section_has_no_unavailable_full_board_link_and_shows_fuller_portraits(self):
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        stylesheet = (ROOT / "assets" / "css" / "homepage.css").read_text(
            encoding="utf-8"
        )

        self.assertNotIn("Meet the full board", html)
        self.assertIn(
            ".advisor-photo img{width:100%;height:100%;object-fit:contain;object-position:center",
            stylesheet,
        )

    def test_advisors_use_an_accessible_cyclic_centre_rail(self):
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        script = (ROOT / "assets" / "js" / "homepage.js").read_text(encoding="utf-8")
        stylesheet = (ROOT / "assets" / "css" / "homepage.css").read_text(
            encoding="utf-8"
        )

        self.assertIn('data-advisor-carousel', html)
        self.assertIn('id="advisor-track"', html)
        self.assertIn('aria-live="polite"', html)
        self.assertRegex(
            html,
            r'<button[^>]+data-advisor-direction="previous"[^>]+aria-controls="advisor-track"',
        )
        self.assertRegex(
            html,
            r'<button[^>]+data-advisor-direction="next"[^>]+aria-controls="advisor-track"',
        )
        self.assertIn("initAdvisorCarousel", script)
        self.assertIn("showAdvisor", script)
        self.assertIn("% cards.length", script)
        self.assertIn("is-previous", script)
        self.assertIn("is-next", script)

    def test_homepage_marquee_skips_clone_loop_for_reduced_motion(self):
        script = (ROOT / "assets" / "js" / "homepage.js").read_text(encoding="utf-8")
        self.assertIn("prefers-reduced-motion: reduce", script)
        self.assertIn("reducedMotionQuery.matches", script)

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

    def test_upcoming_cta_routes_through_preview_before_full_opportunities_page(self):
        text = (ROOT / "index.html").read_text(encoding="utf-8")
        self.assertIn(
            '<a class="button light" href="#opportunities">View upcoming opportunities</a>',
            text,
        )

        preview = text[
            text.index('<section class="section opportunities" id="opportunities">') :
        ]
        self.assertIn(
            '<a class="opportunity-more" href="pages/upcoming.html">View all opportunities →</a>',
            preview,
        )

        stylesheet = (ROOT / "assets" / "css" / "homepage.css").read_text(
            encoding="utf-8"
        )
        self.assertIn(".opportunity-footer", stylesheet)
        self.assertIn(".opportunity-more", stylesheet)

    def test_homepage_carousels_keep_all_programmes_discoverable_and_placeholders_anonymous(self):
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        shared_script = (ROOT / "assets" / "js" / "iyof-carousel.js").read_text(
            encoding="utf-8"
        )

        outer_start = html.index('id="initiative-track"')
        inner_start = html.index('data-iyof-carousel="ambassadors"')
        events_start = html.index('data-tone="yellow"')
        initiatives = html[outer_start:inner_start]
        self.assertIn('data-iyof-carousel="initiatives"', html)
        self.assertIn('id="initiative-track"', initiatives)
        self.assertEqual(1, initiatives.count('data-carousel-slide'))
        self.assertLess(inner_start, events_start)
        for label, href in (
            ("Student Ambassador", "pages/student-ambassador.html"),
            ("Events and Camps", "pages/events-and-camps.html"),
            ("Internship Opportunities", "pages/internship-opportunities.html"),
            ("Alumni Network", "pages/alumni-network.html"),
        ):
            self.assertIn(f">{label}</button>", html)
            self.assertIn(f'href="{href}"', html)

        self.assertIn('data-carousel-mode="single"', html)
        self.assertLess(html.index('data-iyof-carousel="ambassadors"'), html.index('data-tone="yellow"'))
        self.assertEqual(3, html.count('class="ambassador-placeholder-card"'))
        for number in ("01", "02", "03"):
            self.assertIn(f"Student Ambassador {number}", html)
        self.assertEqual(3, html.count("Photo and profile coming soon."))
        self.assertNotIn("Community Connector", html)
        self.assertNotIn("Event Co-host", html)
        self.assertNotIn("Peer Mentor", html)

        self.assertIn("initScopedCarousel", shared_script)
        self.assertIn("slide.inert", shared_script)
        self.assertIn("previousButton.disabled", shared_script)
        self.assertIn("'ArrowLeft'", shared_script)
        self.assertIn("prefers-reduced-motion: reduce", shared_script)
    def test_student_ambassador_detail_uses_the_same_three_anonymous_placeholders(self):
        html = (ROOT / "pages" / "student-ambassador.html").read_text(encoding="utf-8")
        self.assertIn('data-iyof-carousel="ambassadors"', html)
        self.assertEqual(3, html.count('class="static-ambassador-card"'))
        for number in ("01", "02", "03"):
            self.assertIn(f"Student Ambassador {number}", html)
        self.assertEqual(3, html.count("Photo and profile coming soon."))
        self.assertIn('../assets/js/iyof-carousel.js', html)


if __name__ == "__main__":
    unittest.main()
