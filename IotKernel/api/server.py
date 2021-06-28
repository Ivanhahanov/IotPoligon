from fastapi import Depends, FastAPI

from IotKernel.api.routers import device_management, external_modules, executor, update
from IotKernel.translate import upload_translate_to_redis
app = FastAPI()

app.include_router(device_management.router, prefix="/devices", tags=["Devices"])
app.include_router(external_modules.router, prefix="/modules", tags=["Modules"])
app.include_router(executor.router, prefix="/executor", tags=["Executor"])
app.include_router(update.router, prefix="/board_manager", tags=["Board Manager"])
upload_translate_to_redis()

@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}
