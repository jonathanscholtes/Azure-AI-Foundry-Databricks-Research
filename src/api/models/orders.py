from pydantic import BaseModel
from datetime import date
from typing import List
from models.order_lines import OrderLine

class Order(BaseModel):
    order_id: int
    customer_id: int
    order_date: date
    ship_date: date
    sales_channel: str
    region: str
    order_lines: List[OrderLine] = []