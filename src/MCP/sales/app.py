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
            p.product_name,
            ol.quantity,
            ol.unit_price,
            ROUND((ol.quantity * ol.unit_price) * (1 - ol.discount), 2) AS line_unit_price
        FROM sales_orders o
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
                "product_name": r["product_name"],
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
def get_product_category(name: str) -> dict:
    """
    Resolve a user-provided product category string into the canonical category 
    name stored in the database.

    Use this when the category in a user question may be misspelled, pluralized,
    or formatted differently (e.g., 'Brake Pads' vs 'Brake Pad').

    Returns:
        {
            "input": "Brake Pads",
            "resolved_category": "Brake Pad",
            "confidence": 0.92
        }
    """
    try:
        sql = """
        SELECT p.product_category,
               levenshtein(lower(p.product_category), lower(%(name)s)) AS distance
        FROM products p
        GROUP BY p.product_category
        ORDER BY distance ASC
        LIMIT 1
        """
        rows = run_dbquery(sql, {"name": name})

        if not rows:
            return {"input": name, "resolved_category": None, "confidence": 0.0}

        row = rows[0]
        max_len = max(len(name), len(row["product_category"]))
        confidence = 1 - (row["distance"] / max_len)

        return {
            "input": name,
            "resolved_category": row["product_category"],
            "confidence": confidence,
        }

    except Exception as e:
        logger.exception("Error in get_product_category tool")
        return {"input": name, "resolved_category": None, "error": str(e)}

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




if __name__ == "__main__":
    logger.info("Starting the FastMCP Sales...")
    logger.info(f"Service name: {environ.get('SERVICE_NAME', 'unknown')}")   
    app.run(transport="streamable-http")
