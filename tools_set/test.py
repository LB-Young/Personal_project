"""
class:
CLASS_MAPPING = {
    0: "正文标题",
    1: "正文",
    2: "页眉页脚", 
    3: "图片",
    4: "图片标题",
    5: "表格",
    6: "表格标题",
    7: "表格底部单位"
}
"""


import os
import time
import numpy as np
import onnxruntime as ort
import cv2

def resize_boxes(boxes, old_size, new_size):
    old_width,old_height = old_size
    new_width,new_height = new_size
    scale_x, scale_y = (
        old_width / new_width,
        old_height / new_height,
    )
    if not isinstance(boxes, np.ndarray):
        boxes = np.array(boxes)
    boxes[:, 0::2] *= scale_x
    boxes[:, 1::2] *= scale_y
    x1 = np.clip(boxes[:, 0], a_min=0, a_max=old_width)
    y1 = np.clip(boxes[:, 1], a_min=0, a_max=old_height)
    x2 = np.clip(boxes[:, 2], a_min=0, a_max=old_width)
    y2 = np.clip(boxes[:, 3], a_min=0, a_max=old_height)
    return np.stack((x1, y1, x2, y2), axis=-1)

def resize_image(image, min_size=800, max_size=1333):
    height, width = image.shape[:2]
    if height >= min_size and width >= min_size and width <= max_size and height <= max_size:
        return image
    else:
        # calculate the scale
        scale_w = min_size / width
        scale_h = min_size / height
        scale = min(scale_w, scale_h)
        if width * scale > max_size or height * scale > max_size:
            scale = max_size / max(width, height)
        # scale
        new_width = int(width * scale)
        new_height = int(height * scale)
        resized_image = cv2.resize(image, (new_width, new_height))
    return resized_image

def get_img_inputs(sample_image,  min_size=800, max_size=1333):
    original_image = cv2.imread(sample_image)
    height, width = original_image.shape[:2]
    image = resize_image(original_image, min_size, max_size)
    image = image.transpose(2, 0, 1)
    inputs = {"image": image, "height": height, "width": width}
    # Sample ready
    sample_inputs = [inputs]
    return sample_inputs

if __name__ == "__main__":
    image_dir = "/Users/liubaoyang/Desktop/flowchart/output_pic/"
    out_dir = "/Users/liubaoyang/Desktop/flowchart/layout_pic/"
    for image in os.listdir(image_dir):
        if image.startswith(".DS_Store"):
            continue
        image_path = os.path.join(image_dir, image)
        output_path = os.path.join(out_dir, "output_" + image)
        model_path = "/Users/liubaoyang/Documents/YoungL/models/jockerK/layoutlmv3-onnx/jockerK/layoutlmv3-onnx/quantize_model.onnx"
        
        # 检查模型文件是否存在
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"ONNX模型文件不存在: {model_path}")
            
        inputs = get_img_inputs(image_path)
        ori_height, ori_width = inputs[0]["height"], inputs[0]["width"]
        image = inputs[0]['image']
        image = image.astype("float32")
        
        try:
            session = ort.InferenceSession(model_path, providers=['CPUExecutionProvider'])
            height, width = image.shape[1:3]
            start = time.time()
            outputs = session.run(['pred_boxes', 'labels', 'scores'], {
                "image": image
            })
            end = time.time()
            print(f"onnx model inference time: {end - start}, and output img is {output_path}")
            boxes = resize_boxes(outputs[0], (ori_width, ori_height), (width, height))
            labels = outputs[1]
            scores = outputs[2]
            # 绘制边界框
            # 读取原始图像用于绘制
            original_image = cv2.imread(image_path)
            # 设置边界框的颜色和线宽
            color = (0, 255, 0)  # 绿色
            thickness = 2
            # 遍历所有检测到的边界框
            for box, label, score in zip(boxes, labels, scores):
                # 只绘制置信度大于0.5的边界框
                if score > 0.5:
                    # 将坐标转换为整数
                    x1, y1, x2, y2 = map(int, box)
                    
                    # 绘制矩形边界框
                    cv2.rectangle(original_image, (x1, y1), (x2, y2), color, thickness)
                    
                    # 添加标签和置信度文本
                    label_text = f"Class: {label}, Score: {score:.2f}"
                    cv2.putText(original_image, label_text, (x1, y1-10), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, thickness)
            # 保存结果图像
            cv2.imwrite(output_path, original_image)

        except Exception as e:
            print(f"模型推理过程中出错: {str(e)}")