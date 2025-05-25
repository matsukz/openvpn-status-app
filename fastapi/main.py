from fastapi import FastAPI, Depends,  HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

import json

from extend.client_status import parse_openvpn_status

from extend.system_status import check_service_status

from extend.system_operation import start
from extend.system_operation import restart
from extend.system_operation import stop

from extend.class_statusAction import Action

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
  logfile = "/var/log/openvpn-status.log"
  output = parse_openvpn_status(logfile)
  return output

@app.get("/ovpn/api/status/", tags=["APIエンドポイント"], summary="VPNサーバーの状態を取得します")
async def get_status():
  output = check_service_status("openvpn@server")
  status:dict = {"server_status":output}
  return status

@app.put("/ovpn/api/status/", tags=["APIエンドポイント"], summary="VPNサーバーの状態操作を試みます")
async def operation_status(action:Action):

  action = action.dict()

  key:str = "softwaresoftware"

  match action["action"]:

    case "start":
      #result_response = start("openvpn@server")
      result_response = True
    
    case "restart":
        if not action["key"] == key:
          return JSONResponse(
              status_code=status.HTTP_401_UNAUTHORIZED,
              content={"action": action["action"], "result": False,"msg":"There is a problem with the authentication method"}
          )
        #result_response = restart("openvpn@server")
        result_response = True

    case "stop":
        if not action["key"] == key:
          return JSONResponse(
              status_code=status.HTTP_401_UNAUTHORIZED,
              content={"action": action["action"], "result": False,"msg":"There is a problem with the authentication method"}
          )
        #result_response = stop("openvpn@server")
        result_response = True

    case _:
      return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"action": action["action"], "result": False,"msg":"Valid parameters could not be detected"}
    )

  if result_response:
    return {"action":action["action"],"result":result_response}
  else:
    HTTPException(status_code=503, detail="Server Error")