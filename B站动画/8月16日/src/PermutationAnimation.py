from manim import *
from package.ListMobject import ListMobject
from package.MovingCode import MovingCode
from package.PermutationTree import PermutationTree



from pathlib import Path

ASSETS_DIR = Path(__file__).resolve().parent.parent / "assets"
MYCODE_PATH = ASSETS_DIR / "MyCode.py"
SVG_PATH = ASSETS_DIR / "粉色小花.svg"
HAND_PATH = ASSETS_DIR / "引导小手.svg"
END_SVG_PATH = ASSETS_DIR / "wow.svg"

origin_text1 = r"""
\begin{tabular}{p{15 cm}}
\hspace{1em}
大家好,我是巷北,今天给大家带来了全排列问题回溯算法的递归可视化动画.
\end{tabular}
""" 

origin_text2 = r"""
\begin{tabular}{p{15 cm}}
\hspace{1em}
我们先看一下动画过程,再分析一下Python实现的回溯算法.
\end{tabular}
"""

origin_list_text = r"""
\begin{tabular}{p{8 cm}}
\hspace{1em}
初始列表, 初始值为[1, 2, 3, 4], 也就是我们需要获取全排列的数字.
\end{tabular}
"""

return_list_text = r"""
\begin{tabular}{p{8 cm}}
\hspace{1em}
返回结果的列表, 也就是返回1234全排列的列表.
\end{tabular}
"""

excessive_list_text = r"""
\begin{tabular}{p{8 cm}}
\hspace{1em}
过度列表,用于存储临时的排列数.不可或缺, 递归回溯的主要依据
\end{tabular}
"""

end_text = r"""
\begin{tabular{p{8 cm}}}
\hspace{1em}
上面动画展示的都是data = 1时, 排列情况, data = 2,3,4 时的排列树是类似的,时间原因就不再展示.
\end{tabular}
"""

end_text = r"""
\begin{tabular}{p{8 cm}}
\hspace{1em}
上面显示的是data=1时的动画, data = 2,3,4时的动画类似, 
时间原因不再展示(想看的我可以做个动画纯享版.)
\end{tabular}
"""
ps_text = r"""
\begin{tabular}{p{8 cm}}
\hspace{1em}
代码移动时的动画, origin\_list其实是变化的,每次递归传入的是origin\_list的副本,temp\_list.
temp\_list代表的是没有data的origin\_list.这部分动画设计好了,不过在我觉得毫不相关的地方报
错,所以直接去掉了.
\end{tabular}
"""

sanlian = r"""
\begin{tabular}{p{8 cm}}
\hspace{1em}
喜欢的给个三连吧
\end{tabular}
"""

class PermutationAnimation(MovingCameraScene):
    def construct(self):
        mycode = MovingCode(str(MYCODE_PATH))
        mycode.set(width = config.frame_width - 2)
        
        svg = SVGMobject(str(SVG_PATH))
        
        mycode.to_edge(UP*2)
        self.add(mycode)

        # 开头介绍

        tex_begin = Tex(origin_text1, origin_text2, tex_template = TexTemplateLibrary.ctex).scale(0.7)
        tex_begin.shift(DOWN*2.5)

        self.play(Write(tex_begin[0]), run_time = 5)
        self.wait(2)
        self.play(FadeOut(tex_begin[0]), run_time = 2)
        self.wait()
        self.play(Write(tex_begin[1]), run_time = 5)
        self.wait(2)
        self.clear()
        # 开头介绍结束


        p = PermutationTree(self)
        root1 = p.get_TreeNode(1)
        p.get_animation(1,iszoomed=False)
        # 展开动画
        line = p.get_Branch()
        subtree1 = VGroup(line, root1)
        subtree2 = VGroup(line.copy(), p.get_TreeNode(2))
        subtree3 = VGroup(line.copy(), p.get_TreeNode(3))
        subtree4 = VGroup(line.copy(), p.get_TreeNode(4))

        tree = VGroup(subtree1, subtree2, subtree3, subtree4)
        tree.arrange(RIGHT, buff = 1)
        tree.set(width = config.frame_width - 1)

        big_root = p.get_TreeNode()
        big_line = p.get_Branch()
        big_tree = VGroup(big_line, big_root)

        self.add(big_tree)
        self.play(ReplacementTransform(big_tree, tree[0]), run_time = 2)
        self.wait()

        self.play(FadeIn(tree[1]),FadeIn(tree[2]), FadeIn(tree[3]), run_time = 3)
        self.wait(4)

        self.play(ReplacementTransform(tree, mycode), run_time = 1)
        self.wait(2)
        # 设计参考矩形

        # 初始阶段矩形参考
        reference_rec1 = Rectangle()
        reference_rec1.set(height = 3.2)
        reference_rec1.stretch_to_fit_width(5)
        reference_rec1.to_corner(DL, buff = 0)

        reference_rec2 = reference_rec1.copy()
        reference_rec2.stretch_to_fit_width(9.2)
        reference_rec2.to_corner(DR, buff = 0)
        # self.add(reference_rec1, reference_rec2)
        
        # # 代码讲解矩形参考
        # mycode.to_edge(UP,buff = 0)
        # reference_rec1.stretch_to_fit_height(4.2)
        # reference_rec1.to_corner(DL, buff = 0)

        # reference_rec2.stretch_to_fit_height(4.2)
        # reference_rec2.to_corner(DR, buff = 0)
        # 设计参考矩形结束


        # 介绍参数含义

        # 介绍origin_list
        _origin_list = Text("origin_list")
        _origin_list.move_to(reference_rec1.get_center())
        _origin_list_introduce = Tex(origin_list_text, tex_template = TexTemplateLibrary.ctex).scale(0.7).move_to(reference_rec2.get_center())

        hand = SVGMobject(str(HAND_PATH)).scale(0.4)
        hand.shift(UP*3.3+LEFT*2)

        # hand.shift(RIGHT*2.5)
        # hand.shift(RIGHT*2.7)
        
        self.play(Create(hand), Create(_origin_list), run_time = 2)
        self.wait(0.5)
        self.play(Write(_origin_list_introduce), run_time = 4.5)
        self.wait(4)
        
        # 设计return_list
        _return_list = Text("return_list").match_style(_origin_list).move_to(_origin_list.get_center())
        _return_list_introduce = Tex(return_list_text, tex_template = TexTemplateLibrary.ctex).match_style(_origin_list).scale(0.7).move_to(_origin_list_introduce.get_center())

        self.play(
            ReplacementTransform(_origin_list, _return_list), 
            hand.animate.shift(RIGHT*2.5), 
            ReplacementTransform(_origin_list_introduce, _return_list_introduce), 
            run_time = 3.5
        )
        self.wait(6.5)

        # 设计excessive_list
        _excessive_list = Text("excessive_list").match_style(_origin_list).move_to(_origin_list.get_center())
        _excessive_list_introduce = Tex(excessive_list_text, tex_template = TexTemplateLibrary.ctex).match_style(_origin_list).scale(0.7).move_to(_origin_list_introduce.get_center())

        self.play(
            ReplacementTransform(_return_list, _excessive_list),
            hand.animate.shift(RIGHT*2.7),
            ReplacementTransform(_return_list_introduce, _excessive_list_introduce),
            run_time = 3.5
        )
        self.wait(6.5)

        self.play(
            FadeOut(hand),
            FadeOut(_excessive_list),
            FadeOut(_excessive_list_introduce),
            run_time = 1.5
        )
        self.play(
            mycode.animate.to_edge(UP, buff = 0)
        )

        # 代码讲解矩形参考
        # mycode.to_edge(UP,buff = 0)
        reference_rec1.stretch_to_fit_height(4.2)
        reference_rec1.to_corner(DL, buff = 0)

        reference_rec2.stretch_to_fit_height(4.2)
        reference_rec2.to_corner(DR, buff = 0)
        self.wait(1.5)
        # 代码讲解结束


        # 将三个列表弄好

        # self.add(reference_rec1,reference_rec2)
        ori_list = Text("origin_list:")
        ori_list.move_to(reference_rec1.get_top())
        ori_list.scale(0.5)
        ori_list.shift(LEFT*1.3+DOWN*1.3)
        listmobject = ListMobject()
        ori_mob = listmobject.get_list_Mobject()
        ori_mob.scale(0.7)
        ori_mob.next_to(ori_list, RIGHT, buff = 0.5)

        exc_listmobject = ListMobject(origin_list=[0,0,0,0])
        exc_list = Text("excessive_list:")
        exc_list.scale(0.5)
        exc_list.move_to(ori_list.get_center())
        exc_list.shift(DOWN*1.3)
        exc_mob = exc_listmobject.get_list_Mobject()
        exc_mob.scale(0.7)
        exc_mob.next_to(exc_list, RIGHT, buff = 0.5)
        exc_mob.align_to(ori_mob, LEFT)

        # ret_list = Text("return_list:")
        # ret_list.scale(0.5)
        # ret_list.move_to(exc_list.get_center())
        # ret_list.shift(DOWN)
        # ret_tex = Text("[]").scale(0.7)
        # ret_tex.next_to(ret_list,RIGHT, buff = 0.5)
        # ret_tex.align_to(ori_mob, LEFT)

        # self.add(ori_list, ori_mob, exc_list, exc_mob, ret_list, ret_tex)
        self.play(
            Create(ori_list),
            Create(ori_mob),
            Create(exc_list),
            Create(exc_mob),
            # Create(ret_list),
            # Create(ret_tex),
            run_time = 1.7
        )
        self.wait(2.3)
        # 三个列表结束
        # llll = [1]

        # exc_listmobject.change_number_animation(self, llll)


        # 代码讲解
        pp = PermutationTree(self, listmobject = exc_listmobject)
        little_root1 = pp.get_TreeNode(1, reference_rec2.height)
        # little_branch = pp.get_Branch().move_to(reference_rec2.get_center())

        little_root1.move_to(reference_rec2.get_center())
        # self.play(Create(little_branch), Create(little_root1))

        # self.play(Create(moving_rect), Create(moving_svg))
        moving_svg = mycode.get_svg(1, svg)
        moving_rect = mycode.get_rect(1)
        self.play(
            Create(moving_rect),
            Create(moving_svg),
        )
        self.wait(0.2)
        self.play(
            mycode.transform_svg(moving_svg, 2),
            mycode.transform_remark_rectangle(moving_rect, 2),
        )
        self.wait(0.2)
        self.play(
            mycode.transform_remark_rectangle(moving_rect, 6),
            mycode.transform_svg(moving_svg, 6),
        )
        self.wait()
        
        pp.get_animation1(1, False, moving_svg, moving_rect,mycode)
        # p = PermutationTree(self)
        # _tree = p.get_TreeNode(1, reference_rec2.height)
        # branch = p.get_Branch().move_to(reference_rec2.get_center())
        # _tree.move_to(reference_rec2.get_center())
        # self.play(Create(branch), Create(_tree))
        # print(reference_rec2.height)

        # 结束动画
        
        self.clear()
        self.wait()

        _end_text = Tex(end_text, tex_template = TexTemplateLibrary.ctex)
        _ps_text = Tex(ps_text, tex_template = TexTemplateLibrary.ctex)
        _sanlian = Tex(sanlian, tex_template = TexTemplateLibrary.ctex)
        self.play(
            Write(_end_text),
            run_time = 5
        )
        self.wait(6)
        self.play(FadeOut(_end_text),run_time = 1.5)
        self.wait()

        self.play(
            Write(_ps_text),
            run_time = 5
        )
        self.wait(7)
        self.play(FadeOut(_ps_text), run_time = 1.5)
        self.wait()
        
        end_svg = SVGMobject(str(END_SVG_PATH))
        end_grps = VGroup(_sanlian, end_svg)
        end_grps.arrange(RIGHT, buff = 0.5)

        self.play(
            Write(_sanlian),
            Create(end_svg),
            run_time = 1.5
        )
        self.wait(3)