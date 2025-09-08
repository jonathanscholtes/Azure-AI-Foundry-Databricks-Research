from pydantic import BaseModel

class OrderLine(BaseModel):
    order_line_id: int
    product_id: int
    quantity: int
    unit_price: float
    discount: float
    line_total: float