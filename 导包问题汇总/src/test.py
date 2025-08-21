from manim import *
from package.AlgorithmBanner import AlgorithmBanner 
# 从src包中导入package包中文件, 只需要用package.访问就好. 如果src中还有包, 那就不清楚了.

class Test(Scene):
    def construct(self):
        a = AlgorithmBanner()
        self.play(Create(a))
        self.wait()
        self.play(a.expand())
        self.wait(3)