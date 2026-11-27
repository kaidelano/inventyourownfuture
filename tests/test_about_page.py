from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class AboutPageTests(unittest.TestCase):
    def test_main_links_to_programmes_and_contact_without_stock_photos(self):
        page = (ROOT / "pages" / "about-us.html").read_text(encoding="utf-8")
        main = page.split("<main", 1)[1].split("</main>", 1)[0]
        for href in (
            "student-ambassador.html",
            "events-and-camps.html",
            "internship-opportunities.html",
            "alumni-network.html",
            "contact.html",
        ):
            with self.subTest(href=href):
                self.assertIn(f'href="{href}"', main)
        self.assertNotIn("unsplash", page.lower())
