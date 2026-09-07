#!/usr/bin/env python3
"""Exercise IYOF's public static-site behaviour with Firefox WebDriver."""

from __future__ import annotations

import argparse
import base64
import json
from pathlib import Path
from subprocess import DEVNULL, Popen
from time import sleep, time
from urllib.error import URLError
from urllib.request import Request, urlopen


class Driver:
    def __init__(self, reduced_motion: bool = False):
        self.process = Popen(["geckodriver", "--port", "4444"], stdout=DEVNULL, stderr=DEVNULL)
        deadline = time() + 15
        while True:
            try:
                self.request("GET", "/status")
                break
            except URLError:
                if time() >= deadline:
                    self.process.kill()
                    raise RuntimeError("geckodriver did not start")
                sleep(0.1)
        capabilities = {"browserName": "firefox", "moz:firefoxOptions": {"args": ["-headless"]}}
        if reduced_motion:
            capabilities["moz:firefoxOptions"]["prefs"] = {"ui.prefersReducedMotion": 1}
        self.session = self.request("POST", "/session", {"capabilities": {"alwaysMatch": capabilities}})["value"]["sessionId"]

    def request(self, method: str, path: str, payload: object | None = None):
        data = None if payload is None else json.dumps(payload).encode()
        request = Request(f"http://127.0.0.1:4444{path}", data=data, method=method)
        request.add_header("Content-Type", "application/json")
        with urlopen(request, timeout=30) as response:
            return json.load(response)

    def command(self, method: str, path: str, payload: object | None = None):
        return self.request(method, f"/session/{self.session}{path}", payload)["value"]

    def navigate(self, url: str):
        self.command("POST", "/url", {"url": url})

    def execute(self, script: str):
        return self.command("POST", "/execute/sync", {"script": script, "args": []})

    def resize(self, width: int, height: int):
        self.command("POST", "/window/rect", {"width": width, "height": height})

    def key(self, value: str):
        self.command("POST", "/actions", {"actions": [{"type": "key", "id": "keyboard", "actions": [{"type": "keyDown", "value": value}, {"type": "keyUp", "value": value}]}]})

    def screenshot(self, path: Path):
        path.write_bytes(base64.b64decode(self.command("GET", "/screenshot")))

    def close(self):
        try:
            self.command("DELETE", "")
        finally:
            self.process.terminate()
            self.process.wait(timeout=10)


def assert_equal(actual, expected, message):
    if actual != expected:
        raise AssertionError(f"{message}: expected {expected!r}, got {actual!r}")


def capture_pages(driver: Driver, base: str, output: Path):
    routes = {
        "homepage-1440.png": "index.html",
        "student-ambassador-1440.png": "pages/student-ambassador.html",
        "about-1440.png": "pages/about-us.html",
        "upcoming-1440.png": "pages/upcoming.html",
        "article-1440.png": "pages/what-a-3-star-michelin-restaurant-taught-me-about-excellence.html",
        "contact-1440.png": "pages/contact.html",
    }
    driver.resize(1440, 1100)
    for filename, route in routes.items():
        driver.navigate(f"{base}/{route}")
        sleep(0.5)
        audit = driver.execute("""
          return { overflow: document.documentElement.scrollWidth <= window.innerWidth,
            missing: [...document.images].filter(img => { const rect = img.getBoundingClientRect(); return rect.bottom > 0 && rect.top < window.innerHeight && (!img.complete || img.naturalWidth === 0); }).map(img => img.currentSrc || img.src) };
        """)
        if not audit["overflow"] or audit["missing"]:
            raise AssertionError(f"route audit failed for {route}: {audit}")
        if route == "pages/about-us.html":
            assert_equal(driver.execute("return getComputedStyle(document.querySelector('.page-section[data-section-id=\"67cf56b1c7ae533bb48a17ac\"]')).display"), "none", "About hero removal")
        driver.screenshot(output / filename)


def assert_single_slide_geometry(driver: Driver, kind: str):
    geometry = driver.execute(f"""
      const carousel = document.querySelector('[data-iyof-carousel="{kind}"]');
      const windowRect = carousel.querySelector('[data-carousel-window]').getBoundingClientRect();
      return {{ windowWidth: windowRect.width, slides: [...carousel.querySelectorAll('[data-carousel-slide]')].map(slide => {{
        const rect = slide.getBoundingClientRect();
        const title = slide.querySelector('h3,h4');
        return {{ hidden: slide.hidden, display: getComputedStyle(slide).display, width: rect.width, height: rect.height,
          titleWidth: title ? title.clientWidth : 0, titleScrollWidth: title ? title.scrollWidth : 0 }};
      }}) }};
    """)
    active = [slide for slide in geometry["slides"] if not slide["hidden"]]
    hidden = [slide for slide in geometry["slides"] if slide["hidden"]]
    assert_equal(len(active), 1, f"{kind} active slide count")
    if abs(active[0]["width"] - geometry["windowWidth"]) > 1:
        raise AssertionError(f"{kind} active slide width: {active[0]['width']} vs window {geometry['windowWidth']}")
    if active[0]["titleScrollWidth"] > active[0]["titleWidth"]:
        raise AssertionError(f"{kind} active heading is clipped: {active[0]}")
    for slide in hidden:
        if slide["display"] != "none" or slide["width"] != 0 or slide["height"] != 0:
            raise AssertionError(f"{kind} hidden slide remains rendered: {slide}")


def check_normal(base: str, output: Path):
    driver = Driver()
    try:
        driver.resize(1440, 1100)
        driver.navigate(f"{base}/index.html")
        state = driver.execute("""
          const outer = document.querySelector('[data-iyof-carousel="initiatives"]');
          const inner = document.querySelector('[data-iyof-carousel="ambassadors"]');
          return [outer.dataset.carouselIndex, inner.dataset.carouselIndex,
            outer.querySelector('[data-carousel-direction="previous"]').disabled,
            inner.hidden, document.documentElement.scrollWidth <= window.innerWidth];
        """)
        assert_equal(state, ["0", "0", True, False, True], "initial homepage carousel state")
        assert_single_slide_geometry(driver, "initiatives")
        assert_single_slide_geometry(driver, "ambassadors")
        driver.execute("document.querySelector('[data-iyof-carousel=initiatives]').scrollIntoView({block:'start', behavior:'instant'})")
        driver.screenshot(output / "homepage-initiative-01-student-ambassador-1440.png")
        driver.execute("document.querySelector('[data-iyof-carousel=ambassadors]').scrollIntoView({block:'start', behavior:'instant'})")
        driver.screenshot(output / "homepage-ambassadors-01-1440.png")
        driver.execute("document.querySelector('[data-iyof-carousel=initiatives] [data-carousel-direction=next]').click()")
        state = driver.execute("""
          const outer = document.querySelector('[data-iyof-carousel="initiatives"]');
          const inner = document.querySelector('[data-iyof-carousel="ambassadors"]');
          return [outer.dataset.carouselIndex, inner.hidden, inner.getAttribute('aria-hidden'), inner.dataset.carouselIndex,
            [...outer.querySelectorAll('[data-carousel-slide]')].filter(slide => !slide.hidden).length,
            [...outer.querySelectorAll('[data-carousel-slide]')].filter(slide => slide.hidden).every(slide => slide.inert && slide.getAttribute('aria-hidden') === 'true')];
        """)
        assert_equal(state, ["1", True, "true", "0", 1, True], "outer next state and hidden-slide access")
        assert_single_slide_geometry(driver, "initiatives")
        driver.execute("document.querySelector('[data-iyof-carousel=initiatives]').scrollIntoView({block:'start', behavior:'instant'})")
        driver.screenshot(output / "homepage-initiative-02-events-and-camps-1440.png")
        driver.execute("document.querySelector('[data-iyof-carousel=initiatives] [data-carousel-index=\"0\"]').click()")
        driver.execute("document.querySelector('[data-iyof-carousel=ambassadors] [data-carousel-direction=next]').click()")
        state = driver.execute("""
          const outer = document.querySelector('[data-iyof-carousel="initiatives"]');
          const inner = document.querySelector('[data-iyof-carousel="ambassadors"]');
          return [outer.dataset.carouselIndex, inner.dataset.carouselIndex, inner.hidden];
        """)
        assert_equal(state, ["0", "1", False], "inner arrow isolation")
        assert_single_slide_geometry(driver, "initiatives")
        assert_single_slide_geometry(driver, "ambassadors")
        driver.execute("document.querySelector('[data-iyof-carousel=ambassadors]').scrollIntoView({block:'start', behavior:'instant'})")
        driver.screenshot(output / "homepage-ambassadors-02-1440.png")
        driver.execute("document.querySelector('[data-iyof-carousel=initiatives] [data-carousel-window]').focus()")
        driver.key("\ue014")
        assert_equal(driver.execute("return document.querySelector('[data-iyof-carousel=initiatives]').dataset.carouselIndex"), "1", "outer keyboard right arrow")
        assert_single_slide_geometry(driver, "initiatives")
        driver.execute("document.querySelector('[data-iyof-carousel=initiatives] [data-carousel-index=\"2\"]').click()")
        assert_single_slide_geometry(driver, "initiatives")
        driver.execute("document.querySelector('[data-iyof-carousel=initiatives]').scrollIntoView({block:'start', behavior:'instant'})")
        driver.screenshot(output / "homepage-initiative-03-internships-1440.png")
        driver.execute("document.querySelector('[data-iyof-carousel=initiatives] [data-carousel-index=\"3\"]').click()")
        assert_single_slide_geometry(driver, "initiatives")
        driver.execute("document.querySelector('[data-iyof-carousel=initiatives]').scrollIntoView({block:'start', behavior:'instant'})")
        driver.screenshot(output / "homepage-initiative-04-alumni-1440.png")
        assert_equal(driver.execute("return document.querySelector('[data-iyof-carousel=initiatives] [data-carousel-direction=next]').disabled"), True, "outer endpoint next disabled")
        driver.execute("document.querySelector('[data-iyof-carousel=initiatives] [data-carousel-index=\"0\"]').click(); document.querySelector('[data-iyof-carousel=ambassadors] [data-carousel-window]').focus()")
        driver.key("\ue014")
        assert_equal(driver.execute("return [document.querySelector('[data-iyof-carousel=initiatives]').dataset.carouselIndex, document.querySelector('[data-iyof-carousel=ambassadors]').dataset.carouselIndex]"), ["0", "2"], "inner keyboard arrow isolation")
        assert_single_slide_geometry(driver, "initiatives")
        assert_single_slide_geometry(driver, "ambassadors")
        driver.execute("document.querySelector('[data-iyof-carousel=ambassadors]').scrollIntoView({block:'start', behavior:'instant'})")
        driver.screenshot(output / "homepage-ambassadors-03-1440.png")
        driver.execute("document.querySelector('[data-iyof-carousel=initiatives]').scrollIntoView({block:'start', behavior:'instant'})")
        driver.screenshot(output / "homepage-initiatives-1440.png")
        driver.resize(390, 844)
        driver.navigate(f"{base}/index.html")
        assert_equal(driver.execute("return document.documentElement.scrollWidth <= window.innerWidth"), True, "mobile homepage overflow")
        for index in range(4):
            driver.execute(f"document.querySelector('[data-iyof-carousel=initiatives] [data-carousel-index=\"{index}\"]').click()")
            assert_single_slide_geometry(driver, "initiatives")
        driver.execute("document.querySelector('[data-iyof-carousel=initiatives] [data-carousel-index=\"0\"]').click()")
        assert_single_slide_geometry(driver, "ambassadors")
        driver.execute("document.querySelector('[data-iyof-carousel=ambassadors] [data-carousel-direction=next]').click()")
        assert_single_slide_geometry(driver, "ambassadors")
        driver.execute("document.querySelector('[data-iyof-carousel=ambassadors] [data-carousel-direction=next]').click()")
        assert_single_slide_geometry(driver, "ambassadors")
        driver.execute("document.querySelector('[data-iyof-carousel=initiatives]').scrollIntoView({block:'start', behavior:'instant'})")
        driver.screenshot(output / "homepage-initiative-01-390.png")
        driver.execute("document.querySelector('[data-iyof-carousel=ambassadors]').scrollIntoView({block:'start', behavior:'instant'})")
        driver.screenshot(output / "homepage-ambassadors-03-390.png")
        driver.navigate(f"{base}/index.html")
        driver.screenshot(output / "homepage-390.png")
        driver.resize(1440, 1100)
        driver.navigate(f"{base}/pages/student-ambassador.html")
        state = driver.execute("""
          const carousel = document.querySelector('[data-iyof-carousel="ambassadors"]');
          return [carousel.dataset.carouselIndex, carousel.querySelectorAll('[data-carousel-slide]').length];
        """)
        assert_equal(state, ["0", 3], "detail placeholder carousel initial state")
        assert_single_slide_geometry(driver, "ambassadors")
        driver.execute("document.querySelector('[data-iyof-carousel=ambassadors] [data-carousel-direction=next]').click()")
        assert_equal(driver.execute("return document.querySelector('[data-iyof-carousel=ambassadors]').dataset.carouselIndex"), "1", "detail placeholder next arrow")
        assert_single_slide_geometry(driver, "ambassadors")
        driver.execute("document.querySelector('[data-iyof-carousel=ambassadors]').scrollIntoView({block:'start', behavior:'instant'})")
        driver.screenshot(output / "student-ambassador-placeholders-1440.png")
        capture_pages(driver, base, output)
    finally:
        driver.close()


def check_reduced_motion(base: str):
    driver = Driver(reduced_motion=True)
    try:
        driver.navigate(f"{base}/index.html")
        state = driver.execute("""
          const outer = document.querySelector('[data-iyof-carousel="initiatives"]');
          const track = outer.querySelector('.carousel-track');
          return [window.matchMedia('(prefers-reduced-motion: reduce)').matches,
            outer.classList.contains('carousel-reduced-motion'), getComputedStyle(track).transitionDuration];
        """)
        assert_equal(state[0:2], [True, True], "reduced motion state")
        if state[2] not in ("0s", "0.01ms"):
            raise AssertionError(f"reduced motion transition duration: {state[2]!r}")
    finally:
        driver.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("base_url")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    base = args.base_url.rstrip("/")
    from centre_revision_check import check_desktop, check_mobile, check_reduced_motion, check_secondary_pages
    check_desktop(base, args.output)
    check_mobile(base, args.output)
    check_secondary_pages(base, args.output)
    check_reduced_motion(base)
    print(f'centre revision checks passed; screenshots: {args.output}')


if __name__ == "__main__":
    main()
