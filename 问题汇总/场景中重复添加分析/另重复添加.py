from manim import(
    Scene,
    Rectangle, Circle,Ellipse, BLUE,
    FadeIn,Write
)
class Testing(Scene):
    """
        @auther: 巷北
        @time: 2025.9.11
        在self.play()中使用Add(),与self.add(),有区别吗?

        下面两种Add()方式效果类似,不同是如果将c,r放在同一个Add中,manim底层会包装
        成一个Group()统一管理.而后面的就不用

        测试
        ①同一play中添加Add                                   符合层级结构.满足预期.无问题发生.
        ②同一play中Add中添加多对象                            同上 不过输出self.mobjects时Group覆盖二者
        ③同一play中Add中添加多对象并重复添加Add               底层添加与self.add()一致
        ④两个play重复测试上面情况                             问题在下面说了,但也符合预期.  
        ⑤play中Add与self.add对比分析                         问题也在下面说了.
        ⑥Add整体后,在重复产生对象动画.                        由于通过Add()添加到场景了,并且组合成Group了,动画不会再重复添加到场景,所以层级结构不会以再添加动画而改变
        ⑦self.add重新测试⑥                                   self.add不论静帧还是动帧,播放后都不改变层级结构,跟上面类似.

        总结 
        这么来看,self.add 和 Add作用一样.
        但是对于复杂Mobject来说,其层级结构受组的影响.
        这也是主要问题所在,一般情况下不会发生,但发生后需要有解决处理方案.

        最后找到问题在哪了,AnimationGroup与Add可能存在问题。
        最安全的方法是每创建一个对象，就self.add()这个对象在场景中,这个是最安全的
        另外,觉得麻烦,可以将scene作为参数传入对象中,每初始化结束,就scene.add()添加到场景中
        这样也可以.
        我觉得创建mobject,直接将scene作为参数传入吧，靠谱点。
    """
    def construct(self):
        
        r = Rectangle().scale(1.2)
        c = Circle().scale(2)
        e = Ellipse().scale(3).set_color(BLUE)
        # self.play(Add(c,r), run_time = 2)
        # self.play(Add(c), Add(r),run_time = 2)

        # 测试①
        # self.play(
        #     FadeIn(c),
        #     FadeIn(e),
        #     Add(r),
        # )

        # 测试②
        # self.play(
        #     Add(e,r),
        #     FadeIn(c),
        # )

        # 测试③
        # self.play(
        #     Add(e,r),
        #     FadeIn(c),
        #     Add(e,r),
        # )

        # 测试④
        # self.play(
        #     FadeIn(c),
        # )
        # self.play(FadeIn(c))# 正常

        # self.play(Add(c,r), FadeIn(e))
        # print(self.mobjects)
        # print(self.static_mobjects)
        # print(self.moving_mobjects)
        # print(self.animations)
        # print(self.get_attrs())
        # print(self.get_mobject_family_members())
        # self.play(Add(r,c), run_time = 2)# 突越,层级突然变化. 对比输出就能看出来


        # 测试⑤ 
        # self.add(r,c,e)
        # print(self.mobjects)
        # print(self.static_mobjects)
        # print(self.moving_mobjects)
        # print(self.animations)
        # print(self.get_attrs())
        # print(self.get_mobject_family_members())
        # self.play(Add(r,c,e), run_time = 2)   # 可以看到,总会包装成组

        # self.add(r,c,e)
        # print(self.mobjects)
        # print(self.static_mobjects)
        # print(self.moving_mobjects)
        # print(self.animations)
        # print(self.get_attrs())
        # print(self.get_mobject_family_members())
        # self.play(Add(e,c,r), run_time = 2) # 此时可以看到, 以play Add为主

        # self.add(r,c,e)
        # self.wait()
        # self.play(Add(e,c,r),run_time = 2) # 此时有突越,说明静帧add对Add无影响,但要是添加wait变成动帧后,会产生影响

        # self.play(Add(e,c,r), run_time = 2)
        # self.add(r,c,e)

        # self.play(Add(e,c,r), run_time = 2)
        # self.add(r,c,e)
        # self.wait(2)  # 此时很明显能得出结论, self.play(Add(),run_time = 2) 几乎等价于 self.add() wait(2)但如果静帧self.add(),对play无影响.区别就是是否包装成组.


        # 测试⑥

        # self.play(
        #     Add(c,e,r),
        #     Write(e),
        #     FadeIn(c)
        # )

        # 测试⑦
        self.add(c,e,r)
        # self.wait()
        self.play(FadeIn(e))
        print(self.mobjects)
        print(self.static_mobjects)
        print(self.moving_mobjects)
        print(self.animations)
        print(self.get_attrs())

        print(self.get_mobject_family_members())
