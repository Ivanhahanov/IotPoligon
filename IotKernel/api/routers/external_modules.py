from fastapi import APIRouter
from pydantic import BaseModel
from typing import Dict, Optional
from IotKernel.modules import ExternalModules

router = APIRouter()


class Module(BaseModel):
    name: str
    description: str
    description_ru: Optional[str] = None
    protocol: str
    devices: Dict


@router.post("/register")
async def register_module(module: Module):
    """
    :param module:
    :return:
    """
    external_module = ExternalModules(module.dict())
    module_check = external_module.check_module()
    if module_check is not True:
        return {"detail": module_check}
    external_module.add_module()
    return {"status": True}
