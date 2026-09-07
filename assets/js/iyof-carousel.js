(() => {
  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');

  const initScopedCarousel = (carousel, onChange) => {
    const track = carousel.querySelector('[data-carousel-track]');
    const slides = track ? [...track.children].filter((child) => child.matches('[data-carousel-slide]')) : [];
    const previousButton = carousel.querySelector('[data-carousel-direction="previous"]');
    const nextButton = carousel.querySelector('[data-carousel-direction="next"]');
    const selectors = [...carousel.querySelectorAll('[data-carousel-index]')];
    const windowElement = carousel.querySelector('[data-carousel-window]');
    const current = carousel.querySelector('[data-carousel-current]');
    const total = carousel.querySelector('[data-carousel-total]');
    const rail = carousel.dataset.carouselMode === 'rail';
    if (!slides.length || !previousButton || !nextButton || !windowElement) return;

    let index = 0;
    const show = (nextIndex) => {
      index = rail
        ? (nextIndex + slides.length) % slides.length
        : Math.max(0, Math.min(nextIndex, slides.length - 1));
      const previousIndex = (index - 1 + slides.length) % slides.length;
      const nextRailIndex = (index + 1) % slides.length;

      slides.forEach((slide, slideIndex) => {
        const active = slideIndex === index;
        const previous = rail && slideIndex === previousIndex;
        const next = rail && slideIndex === nextRailIndex;
        const preview = previous || next;
        slide.hidden = rail ? !active && !preview : !active;
        slide.inert = !active;
        slide.classList.toggle('is-active', active);
        slide.classList.toggle('is-previous', previous);
        slide.classList.toggle('is-next', next);
        slide.classList.toggle('is-hidden', !active && !preview);
        slide.setAttribute('aria-hidden', String(!active));
      });
      selectors.forEach((selector, selectorIndex) => {
        const active = selectorIndex === index;
        selector.setAttribute('aria-current', String(active));
        selector.setAttribute('aria-pressed', String(active));
      });
      previousButton.disabled = !rail && index === 0;
      nextButton.disabled = !rail && index === slides.length - 1;
      if (current) current.textContent = String(index + 1);
      if (total) total.textContent = String(slides.length);
      carousel.dataset.carouselIndex = String(index);
      onChange?.(index);
    };

    previousButton.addEventListener('click', () => show(index - 1));
    nextButton.addEventListener('click', () => show(index + 1));
    selectors.forEach((selector, selectorIndex) => {
      selector.addEventListener('click', () => show(selectorIndex));
    });
    windowElement.addEventListener('keydown', (event) => {
      if (event.key !== 'ArrowLeft' && event.key !== 'ArrowRight') return;
      event.preventDefault();
      event.stopPropagation();
      show(index + (event.key === 'ArrowRight' ? 1 : -1));
    });
    carousel.classList.toggle('carousel-reduced-motion', reducedMotion.matches);
    show(0);
  };

  const initCarousels = () => {
    document.querySelectorAll('[data-iyof-carousel="initiatives"]').forEach((carousel) => {
      carousel.dataset.carouselMode = 'rail';
      initScopedCarousel(carousel);
    });
    document.querySelectorAll('[data-iyof-carousel="ambassadors"]').forEach((carousel) => {
      initScopedCarousel(carousel);
    });
  };

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initCarousels);
  } else {
    initCarousels();
  }
})();
