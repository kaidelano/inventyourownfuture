#!/usr/bin/env python3
"""Browser acceptance checks for the IYOF centre-focused carousel revision."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))
from browser_check import Driver, assert_equal


def capture(driver: Driver, output: Path, name: str, selector: str):
    driver.execute(f"document.querySelector('{selector}').scrollIntoView({{block:'start', behavior:'instant'}})")
    driver.screenshot(output / name)


def rail_state(driver: Driver, selector: str, width_range: tuple[float, float]):
    state = driver.execute(f"""
      const rail = document.querySelector('{selector}');
      const windowRect = (rail.querySelector('[data-carousel-window]') || rail.querySelector('[data-carousel-track]')).getBoundingClientRect();
      return {{
        index: rail.dataset.carouselIndex,
        overflow: document.documentElement.scrollWidth <= globalThis.innerWidth,
        slides: [...rail.querySelector('[data-carousel-track]').children].filter(slide => slide.matches('[data-carousel-slide]')).map(slide => {{
          const rect = slide.getBoundingClientRect();
          const heading = slide.querySelector('h3,h4');
          const overflow = [...slide.querySelectorAll('h3,h4,p,a,button,.initiative-ambassadors,.ambassador-placeholder-card')].filter(node => {{
            const inner = node.getBoundingClientRect();
            return inner.width > 0 && inner.height > 0 && (inner.top < rect.top - 1 || inner.bottom > rect.bottom + 1 || inner.left < rect.left - 1 || inner.right > rect.right + 1);
          }}).map(node => node.className || node.tagName);
          return {{ classes: [...slide.classList], inert: slide.inert, display: getComputedStyle(slide).display,
            left: rect.left, top: rect.top, width: rect.width, height: rect.height, overflow,
            heading: heading ? [heading.scrollWidth, heading.clientWidth] : [0, 0] }};
        }}),
        window: [windowRect.left, windowRect.width, windowRect.top]
      }};
    """)
    active = [slide for slide in state["slides"] if "is-active" in slide["classes"]]
    previews = [slide for slide in state["slides"] if "is-previous" in slide["classes"] or "is-next" in slide["classes"]]
    hidden = [slide for slide in state["slides"] if "is-hidden" in slide["classes"]]
    assert_equal(len(active), 1, f"{selector} active card count")
    assert_equal(len(previews), 2, f"{selector} visible neighbour count")
    assert_equal(len(hidden), len(state["slides"]) - 3, f"{selector} remote card count")
    active_card = active[0]
    centre = active_card["left"] + active_card["width"] / 2
    rail_centre = state["window"][0] + state["window"][1] / 2
    if abs(centre - rail_centre) > 2:
        raise AssertionError(f"{selector} active card is not centred: {centre} vs {rail_centre}")
    ratio = active_card["width"] / state["window"][1]
    if not width_range[0] <= ratio <= width_range[1]:
        raise AssertionError(f"{selector} active width ratio {ratio:.3f} outside {width_range}")
    if active_card["heading"][0] > active_card["heading"][1]:
        raise AssertionError(f"{selector} active heading is clipped: {active_card['heading']}")
    if active_card["overflow"]:
        raise AssertionError(f"{selector} active content escapes card bounds: {active_card['overflow']}")
    if active_card["inert"]:
        raise AssertionError(f"{selector} active card is inert")
    for preview in previews:
        if preview["display"] == "none" or not preview["inert"]:
            raise AssertionError(f"{selector} neighbour state invalid: {preview}")
        if preview["width"] >= active_card["width"] or preview["top"] <= active_card["top"]:
            raise AssertionError(f"{selector} neighbour is not smaller/lower: {preview}")
    for remote in hidden:
        if remote["display"] != "none" or not remote["inert"]:
            raise AssertionError(f"{selector} remote card remains interactive/rendered: {remote}")
    if not state["overflow"]:
        raise AssertionError(f"{selector} causes page overflow")


def click(driver: Driver, selector: str):
    driver.execute(f"document.querySelector('{selector}').click()")
    from time import sleep
    sleep(0.35)


def check_desktop(base: str, output: Path):
    driver = Driver()
    try:
        driver.resize(1440, 1100)
        driver.navigate(f"{base}/index.html")
        outer = '[data-iyof-carousel="initiatives"]'
        inner = '[data-iyof-carousel="ambassadors"]'
        advisors = '[data-advisor-carousel]'
        assert_equal(driver.execute(f"return document.querySelector('{inner}').closest('.initiative-slide').classList.contains('is-active')"), True, "inner component is integrated in active Student Ambassador card")
        rail_state(driver, outer, (0.62, 0.68))
        rail_state(driver, advisors, (0.38, 0.44))
        capture(driver, output, 'initiative-student-inner-01-1440.png', outer)
        capture(driver, output, 'ambassador-inner-01-1440.png', inner)
        for expected in ("1", "2", "3", "0"):
            click(driver, f'{outer} [data-carousel-direction="next"]')
            assert_equal(driver.execute(f"return document.querySelector('{outer}').dataset.carouselIndex"), expected, "initiative cyclic next")
            rail_state(driver, outer, (0.62, 0.68))
        click(driver, f'{outer} [data-carousel-index="0"]')
        driver.execute(f"document.querySelector('{outer} [data-carousel-window]').focus()")
        driver.key("\ue014")
        from time import sleep
        sleep(0.35)
        assert_equal(driver.execute(f"return document.querySelector('{outer}').dataset.carouselIndex"), "1", "outer scoped keyboard next")
        click(driver, f'{outer} [data-carousel-index="0"]')
        click(driver, f'{inner} [data-carousel-direction="next"]')
        assert_equal(driver.execute(f"return [document.querySelector('{outer}').dataset.carouselIndex, document.querySelector('{inner}').dataset.carouselIndex]"), ["0", "1"], "inner arrow isolation")
        driver.execute(f"document.querySelector('{inner} [data-carousel-window]').focus()")
        driver.key("\ue014")
        sleep(0.35)
        assert_equal(driver.execute(f"return [document.querySelector('{outer}').dataset.carouselIndex, document.querySelector('{inner}').dataset.carouselIndex]"), ["0", "2"], "inner scoped keyboard isolation")
        capture(driver, output, 'initiative-student-inner-03-1440.png', inner)
        click(driver, f'{outer} [data-carousel-index="1"]')
        assert_equal(driver.execute(f"return document.querySelector('{inner}').closest('.initiative-slide').classList.contains('is-active')"), False, "inner hides with inactive Student Ambassador card")
        capture(driver, output, 'initiative-events-1440.png', outer)
        for expected in ("1", "2", "3", "4", "0"):
            click(driver, f'{advisors} [data-advisor-direction="next"]')
            assert_equal(driver.execute(f"return document.querySelector('{advisors}').dataset.advisorIndex"), expected, "advisor cyclic next")
            rail_state(driver, advisors, (0.38, 0.44))
            if expected in ("0", "2", "4"):
                capture(driver, output, f'advisors-{expected}-1440.png', advisors)
        capture(driver, output, 'programme-evidence-1440.png', '#impact')
        capture(driver, output, 'opportunities-1440.png', '#opportunities')
    finally:
        driver.close()


def check_mobile(base: str, output: Path):
    driver = Driver()
    try:
        driver.resize(390, 844)
        driver.navigate(f"{base}/index.html")
        outer = '[data-iyof-carousel="initiatives"]'
        inner = '[data-iyof-carousel="ambassadors"]'
        rail_state(driver, outer, (0.88, 0.92))
        capture(driver, output, 'initiative-student-inner-01-390.png', outer)
        click(driver, f'{inner} [data-carousel-direction="next"]')
        click(driver, f'{inner} [data-carousel-direction="next"]')
        capture(driver, output, 'ambassador-inner-03-390.png', inner)
        click(driver, f'{outer} [data-carousel-index="2"]')
        rail_state(driver, outer, (0.88, 0.92))
        capture(driver, output, 'initiative-internships-390.png', outer)
    finally:
        driver.close()



def check_secondary_pages(base: str, output: Path):
    routes = {
        'student-ambassador-1440.png': 'pages/student-ambassador.html',
        'about-1440.png': 'pages/about-us.html',
        'upcoming-1440.png': 'pages/upcoming.html',
        'article-1440.png': 'pages/what-a-3-star-michelin-restaurant-taught-me-about-excellence.html',
        'contact-1440.png': 'pages/contact.html',
    }
    driver = Driver()
    try:
        driver.resize(1440, 1100)
        for name, route in routes.items():
            driver.navigate(f"{base}/{route}")
            state = driver.execute("return document.documentElement.scrollWidth <= window.innerWidth")
            assert_equal(state, True, f'{route} desktop overflow')
            driver.screenshot(output / name)
    finally:
        driver.close()


def check_reduced_motion(base: str):
    driver = Driver(reduced_motion=True)
    try:
        driver.resize(1440, 1100)
        driver.navigate(f"{base}/index.html")
        outer = '[data-iyof-carousel="initiatives"]'
        state = driver.execute(f"""
          const rail = document.querySelector('{outer}');
          const card = rail.querySelector('.initiative-slide.is-active');
          return [window.matchMedia('(prefers-reduced-motion: reduce)').matches,
            rail.classList.contains('carousel-reduced-motion'), getComputedStyle(card).transitionDuration];
        """)
        assert_equal(state[:2], [True, True], 'reduced-motion carousel state')
        if state[2] not in ('0s', '0.01ms'):
            raise AssertionError(f'reduced-motion transition remains active: {state[2]}')
        click(driver, f'{outer} [data-carousel-direction="next"]')
        assert_equal(driver.execute(f"return document.querySelector('{outer}').dataset.carouselIndex"), '1', 'reduced-motion state change')
    finally:
        driver.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('base_url')
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    base = args.base_url.rstrip('/')
    check_desktop(base, args.output)
    check_mobile(base, args.output)
    check_secondary_pages(base, args.output)
    check_reduced_motion(base)
    print(f'centre revision checks passed; screenshots: {args.output}')


if __name__ == '__main__':
    main()
