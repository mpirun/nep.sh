#!/usr/bin/env python
# coding: utf-8

from ase import Atom, Atoms
from ase.io import read
from pynep.calculate import NEP

import glob
import os
import re
from sys import argv

order = int(argv[1])

if order == 2:
    poscars = glob.glob('POSCAR-*')
elif order == 3:
    poscars = glob.glob('3RD.POSCAR.*')
elif order == 4:
    poscars = glob.glob('4TH.POSCAR.*')
elif order == 5:
    files = os.listdir()

    for filename in files:
        if filename.startswith('disp') and filename.endswith('.POSCAR'):
            match = re.search(r'\d+', filename)
            if match:
                number_part = match.group()
                new_filename = f'disp-POSCAR-{number_part}'
                
                # 构建源文件和目标文件的完整路径
                source_path = os.path.abspath(filename)
                target_path = os.path.join(os.getcwd(), new_filename)

                # 执行文件重命名操作
                os.rename(source_path, target_path)

    poscars = glob.glob('disp-POSCAR-*')





import subprocess
import shutil
if not os.path.exists('poscars'):
    os.makedirs('poscars')
else:
    shutil.rmtree('poscars')
    os.makedirs('poscars')
if order==2:
    subprocess.call('mv POSCAR-* poscars', shell=True)
elif order==3:
    subprocess.call('mv 3RD.POSCAR.* poscars', shell=True)
elif order==4:
    subprocess.call('mv 4TH.POSCAR.* poscars', shell=True)
elif order==5:
    subprocess.call('mv disp-POSCAR-* poscars', shell=True)

if not os.path.exists('vaspruns'):
    os.makedirs('vaspruns')
else:
    shutil.rmtree('vaspruns')
    os.makedirs('vaspruns')

def write_vasprun(file_name, forces):
    """ Writes dummy vasprun file with only forces """

    f = open(file_name, 'w')
    f.write('<?xml version="1.0" encoding="ISO-8859-1"?>\n')
    f.write('<modelling>\n')

    f.write(' <generator>\n')
    f.write('  <i name="version" type="string">4.6.35 </i>\n')
    f.write('</generator>\n')

    f.write(' <calculation>\n')
    f.write('   <structure>\n')
    f.write(' <varray name="positions" >\n')
    f.write('      </varray>\n')
    f.write('   </structure>\n')


    f.write('  <varray name="forces" >\n')
    for force in forces:
        f.write('  <v>%16.12f   %16.12f   %16.12f </v>\n'
                % (force[0], force[1], force[2]))
    f.write('  </varray>\n')

    f.write('    <energy>\n')
    f.write('     <i name="e_fr_energy">   0.000 </i>\n')
    f.write('     <i name="e_wo_entrp">   0.000 </i>\n')
    f.write('     <i name="e_0_energy">   0.000 </i>\n')
    f.write('    </energy>\n')

    f.write(' </calculation>\n')
    f.write('</modelling>\n')

    f.close()

calc = NEP('nep.txt')
for poscar in poscars:
    if order==2:
        poscar_number = poscar.split('-')[-1]
    elif order==3:
        poscar_number = poscar.split('.')[-1]
    elif order==4:
        poscar_number = poscar.split('.')[-1]
    elif order==5:
        poscar_number = poscar.split('-')[-1]
    vasprun_name = 'vasprun.xml-%s' % poscar_number
    atoms = read('./poscars/' + poscar)
    atoms.set_calculator(calc)
    forces = atoms.get_forces()
    write_vasprun(os.path.join('./vaspruns/', vasprun_name), forces)






if order == 5:
    poscar_folder = 'poscars'
    vasprun_folder = 'vaspruns'

    # 获取poscar文件列表
    poscar_files = [filename for filename in os.listdir(poscar_folder) if filename.startswith('disp-POSCAR-')]

    # 处理每个POSCAR文件
    for poscar_filename in poscar_files:
        # 构建POSCAR文件和vasprun.xml文件的完整路径
        poscar_path = os.path.join(poscar_folder, poscar_filename)
        vasprun_number = poscar_filename.replace('disp-POSCAR-', '').replace('.POSCAR', '')
        vasprun_filename = f'vasprun.xml-{vasprun_number}'
        vasprun_path = os.path.join(vasprun_folder, vasprun_filename)

        # 打开POSCAR文件并读取第九行及其之后的数据
        with open(poscar_path, 'r') as poscar_file:
            data_lines = poscar_file.readlines()[8:]  # 从第九行开始读取数据

        # 格式化每一行数据
        formatted_lines = [f'<v> {line.strip()} </v>\n' for line in data_lines]

        # 打开vasprun.xml文件并读取已有内容
        with open(vasprun_path, 'r') as vasprun_file:
            existing_lines = vasprun_file.readlines()

        # 将格式化后的数据插入到第八行之后
        existing_lines[8:8] = formatted_lines

        # 写入更新后的内容回vasprun.xml文件
        with open(vasprun_path, 'w') as vasprun_file:
            vasprun_file.writelines(existing_lines)





