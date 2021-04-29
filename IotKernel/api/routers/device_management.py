from fastapi import APIRouter, HTTPException
from IotKernel.devices import DeviceManagement, CrudDevice
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter()


class Device(BaseModel):
    name: str
    module: Optional[str] = 'main'


class FullDevice(Device):
    description: str
    description_ru: str
    available_commands: List[str]


@router.get("/")
async def get_devices():
    devices = DeviceManagement().load_devices()
    return devices


@router.put("/add")
async def add_device(device: FullDevice):
    add = CrudDevice(device.dict(by_alias=True))
    check = add.check_device()
    if check is not True:
        raise HTTPException(status_code=400, detail=check)
    add.add_device()
    return DeviceManagement().load_devices(device.module)


@router.post("/info")
async def device_info(device: Device):
    info = CrudDevice(device.dict(by_alias=True))
    return info.device_info()


@router.post("/update")
async def update_device(device: FullDevice):
    update = CrudDevice(device.dict(by_alias=True))
    update.update_device()
    return DeviceManagement().load_devices(device.module)


@router.delete("/delete")
async def delete_device(device: Device):
    delete = CrudDevice(device.dict(by_alias=True))
    delete.delete_device()
    return DeviceManagement().load_devices(device.module)

def check_device_exist():
    pass