import os
import shutil

def organize_files(a_dir, b_dir):
    """
    根据文件命名规则，将 a_dir 下的文件移动到 b_dir 中对应的子文件夹中。
    文件名格式： a_b_c.xxx，其中 a 和 c 部分可能包含下划线，
    b 为纯数字且唯一，且不在文件名的开头或结尾。
    目标文件夹名格式：如果包含空格，则取空格前的部分作为前缀；否则使用整个名称。
    """
    # 构建目标文件夹映射：前缀 -> 文件夹全路径
    b_folders = {}
    for entry in os.listdir(b_dir):
        full_path = os.path.join(b_dir, entry)
        if os.path.isdir(full_path):
            prefix = entry.split(" ", 1)[0] if " " in entry else entry
            b_folders[prefix] = full_path

    # 遍历 a_dir 下所有文件进行移动
    for file in os.listdir(a_dir):
        file_path = os.path.join(a_dir, file)
        if os.path.isfile(file_path):
            filename_no_ext, ext = os.path.splitext(file)
            tokens = filename_no_ext.split('_')
            # 找出所有纯数字的部分（对应 b）
            numeric_indices = [i for i, token in enumerate(tokens) if token.isdigit()]
            if len(numeric_indices) >= 1:
                i = numeric_indices[0]
                if i == 0 or i == len(tokens) - 1:
                    print(f"文件 {file} 格式不符合要求（a或c部分为空），跳过")
                    continue
                a_prefix = "_".join(tokens[:i])
                if a_prefix in b_folders:
                    destination = os.path.join(b_folders[a_prefix], file)
                    shutil.move(file_path, destination)
                    print(f"已将 {file} 移动到 {b_folders[a_prefix]}")
                else:
                    print(f"未找到前缀为 {a_prefix} 的目标文件夹，跳过 {file}")
            else:
                print(f"文件 {file} 格式不符合要求（未找到唯一的纯数字b部分），跳过")

    # 检查目标文件夹下是否存在子文件夹并打印
    print("\n以下目标文件夹存在子文件夹：")
    for entry in os.listdir(b_dir):
        folder_path = os.path.join(b_dir, entry)
        if os.path.isdir(folder_path):
            subfolders = [d for d in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, d))]
            if subfolders:
                print(entry)