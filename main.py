from fastapi import FastAPI
from fastapi.responses import JSONResponse

from app.db.base import engine
from app.core.config import SQLALCHEMY_DATABASE_URL
from app import models, routes


import uvicorn


app = FastAPI(
    title="Sample FastAPI Application",
    description="Sample FastAPI Application with Swagger and Sqlalchemy",
    version="1.0.0",
)

models.Base.metadata.create_all(bind=engine)


@app.exception_handler(Exception)
def validation_exception_handler(request, err):
    base_error_message = f"Failed to execute: { request.method }: { request.url }"
    return JSONResponse(status_code=400, content={"message": f"{base_error_message}. Detail: {err}"})


app.include_router(routes.item_router, prefix="/api/v1")
app.include_router(routes.store_router, prefix="/api/v1")


def main():
    uvicorn.run("main:app", reload=True)


if __name__=='__main__':
    main()