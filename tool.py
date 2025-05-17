import os
import cv2
import torchvision.transforms as transforms
from PIL import Image

def process_images(input_dir, output_dir):
    # 定义处理流程
    process = transforms.Compose([
        transforms.ToPILImage(),
        transforms.Resize(512, interpolation=Image.Resampling.BILINEAR),
        transforms.CenterCrop(512),
        transforms.ToTensor(),
    ])

    # 遍历输入目录
    for root, dirs, files in os.walk(input_dir):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
                # 构建路径
                src_path = os.path.join(root, file)
                rel_path = os.path.relpath(src_path, input_dir)
                dest_path = os.path.join(output_dir, rel_path)
                
                # 创建目标目录
                os.makedirs(os.path.dirname(dest_path), exist_ok=True)

                try:
                    # 读取图像并转换颜色通道
                    img = cv2.imread(src_path)
                    if img is None:
                        raise ValueError(f"无法读取图像文件：{src_path}")
                    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

                    # 应用处理流程
                    tensor = process(img)
                    
                    # 转换回PIL图像并保存
                    transforms.ToPILImage()(tensor).save(dest_path)
                    print(f"处理成功: {src_path} -> {dest_path}")

                except Exception as e:
                    print(f"处理失败: {src_path} - 错误: {str(e)}")

if __name__ == "__main__":
    input_directory = "/workspace/datasets/SD_Rest/train"  # 替换为输入目录
    output_directory = "/workspace/datasets/SD_Rest/new_train" # 替换为输出目录
    
    process_images(input_directory, output_directory)
