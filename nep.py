#!/usr/bin/env python
# coding: utf-8


import matplotlib.pyplot as plt
import numpy as np


# 设置全局坐标轴标签大小和刻度大小
plt.rcParams['axes.labelsize'] = 14
plt.rcParams['xtick.labelsize'] = 16
plt.rcParams['ytick.labelsize'] = 16

# 创建2x2子图布局
fig, axs = plt.subplots(2, 2, figsize=(10, 8), constrained_layout=True)

# 加载数据
loss = np.loadtxt('loss.out')
force_test = np.loadtxt('force_train.out')
virial_test = np.loadtxt('virial_train.out')
energy_test = np.loadtxt('energy_train.out')

# 第1个子图：绘制loss数据
axs[0, 0].loglog(loss[:, 1:4], linewidth=2)
axs[0, 0].loglog(loss[:, 4:6], linewidth=2)
axs[0, 0].loglog(loss[:, 6], linewidth=2)
axs[0, 0].set_xlabel('Generation/200')
axs[0, 0].set_ylabel('Loss')
axs[0, 0].legend(['Total', 'L1-Reg', 'L2-Reg', 'Energy-train', 'Force-train', 'Virial-train'], loc='lower left')
axs[0, 0].set_title('loss.out',fontsize=16)

# 第2个子图：绘制energy散点图
axs[0, 1].plot(energy_test[:, 1], energy_test[:, 0], 'o', markersize=6)
diagonal_line = [min(energy_test[:, 0].min(), energy_test[:, 1].min()),
                 max(energy_test[:, 0].max(), energy_test[:, 1].max())]
axs[0, 1].plot(diagonal_line, diagonal_line, '-', color='orange', linewidth=2, label='Ideal: y=x')
axs[0, 1].set_xlabel('DFT Energy (eV/atom)')
axs[0, 1].set_ylabel('Predicted Energy (eV/atom)')
axs[0, 1].set_title('energy_train.out',fontsize=16)
axs[0, 1].legend()

# 第3个子图：绘制force散点图
for i, label in enumerate(['x direction', 'y direction', 'z direction']):
    axs[1, 0].plot(force_test[:, i + 3], force_test[:, i], '.', label=label)
diagonal_line = [min(force_test[:, :3].flatten()), max(force_test[:, :3].flatten())]
axs[1, 0].plot(diagonal_line, diagonal_line, '-', color='orange', label='Ideal: y=x')
axs[1, 0].set_xlabel('DFT Force (eV/Å)')
axs[1, 0].set_ylabel('Predicted Force (eV/Å)')
axs[1, 0].set_title('force_train.out',fontsize=16)
axs[1, 0].legend()

# 第4个子图：绘制virial散点图
for i in range(6):
    axs[1, 1].plot(virial_test[:, i + 6], virial_test[:, i], '.', label=f'Component {i+1}')
diagonal_line = [min(virial_test[:, :6].flatten()), max(virial_test[:, :6].flatten())]
axs[1, 1].plot(diagonal_line, diagonal_line, '-', color='orange', label='Ideal: y=x')
axs[1, 1].set_xlabel('DFT Virial (eV/atom)')
axs[1, 1].set_ylabel('Predicted Virial (eV/atom)')
axs[1, 1].set_title('virial_train.out',fontsize=16)
axs[1, 1].legend()
for ax in axs.flat:  # axs.flat将二维数组扁平化处理，可以让我们迭代所有子图
    for axis in ['top', 'bottom', 'left', 'right']:
        ax.spines[axis].set_linewidth(2)  # 设置边框宽度为2



plt.savefig('nep.png')
print("成功生成 nep.png")
