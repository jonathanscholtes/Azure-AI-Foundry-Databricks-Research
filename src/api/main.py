from routes import orders, products, customers
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
from fastapi.logger import logger
from os import environ
from dotenv import load_dotenv

load_dotenv(override=True)

# Configure Logging to use Gunicorn log settings, if available
logger = logging.getLogger(__name__)

gunicorn_logger = logging.getLogger('gunicorn.error')
logger.handlers = gunicorn_logger.handlers
logger.setLevel(gunicorn_logger.level)


server_url = environ.get("SERVER_URL")


app = FastAPI(
    title="Automotive Sales Service",
    description="API for analyzing sales data",
    servers=[
        {"url": server_url, "description": "Lab environment"}
    ]
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes
app.include_router(customers.router, prefix="/customers", tags=["Customers"])
app.include_router(products.router, prefix="/products", tags=["Products"])
app.include_router(orders.router, prefix="/orders", tags=["Orders"])


@app.get("/")
def get_status() -> str:
    """Root endpoint to check if the application is running."""
    logger.info("**Logging - RUNNING**")
    return "running"

# Run the application using Uvicorn when executed directly
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)