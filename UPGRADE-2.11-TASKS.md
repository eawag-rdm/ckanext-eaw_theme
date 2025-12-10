# ckanext-eaw_theme CKAN 2.11 Upgrade Tasks

This document outlines all changes required to upgrade ckanext-eaw_theme from CKAN 2.9 to CKAN 2.11, based on the successful eric-open upgrade.

**Reference:** `git diff v2.9.10-eric-open v2.11.4-eric-open`

## Summary of Changes

| Category | Files Affected | Priority |
|----------|---------------|----------|
| Plugin Interface | `plugin.py` | HIGH |
| Bootstrap 5 Migration | Templates, CSS | HIGH |
| Template Updates | 15+ template files | HIGH |
| CSS Updates | `eaw_theme.css` | MEDIUM |
| CI/Workflow | `.github/workflows/test.yml` | LOW |
| Dependencies | `dev-requirements.txt` | LOW |

---

## 1. Plugin Interface Changes (HIGH PRIORITY)

### File: `ckanext/eaw_theme/plugin.py`

#### 1.1 Rename `before_search` to `before_dataset_search`

**Why:** CKAN 2.11 renamed the IPackageController interface method.

```python
# OLD (CKAN 2.9)
def before_search(self, search_params):

# NEW (CKAN 2.11)
def before_dataset_search(self, search_params):
```

**Commit Reference:** `20be31f change before_search to before_dataset_search`

---

## 2. Template Changes (HIGH PRIORITY)

### 2.1 Bootstrap 5 Class Migrations

CKAN 2.11 uses Bootstrap 5 instead of Bootstrap 3. The following class changes are required:

| Bootstrap 3 | Bootstrap 5 | Files Affected |
|-------------|-------------|----------------|
| `col-xs-*` | `col-*` | `group/index.html`, `disclaimer/disclaimer.html` |
| `col-sm-*` | `col-sm-*` or `col-md-*` | Various |
| `navbar-toggle` | `navbar-toggler` | `header.html` |
| `data-toggle` | `data-bs-toggle` | `header.html` |
| `data-target` | `data-bs-target` | `header.html` |
| `sr-only` | `visually-hidden` | `header.html` |
| `navbar-left` | (use flexbox) | `header.html` |
| `navbar-right` | `ms-auto` | `header.html` |
| `media` | `d-flex` / `row` | `home/snippets/about_text.html` |
| `media-left` | `col-auto` / `me-3` | `home/snippets/about_text.html` |
| `media-body` | `col` | `home/snippets/about_text.html` |
| `media-heading` | (use standard headings) | `home/snippets/about_text.html` |
| `media-object` | (removed) | `home/snippets/about_text.html` |
| `img-rounded` | `rounded` | Various |
| `jumbotron` | Custom class (removed in BS5) | `about_text.html`, CSS |
| `pull-left`/`pull-right` | `float-start`/`float-end` | Various |
| `text-left`/`text-right` | `text-start`/`text-end` | Various |

### 2.2 Header Template (`templates/header.html`)

**Major rewrite required.** Key changes:

1. Replace `<hgroup>` with `<div>` (HTML5 deprecated hgroup)
2. Update navbar structure for Bootstrap 5
3. Change `data-toggle="collapse"` → `data-bs-toggle="collapse"`
4. Change `data-target` → `data-bs-target`
5. Update navigation helper syntax:
   ```jinja2
   # OLD
   {{ h.build_nav_main(('dataset.search', _('Datasets')), ...) }}

   # NEW (with entity type humanization)
   {% set dataset_type = h.default_package_type() %}
   {{ h.build_nav_main((dataset_type ~ '.search', h.humanize_entity_type('package', dataset_type, 'main nav') or _('Datasets'), ["dataset", "resource"]), ...) }}
   ```
6. Replace debug block variables:
   - `c.controller` → `g.blueprint`
   - `c.action` → `g.view`

**Commit Reference:** `54fba63 Bootstrap 3 -> Bootstrap 5`, `9822848 updates to formatting and Bootstrap 3 to Bootstrap 5`

### 2.3 Footer Template (`templates/footer.html`)

Remove deprecated debug block:
```jinja2
# REMOVE this entire block
{% block footer_debug %}
    {% if g.debug %}
        {% include 'snippets/debug.html' %}
    {% endif %}
{% endblock %}
```

**Commit Reference:** `33b403e remove deprecated debug insert`

### 2.4 Homepage Templates

#### Delete: `templates/home/layout3.html`
**Why:** `ckan.homepage_style` config removed in CKAN 2.11. Only one layout available.

**Commit Reference:** `c9673a5 removing unused deprecated variable`

#### Create: `templates/home/index.html`
Replace layout system with direct index.html override:

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

**Commit Reference:** `140a6e7 incoorporating layout in index`

### 2.5 About Text Template (`templates/home/snippets/about_text.html`)

Complete Bootstrap 5 rewrite required:
- Replace all `media` classes with flexbox (`d-flex`, `row`, `col`)
- Replace `jumbotron` with custom styling (`bg-info bg-opacity-25 rounded p-5 mb-4`)
- Replace `page-header` with custom styling
- Update icon containers

### 2.6 Disclaimer Templates

#### `templates/disclaimer/disclaimer.html`
```jinja2
# OLD
<div class="primary col-sm-11 col-xs-12">

# NEW
<div class="primary col-12 col-md-11 mx-auto">
```

#### Snippet files - Add Bootstrap 5 spacing classes:
- `copyright.html`: Add `mb-3`, `mb-4` classes to headings
- `dataprotection.html`: Add `mb-3`, `mt-4` classes, update content structure
- `legal_notice.html`: Add `mb-3` class
- `liability.html`: Add `mb-3`, `mt-4` classes

### 2.7 Group/Organization Templates

#### `templates/group/index.html`
```jinja2
# OLD
<div class="col-xs-12">

# NEW
<div class="col-12">
```

#### `templates/group/member_new.html` & `templates/organization/member_new.html`
- Add `{{ h.csrf_input() }}` (CSRF protection required in CKAN 2.11)
- Update form structure for Bootstrap 5
- Change `class="controls"` wrapper structure

### 2.8 CSRF Token Addition

**All forms must include CSRF protection:**
```jinja2
<form method="post">
    {{ h.csrf_input() }}
    <!-- form fields -->
</form>
```

Affected files:
- `templates/group/member_new.html`
- `templates/organization/member_new.html`

---

## 3. CSS Changes (MEDIUM PRIORITY)

### File: `ckanext/eaw_theme/assets/css/eaw_theme.css`

#### 3.1 Add footer text color
```css
.site-footer {
  color: #CCDEE3;
}
```

#### 3.2 Update homepage background height
```css
div.homepage.layout-3 {
  background: url("../../images/airbubbles.jpg");
  background-size: 100%;
  min-height: 80vh;  /* ADD THIS */
}
```

#### 3.3 Fix search form spacing
```css
.search-form {
    clear: both;
    /* margin-bottom: -30px; */  /* REMOVE */
    margin-bottom: 0px;           /* ADD */
    padding-bottom: 25px;         /* ADD */
    border-bottom: 0px;           /* ADD */
}
```

#### 3.4 Replace deprecated jumbotron class
```css
/* OLD */
article.module div.jumbotron {
  background-color: #AED6E3 !important;
}

/* NEW */
article.module div.eaw-color {
  background-color: #AED6E3 !important;
}
```

#### 3.5 Remove deprecated nav-pills styling
```css
/* REMOVE these rules (Bootstrap 5 doesn't use this pattern) */
.nav-pills > li > a.upstream_link { ... }
.nav-pills > li > a.upstream_link::after { ... }
```

#### 3.6 Update homepage search tags styling
```css
.homepage .module-search .tags {
    padding: 0px 10px 10px 10px;  /* Changed from 5px */
    background-color: #005d7a;    /* Removed extra semicolon */
    ...
    margin-top: -10px;            /* ADD */
}
```

#### 3.7 Add search form padding
```css
/* ADD */
.homepage .module-search .search-form {
  padding: 15px 20px;
}
```

#### 3.8 Add Markdown view styling fixes
```css
/* ADD - Markdown view styling fixes */
#markdown_content {
    background-color: #fff !important;
    padding: 20px !important;
    border-radius: 3px !important;
    min-height: 100vh !important;
    margin: 0 !important;
}

body.resource.view {
    background: #fff !important;
}

body.resource.view .main {
    background: #fff !important;
}
```

---

## 4. CI/Workflow Updates (LOW PRIORITY)

### File: `.github/workflows/test.yml`

Update to:
- Target CKAN 2.11
- Use solr9
- Use actions/checkout@v4

---

## 5. Dependencies (LOW PRIORITY)

### File: `dev-requirements.txt`

Update PyYAML version constraint if present.

**Commit Reference:** `0b70967 upgrading pyyaml dependecy`

---

## 6. Public Files

### File: `ckanext/eaw_theme/public/robots.txt`

Update for new CKAN 2.11 routes if necessary.

**Commit Reference:** `c52aa7a adjusted robots.txt to new ckan version`

---

## ERIC-Specific Considerations

The eric-open upgrade included some changes that are **NOT needed for ERIC**:

1. **Anubis bot protection** - The dataprotection.html was updated to mention Anubis. ERIC does not use Anubis, so keep the original privacy policy text.

2. **Docs link** - eric-open changed the header navigation to link to `/docs/intro.html`. Verify if ERIC needs this or should keep the RDM Project link.

---

## Implementation Order

1. **plugin.py** - Rename `before_search` → `before_dataset_search`
2. **header.html** - Bootstrap 5 navbar migration
3. **footer.html** - Remove deprecated debug block
4. **home/index.html** - Create new file, delete layout3.html
5. **CSS updates** - All eaw_theme.css changes
6. **Disclaimer templates** - Bootstrap 5 classes
7. **Group/Organization templates** - CSRF + Bootstrap 5
8. **about_text.html** - Full Bootstrap 5 rewrite
9. **CI/Dependencies** - Update workflow and requirements

---

## Testing Checklist

- [ ] Homepage renders correctly with background image
- [ ] Navigation menu works (desktop and mobile)
- [ ] Search functionality works
- [ ] Dataset/Organization/Group pages render
- [ ] Member management forms work (CSRF)
- [ ] Disclaimer pages render with proper spacing
- [ ] About page FAIR icons display correctly
- [ ] Footer displays correctly
- [ ] No JavaScript console errors
- [ ] Mobile responsive layout works
