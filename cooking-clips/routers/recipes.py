from fastapi import APIRouter

router = APIRouter(
    prefix="/recipes",
    tags=["recipes"],
    #dependencies=[Depends(get_token_header)],
)