import os
import argparse
import sys

def main():
    # 设置命令行参数解析
    parser = argparse.ArgumentParser(description='删除文件夹B中不在A中的PNG图片')
    parser.add_argument('folder_a', help='文件夹A的路径')
    parser.add_argument('folder_b', help='文件夹B的路径')
    parser.add_argument('--yes', '-y', action='store_true', help='直接确认删除，无需交互')
    args = parser.parse_args()

    # 获取文件夹A中的.png文件名（区分大小写）
    a_files = set()
    for f in os.listdir(args.folder_a):
        if f.lower().endswith('.png'):
            a_files.add(f)

    # 获取文件夹B中的.png文件名
    b_files = set()
    for f in os.listdir(args.folder_b):
        if f.lower().endswith('.png'):
            b_files.add(f)

    # 计算需要删除的文件
    to_delete = b_files - a_files
    if not to_delete:
        print("没有需要删除的文件。")
        sys.exit(0)

    # 显示即将删除的文件列表
    print(f"发现 {len(to_delete)} 个待删除文件：")
    for idx, filename in enumerate(sorted(to_delete), 1):
        print(f"  {idx}. {filename}")

    # 确认删除
    if not args.yes:
        answer = input("是否确认删除？(y/N): ").strip().lower()
        if answer != 'y':
            print("操作已取消。")
            sys.exit(0)

    # 执行删除操作
    deleted_count = 0
    for filename in to_delete:
        file_path = os.path.join(args.folder_b, filename)
        try:
            os.remove(file_path)
            deleted_count += 1
            print(f"已删除: {file_path}")
        except Exception as e:
            print(f"删除失败【{file_path}】: {str(e)}")

    print(f"操作完成，成功删除 {deleted_count}/{len(to_delete)} 个文件。")

if __name__ == "__main__":
    main()
