from pathlib import Path
import re
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
HTML_FILES = [ROOT / "index.html", *sorted((ROOT / "pages").glob("*.html"))]


class InitiativesPageTests(unittest.TestCase):
    def test_initiatives_page_exists_and_lists_all_four_programmes(self):
        page = ROOT / "pages" / "initiatives.html"
        self.assertTrue(page.exists(), "pages/initiatives.html should exist")
        text = page.read_text(encoding="utf-8")
        expected = {
            "student-ambassador.html": "Student Ambassador",
            "events-and-camps.html": "Events and Camps",
            "internship-opportunities.html": "Internship Opportunities",
            "alumni-network.html": "Alumni Network",
        }
        for href, label in expected.items():
            self.assertIn(f'href="{href}"', text)
            self.assertIn(label, text)
        self.assertEqual(4, len(re.findall(r'class="initiative-card\b', text)))

    def test_every_page_uses_a_direct_initiatives_navigation_link(self):
        for page in HTML_FILES:
            with self.subTest(page=page.relative_to(ROOT)):
                text = page.read_text(encoding="utf-8")
                href = "pages/initiatives.html" if page == ROOT / "index.html" else "initiatives.html"
                if page == ROOT / "index.html":
                    direct_links = re.findall(
                        rf'<a href="{re.escape(href)}"[^>]*>\s*Initiatives\s*</a>',
                        text,
                        flags=re.S,
                    )
                else:
                    direct_links = re.findall(
                        rf'<a href="{re.escape(href)}"[^>]*data-animation-role="header-element"[^>]*>\s*Initiatives\s*</a>',
                        text,
                        flags=re.S,
                    )
                self.assertGreaterEqual(len(direct_links), 1)
                self.assertNotIn('aria-controls="initiatives"', text)
                self.assertNotIn('data-folder-id="/initiatives"', text)
                self.assertNotIn('data-folder="/initiatives"', text)

    def test_initiatives_page_uses_brand_colour_accents_and_responsive_grid(self):
        page = (ROOT / "pages" / "initiatives.html").read_text(encoding="utf-8")
        for accent in ("yellow", "teal", "pink", "purple"):
            self.assertIn(f"initiative-card--{accent}", page)
        css = (ROOT / "assets" / "css" / "static-site.css").read_text(encoding="utf-8")
        self.assertIn(".initiatives-grid", css)
        self.assertRegex(css, r"@media\s*\(max-width:\s*700px\)")

    def test_site_validator_passes_with_javascript_source_files_present(self):
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "check-site.py")],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
