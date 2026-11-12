from fastapi import FastAPI
from src.controllers.request_router import router as request_router
from src.controllers.reference_router import router as reference_router

app = FastAPI(
    title="RequestSystem API",
    description="API для системы учёта заявок",
    version="1.0.0"
)

# Подключаем наши роутеры
app.include_router(request_router)
app.include_router(reference_router)

@app.get("/")
def root():
    return {"message": "Добро пожаловать в RequestSystem API!"}