# Bootstrap 3 → Bootstrap 5 Migration Guide for ckanext-eaw_theme

This document provides a detailed template-by-template guide for migrating from Bootstrap 3 to Bootstrap 5.

---

## CRITICAL: Template Relocations in CKAN 2.11

CKAN 2.11 relocated several template files. Extensions overriding these must update paths:

| Old Path (CKAN 2.9) | New Path (CKAN 2.11) | Notes |
|---------------------|----------------------|-------|
| `snippets/organization.html` | `organization/snippets/info.html` | Consistency with other entities |
| `user/read_base.html` | `user/snippets/info.html` | User info snippet relocated |

### Required File Operations:

1. **RENAME** `templates/snippets/organization.html` → `templates/organization/snippets/info.html`
2. **RENAME** `templates/user/read_base.html` → `templates/user/snippets/info.html`

---

## Removed Template Configuration Options

These config options no longer work in CKAN 2.11:

| Removed Config | Alternative |
|----------------|-------------|
| `ckan.homepage_style` | Override `home/index.html` template |
| `template_head_end` | Extend `base.html` template |
| `template_footer_end` | Extend `base.html` template |
| `ckan.main_css` | Use `ckan.theme` (webassets) |
| `ckan.i18n.rtl_css` | Use `ckan.i18n.rtl_theme` (webassets) |

---

## Removed/Changed Template Blocks

| Block | Status | Alternative |
|-------|--------|-------------|
| `footer_debug` | REMOVED | Delete block override |
| `promoted` | REMOVED from homepage | Use custom `home/index.html` |
| `stats` | REMOVED from homepage | Use custom `home/index.html` |
| `header_extra` | RESTORED in 2.11.4 | Safe to use |
| `body_extra` | RESTORED in 2.11.4 | Safe to use |

---

## Quick Reference: Class Changes

| Bootstrap 3 | Bootstrap 5 | Notes |
|-------------|-------------|-------|
| `col-xs-*` | `col-*` | xs breakpoint removed |
| `col-sm-*` | `col-sm-*` | Same |
| `col-md-*` | `col-md-*` | Same |
| `col-lg-*` | `col-lg-*` | Same |
| `col-xl-*` | `col-xl-*` | New in BS4+ |
| `pull-left` | `float-start` | RTL support |
| `pull-right` | `float-end` | RTL support |
| `text-left` | `text-start` | RTL support |
| `text-right` | `text-end` | RTL support |
| `sr-only` | `visually-hidden` | Screen reader |
| `btn-default` | `btn-light` or `btn-secondary` | |
| `img-responsive` | `img-fluid` | |
| `img-rounded` | `rounded` | |
| `img-circle` | `rounded-circle` | |
| `navbar-toggle` | `navbar-toggler` | |
| `navbar-right` | `ms-auto` | Use flexbox |
| `navbar-left` | `me-auto` | Use flexbox |
| `navbar-form` | `d-flex` | Use flexbox |
| `navbar-fixed-top` | `fixed-top` | |
| `navbar-static-top` | (removed) | Use sticky-top or custom |
| `data-toggle` | `data-bs-toggle` | All data attrs |
| `data-target` | `data-bs-target` | All data attrs |
| `data-dismiss` | `data-bs-dismiss` | All data attrs |
| `media` | `d-flex` | Use flexbox |
| `media-left` | `flex-shrink-0` / `me-3` | |
| `media-body` | `flex-grow-1` | |
| `media-heading` | (removed) | Use standard headings |
| `jumbotron` | (removed) | Use custom classes |
| `page-header` | (removed) | Use custom classes |
| `well` | `card` or custom | |
| `panel` | `card` | |
| `panel-heading` | `card-header` | |
| `panel-body` | `card-body` | |
| `label` (badge) | `badge` | |
| `badge` | `badge rounded-pill` | For pill shape |
| `list-inline > li` | `list-inline-item` | |
| `table-condensed` | `table-sm` | |
| `table-responsive` | Wrapper div needed | |
| `form-horizontal` | `row` + `col-*` | |
| `form-group` | `mb-3` | Margin bottom |
| `control-label` | `form-label` | |
| `form-control-static` | `form-control-plaintext` | |
| `input-lg` | `form-control-lg` | |
| `input-sm` | `form-control-sm` | |
| `help-block` | `form-text` | |
| `has-error` | `is-invalid` | |
| `has-success` | `is-valid` | |
| `hidden-xs` | `d-none d-sm-block` | |
| `hidden-sm` | `d-sm-none d-md-block` | |
| `visible-xs` | `d-block d-sm-none` | |
| `center-block` | `mx-auto d-block` | |
| `close` | `btn-close` | |
| `caret` | (removed) | Use CSS or icon |

---

## Template-by-Template Analysis

### 1. `templates/header.html` - HIGH PRIORITY

**Current Issues:**
- Uses `navbar-static-top` (removed in BS5)
- Uses `navbar-toggle` (→ `navbar-toggler`)
- Uses `data-toggle` and `data-target` (→ `data-bs-toggle`, `data-bs-target`)
- Uses `sr-only` (→ `visually-hidden`)
- Uses `navbar-right` / `navbar-left` (→ flexbox)
- Uses `hgroup` element (deprecated HTML5)
- Uses `nav-pills` (still valid but structure changed)
- Uses `c.controller` / `c.action` debug vars (→ `g.blueprint` / `g.view`)

**Required Changes:**

```html
<!-- OLD -->
<header class="navbar navbar-static-top masthead">

<!-- NEW -->
<header class="masthead">
```

```html
<!-- OLD -->
<div class="navbar-right">
    <button data-target="#main-navigation-toggle"
            data-toggle="collapse"
            class="navbar-toggle collapsed"
            type="button">
        <span class="sr-only">{{ _("Toggle navigation") }}</span>
        <span class="fa fa-bars"></span>
    </button>
</div>

<!-- NEW -->
<button class="navbar-toggler"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#main-navigation-toggle"
        aria-controls="main-navigation-toggle"
        aria-expanded="false"
        aria-label="{{ _("Toggle navigation") }}">
    <span class="fa fa-bars text-white"></span>
</button>
```

```html
<!-- OLD -->
<hgroup class="{{ g.header_class }} navbar-left">

<!-- NEW -->
<div class="{{ g.header_class }} navbar-left">
```

```html
<!-- OLD -->
<div class="collapse navbar-collapse" id="main-navigation-toggle">
    <nav class="section navigation">
        <ul class="nav nav-pills">

<!-- NEW -->
<div class="main-navbar collapse navbar-collapse" id="main-navigation-toggle">
    <ul class="navbar-nav ms-auto mb-2 mb-lg-0">
```

```html
<!-- OLD (debug block) -->
Controller : {{ c.controller }}
Action : {{ c.action }}

<!-- NEW -->
Blueprint : {{ g.blueprint }}
View : {{ g.view }}
```

**Navigation Helper Update:**
```jinja2
{# OLD #}
{{ h.build_nav_main(('dataset.search', _('Datasets')),
('organization.index', _('Organizations')),
('group.index', _('Groups')),
('home.about', _('About'))) }}

{# NEW #}
{% set dataset_type = h.default_package_type() %}
{% set org_type = h.default_group_type('organization') %}
{% set group_type = h.default_group_type('group') %}
{{ h.build_nav_main(
    (dataset_type ~ '.search', h.humanize_entity_type('package', dataset_type, 'main nav') or _('Datasets'), ["dataset", "resource"]),
    (org_type ~ '.index', h.humanize_entity_type('organization', org_type, 'main nav') or _('Organizations'), ['organization']),
    (group_type ~ '.index', h.humanize_entity_type('group', group_type, 'main nav') or _('Groups'), ['group']),
    ('home.about', _('About'))
) }}
```

---

### 2. `templates/footer.html` - LOW PRIORITY

**File does not exist in current branch** (check if inherited from CKAN core)

**If creating/overriding:**
- Remove `{% block footer_debug %}` block (deprecated)

---

### 3. `templates/home/layout3.html` - DELETE THIS FILE

**Why:** CKAN 2.11 removed `ckan.homepage_style` config. Only one layout available.

**Action:** Delete this file and create `templates/home/index.html` instead.

---

### 4. `templates/home/index.html` - CREATE NEW FILE

```jinja2
{% extends "page.html" %}
{% block subtitle %}{{ _("Welcome") }}{% endblock %}
{% block maintag %}{% endblock %}
{% block toolbar %}{% endblock %}
{% block content %}
    <div class="homepage layout-3">
        <div id="content" class="container">{{ self.flash() }}</div>
        {% block primary_content %}
            <div role="main" class="hero">
                <div class="container">
                    {% block search %}
                        {% snippet 'home/snippets/search.html' %}
                    {% endblock %}
                </div>
            </div>
        {% endblock %}
    </div>
{% endblock %}
```

---

### 5. `templates/home/about.html` - NO CHANGES NEEDED

This template uses `{% ckan_extends %}` and only overrides content blocks. No Bootstrap classes present.

---

### 6. `templates/home/snippets/about_text.html` - MEDIUM PRIORITY

**Current Issues:**
- Uses inline styles (not BS related but could be improved)
- Uses `fa-external-link-square` (check FA6 compatibility)

**Changes Needed:**
- FontAwesome icon check: `fa-external-link-square` → `fa-arrow-up-right-from-square` (FA6) or keep for FA5 compatibility
- No Bootstrap class issues found

**Optional Improvements:**
```html
<!-- Consider replacing inline styles with Bootstrap utility classes -->
<!-- OLD -->
<div style="border:1px; border-style:solid; padding:5px 30px 5px 30px; ...">

<!-- NEW (optional) -->
<div class="border p-4 shadow bg-warning my-4">
```

---

### 7. `templates/group/member_new.html` - MEDIUM PRIORITY

**Current Issues:**
- Uses `pull-left` (→ `float-start`)
- CSRF input uses conditional: `{{ h.csrf_input() if 'csrf_input' in h }}`

**Required Changes:**

```html
<!-- OLD -->
<a href="..." class="btn btn-danger pull-left" ...>

<!-- NEW -->
<a href="..." class="btn btn-danger float-start" ...>
```

```jinja2
{# OLD #}
{{ h.csrf_input() if 'csrf_input' in h }}

{# NEW - unconditional in CKAN 2.11 #}
{{ h.csrf_input() }}
```

**Form structure update (optional but recommended):**
```html
<!-- OLD -->
<div class="controls">

<!-- NEW -->
<div class="form-group">
```

---

### 8. `templates/group/snippets/helper.html` - NO CHANGES NEEDED

Uses standard HTML. No Bootstrap-specific classes.

---

### 9. `templates/organization/member_new.html` - MEDIUM PRIORITY

**Current Issues:**
- Uses `pull-left` (→ `float-start`)
- Already has unconditional `{{ h.csrf_input() }}` ✓

**Required Changes:**

```html
<!-- OLD -->
<a href="..." class="btn btn-danger pull-left" ...>

<!-- NEW -->
<a href="..." class="btn btn-danger float-start" ...>
```

---

### 10. `templates/organization/members.html` - MEDIUM PRIORITY

**Current Issues:**
- Uses `pull-right` (→ `float-end`)
- Uses `btn-default` (→ `btn-light` or `btn-secondary`)
- Uses `media` class on `<td>` (unusual usage)

**Required Changes:**

```html
<!-- OLD -->
<div class="btn-group pull-right">
    <a class="btn btn-default btn-sm" ...>

<!-- NEW -->
<div class="btn-group float-end">
    <a class="btn btn-secondary btn-sm" ...>
```

```html
<!-- OLD -->
<td class="media">

<!-- NEW - media class on td is unusual, consider: -->
<td class="d-flex align-items-center">
<!-- OR just remove the class if not needed -->
<td>
```

---

### 11. `templates/organization/read.html` - NO CHANGES NEEDED

Uses `{% ckan_extends %}` and only adds content. No Bootstrap classes.

---

### 12. `templates/organization/new_organization_form.html` - NO CHANGES NEEDED

Only removes a block. No Bootstrap classes.

---

### 13. `templates/organization/snippets/helper.html` - NO CHANGES NEEDED

Same as group helper. Standard HTML, no Bootstrap classes.

---

### 14. `templates/package/base_form_page.html` - NO CHANGES NEEDED

Uses `{% ckan_extends %}` and `module-*` classes (CKAN-specific, not Bootstrap).

---

### 15. `templates/package/read.html` - NO CHANGES NEEDED

Uses `{% ckan_extends %}` and includes a snippet. No Bootstrap classes.

---

### 16. `templates/package/search.html` - NO CHANGES NEEDED

Uses `{% ckan_extends %}` and `{{ super() }}`. No Bootstrap classes.

---

### 17. `templates/package/snippets/resource_item.html` - NO CHANGES NEEDED

Uses `{% ckan_extends %}` and custom classes. No Bootstrap classes.

---

### 18. `templates/package/snippets/package_form.html` - NO CHANGES NEEDED

Only removes a block. No Bootstrap classes.

---

### 19. `templates/scheming/display_snippets/repeating_text.html` - NO CHANGES NEEDED

Standard `<ol>` list. No Bootstrap classes.

---

### 20. `templates/scheming/form_snippets/repeating_text.html` - LOW PRIORITY

**Current Issues:**
- Uses `control-medium` class (CKAN-specific, check if still valid)

**No Bootstrap changes needed**, but verify `control-medium` works in CKAN 2.11.

---

### 21. `templates/snippets/organization.html` - NO CHANGES NEEDED

Uses `{% ckan_extends %}` only. No content changes.

---

### 22. `templates/snippets/package_item.html` - NO CHANGES NEEDED

Uses `{% ckan_extends %}` only. No content changes.

---

### 23. `templates/user/dashboard.html` - NO CHANGES NEEDED

Uses `{% ckan_extends %}` and `{{ super() }}`. No Bootstrap classes.

---

### 24. `templates/user/list.html` - NO CHANGES NEEDED

Uses `{% ckan_extends %}` and only overrides content. No Bootstrap classes.

---

### 25. `templates/user/login.html` - NO CHANGES NEEDED

Uses `{% ckan_extends %}` and CKAN module classes only. No Bootstrap classes.

---

### 26. `templates/user/read_base.html` - NO CHANGES NEEDED

Uses `{% ckan_extends %}` and standard HTML. No Bootstrap classes.

---

### 27. `templates/base.html` - NO CHANGES NEEDED

Uses `{% ckan_extends %}` and asset loading. No Bootstrap classes.

---

## Summary: Files Requiring Changes

| Priority | File | Changes Needed |
|----------|------|----------------|
| **CRITICAL** | `snippets/organization.html` | RENAME → `organization/snippets/info.html` |
| **CRITICAL** | `user/read_base.html` | RENAME → `user/snippets/info.html` |
| HIGH | `header.html` | Major rewrite for BS5 navbar |
| HIGH | `home/layout3.html` | DELETE |
| HIGH | `home/index.html` | CREATE NEW |
| HIGH | `footer.html` | Remove `footer_debug` block |
| MEDIUM | `group/member_new.html` | `pull-left` → `float-start`, CSRF unconditional |
| MEDIUM | `organization/member_new.html` | `pull-left` → `float-start` |
| MEDIUM | `organization/members.html` | `pull-right` → `float-end`, `btn-default` → `btn-secondary` |
| MEDIUM | `group/index.html` | `col-xs-12` → `col-12` |
| MEDIUM | `organization/index.html` | `col-xs-12` → `col-12` (check if exists) |
| NONE | Other templates | No changes needed |

---

## CSS File Changes (`assets/css/eaw_theme.css`)

In addition to template changes, update the CSS file:

### Remove deprecated selectors:
```css
/* REMOVE - nav-pills pattern changed */
.nav-pills > li > a.upstream_link { ... }
.nav-pills > li > a.upstream_link::after { ... }
```

### Replace jumbotron references:
```css
/* OLD */
article.module div.jumbotron { ... }

/* NEW */
article.module div.eaw-color { ... }
```

### Add Bootstrap 5 compatible styles:
```css
/* Footer text color (BS5 footer styling different) */
.site-footer {
    color: #CCDEE3;
}

/* Markdown view fixes */
#markdown_content {
    background-color: #fff !important;
    padding: 20px !important;
}
```

---

## Testing Checklist

After making changes, test:

- [ ] **Navigation**
  - [ ] Desktop menu displays correctly
  - [ ] Mobile hamburger menu works
  - [ ] Menu items link correctly
  - [ ] Active state highlights correctly

- [ ] **Homepage**
  - [ ] Background image displays
  - [ ] Search box works
  - [ ] Layout is correct

- [ ] **Forms**
  - [ ] Member add forms work
  - [ ] CSRF tokens present
  - [ ] Form validation displays

- [ ] **Tables**
  - [ ] Members table displays correctly
  - [ ] Button groups align properly

- [ ] **Responsive**
  - [ ] Test at mobile breakpoint
  - [ ] Test at tablet breakpoint
  - [ ] Test at desktop breakpoint

- [ ] **Buttons**
  - [ ] All buttons visible and styled
  - [ ] Hover/active states work

---

## FontAwesome Notes

CKAN 2.11 uses FontAwesome 6. Some icon names changed:

| FA4/5 | FA6 | Notes |
|-------|-----|-------|
| `fa-external-link-square` | `fa-arrow-up-right-from-square` | Or use `fa-up-right-from-square` |
| `fa-sign-out` | `fa-right-from-bracket` | |
| `fa-sign-in` | `fa-right-to-bracket` | |
| `fa-gavel` | `fa-gavel` | Same |
| `fa-tachometer` | `fa-gauge` | |
| `fa-cog` | `fa-gear` | |
| `fa-wrench` | `fa-wrench` | Same |
| `fa-times` | `fa-xmark` | |
| `fa-bars` | `fa-bars` | Same |
| `fa-search` | `fa-magnifying-glass` | |
| `fa-plus-square` | `fa-square-plus` | |
| `fa-info-circle` | `fa-circle-info` | |

**Note:** FontAwesome 6 has compatibility shims, so old names may still work. Test to confirm.
