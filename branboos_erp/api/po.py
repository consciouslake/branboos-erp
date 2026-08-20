# -*- coding: utf-8 -*-
"""
API endpoint called by Quarry to write a Purchase Order once a
procurement decision from a Quarry recommendation is approved.

Exposed at: POST /api/method/branboos_erp.api.po.create
Auth: standard Frappe API key/secret pair (FORMWORK_API_TOKEN).
"""

from __future__ import annotations

import frappe
from frappe import _


@frappe.whitelist(methods=["POST"])
def create(supplier: str, items: list, schedule_date: str | None = None):
    """
    Create a draft Purchase Order for the given supplier and items.

    Left as a draft (not submitted) — approval remains a human step
    inside ERPNext, this endpoint only stages the PO.
    """
    if not supplier:
        frappe.throw(_("supplier is required"))
    if not items:
        frappe.throw(_("items is required and must be a non-empty list"))

    po = frappe.get_doc(
        {
            "doctype": "Purchase Order",
            "supplier": supplier,
            "schedule_date": schedule_date,
            "items": items,
        }
    )
    po.insert(ignore_permissions=True)

    return {"name": po.name, "status": po.status}
