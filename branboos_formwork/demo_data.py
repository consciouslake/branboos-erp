# -*- coding: utf-8 -*-
"""
Seeds sample Suppliers for local development / demos.
Run with: bench --site <site> execute branboos_formwork.demo_data.run
"""

from __future__ import annotations

import frappe

SUPPLIERS = [
    {
        "supplier_name": "Karnataka RMC Solutions",
        "custom_city": "Bangalore",
        "custom_current_quote": 6150,
        "custom_on_time_rate": 96,
        "custom_quality_rating": 4.5,
        "custom_dispute_count": 0,
        "custom_past_project_count": 20,
    },
    {
        "supplier_name": "Vajra Readymix",
        "custom_city": "Bangalore",
        "custom_current_quote": 5800,
        "custom_on_time_rate": 65,
        "custom_quality_rating": 3.0,
        "custom_dispute_count": 5,
        "custom_past_project_count": 8,
    },
    {
        "supplier_name": "Chennai Steel Traders",
        "custom_city": "Chennai",
        "custom_current_quote": 48500,
        "custom_on_time_rate": 88,
        "custom_quality_rating": 4.0,
        "custom_dispute_count": 1,
        "custom_past_project_count": 34,
    },
    {
        "supplier_name": "Anantapur Aggregates Co.",
        "custom_city": "Anantapur",
        "custom_current_quote": 1450,
        "custom_on_time_rate": 91,
        "custom_quality_rating": 4.2,
        "custom_dispute_count": 0,
        "custom_past_project_count": 12,
    },
]


def run():
    created = []
    for supplier in SUPPLIERS:
        if frappe.db.exists("Supplier", {"supplier_name": supplier["supplier_name"]}):
            continue
        doc = frappe.get_doc(
            {
                "doctype": "Supplier",
                "supplier_group": "All Supplier Groups",
                "supplier_type": "Company",
                **supplier,
            }
        )
        doc.insert(ignore_permissions=True)
        created.append(doc.name)
    frappe.db.commit()
    print(f"Created {len(created)} Suppliers: {created}")
