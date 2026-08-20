# branboos_formwork

> Custom Frappe app for **Branboos ERP customizations**.

## Install

```bash
# From inside your bench directory:
bench get-app https://github.com/branboos/branboos-formwork
bench install-app branboos_formwork
```

## What's in here

| Path | Purpose |
|---|---|
| `branboos_formwork/` | Python app package |
| `branboos_formwork/hooks.py` | Frappe app hooks (DocType events, scheduled tasks) |
| `branboos_formwork/custom/` | Custom field definitions & property setters |
| `branboos_formwork/overrides/` | Controller overrides for standard ERP DocTypes |

## Structure note

This is intentionally **separate from `branboos-structura`** and **`branboos-groundwork`** because Frappe's `bench get-app` clones a git URL directly — CRM and ERP apps are separate Frappe apps that may be installed independently.

## Related repos

- [`branboos-structura`](https://github.com/branboos/branboos-structura) — Backend services monorepo
- [`branboos-groundwork`](https://github.com/branboos/branboos-groundwork) — CRM customization Frappe app
