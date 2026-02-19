from fastapi import APIRouter
from pydantic import BaseModel
from services import ai_service

router = APIRouter(prefix="/api/settings", tags=["settings"])


@router.get("/config")
async def get_ai_config():
    status = await ai_service.get_ai_config_status()
    return status


class AiConfigUpdate(BaseModel):
    api_key: str
    base_url: str
    model_name: str


@router.post("/config")
async def save_ai_config(body: AiConfigUpdate):
    if not body.api_key.strip():
        from fastapi import HTTPException
        raise HTTPException(status_code=400, detail="API Key 不能为空")
    
    if not body.base_url.strip():
        from fastapi import HTTPException
        raise HTTPException(status_code=400, detail="API Base URL 不能为空")
        
    if not body.model_name.strip():
        from fastapi import HTTPException
        raise HTTPException(status_code=400, detail="模型名称不能为空")

    ai_service.save_ai_config(
        body.api_key.strip(), 
        body.base_url.strip(), 
        body.model_name.strip()
    )
    return {"message": "AI配置已保存！无需重启即可生效"}
