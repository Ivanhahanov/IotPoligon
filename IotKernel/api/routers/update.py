from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Optional
from IotKernel.update_firmware import ESPOptions

router = APIRouter()


class UpdateRequest(BaseModel):
    filename: Optional[str] = "esp_test"
    esp_ip: Optional[str] = "192.168.1.79"
    board: Optional[str] = "esp8266:esp8266:nodemcuv2"


@router.post("/update")
async def update(request: UpdateRequest):
    esp = ESPOptions(request.filename,
                     request.esp_ip,
                     request.board)
    update_result = esp.update()
    if update_result != 0:
        raise HTTPException(status_code=400, detail="Update failed!")
    return {"message": "Updade Successfully Completed"}


@router.post("/build")
async def build(request: UpdateRequest):
    esp = ESPOptions(request.filename,
                     request.esp_ip,
                     request.board)
    esp.convert_code()
    build_result = esp.build()
    # esp.check_external_libs()
    if build_result is not True:
        raise HTTPException(status_code=400, detail=build_result)
    return {"message": "Build Successfully Completed"}


@router.post("/available_boards")
def get_available_boards():
    pass
