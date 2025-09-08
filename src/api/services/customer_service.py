from typing import List, Optional
from db import run_query
from models.customers import Customer

def get_customers(
    customer_industry: Optional[str] = None,
    customer_account_manager: Optional[str] = None,
    limit: int = 100
) -> List[Customer]:
    filters = []
    params = {}

    if customer_industry:
        filters.append("c.industry = %(customer_industry)s")
        params["customer_industry"] = customer_industry  # match placeholder

    if customer_account_manager:
        filters.append("c.account_manager = %(customer_account_manager)s")
        params["customer_account_manager"] = customer_account_manager  # match placeholder

    where_clause = f"WHERE {' AND '.join(filters)}" if filters else ""

    sql = f"""
    SELECT 
        customer_id,
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

    rows = run_query(sql, params)
    return [
        Customer(
            customer_id=r[0],
            customer_name=r[1],
            region=r[2],
            industry=r[3],
            account_manager=r[4]
        )
        for r in rows
    ]
