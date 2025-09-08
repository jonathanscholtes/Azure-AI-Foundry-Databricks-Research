from pydantic import BaseModel

class Customer(BaseModel):
    customer_id: int
    customer_name: str
    region: str
    industry: str
    account_manager: str