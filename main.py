import os
import nest_asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from app.chat import router as chat_router
from app.agent_rent import router as agent_rent_router

nest_asyncio.apply()

app = FastAPI(
    title="Rentier API",
    description="API для управления арендой помещений",
    version="1.0.0"
)

# CORS настройки
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем роутеры
app.include_router(chat_router, prefix="/api")
app.include_router(agent_rent_router, prefix="/api")

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port) 