from pydantic import BaseModel

class Product(BaseModel):
    product_id: int
    product_name: str
    product_category: str
    unit_cost: float
    unit_price: float