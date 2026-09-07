(() => {
  const reducedMotionQuery = window.matchMedia('(prefers-reduced-motion: reduce)');

  const initMarquees = () => {
    document.querySelectorAll('.marquee').forEach((marquee) => {
      const track = marquee.querySelector('.marquee-track');
      const source = track?.querySelector('.logo-sequence:not([aria-hidden])');
      if (!track || !source) return;

      track.classList.remove('ready');
      track.querySelectorAll('.logo-sequence[aria-hidden="true"]').forEach((sequence) => sequence.remove());
      source.querySelectorAll('.marquee-filler').forEach((item) => item.remove());
      if (reducedMotionQuery.matches) {
        track.style.removeProperty('--marquee-start');
        track.classList.add('ready');
        return;
      }

      const originals = [...source.children].map((item) => item.cloneNode(true));
      const targetWidth = marquee.clientWidth + 320;
      while (source.scrollWidth < targetWidth) {
        originals.forEach((template) => {
          const clone = template.cloneNode(true);
          clone.classList.add('marquee-filler');
          clone.setAttribute('aria-hidden', 'true');
          clone.querySelectorAll('img').forEach((img) => { img.alt = ''; });
          source.append(clone);
        });
      }

      const mirror = source.cloneNode(true);
      mirror.setAttribute('aria-hidden', 'true');
      mirror.querySelectorAll('img').forEach((img) => { img.alt = ''; });
      track.append(mirror);
      track.style.setProperty('--marquee-start', `-${source.scrollWidth}px`);
      track.classList.add('ready');
    });
  };

  const initAdvisorCarousel = () => {
    document.querySelectorAll('[data-advisor-carousel]').forEach((carousel) => {
      const track = carousel.querySelector('#advisor-track');
      const cards = [...carousel.querySelectorAll('.advisor-card')];
      const previousButton = carousel.querySelector('[data-advisor-direction="previous"]');
      const nextButton = carousel.querySelector('[data-advisor-direction="next"]');
      const currentLabel = carousel.querySelector('[data-advisor-current]');
      const totalLabel = carousel.querySelector('[data-advisor-total]');
      if (!track || !cards.length || !previousButton || !nextButton) return;

      let activeIndex = 0;
      const showAdvisor = (nextIndex) => {
        activeIndex = (nextIndex + cards.length) % cards.length;
        const previousIndex = (activeIndex - 1 + cards.length) % cards.length;
        const nextCardIndex = (activeIndex + 1) % cards.length;
        cards.forEach((card, cardIndex) => {
          const active = cardIndex === activeIndex;
          const previous = cardIndex === previousIndex;
          const next = cardIndex === nextCardIndex;
          const preview = previous || next;
          card.inert = !active;
          card.classList.toggle('is-active', active);
          card.classList.toggle('is-previous', previous);
          card.classList.toggle('is-next', next);
          card.classList.toggle('is-hidden', !active && !preview);
          card.setAttribute('aria-hidden', String(!active));
          if (active) card.setAttribute('aria-current', 'true');
          else card.removeAttribute('aria-current');
        });
        if (currentLabel) currentLabel.textContent = String(activeIndex + 1);
        if (totalLabel) totalLabel.textContent = String(cards.length);
        carousel.dataset.advisorIndex = String(activeIndex);
      };

      previousButton.addEventListener('click', () => showAdvisor(activeIndex - 1));
      nextButton.addEventListener('click', () => showAdvisor(activeIndex + 1));
      track.addEventListener('keydown', (event) => {
        if (event.key !== 'ArrowLeft' && event.key !== 'ArrowRight') return;
        event.preventDefault();
        showAdvisor(activeIndex + (event.key === 'ArrowRight' ? 1 : -1));
      });
      showAdvisor(0);
    });
  };

  const navToggle = document.querySelector('.nav-toggle');
  const navigation = document.querySelector('#primary-navigation');
  const setNavigationOpen = (open) => {
    if (!navToggle || !navigation) return;
    navToggle.setAttribute('aria-expanded', String(open));
    navigation.classList.toggle('open', open);
  };

  navToggle?.addEventListener('click', () => {
    setNavigationOpen(navToggle.getAttribute('aria-expanded') !== 'true');
  });
  navigation?.querySelectorAll('a').forEach((link) => {
    link.addEventListener('click', () => setNavigationOpen(false));
  });
  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape') setNavigationOpen(false);
  });

  document.querySelectorAll('.filter').forEach((button) => {
    button.setAttribute('aria-pressed', String(button.classList.contains('active')));
    button.addEventListener('click', () => {
      document.querySelectorAll('.filter').forEach((item) => {
        const active = item === button;
        item.classList.toggle('active', active);
        item.setAttribute('aria-pressed', String(active));
      });
      document.querySelectorAll('.job').forEach((job) => {
        job.style.display = button.dataset.filter === 'all' || job.dataset.type === button.dataset.filter ? 'flex' : 'none';
      });
    });
  });

  initAdvisorCarousel();
  initMarquees();
  reducedMotionQuery.addEventListener('change', initMarquees);
  let marqueeResizeTimer;
  window.addEventListener('resize', () => {
    clearTimeout(marqueeResizeTimer);
    marqueeResizeTimer = window.setTimeout(initMarquees, 180);
    if (window.innerWidth > 1000) setNavigationOpen(false);
  });
})();
