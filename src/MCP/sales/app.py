from mcp.server.fastmcp import FastMCP
import logging
from typing import List, Optional
from db import run_dbquery  
from os import environ
from dotenv import load_dotenv

# Load environment variables
load_dotenv(override=True)

# Initialize logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastMCP(
    name="Server for Automotive Sales Data",
    host="0.0.0.0",
     port=int(environ.get("MCP_PORT", 80))
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

    Always includes order_id, customer_id, customer_name, order_date, region,
    product_id, quantity, unit_price, and line_unit_price.
    """
    try:
        filters = []
        params = {}

        if customer_id is not None:
            filters.append("c.customer_id = %(customer_id)s")
            params["customer_id"] = customer_id

        if product_id is not None:
            filters.append("p.product_id = %(product_id)s")
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
            o.order_id,
            c.customer_id,
            c.customer_name,
            o.order_date,
            o.region,
            p.product_id,
            ol.quantity,
            ol.unit_price,
            ROUND((ol.quantity * ol.unit_price) * (1 - ol.discount), 2) AS line_unit_price
        FROM orders o
        JOIN customers c ON o.customer_id = c.customer_id
        JOIN order_lines ol ON o.order_id = ol.order_id
        JOIN products p ON ol.product_id = p.product_id
        {where_clause}
        ORDER BY o.order_date DESC
        LIMIT %(limit)s
        """
        params["limit"] = limit

        rows = run_dbquery(sql, params)

        return [
            {
                "order_id": r["order_id"],
                "customer_id": r["customer_id"],
                "customer_name": r["customer_name"],
                "order_date": r["order_date"],
                "region": r["region"],
                "product_id": r["product_id"],
                "quantity": r["quantity"],
                "unit_price": r["unit_price"],
                "line_unit_price": r["line_unit_price"],
            }
            for r in rows
        ]

    except Exception as e:
        logger.exception("Error in get_orders tool")
        return [{"error": str(e)}]


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

    try:
        logger.info("Get Customers called")

        filters = []
        params = {}

        if customer_id:
            filters.append("c.customer_id = %(customer_id)s")
            params["customer_id"] = customer_id

        if industry:
            filters.append("c.industry = %(industry)s")
            params["industry"] = industry

        if region:
            filters.append("c.region = %(region)s")
            params["region"] = region

        where_clause = f"WHERE {' AND '.join(filters)}" if filters else ""

        sql = f"""
        SELECT 
            c.customer_id,
            c.customer_name,
            c.region,
            c.industry,
            c.account_manager
        FROM customers c
        {where_clause}
        ORDER BY c.customer_name
        LIMIT %(limit)s
        """
        params["limit"] = limit

        logger.debug(f"SQL: {sql}, Params: {params}")

        rows = run_dbquery(sql, params)
        logger.info(f"Returned {len(rows)} rows")
        logger.info([dict(r) for r in rows])

        return [
        {
            "customer_id": r["customer_id"],
            "customer_name": r["customer_name"],
            "region": r["region"],
            "industry": r["industry"],
            "account_manager": r["account_manager"],
        }
        for r in rows
    ]

    except Exception as e:
        logger.exception("Error in get_customers tool: %s", e)

        # Return an MCP-safe error object (JSON-serializable)
        return [{
            "error": "Error retrieving customers"
        }]


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

    Always return product_id, product_name, product_category, unit_cost, and unit_price.

    Example use cases:
    - "What is the unit price of product 7?"
    - "List all products in the 'Brakes' category."
    """
    try:
        filters = []
        params = {}

        if product_id is not None:
            filters.append("p.product_id = %(product_id)s")
            params["product_id"] = product_id

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

        rows = run_dbquery(sql, params)

        return [
            {
                "product_id": r["product_id"],
                "product_name": r["product_name"],
                "product_category": r["product_category"],
                "unit_cost": r["unit_cost"],
                "unit_price": r["unit_price"],
            }
            for r in rows
        ]

    except Exception as e:
        logger.exception("Error in get_products tool")
        return [{"error": str(e)}]


@app.tool()
def list_tables() -> List[str]:
    """
    List all available tables in the Databricks schema.

    Use this tool when you need to explore the database structure
    before forming custom queries.
    """
    try:
        rows = run_dbquery("SHOW TABLES")

        # Determine if rows are dicts or tuples
        if rows and isinstance(rows[0], dict):
            return [r["tableName"] for r in rows]
        elif rows:
            # Assume 'tableName' is the second column in the result
            return [r[1] for r in rows]
        else:
            return []

    except Exception as e:
        logger.exception("Error in list_tables tool")
        return [{"error": str(e)}]


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
    """
    try:
        if not sql.strip().lower().startswith("select"):
            return {"error": "Only SELECT queries are allowed."}

        rows = run_dbquery(sql)

        if not rows:
            return {"columns": [], "rows": []}

        # Determine if rows are dicts or tuples
        if isinstance(rows[0], dict):
            columns = list(rows[0].keys())
            data_rows = [list(r.values()) for r in rows]
        else:
            # fallback: convert tuple rows to list
            # assume column order unknown, return generic indices
            columns = [f"col_{i}" for i in range(len(rows[0]))]
            data_rows = [list(r) for r in rows]

        return {"columns": columns, "rows": data_rows}

    except Exception as e:
        logger.exception("Error in run_query tool")
        return {"error": str(e)}


if __name__ == "__main__":
    logger.info("Starting the FastMCP Sales...")
    logger.info(f"Service name: {environ.get('SERVICE_NAME', 'unknown')}")   
    app.run(transport="streamable-http")
