from pathlib import Path
import os

# # 方法1
# ASSETS_DIR1 = Path(__file__).resolve()
# print(ASSETS_DIR1) # F:\0项目模拟\数据结构可视化\源代码存储\package\路径分析.py

# ASSETS_DIR1 = ASSETS_DIR1.parent
# print(ASSETS_DIR1) # F:\0项目模拟\数据结构可视化\源代码存储\package

# ASSETS_DIR1 = ASSETS_DIR1.parent
# print(ASSETS_DIR1) # F:\0项目模拟\数据结构可视化\源代码存储

# ASSETS_DIR1 = ASSETS_DIR1 / "assets"

# print(ASSETS_DIR1) # F:\0项目模拟\数据结构可视化\源代码存储\assets


# 方法2

# ASSETS_DIR2 = Path().cwd()

# 方法3

# ASSETS_DIR3 = Path(os.getcwd())

# 方法1 最靠谱, 方法2、3显示不是当前路径, 可能存在危险.