from manim import*
#_说明
"""
    怎么说呢,下面是传参举例
    对于set_color_by_gradient,传入的是*colors
    位置传参,从解包角度理解,相当于一个一个传入,这也是问题所在,
    一个一个传没有效果,相反,[]列表传入可以显示.
    回溯看了之后,发现,理论上就应该一个一个传,[]传反而
    不行.可是从表现上来看,恰恰相反.那么问题出现在了哪里呢??
    先暂存一下吧...

    
"""
class Test(Scene):
    def construct(self):
        self.test("1", "2", "3", "4")
    def test(self, *colors):
        print(colors)
        print(*colors)
        self.test2(*colors)

    def test2(self, *colors):
        print(colors)
        print(*colors)


