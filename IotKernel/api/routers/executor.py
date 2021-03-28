from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from IotKernel.execute.executor import Executor

router = APIRouter()


class Command(BaseModel):
    module: Optional[str] = "main"
    device: str
    command: str


@router.post("/execute")
async def get_devices(command: Command):
    executor = Executor(command.dict(by_alias=True))
    check_result = executor.check_command()
    if check_result is not True:
        return {"detail": check_result}
    if executor.send_command():
        return {"status": True}
