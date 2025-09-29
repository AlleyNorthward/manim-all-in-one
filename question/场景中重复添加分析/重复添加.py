from manim import(
    Scene, Rectangle, Circle,
)
class RepeatAdding(Scene):
    """
        @auther: 巷北
        @time: 2025.9.11
        重复添加会存在什么问题?

        wait()会产生Mobject占位.重复添加仍然会将mobject添加到场景只不过静帧不会调用,动画产生时,才会调用渲染机制
        重复添加,但仍然会去重.
        如下,self.mobjects应该是[M,R,C],不去重的话,实际上是[M,R,C,R,C]
        去重是去除前面重复的,所以显示为[M,R,C]
        将wait()添加到中间,可以看看输出结果.理应是[R,C,M,R,C]去重后为[M,R,C],并不是[R,M,C],所以多次使用add()
        确实会重复添加,但manim底层仍有去重机制,防止重复渲染,浪费时间.
        将wait()添加到最后,发现结果是[R,C,M],复合预期.

        最明显的是将r,c换个位置,就能发现r在c的上面了,再次论证我们上面所说.
    """
    def construct(self):
        
        r = Rectangle().scale(1.2)
        c = Circle().scale(2)
        # self.wait()
        self.add(r,c)
        # self.wait()
        self.add(r,c)

        self.add(c, r)

        self.wait()
        print(self.mobjects)
        print(self.static_mobjects)
        print(self.moving_mobjects)
        print(self.animations)
        print(self.get_attrs())
        print(self.get_mobject_family_members())