from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from app.config import Container
from app.user.router import router as user_router
import uvicorn

def create_app() -> FastAPI:
    app = FastAPI()
    container = Container()
    app.container = container
    app.include_router(user_router)
    register_tortoise(
    app=app,
    db_url='sqlite://db.sqlite3',
    modules={'models':['app.user.user_model']},
    generate_schemas=True,
    add_exception_handlers=True
    )
    return app


if __name__ == "__main__":
    app = create_app()
    uvicorn.run(app)