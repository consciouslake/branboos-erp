# -*- coding: utf-8 -*-
# Frappe app hooks for branboos_erp (ERP customizations)
# Docs: https://frappeframework.com/docs/user/en/python-api/hooks

app_name        = "branboos_erp"
app_title       = "Branboos ERP"
app_publisher   = "Branboos"
app_description = "ERP customizations for the Branboos platform"
app_email       = "dev@branboos.com"
app_license     = "MIT"

# ── Branding ──────────────────────────────────────────────────────────────────
# Small logo shown in the desk app-switcher / sidebar for this app.
# Served from branboos_erp/public/images/ at /assets/branboos_erp/...
app_logo_url = "/assets/branboos_erp/images/logo.png"

# Gives this app its own tile on the /apps switcher screen (otherwise it's
# invisible there — only apps listed here get a tile), pointing at our
# branded Workspace (see branboos_erp/workspace/branboos/branboos.json).
add_to_apps_screen = [
    {
        "name": "branboos_erp",
        "logo": app_logo_url,
        "title": "ERP",
        "route": "/app/erp",
        "has_permission": "frappe.permissions.check_app_permission",
    }
]

# ── DocType JS overrides ────────────────────────────────────────────────────
# doctype_js = {
#   "Supplier": "public/js/supplier.js",
# }

# ── Scheduled tasks ──────────────────────────────────────────────────────────
# scheduler_events = {
#   "daily": [
#     "branboos_erp.tasks.daily",
#   ],
# }

# ── Install / migrate hooks ──────────────────────────────────────────────────
# Applies site-wide branding (navbar logo, favicon, login page, and the
# default Letter Head used on Purchase Orders / invoices) automatically.
after_install = "branboos_erp.install.after_install"
after_migrate = "branboos_erp.install.after_install"

# ── Custom field fixtures ────────────────────────────────────────────────────
# Commit custom fields to version control via fixtures so they deploy cleanly:
fixtures = [
    {"dt": "Custom Field", "filters": [["module", "=", "Branboos ERP"]]},
]
