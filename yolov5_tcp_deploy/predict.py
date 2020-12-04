#! /usr/bin/env python3
# *_* coding: utf-8 *_*
# @File  : predict.py
# @Author: Frank1126lin
# @Date  : 2020/7/14


import os
import time
import json
import platform
import random
from pathlib import Path

import torch
import cv2
from models.experimental import attempt_load
from utils.torch_utils import select_device, time_synchronized
from utils.datasets import LoadImages
from utils.general import check_img_size, non_max_suppression, scale_coords, xyxy2xywh
from utils.plots import plot_one_box


yolo_config = json.load(open("yolov5_config.json", "r"))
for k,v in yolo_config.items():
    print(k,":", v)
weights = yolo_config["weights"]
source = yolo_config["source"]
save_dir = yolo_config["save-dir"]
device = yolo_config["device"]
img_size = yolo_config["img-size"]
conf_thres = yolo_config["conf-thres"]
iou_thres = yolo_config["iou-thres"]
classes = yolo_config["classes"] if yolo_config["classes"] != "all" else None


def predict( save_img = True, weights = weights, source = source, out = save_dir, imgsz = img_size, conf_thres = conf_thres,
            iou_thres = iou_thres, device = device, save_txt = True, classes = classes, agnostic_nms = False,):
    # Initialize
    device = select_device(device)
    half = device.type != 'cpu'  # half precision only supported on CUDA
    # Load model
    model = attempt_load(weights, map_location=device)  # load FP32 model
    imgsz = check_img_size(imgsz, s=model.stride.max())  # check img_size
    if half:
        model.half()  # to FP16

    # Set Dataloader
    dataset = LoadImages(source, img_size=imgsz) # 图片类

    # Get names and colors
    names = model.module.names if hasattr(model, 'module') else model.names
    colors = [[random.randint(0, 255) for _ in range(3)] for _ in range(len(names))]

    # Run inference
    img = torch.zeros((1, 3, imgsz, imgsz), device=device)  # init img
    _ = model(img.half() if half else img) if device.type != 'cpu' else None  # run once
    for path, img, im0s, vid_cap in dataset:
        img = torch.from_numpy(img).to(device)
        img = img.half() if half else img.float()  # uint8 to fp16/32
        img /= 255.0  # 0 - 255 to 0.0 - 1.0
        if img.ndimension() == 3:
            img = img.unsqueeze(0)

        # Inference
        pred = model(img)[0]

        # Apply NMS
        pred = non_max_suppression(pred, conf_thres, iou_thres, classes=classes, agnostic=agnostic_nms)

        # Process detections
        p, s, im0 = path, '', im0s

        ss = {"imgPath":source} # dict format
        save_path = str(save_dir / p.name)
        for i, det in enumerate(pred): # detections in image

            if len(det):
                # Rescale boxes from img_size to im0 size
                det[:, :4] = scale_coords(img.shape[2:], det[:, :4], im0.shape).round()
                for *xyxy, conf, cls in det:
                    xyxy = torch.tensor(xyxy).view(1,4).view(-1).tolist()
                    conf = conf.item()
                    obj = {"label": names[int(cls)], "conf": conf, "points": xyxy}
                    ss[i] = obj
                    label =  "{}:{:.2f}%".format(names[int(cls)], conf*100)
                    plot_one_box(xyxy, im0, label=label, color=colors[int(cls)], line_thickness=2)
        if save_img:
            cv2.imwrite(save_path, im0)

        return ss, im0

# if __name__ == '__main__':
#     with torch.no_grad():
#             predict()

