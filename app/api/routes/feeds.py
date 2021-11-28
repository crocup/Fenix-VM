from fastapi import APIRouter
from starlette import status

router = APIRouter()


@router.post("/download", status_code=status.HTTP_200_OK, name="feeds:download", )
async def download_feeds():
    pass
