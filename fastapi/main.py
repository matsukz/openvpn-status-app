from fastapi import FastAPI, Depends,  HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from extend.client_status import parse_openvpn_status
from extend.system_status import check_service_status

description = """
  OpenVPNのステータスを出力するWebAPIです
  """

app = FastAPI(
  title = "OpenVPN ステータス取得API - FastAPI",
  description=description
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],   
    allow_headers=["*"]    
)

@app.on_event("startup")
async def startup():
  pass

#終了時
@app.on_event("shutdown")
async def shutdown():
  pass

@app.get("/ovpn/api/client/", tags=["APIエンドポイント"], summary="すべてのセッション情報を取得します")
async def get_client():
  logfile = "/src/openvpn-status.log"
  output = parse_openvpn_status(logfile)
  return output

@app.get("/ovpn/api/status/", tags=["APIエンドポイント"], summary="すべてのセッション情報を取得します")
async def get_status():
  output = check_service_status("openvpn@server")
  status:dict = {"server_status":output}
  return status