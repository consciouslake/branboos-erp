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
    {
        "supplier_name": "Konkan Cement Distributors",
        "custom_city": "Mumbai",
        "custom_current_quote": 415,
        "custom_on_time_rate": 93,
        "custom_quality_rating": 4.3,
        "custom_dispute_count": 1,
        "custom_past_project_count": 41,
    },
    {
        "supplier_name": "Yamuna Steel & Rebar Co.",
        "custom_city": "Noida",
        "custom_current_quote": 52500,
        "custom_on_time_rate": 79,
        "custom_quality_rating": 3.6,
        "custom_dispute_count": 3,
        "custom_past_project_count": 17,
    },
    {
        "supplier_name": "Deccan Aggregates & Aggregates",
        "custom_city": "Hyderabad",
        "custom_current_quote": 1320,
        "custom_on_time_rate": 89,
        "custom_quality_rating": 4.1,
        "custom_dispute_count": 0,
        "custom_past_project_count": 25,
    },
    {
        "supplier_name": "Sahyadri RMC Pune",
        "custom_city": "Pune",
        "custom_current_quote": 5950,
        "custom_on_time_rate": 97,
        "custom_quality_rating": 4.7,
        "custom_dispute_count": 0,
        "custom_past_project_count": 29,
    },
    {
        "supplier_name": "Hooghly Brick & Block Works",
        "custom_city": "Kolkata",
        "custom_current_quote": 8.5,
        "custom_on_time_rate": 72,
        "custom_quality_rating": 3.2,
        "custom_dispute_count": 4,
        "custom_past_project_count": 15,
    },
    {
        "supplier_name": "Sabarmati Glass & Facade Co.",
        "custom_city": "Ahmedabad",
        "custom_current_quote": 2450,
        "custom_on_time_rate": 85,
        "custom_quality_rating": 4.0,
        "custom_dispute_count": 1,
        "custom_past_project_count": 19,
    },
]


def _ensure_supplier_group() -> str:
    """Fresh ERPNext sites created non-interactively (no Setup Wizard) have
    no Supplier Group records — Supplier.supplier_group is a mandatory Link,
    so create a root group if none exists."""
    existing = frappe.db.get_value("Supplier Group", {"is_group": 1}, "name")
    if existing:
        return existing

    group = frappe.get_doc(
        {
            "doctype": "Supplier Group",
            "supplier_group_name": "All Supplier Groups",
            "is_group": 1,
        }
    )
    group.insert(ignore_permissions=True)
    return group.name


def run():
    supplier_group = _ensure_supplier_group()

    created = []
    for supplier in SUPPLIERS:
        if frappe.db.exists("Supplier", {"supplier_name": supplier["supplier_name"]}):
            continue
        doc = frappe.get_doc(
            {
                "doctype": "Supplier",
                "supplier_group": supplier_group,
                "supplier_type": "Company",
                **supplier,
            }
        )
        doc.insert(ignore_permissions=True)
        created.append(doc.name)
    frappe.db.commit()
    print(f"Created {len(created)} Suppliers: {created}")
