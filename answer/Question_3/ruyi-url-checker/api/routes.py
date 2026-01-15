from fastapi import APIRouter, HTTPException
from core.url_check import batch_check_all_urls
from core.url_check import get_all_results, get_results_by_name
from api.schemas import CheckResponse

router = APIRouter()


@router.get("/health", summary="服务健康检查")
async def health_check():
    return {"status": "healthy"}


@router.get("/check/status", response_model=CheckResponse, summary="获取所有URL检查结果")
async def get_all_check_status():
    try:
        results = get_all_results()
        return CheckResponse(
            success=True,
            data=results,
            message=f"成功获取{len(results)}个检查结果"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/check/status/{name}", response_model=CheckResponse, summary="按名称查询结果")
async def get_board_image_status(name: str):
    try:
        results = get_results_by_name(name)
        if not results:
            return CheckResponse(
                success=True,
                data=[],
                message=f"未找到「{name}」相关结果"
            )
        return CheckResponse(
            success=True,
            data=results,
            message=f"找到{len(results)}个「{name}」相关结果"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/check/refresh", response_model=CheckResponse, summary="手动触发检查")
async def refresh_check_status():
    try:
        results = batch_check_all_urls()
        return CheckResponse(
            success=True,
            data=results,
            message=f"手动检查完成，共处理{len(results)}个版本"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
