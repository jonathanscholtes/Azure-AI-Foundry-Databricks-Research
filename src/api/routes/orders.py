from fastapi import APIRouter, Query
from typing import List, Optional
from datetime import date
from services.order_service import get_orders_filtered
from models.orders import Order

router = APIRouter(tags=["Orders"])

@router.get(
    "/orders",
    response_model=List[Order],
    summary="Retrieve orders with filters",
    description=(
        "Retrieve a list of orders with nested order lines and products. "
        "Supports filtering by customer, product, date range, and region."
    ),
)
def list_orders(
    customer_id: Optional[int] = Query(None, description="Filter by customer ID"),
    product_id: Optional[int] = Query(None, description="Filter by product ID"),
    start_date: Optional[date] = Query(None, description="Filter orders on or after this date"),
    end_date: Optional[date] = Query(None, description="Filter orders on or before this date"),
    region: Optional[str] = Query(None, description="Filter by region"),
    limit: int = Query(100, description="Maximum number of orders to return"),
):
    return get_orders_filtered(customer_id, product_id, start_date, end_date, region, limit)


