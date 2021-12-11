from fastapi import APIRouter
from starlette import status

router = APIRouter()


@router.post("/edit", status_code=status.HTTP_200_OK, name="setting:edit", )
async def edit_setting():
    pass
