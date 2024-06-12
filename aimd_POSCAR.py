import os
import numpy as np
from ase.io import read, write
from tqdm import tqdm

# 读取XDATCAR文件并创建POSCAR文件
def create_poscar_files():
    trajectory = read('XDATCAR', index=':', format='vasp-xdatcar')

    if not os.path.exists('POSCARs'):
        os.makedirs('POSCARs')

    # 使用tqdm来显示进度条
    for i, atoms in enumerate(tqdm(trajectory, desc='Processing frames', unit='frame')):
        write(f'POSCARs/POSCAR-{i}.vasp', atoms, format='vasp')

# 从目录中按等间距选取指定个数的文件
def select_files(directory, num_files, start_index):
    all_poscars = sorted([f for f in os.listdir(directory) if f.startswith('POSCAR-') and f.endswith('.vasp')])
    if start_index < 1 or start_index > len(all_poscars):
        raise ValueError("开始索引超出范围")
    all_poscars = all_poscars[start_index-1:]
    selected_indices = np.linspace(0, len(all_poscars) - 1, num_files, dtype=int, endpoint=True)
    return [all_poscars[i] for i in selected_indices]

# 主程序
def main():
    # 首先创建POSCAR文件
    create_poscar_files()

    # 用户输入
    num_to_select = int(input("输入抽取构型个数："))
    start_index = int(input("输入从第几个构型开始："))

    # 原POSCAR文件夹
    source_dir = 'POSCARs'
    # 目标文件夹
    target_dir = 'AIMD_POSCAR'
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    # 选择文件
    selected_poscars = select_files(source_dir, num_to_select, start_index)

    # 复制和重命名选定的POSCAR文件
    for poscar_file in tqdm(selected_poscars, desc='Copying selected POSCARs', unit='file'):
        old_path = os.path.join(source_dir, poscar_file)
        new_path = os.path.join(target_dir, f'SPOSCAR-{start_index}')
        atoms = read(old_path, format='vasp')
        write(new_path, atoms, format='vasp')
        start_index += 1  # Increment the index for naming

    print(f"成功抽取并重命名{num_to_select}个构型到目录{target_dir}.")  # 修正错误的变量名

# 运行主程序
if __name__ == "__main__":
    main()
