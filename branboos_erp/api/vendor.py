# -*- coding: utf-8 -*-
"""
API endpoint called by Quarry to read vendor data from Formwork (ERP).

Exposed at: GET /api/method/branboos_erp.api.vendor.list
Auth: standard Frappe API key/secret pair (the FORMWORK_API_TOKEN Quarry
holds is used as the Authorization header when calling this endpoint).

Returns the Vendor shape Quarry's scoring.js expects (vendor design
spec §6): name, city, quote, on_time, quality, disputes, past_projects.
"""

from __future__ import annotations

import frappe


@frappe.whitelist(methods=["GET"])
def list(city: str | None = None):
    """Return active suppliers with the fields Quarry's scoring model needs."""
    filters = {"disabled": 0}
    if city:
        filters["custom_city"] = city

    vendors = frappe.get_all(
        "Supplier",
        filters=filters,
        fields=[
            "supplier_name as name",
            "custom_city as city",
            "custom_current_quote as quote",
            "custom_on_time_rate as on_time",
            "custom_quality_rating as quality",
            "custom_dispute_count as disputes",
            "custom_past_project_count as past_projects",
        ],
    )

    return {"vendors": vendors}
