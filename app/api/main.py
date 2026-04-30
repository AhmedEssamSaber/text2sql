from fastapi import FastAPI

from app.api.routes import router


app = FastAPI(
    title="Text2SQL API",
    version="1.0"
)

# register routes
app.include_router(router)