from ultralytics import YOLO
YOLO("yolo26n.pt").export(format="ncnn", imgsz=640, device="cpu")