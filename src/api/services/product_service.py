# app/services/product_service.py
from db import run_query
from typing import List, Optional
from models.products import Product

def get_products_filtered(category: Optional[str] = None, limit: int = 100) -> List[Product]:
    filters = []
    params = {}

    if category:
        filters.append("p.product_category = %(category)s")
        params["category"] = category

    where_clause = f"WHERE {' AND '.join(filters)}" if filters else ""

    sql = f"""
    SELECT 
        p.product_id AS product_id,
        p.product_name AS product_name,
        p.product_category AS product_category,
        p.unit_cost AS unit_cost,
        p.unit_price AS unit_price
    FROM products p
    {where_clause}
    ORDER BY p.product_name
    LIMIT %(limit)s
    """
    params["limit"] = limit

    rows = run_query(sql, params)
    return [
        Product(
            product_id=r[0],
            product_name=r[1],
            product_category=r[2],
            unit_cost=r[3],
            unit_price=r[4]
        )
        for r in rows
    ]
