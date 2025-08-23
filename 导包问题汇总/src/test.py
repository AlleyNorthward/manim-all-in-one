from manim import *
# 注意, 下列语句不是必须的, 当且仅当想在test中运行manim时添加. 调用命令: manim .\srt\test.py -pqm
# 正常情况下, 这test命令行, 输入 python .\src\test.py , 输出__name__, 是__main__,不过通过
# manim运行, manim .\src\test.py -pqm, __name__,就不是__main__, 虽然我么主观上认为test.py文件是主
# 文件, 但是, 实际上python仍然认为是个包, 无法导入package, 所以添加下面导入, 是为了方便我们在test中
# debug的, 不过不影响main中运行
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from package.AlgorithmBanner import AlgorithmBanner 

class Test(Scene):
    def construct(self):
        a = AlgorithmBanner()
        self.play(Create(a))
        self.wait()
        self.play(a.expand())

        self.wait(3)
