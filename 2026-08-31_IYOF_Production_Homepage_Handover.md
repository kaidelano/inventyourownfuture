# IYOF Production Homepage Handover

**Prepared:** 31 August 2026, 11:51 HKT

**Repository:** `/home/kai/General/work/IYOF/inventyourownfuture/`

**GitHub:** <https://github.com/KelvinLi24/inventyourownfuture>

**Branch:** `feature/homepage-redesign`

**Production-homepage commit:** `a26544cb4fb12be92b976c81434aaf47467b7118`

**Status:** Approved design implemented in the root `index.html`, verified, committed, and pushed. The branch has not yet been merged into `main`.

---

## 1. Executive summary

The owner/team-approved **Initiatives-First Platform Hybrid** homepage has been promoted from a design prototype to the real production entry point:

- `index.html`

The former CMS-exported root homepage was replaced with a smaller, maintainable static page using dedicated homepage CSS and JavaScript. The implementation keeps IYOF's organisation, initiatives, programme delivery, education network, and advisors ahead of a secondary opportunity-preview layer.

The production branch is pushed and clean. The next release action is to open, review, and merge a pull request into `main`. GitHub Pages is enabled for the repository, but this handover found no `.github` deployment workflow or root `CNAME`; confirm the repository's Pages source/settings during merge.

---

## 2. Product and scope boundaries

IYOF is being developed as two related products:

1. **Public website:** the organisation's trust and information layer for students, parents, schools, institutional partners, advisors, and stakeholders.
2. **Future student platform/app:** a moderated opportunity and network product for students aged approximately 13–18.

The current website phase remains **frontend only**. Do not imply that the following exist until a backend is intentionally designed and implemented:

- account registration or authentication
- profile or application storage
- persistent saved opportunities
- messaging
- database-backed opportunity management
- automated application processing

For this reason, the earlier prototype-only save/heart controls were removed from production rather than presenting unsupported functionality.

---

## 3. Approved design direction

### Direction

**Initiatives-First Platform Hybrid**

### Core visual identity

- Yellow: `#FDB712`
- Teal: `#62C2AC`
- Pink: `#F0127A`
- Purple: `#6457A4`

### Design principles

- youthful without looking childish
- credible to parents, schools, partners, advisors, and shareholders
- authentic programme photography
- wider compositions that remain substantial on large displays
- strong brand-colour blocks used intentionally
- programme and impact content before job-style opportunities
- honest distinction between institutional partners and schools represented by past participants

### Production hierarchy

1. Mission-led hero
2. IYOF at a glance
3. Four initiatives
4. Education network
5. Programme delivery and student outcomes
6. Compact Board of Advisors section
7. Secondary opportunity preview
8. Final call to action and footer

The standalone yellow stakeholder/company-story block from an earlier prototype iteration remains intentionally removed.

---

## 4. Production implementation

### Root homepage

- `index.html`

The page now uses semantic, project-owned HTML instead of the former large CMS export. The production headline is:

> Open more paths for ambitious students.

### Homepage-specific styles

- `assets/css/homepage.css`

Homepage rules are scoped through the homepage markup rather than being pushed into every secondary page. This reduces regression risk across the existing static export.

### Homepage-specific behavior

- `assets/js/homepage.js`

Implemented behavior includes:

- responsive mobile navigation
- opportunity-category filters
- refresh-safe two-row education-network marquees
- dynamic marquee width filling for wide viewports
- hover/focus pausing
- reduced-motion fallback without clone loops or animation
- debounced marquee reconstruction after resize

### Regression coverage

- `tests/test_homepage.py`
- `tests/test_initiatives_page.py`

The homepage tests cover the approved production structure, real destinations, explicit button semantics, accessibility hooks, color-contrast overrides, and reduced-motion implementation.

---

## 5. Initiatives and real destinations

The four homepage initiative cards point to their real pages:

1. **Student Ambassador** → `pages/student-ambassador.html`
2. **Events and Camps** → `pages/events-and-camps.html`
3. **Internship Opportunities** → `pages/internship-opportunities.html`
4. **Alumni Network** → `pages/alumni-network.html`

The central Initiatives navigation links to:

- `pages/initiatives.html`

Other important homepage destinations include:

- About Us: `pages/about-us.html`
- Upcoming: `pages/upcoming.html`
- Contact: `pages/contact.html`
- Career Blog: `pages/career-blog.html`

No production CTA uses a placeholder `href="#"`.

---

## 6. Education-network marquee

The education network is deliberately split into two rows:

1. **Universities and institutional partners**
2. **Primary and secondary schools represented by past programme participants**

This avoids falsely presenting every listed school as a formal IYOF partner or endorser.

Institutional logo derivatives are stored under:

- `assets/images/partner-logos/`

The marquee implementation:

- fills wide viewports before becoming visible
- starts without a blank right edge after refresh
- moves left to right
- pauses on hover and keyboard focus
- hides accessibility-duplicate sequences from assistive technology
- disables animation and filler cloning under `prefers-reduced-motion: reduce`
- becomes horizontally usable when motion is reduced

---

## 7. Board of Advisors

The homepage contains a concise five-card advisor section rather than full biographies:

- Yeung Kwok Mung, Ken
- Dr. Tony Chen
- Dr. Witman Hung, JP
- Gloria Tam
- Mr. Lai Man-hin, SBS, FSDSM, FSMSM

Each card focuses on how the advisor strengthens IYOF. Full profiles remain on:

- `pages/about-us.html`

This keeps the homepage credible and impactful without making it biography-heavy.

---

## 8. Accessibility and production corrections

An initial independent review identified three blocking issues. All were fixed before the production commit:

1. **Missing keyboard skip link:** Added `Skip to content` targeting `#main-content`.
2. **Insufficient hero/focus contrast:** Added a dark hero-eyebrow override and dual-contrast focus treatment.
3. **Unsupported save controls:** Removed the three in-memory save/heart controls because no persistence or saved-opportunities destination exists.

Additional production semantics:

- interactive buttons have explicit `type="button"`
- menu and filters have accessible names
- the page contains one semantic `<main>` and one footer
- images have alternative text
- focus styling is visible across light and saturated backgrounds
- reduced-motion preferences are honored

A second independent review passed with:

- no security concerns
- no logic errors
- no remaining release blocker

---

## 9. Verification evidence

### Canonical tests

Command:

```bash
python3 -m unittest discover -s tests -v
```

Latest result:

```text
Ran 7 tests in 0.433s
OK
```

### Static-site validator

Command:

```bash
python3 scripts/check-site.py
```

Latest result:

- `missing_local_references`: none
- `forbidden_local_or_browser_paths`: none
- `squarespace_domains`: none
- `ok`: `true`

### JavaScript and Git checks

```bash
node --check assets/js/homepage.js
git diff --check
```

Both passed before commit.

### Rendered browser verification

The real page was exercised at desktop, wide desktop, and `390px` mobile sizes. Confirmed:

- no page-level horizontal overflow
- no broken rendered images
- no failed page requests in the focused browser run
- visible and working keyboard skip link
- mobile menu opens and closes
- opportunity filtering changes three visible cards to one internship card
- normal marquee movement works
- reduced-motion mode has no marquee animation or filler clones
- hero eyebrow uses the corrected dark text color

### HTTP preview checks

Latest focused post-commit check:

- local root: HTTP `200`
- Tailscale root: HTTP `200`
- Git worktree: clean before creating this handover file

---

## 10. Preview and review links

### Production root on the development server

- Local: <http://127.0.0.1:8080/index.html>
- Tailscale IP: <http://100.125.15.37:8080/index.html>
- Tailscale hostname: <http://mini-pc:8080/index.html>

The Tailscale URLs require the reviewing device to be connected to the same tailnet.

The preview server is managed by the user-level service:

- `iyof-preview.service`

### GitHub

- Branch: <https://github.com/KelvinLi24/inventyourownfuture/tree/feature/homepage-redesign>
- Open pull request: <https://github.com/KelvinLi24/inventyourownfuture/pull/new/feature/homepage-redesign>

### Historical design reference

- Comparison page: `sketches/homepage-variants/index.html`
- Approved prototype: `sketches/homepage-variants/initiatives-platform-hybrid/index.html`
- Prototype rationale: `sketches/homepage-variants/initiatives-platform-hybrid/README.md`
- Earlier design handover: `2026-08-30_IYOF_Website_Homepage_Design_Handover.md`

The earlier handover is a historical design record. Statements in it saying that production was not implemented are superseded by this document.

---

## 11. Git state and commit history

Remote used for team delivery:

```text
upstream  https://github.com/KelvinLi24/inventyourownfuture.git
```

Current feature sequence:

```text
6f8d5b7  feat: add initiatives landing page
3689874  feat: add approved homepage design prototype
a26544c  [verified] feat: promote approved homepage to production
```

The local, remote-branch, and GitHub API SHAs were verified to match at:

```text
a26544cb4fb12be92b976c81434aaf47467b7118
```

The branch was clean and synchronized with `upstream/feature/homepage-redesign` before this handover file was created.

---

## 12. Deployment status and next actions

### Current status

- Production root implemented: **yes**
- Tests and validator green: **yes**
- Independent review passed: **yes**
- Branch pushed: **yes**
- Merged into `main`: **no**
- Public GitHub Pages release confirmed: **no**

### Required release steps

1. Open a pull request from `feature/homepage-redesign` to `main`.
2. Review the PR diff, especially the large deletion caused by replacing the legacy CMS-exported `index.html`.
3. Confirm all intended commits are included.
4. Merge into `main` after owner/team approval.
5. Confirm the GitHub Pages source/build setting for the repository.
6. Wait for Pages deployment to complete.
7. Check the public URL at <https://kelvinli24.github.io/inventyourownfuture/>.
8. Re-run key link, mobile, image, and reduced-motion checks against the deployed site.
9. If the organisation uses a custom domain, configure and verify the domain separately; no root `CNAME` file was present during this handover.

Do not call the feature-branch implementation publicly deployed until the merge and Pages verification are complete.

---

## 13. Non-blocking follow-up improvements

These are useful improvements, not release blockers:

1. Return keyboard focus to the mobile menu toggle when Escape closes the menu.
2. Add canonical, favicon, Open Graph, and Twitter metadata.
3. Add explicit image dimensions/aspect ratios to reduce layout shift.
4. Lazy-load below-the-fold images where appropriate.
5. Improve keyboard ergonomics for the horizontally scrolling advisor row at tablet/mobile widths.
6. Add deployment-level browser checks against the final GitHub Pages URL.

Do not introduce new abstractions or dependencies solely for these items; use native HTML, CSS, and vanilla JavaScript unless a real need appears.

---

## 14. Safe continuation rules

- Preserve the approved production direction unless the owner/team requests a redesign.
- Keep additions honest about the frontend-only phase.
- Do not invent partnerships, impact metrics, opportunity availability, or student outcomes.
- Treat institutional partners and participant-represented schools as distinct evidence classes.
- Keep opportunity/job-card content secondary to IYOF's organisational story.
- Verify all local paths after moving or renaming assets.
- Run the canonical tests and validator before every release claim.
- Review at normal laptop, wide desktop, and mobile widths after substantial layout changes.

---

## 15. Session starter prompt

> Continue the IYOF production homepage work in `/home/kai/General/work/IYOF/inventyourownfuture/`. Read `2026-08-31_IYOF_Production_Homepage_Handover.md` first. The approved Initiatives-First Platform Hybrid has already replaced the root `index.html` on `feature/homepage-redesign`; dedicated assets are `assets/css/homepage.css` and `assets/js/homepage.js`. Commit `a26544cb4fb12be92b976c81434aaf47467b7118` is pushed to `KelvinLi24/inventyourownfuture`. Tests and validation passed, and an independent review found no remaining security or logic blocker. Do not redesign or add fake backend behavior. First check Git status and the open PR/Pages deployment state, then continue only with the requested delta.

---

**End of handover**
