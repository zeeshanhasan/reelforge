# Design system

**Placeholder.** This file is replaced in spec-02 by a `DESIGN.md` taken from
[getdesign.md](https://getdesign.md/design-md), once Zeeshan picks a design from
the catalogue. Until then the builder proposes two options with a one-line
reason each.

Rules that apply whatever design is picked (spec-00 section 11):

- All tokens live in one plain-CSS file as custom properties: colour (light and
  dark themes), type scale, spacing, radius, shadow, motion. No build step.
- No raw colour codes or pixel values in component or page styles.
- Icons: Lucide only. No mixing sets, no emoji as icons.
- Standard components, each with default, hover, focus, disabled, loading and
  error states: button, input, select, checkbox, card, table, status badge,
  tabs, modal, toast, progress bar, empty state, error state, video preview frame.
- A `/styleguide` page shows every component and state. New components are
  added there first, then used.
- Pages use only these components. A one-off style on a page is a defect.
- Use a catalogue design's style only. Never copy a brand's name, logo or assets.
- This governs the app's own screens. Reels follow Prept's brand in
  `content/brand/`. The two are never mixed.
