from manim import *
from src.test import Test  # 这里是导入源代码, 如果只导入import src这个包, 我们需要在src的__init__中,导入所有的类, 就像8月16动画那样 

class A(Test):
    def construct(self):
        return super().construct()
    