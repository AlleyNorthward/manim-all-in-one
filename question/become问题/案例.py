from manim import *

class SingleNode_scene(Scene):
    # 说明

    """
        @auther 巷北
        @time 2025.9.27 12:15
        我们无法改变submobjects内部结构,所以下面的所有的print
        都是一样的.我们的交换,只是动画中显示的交换,become也只是
        改变了其引用对象,但是输出v.submobject却无变化.
        然而,这没有任何影响.目前我们交换的是不同对象,没有修改方案.
        我们可以通过删除v,清空场景,创建新v,来显式地改变其submobject,
        从而使得其输出与我们目标样式保持一致.
        如果是采用结点的方式,我们可以专门使用value来表示当前节点的数值,
        become后,再显示地set_value,从而达到更新submobject,来保持其与
        目标顺序一致.
    """
    def construct(self):
        self.camera.background_color = "#cee"
        s = Square()
        c = Circle()
        t = Triangle()
        star = Star()
        basic = [s,c,t,star]
        v = VGroup(*basic).arrange(RIGHT, buff = 0)
        print(v.submobjects)

        self.add(v)
        base = v[0].save_state()
        target = v[1].save_state()
        self.play(
            base.animate.move_to(target.get_center()),
            target.animate.move_to(base.get_center())
        )
        print(v.submobjects)

        # 方式一 缺点:submobject无法更新
        # base.become(target.saved_state).move_to(base.saved_state.get_center())
        # target.become(base.saved_state).move_to(target.saved_state.get_center())

        # 方式二 缺点:速度偏慢
        del v
        self.remove(s)
        basic[0], basic[1] = basic[1], basic[0]
        v = VGroup(*basic).arrange(RIGHT, buff = 0)

        print(v.submobjects)
        base = v[1].save_state()
        target = v[2].save_state()
        self.play(
            base.animate.move_to(target.get_center()),
            target.animate.move_to(base.get_center())
        )
        print(v.submobjects)
