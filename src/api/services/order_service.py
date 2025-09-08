# app/services/order_service.py
from db import run_query
from models.orders import Order
from models.order_lines import OrderLine
from models.products import Product
from typing import Optional
from datetime import date

def _map_orders(rows):
    """Helper: transform SQL rows into nested Order objects."""
    orders_dict = {}

    for r in rows:
        order_id = r["order_id"]

        if order_id not in orders_dict:
            orders_dict[order_id] = Order(
                order_id=r["order_id"],
                customer_id=r["customer_id"],
                order_date=r["order_date"],
                ship_date=r["ship_date"],
                sales_channel=r["sales_channel"],
                region=r["region"],
                order_lines=[]
            )

        if r["order_line_id"] is not None:
          
            orders_dict[order_id].order_lines.append(OrderLine(
                order_line_id=r["order_line_id"],
                quantity=r["quantity"],
                discount=r["discount"],
                unit_price=r["line_unit_price"],
                line_total=r["line_total"],
                product_id=r["product_id"]
            ))

    return list(orders_dict.values())

def get_orders_filtered(
    customer_id: Optional[int] = None,
    product_id: Optional[int] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    region: Optional[str] = None,
    limit: int = 100
):
    filters = []
    params = {}

    if customer_id:
        filters.append("o.customer_id = %(customer_id)s")
        params["customer_id"] = customer_id
    if product_id:
        filters.append("l.product_id = %(product_id)s")
        params["product_id"] = product_id
    if start_date:
        filters.append("o.order_date >= %(start_date)s")
        params["start_date"] = start_date
    if end_date:
        filters.append("o.order_date <= %(end_date)s")
        params["end_date"] = end_date
    if region:
        filters.append("o.region = %(region)s")
        params["region"] = region

    where_clause = f"WHERE {' AND '.join(filters)}" if filters else ""

    sql = f"""
    SELECT 
        o.order_id AS order_id,
        o.customer_id AS customer_id,
        o.order_date AS order_date,
        o.ship_date AS ship_date,
        o.sales_channel AS sales_channel,
        o.region AS region,
        l.order_line_id AS order_line_id,
        l.product_id AS product_id,
        l.quantity AS quantity,
        l.unit_price AS line_unit_price,
        l.discount AS discount,
        l.line_total AS line_total,
        p.product_name AS product_name,
        p.product_category AS product_category,
        p.unit_price AS unit_price,
        p.unit_cost AS unit_cost
    FROM sales_orders o
    LEFT JOIN order_lines l ON o.order_id = l.order_id
    LEFT JOIN products p ON l.product_id = p.product_id
    {where_clause}
    ORDER BY o.order_id
    LIMIT %(limit)s
    """
    params["limit"] = limit * 5  # adjust to return enough rows for nested order lines

    rows = run_query(sql, params)

    # If run_query returns list of tuples, map columns explicitly:
    columns = ["order_id","customer_id","order_date","ship_date","sales_channel","region",
               "order_line_id","product_id","quantity","line_unit_price","discount","line_total",
               "product_name","product_category","product_unit_price"]
    rows_dicts = [dict(zip(columns, r)) for r in rows]

    return _map_orders(rows_dicts)
