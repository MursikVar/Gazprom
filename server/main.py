from contextlib import asynccontextmanager
from pathlib import Path

import uvicorn
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI
from src.api.routes.auth import router as auth_router
from src.api.routes.users import router as users_router
from src.api.routes.dict_table import router as dict_router
from src.api.routes.event import router as event_router
from fastapi.middleware.cors import CORSMiddleware
from src.database import init_models, init_database
from src.create_rows import create_initial_data

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_database()
    await init_models()
    await create_initial_data()
    print("Таблицы успешно созданы!")
    yield
    # Выполняется при остановке
    pass

def initialize_backend_application() -> FastAPI:
    app = FastAPI(lifespan=lifespan)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    #
    app.include_router(router=auth_router)
    app.include_router(router=users_router)
    app.include_router(router=dict_router)
    app.include_router(router=event_router)
    return app

app: FastAPI = initialize_backend_application()

# Аватары
static_dir = Path("../static")
static_dir.mkdir(exist_ok=True)
app.mount("/static", StaticFiles(directory="../static"), name="static")


if __name__ == "__main__":
    uvicorn.run(
        app="main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )
