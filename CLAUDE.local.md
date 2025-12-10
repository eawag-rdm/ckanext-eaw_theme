# ckanext-eaw_theme - CKAN 2.11 Upgrade

## Current Task

Upgrade this extension from CKAN 2.9 to CKAN 2.11 compatibility.

**Working Branch:** `eric-upgrade-2-11`
**Reference:** eric-open upgrade (`v2.9.10-eric-open` → `v2.11.4-eric-open`)

## Task Documentation

| Document | Purpose |
|----------|---------|
| **`UPGRADE-2.11-TASKS.md`** | Complete upgrade plan, implementation order, testing checklist |
| **`BOOTSTRAP-5-MIGRATION.md`** | Detailed template-by-template Bootstrap 3→5 migration guide |

## Quick Reference

### Critical Changes

1. **Template Relocations** (CKAN 2.11 moved these):
   - `snippets/organization.html` → `organization/snippets/info.html`
   - `user/read_base.html` → `user/snippets/info.html`
2. **plugin.py**: `before_search` → `before_dataset_search`
3. **Templates**: Bootstrap 5 class migrations
4. **Forms**: Add `{{ h.csrf_input() }}` to all POST forms
5. **Homepage**: Delete `layout3.html`, create `index.html`
6. **Removed blocks**: `footer_debug`, `promoted`, `stats`

### View eric-open Changes

```bash
# Full diff
git diff v2.9.10-eric-open v2.11.4-eric-open

# Specific file
git diff v2.9.10-eric-open v2.11.4-eric-open -- <filepath>

# Commit history
git log v2.9.10-eric-open..v2.11.4-eric-open --oneline
```

## ERIC vs eric-open Differences

**Skip these eric-open changes for ERIC:**
- Anubis bot protection text in `dataprotection.html`
- Verify if docs link change in header is appropriate

## Files to Modify

| Priority | File | Change |
|----------|------|--------|
| **CRITICAL** | `snippets/organization.html` | RENAME → `organization/snippets/info.html` |
| **CRITICAL** | `user/read_base.html` | RENAME → `user/snippets/info.html` |
| HIGH | `plugin.py` | `before_search` → `before_dataset_search` |
| HIGH | `header.html` | Major BS5 navbar rewrite |
| HIGH | `footer.html` | Remove `footer_debug` block |
| HIGH | `home/layout3.html` | DELETE |
| HIGH | `home/index.html` | CREATE NEW |
| MEDIUM | `group/member_new.html` | `pull-left` → `float-start`, CSRF |
| MEDIUM | `organization/member_new.html` | `pull-left` → `float-start` |
| MEDIUM | `organization/members.html` | `pull-right`, `btn-default` |
| MEDIUM | `group/index.html` | `col-xs-12` → `col-12` |
| MEDIUM | `assets/css/eaw_theme.css` | Various fixes |
