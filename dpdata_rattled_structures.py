#!/usr/bin/env python 
# coding: utf-8
from dpdata import LabeledSystem,MultiSystems
import os 
import dpdata
import shutil

def GetFileFromThisRootDir(dir,ext = None):
    allfiles = []
    needExtFilter = (ext != None)
    for root,dirs,files in os.walk(dir):
        for filespath in files:
            #filepath = os.path.join(root, filespath)
            filepath = os.path.join( filespath)
            extension = os.path.splitext(filepath)[1][1:]
            if needExtFilter and extension in ext:
                allfiles.append(filepath)
            elif not needExtFilter:
                allfiles.append(filepath)
    return allfiles
def del_folder(filepath):
    """
    删除某一目录下的所有文件或文件夹
    :param filepath: 路径
    :return:
    """
    del_list = os.listdir(filepath)
    for f in del_list:
        file_path = os.path.join(filepath, f)
        if os.path.isfile(file_path):
            os.remove(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
# 转换文件格式和编码方式
structure_name_list = GetFileFromThisRootDir( "./input/")
if os.path.exists('./output_structure')==False:
    os.mkdir('./output_structure')
else:
    del_folder('./output_structure')
print("每个构型扰动生成多少帧构型! ")
num_frame = int(input(""))
print("晶胞扰动的幅度! ")
cell_pert_fraction = float(input(""))
print("原子距离扰动的幅度,单位埃! ")
atom_pert_distance = float(input(""))
for structure_name in structure_name_list:
    print(structure_name)
    perturbed_system = dpdata.System('./input/'+structure_name,fmt="vasp/poscar").perturb(pert_num=num_frame, 
        cell_pert_fraction=cell_pert_fraction, 
        atom_pert_distance=atom_pert_distance, 
        atom_pert_style='normal')#normal-正态分布 uniform-限定长度均匀散点 const-常数
    for i in range(num_frame):
        perturbed_system.to('vasp/poscar','./output_structure/' +structure_name+"-"+str(i+1),frame_idx=i)
