#!/usr/bin/env python3
# *_* coding: UTF-8 *_*
# @File  : aiserver.py
# @Author: Frank1126lin
# @Date  : 2021/2/20

import os
import time
import base64
from fastapi import FastAPI, File, UploadFile
from fastapi.requests import Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse
from predict import predict

app = FastAPI()
template = Jinja2Templates(directory="templates")

@app.get("/")
async def index(request:Request):
    return template.TemplateResponse("index.html",{"request":request})

@app.post("/upload")
async def handle(request:Request, file:UploadFile=File(...)):
    content = await file.read()
    filename = file.filename
    dir_in = "input"
    if not os.path.exists(dir_in):
        os.mkdir(dir_in)
    dir_inf = os.path.join(dir_in, filename)
    with open(dir_inf, "wb") as f:
        f.write(content)
    print("source:", dir_inf)
    rst = predict(source=dir_inf) # 当前为base64编码
    # dir_outf = os.path.join("output", filename)
    # cv2.imwrite(dir_outf, rst)
    # print(rst)
    # rst = str(rst,'utf-8')
    return template.TemplateResponse("result.html",{"request":request,"img": rst})

# @app.get("output/{filename}")
# async def get_img(filename:str):
#     return FileResponse("./output/"+filename)

if __name__ == '__main__':
    import uvicorn
    port = 8080
    uvicorn.run(app, host="0.0.0.0", port=port)
