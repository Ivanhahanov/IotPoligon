from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from IotKernel.execute import Executor

router = APIRouter()


class Command(BaseModel):
    module: Optional[str] = "main"
    device: str
    command: str


class GetData(BaseModel):
    module: Optional[str] = "main"
    device: str


@router.post("/execute")
async def execute(command: Command):
    executor = Executor(**command.dict())
    check_result = executor.check_command()
    if check_result is not True:
        raise HTTPException(status_code=400, detail=check_result)
    if executor.send_command():
        return {"status": True}


@router.post("/data")
async def execute_with_answer(data: GetData):
    executor = Executor(**data.dict())
    return executor.get_answer()
