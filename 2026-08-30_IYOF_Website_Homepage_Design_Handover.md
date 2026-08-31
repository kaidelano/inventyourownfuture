# IYOF Website and Homepage Design Handover

**Date:** 30 August 2026, 21:25 HKT
**Repository:** `/home/kai/General/work/IYOF/inventyourownfuture/`
**Current branch:** `feature/initiatives-page`
**Purpose:** Continue the IYOF public website redesign and eventually prepare a compatible frontend direction for the student app.

---

## 1. Current product direction

IYOF is being developed as two connected products:

1. **Website:** the public face and trust layer for students, parents, schools, partners, and shareholders.
2. **Future app:** a moderated opportunity/network platform for students aged approximately 13–18.

The current work is **frontend only**. No backend, authentication, database, profile storage, messaging, or real application processing should be added yet.

The website should explain the organisation first. Opportunity or job-post functionality should be visible as a future-facing access layer, but it must not make IYOF look like only a job board.

---

## 2. Confirmed visual identity

Use the exact colours extracted from the IYOF logo:

- **Yellow:** `#FDB712`
- **Teal:** `#62C2AC`
- **Pink:** `#F0127A`
- **Purple:** `#6457A4`

Approved visual principles:

- youthful but not childish
- credible to parents, schools, institutional partners, and shareholders
- authentic student photography
- wide layouts that do not become thin when zoomed out
- strong colour blocks used intentionally
- programme and impact content before individual opportunity listings

---

## 3. Initiatives-page work completed

### New page

Created:

- `pages/initiatives.html`

The page presents four initiatives in a responsive card layout:

1. Student Ambassador
2. Events and Camps
3. Internship Opportunities
4. Alumni Network

### Navigation change

**Initiatives** was converted from a dropdown into a normal navigation link across the static site.

Because navigation markup is duplicated in this static export, the change touched `index.html` and all existing files under `pages/`.

### Design refinements completed

- exact IYOF colours applied
- desktop two-column card grid
- mobile single-column layout
- wider content area for large screens
- larger card images, headings, and descriptions
- CTA and footer use the same purple background token
- CTA links to Upcoming and Contact pages

### Initiatives preview links

Local:

- `http://localhost:8080/pages/initiatives.html`

Tailscale:

- `http://100.125.15.37:8080/pages/initiatives.html`
- `http://mini-pc:8080/pages/initiatives.html`

---

## 4. Homepage plan

A detailed homepage implementation plan was created at:

- `.hermes/plans/2026-08-30_181542-homepage-redesign.md`

It covers:

- homepage diagnosis
- proposed section hierarchy
- hero copy and calls to action
- Initiatives integration
- programme and impact storytelling
- secondary opportunity/job-post presentation
- partners, press, schools, advisors, and Career Blog
- responsive layout rules
- implementation sequence
- files likely to change
- acceptance criteria and open decisions

The production homepage has **not** been redesigned yet.

---

## 5. Homepage design sketches

Sketch directory:

- `sketches/homepage-variants/`

Comparison page:

- Local: `http://localhost:8080/sketches/homepage-variants/`
- Tailscale: `http://100.125.15.37:8080/sketches/homepage-variants/`

### Variant 1: Editorial Trust

Files:

- `sketches/homepage-variants/editorial-trust/index.html`
- `sketches/homepage-variants/editorial-trust/README.md`

Direction:

- warm, spacious, photography-led
- strongest for institutional trust
- less app-like

### Variant 2: Opportunity Platform

Files:

- `sketches/homepage-variants/opportunity-platform/index.html`
- `sketches/homepage-variants/opportunity-platform/README.md`

Direction:

- more interactive and app-like
- opportunity filters, save buttons, and job-style cards
- strongest for student engagement
- too platform-heavy if used without organisation/impact context

### Variant 3: Impact Mosaic

Files:

- `sketches/homepage-variants/impact-mosaic/index.html`
- `sketches/homepage-variants/impact-mosaic/README.md`

Direction:

- bold yellow/purple/teal/pink composition
- closest visual expression of the IYOF logo
- programme photography and student outcomes dominate
- strongest for NGO storytelling

### Variant 4: Initiatives-First Platform Hybrid — approved production direction

Files:

- `sketches/homepage-variants/initiatives-platform-hybrid/index.html`
- `sketches/homepage-variants/initiatives-platform-hybrid/README.md`

Preview:

- Local: `http://localhost:8080/sketches/homepage-variants/initiatives-platform-hybrid/index.html`
- Tailscale: `http://100.125.15.37:8080/sketches/homepage-variants/initiatives-platform-hybrid/index.html`

This hybrid combines:

- the platform-style cards and interactions of Variant 2
- the colour-block identity and impact storytelling of Variant 3

Its content priority is intentionally:

1. What IYOF is
2. What IYOF does
3. Four connected initiatives
4. Evidence through real programme stories
5. Secondary opportunity/job-post preview
6. Clear company narrative for shareholders
7. Final call to action

It includes functioning prototype-only filters and save/heart states. These do not connect to any backend.

---

## 6. Approved homepage direction

The owner and team approved the **Initiatives-First Platform Hybrid** as the base direction for the real homepage on 31 August 2026.

Why:

- makes IYOF understandable to shareholders and partners
- keeps the organisation’s programmes and mission central
- shows evidence of delivery through authentic event stories
- introduces job/opportunity-card patterns without reducing IYOF to a jobs board
- visually matches the IYOF logo more closely
- creates a bridge to the future student app

The approved sketch was subsequently refined with a shorter, viewport-aware hero and a two-row education-network marquee: universities and institutional partners above, primary and secondary schools represented by past participants below. The standalone yellow stakeholder/company-story block was removed. Production implementation should follow this direction rather than starting another unrelated design exploration.

---

## 7. Recommended production homepage hierarchy

1. **Hero:** mission, audience, and two primary calls to action
2. **IYOF at a glance:** explain that the organisation is more than an opportunity board
3. **Four initiatives:** the central operating model
4. **IYOF in action:** programme stories and student outcomes
5. **Opportunity preview:** compact job-post-style cards, secondary to the organisation
6. **Trust layer:** partners, schools, press, and advisors
7. **Stakeholder/company story:** how the initiatives and platform fit together
8. **Career content:** selected Career Blog articles
9. **Final CTA and footer**

---

## 8. Event-copy work available

Event drafts are stored separately at:

- `/home/kai/General/work/IYOF/website_event_drafts/`

Important drafts include:

- `2026-08-11_IYOF_Events_Camps_Update_Draft.md`
- `2026-08-11_IYOF_Fintech_Investment_Banking_Event_Draft.md`
- `2026-08-11_IYOF_GBA_Silver_Economy_Study_Delegation_Event_Draft.md`

These provide copy and context for future homepage impact cards and the Events and Camps archive.

Public-content rule:

- do not publish individual student names from internal outcome reports without explicit permission
- use aggregated student outcomes
- compress internal ceremony schedules into public-facing summaries

---

## 9. Verification already performed

### Initiatives page

Earlier focused checks confirmed:

- four initiative cards exist
- direct Initiatives navigation is present across the static pages
- old desktop and mobile dropdown markup is removed
- local images resolve
- responsive mobile fallback exists
- static-site validation passed after correcting a JavaScript false positive in `scripts/check-site.py`

### Homepage sketches

Focused ad-hoc checks confirmed:

- all variants load from the local server
- local images and logo assets resolve
- the hybrid appears correctly at desktop and 390px mobile widths
- the hybrid places initiatives and impact before opportunity cards
- the comparison page links to the hybrid

Do not interpret this as a claim that a canonical project-wide test suite is green. The project has no documented canonical suite command.

---

## 10. Important Git state

The repository currently has **uncommitted changes**.

Current branch:

- `feature/initiatives-page`

Modified/untracked work includes:

- navigation updates across `index.html` and `pages/*.html`
- `pages/initiatives.html`
- Initiatives CSS in `assets/css/static-site.css`
- `scripts/check-site.py`
- `reports/validation.json`
- `tests/`
- `.hermes/plans/`
- `sketches/`
- generated `scripts/__pycache__/`

### Do not immediately overwrite or reset the working tree

Before implementing the real homepage:

1. Review the Initiatives page one final time.
2. Remove generated `scripts/__pycache__/` files.
3. Decide whether the sketches should be committed or retained as design references only.
4. Checkpoint/commit the approved Initiatives work.
5. Create a separate homepage branch such as `feature/homepage-redesign`.
6. Implement the selected hybrid design against the real `index.html`.

No production push should occur without reviewing the final diff.

---

## 11. Open decisions for the next session

1. **Resolved:** the Initiatives-First Hybrid is approved as the production base direction.
2. Which hero headline should be final?
3. Which real photograph should be the primary homepage hero image?
4. Which three programme stories should be featured?
5. Which opportunity/job-style cards can be shown with accurate current details?
6. Which verified impact numbers can be published?
7. Should all advisors be previewed or only selected advisors?
8. Should partner and school logos remain separate or be combined into one trust section?
9. Should the Career Blog remain on the homepage, and if so, how many posts?

---

## 12. Recommended next execution order

1. Review the final compact-hero and school-partnership refinements.
2. Treat the approved hybrid as the production design contract.
3. Clean and checkpoint the Initiatives branch.
4. Create a homepage implementation branch.
5. Implement only the hero and company-at-a-glance sections first.
6. Visually review desktop and mobile.
7. Implement the four Initiatives section.
8. Implement programme-impact stories.
9. Add the smaller opportunity/job-post preview.
10. Add trust, advisor, blog, CTA, and footer sections.
11. Validate references, responsive behaviour, and accessibility.
12. Review the complete diff before commit/push.

---

## 13. Session starter prompt

> We are continuing the IYOF website redesign in `/home/kai/General/work/IYOF/inventyourownfuture/`. Read `2026-08-30_IYOF_Website_Homepage_Design_Handover.md` and `.hermes/plans/2026-08-30_181542-homepage-redesign.md`. The Initiatives landing page and flattened Initiatives navigation are implemented but uncommitted on `feature/initiatives-page`. Four homepage sketches exist under `sketches/homepage-variants/`; the current preferred direction is `initiatives-platform-hybrid`, which places IYOF’s mission, initiatives, and programme impact before a secondary job-post-style opportunity preview. Do not add backend functionality or overwrite the current working tree. First review the hybrid with me and decide the final homepage direction.

---

**End of handover**
