from fastapi import FastAPI, APIRouter
import uvicorn
from routers.auth_router import auth_router
from settings import path_settings


app = FastAPI(title="fastapi_api_yamdb")

main_api_router = APIRouter(prefix='/api/v1')
main_api_router.include_router(auth_router, prefix='/auth', tags=['auth'])

app.include_router(main_api_router)

if __name__=='__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)