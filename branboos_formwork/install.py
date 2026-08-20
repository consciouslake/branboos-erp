# -*- coding: utf-8 -*-
"""
Applies BranBoos branding site-wide. Runs on `bench install-app` and every
`bench migrate`, so branding stays applied without a manual click-through
after every deploy.

Assets live in branboos_formwork/public/images/ and are served by Frappe
at /assets/branboos_formwork/images/<file> once the app is installed.
"""

from __future__ import annotations

import frappe

LOGO = "/assets/branboos_formwork/images/logo.png"
FAVICON = "/assets/branboos_formwork/images/favicon.png"
LETTERHEAD_LOGO = "/assets/branboos_formwork/images/letterhead-logo.png"
LETTERHEAD_NAME = "BranBoos"


def after_install():
    _apply_website_settings()
    _apply_letter_head()


def _apply_website_settings():
    settings = frappe.get_single("Website Settings")
    settings.app_logo = LOGO
    settings.banner_image = LOGO
    settings.favicon = FAVICON
    settings.save(ignore_permissions=True)


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
