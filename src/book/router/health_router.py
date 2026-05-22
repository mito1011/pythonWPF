from fastapi import APIRouter

router = APIRouter(prefix="/health", tags=["Health"])


@router.get("/live")
def live():
    return {"status": "ok"}
