from fastapi import APIRouter, Query
from typing import List, Optional
from services.customer_service import get_customers
from models.customers import Customer

router = APIRouter(tags=["Customers"])

@router.get(
    "/customers",
    response_model=List[Customer],
    summary="Retrieve customers",
    description=(
        "Retrieve a list of customers with optional filters for industry and account manager. "
        "Useful for AI agents to analyze customer-related metrics."
    ),
)
def list_customers(
    industry: Optional[str] = Query(None, description="Filter by industry"),
    account_manager: Optional[str] = Query(None, description="Filter by account manager"),
    limit: int = Query(100, description="Maximum number of customers to return")
):
    return get_customers(industry, account_manager, limit)