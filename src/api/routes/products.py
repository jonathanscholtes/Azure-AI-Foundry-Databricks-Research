from fastapi import APIRouter, Query
from typing import List, Optional
from services.product_service import get_products_filtered
from models.products import Product

router = APIRouter(tags=["Products"])

@router.get(
    "/products",
    response_model=List[Product],
    summary="Retrieve products",
    description="Retrieve a list of products with optional category filtering.",
)
def list_products(
    category: Optional[str] = Query(None, description="Filter by product category"),
    limit: int = Query(100, description="Maximum number of products to return"),
):
    return get_products_filtered(category, limit)