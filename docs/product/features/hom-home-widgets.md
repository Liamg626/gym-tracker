# HOM: Home screen and widgets

The home screen works like an iOS home screen made of widgets.

## Rules

- Widgets are self-contained components from day one; customisation is a layout layer on top.
- A 4-column grid on the phone; a wider grid on the dashboard. Each device class has **its own layout**, saved to the API.
- Fixed sizes: small 1×1, wide 2×1, large 2×2, full-width 4×2. Each widget declares which sizes it supports.
- Long-press enters edit mode: drag to move, change size, add from the catalogue, remove.

## Widget catalogue

| Widget | Release |
|---|---|
| Start Workout (pick a Routine or start empty); phone only | MVP |
| Recovery Map | MVP |
| Quick Weigh-in | MVP |
| This week (Workouts vs Weekly Target) | MVP |
| Last Workout | MVP |
| Latest Body Fat Estimate | MVP |
| Weight and Body Fat chart: Trend Weight (left axis) and Body Fat Estimate (right axis) over time, with This week / 1 month / 3 months / All time | MVP |
| Trend Weight sparkline | v1.1 |
| Next Milestone | v1.1 |
| Recent PRs | v1.1 |
| Weekly Breakdown snapshot | v1.2 |
| Volume per Muscle | v1.2 |

## Stories

**HOM: Widget framework and fixed default layout** (MVP)
- Widget registry (id, component, supported sizes); the home screen renders a hard-coded default layout for phone and for desktop

**HOM: MVP widgets** (MVP): one story per widget, or grouped when they're small

**HOM: Edit mode: move and resize** (v1.1)

**HOM: Add/remove widgets from the catalogue** (v1.1)

**HOM: Save layouts per device class to the API** (v1.1)
