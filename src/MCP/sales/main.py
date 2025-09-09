# sales_mcp_server.py
from fastmcp import FastMCP
import logging
from typing import List, Optional
from db import run_query  # your Databricks connection wrapper
from os import environ
from dotenv import load_dotenv

# Load environment variables
load_dotenv(override=True)

# Initialize logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastMCP(
    name="Server for Automotive Sales Data",
     port=int(environ.get("MCP_PORT", 8082)), on_duplicate_tools="error",
    description=(
        "MCP server exposing automotive sales data from Databricks. "
        "Use these tools to analyze sales performance, customer activity"
    )
)


@app.tool()
def get_orders(
    customer_id: Optional[int] = None,
    product_id: Optional[int] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    region: Optional[str] = None,
    limit: int = 100
) -> List[dict]:
    """
    Retrieve sales orders, including nested order lines and product details.

    Use this tool when the question is about sales, revenue, discounts,
    customer purchasing behavior, or product sales. Supports filters:

    - customer_id: only return orders from a specific customer
    - product_id: only return orders containing a specific product
    - start_date / end_date: restrict to an order date range (YYYY-MM-DD)
    - region: filter by sales region (e.g., 'NA', 'EU')
    - limit: maximum number of rows to return (default: 100)

    Always includes customer_id, customer_name, product_id, product_name,
    quantity, unit_price, and line_total_usd.

    Example use cases:
    - "Which products generated the most revenue in the EU last quarter?"
    - "List all orders for customer 42 containing product 7."
    """
    sql = f"""
    SELECT o.order_id, c.customer_id, c.customer_name, o.order_date, o.region,
           p.product_id, p.product_name, ol.quantity, ol.unit_price,
           ROUND((ol.quantity * ol.unit_price) * (1 - ol.discount), 2) AS line_total_usd
    FROM orders o
    JOIN customers c ON o.customer_id = c.customer_id
    JOIN order_lines ol ON o.order_id = ol.order_id
    JOIN products p ON ol.product_id = p.product_id
    WHERE 1=1
    """
    params = []
    if customer_id: sql += " AND c.customer_id = ?"; params.append(customer_id)
    if product_id: sql += " AND p.product_id = ?"; params.append(product_id)
    if start_date: sql += " AND o.order_date >= ?"; params.append(start_date)
    if end_date: sql += " AND o.order_date <= ?"; params.append(end_date)
    if region: sql += " AND o.region = ?"; params.append(region)

    sql += " LIMIT ?"; params.append(limit)

    rows = run_query(sql, params)
    return [dict(r) for r in rows]


@app.tool()
def get_customers(
    customer_id: Optional[int] = None,
    industry: Optional[str] = None,
    region: Optional[str] = None,
    limit: int = 100
) -> List[dict]:
    """
    Retrieve customer information.

    Use this tool when the question references customers by ID, name,
    industry, or region. Supports filters:

    - customer_id: return a specific customer
    - industry: filter customers by industry (e.g., 'Automotive', 'Aerospace')
    - region: filter customers by sales region (e.g., 'NA', 'EU')
    - limit: maximum number of customers to return (default: 100)

    Always return customer_id and customer_name.

    Example use cases:
    - "Who are our top aerospace industry customers?"
    - "Get customer 42's details."
    """
    sql = "SELECT customer_id, customer_name, industry, region FROM customers WHERE 1=1"
    params = []
    if customer_id:
        sql += " AND customer_id = ?"; params.append(customer_id)
    if industry:
        sql += " AND industry = ?"; params.append(industry)
    if region:
        sql += " AND region = ?"; params.append(region)

    sql += " ORDER BY customer_name LIMIT ?"
    params.append(limit)

    rows = run_query(sql, params)
    return [dict(r) for r in rows]


@app.tool()
def get_products(
    product_id: Optional[int] = None,
    category: Optional[str] = None,
    limit: int = 100
) -> List[dict]:
    """
    Retrieve product catalog data.

    Use this tool when the question involves product details, pricing,
    or categories. Supports filters:

    - product_id: return a specific product
    - category: filter by category (e.g., 'Brakes', 'Tires')
    - limit: maximum number of products to return (default: 100)

    Always return product_id, product_name, category, and unit_price.

    Example use cases:
    - "What is the unit price of product 7?"
    - "List all products in the 'Brakes' category."
    """
    sql = "SELECT product_id, product_name, category, unit_price FROM products WHERE 1=1"
    params = []
    if product_id:
        sql += " AND product_id = ?"; params.append(product_id)
    if category:
        sql += " AND category = ?"; params.append(category)

    sql += " ORDER BY product_name LIMIT ?"
    params.append(limit)

    rows = run_query(sql, params)
    return [dict(r) for r in rows]


@app.tool()
def list_tables() -> List[str]:
    """
    List all available tables in the Databricks schema.

    Use this tool when you need to explore the database structure
    before forming custom queries.
    """
    sql = "SHOW TABLES"
    rows = run_query(sql)
    return [r["tableName"] for r in rows]


@app.tool()
def run_query(sql: str) -> dict:
    """
    Run a custom SQL query against Databricks.

    Restrictions:
    - Only SELECT statements are allowed.
    - Results are limited to 500 rows.

    Use this tool for advanced analysis that cannot be handled by
    get_orders, get_customers, or get_products.

    Returns:
    - columns: list of column names
    - rows: list of row values

    Example use cases:
    - "Calculate average discount across all orders."
    - "Find total revenue by region and product category."
    """
    if not sql.strip().lower().startswith("select"):
        return {"error": "Only SELECT queries are allowed."}
    sql += " LIMIT 500"
    rows = run_query(sql)
    return {
        "columns": list(rows[0].keys()) if rows else [],
        "rows": [list(r.values()) for r in rows]
    }


if __name__ == "__main__":
    logger.info("Starting the FastMCP Sales...")
    logger.info(f"Service name: {environ.get('SERVICE_NAME', 'unknown')}")   
    app.run(transport="streamable-http")
