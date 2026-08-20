# -*- coding: utf-8 -*-
"""
Applies BranBoos branding site-wide. Runs on `bench install-app` and every
`bench migrate`, so branding stays applied without a manual click-through
after every deploy.

Assets live in branboos_erp/public/images/ and are served by Frappe
at /assets/branboos_erp/images/<file> once the app is installed.
"""

from __future__ import annotations

import frappe

LOGO = "/assets/branboos_erp/images/logo.png"
FAVICON = "/assets/branboos_erp/images/favicon.png"
LETTERHEAD_LOGO = "/assets/branboos_erp/images/letterhead-logo.png"
LETTERHEAD_NAME = "BranBoos"
DEFAULT_WORKSPACE = "ERP"


def after_install():
    _apply_website_settings()
    _apply_navbar_settings()
    _set_default_workspace()
    _apply_letter_head()


def _apply_website_settings():
    settings = frappe.get_single("Website Settings")
    settings.app_logo = LOGO
    settings.banner_image = LOGO
    settings.favicon = FAVICON
    settings.save(ignore_permissions=True)


def _apply_navbar_settings():
    """Website Settings.app_logo covers the public site; the desk's own
    top-left logo (next to the app switcher) is a separate setting."""
    navbar = frappe.get_single("Navbar Settings")
    navbar.app_logo = LOGO
    navbar.save(ignore_permissions=True)


def _set_default_workspace():
    """Land on our own branded Workspace (see workspace/branboos/branboos.json)
    instead of the generic app home screen after login."""
    if not frappe.db.exists("Workspace", DEFAULT_WORKSPACE):
        return
    for user in frappe.get_all("User", filters={"user_type": "System User"}, pluck="name"):
        frappe.db.set_value("User", user, "default_workspace", DEFAULT_WORKSPACE)


def _apply_letter_head():
    """Create (or update) the default Letter Head used on POs / invoices."""
    if frappe.db.exists("Letter Head", LETTERHEAD_NAME):
        letter_head = frappe.get_doc("Letter Head", LETTERHEAD_NAME)
    else:
        letter_head = frappe.new_doc("Letter Head")
        letter_head.letter_head_name = LETTERHEAD_NAME

    letter_head.source = "Image"
    letter_head.image = LETTERHEAD_LOGO
    letter_head.is_default = 1
    letter_head.save(ignore_permissions=True)
