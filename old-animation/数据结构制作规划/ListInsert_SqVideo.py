from manim import (
    TexTemplateLibrary, Tex, SVGMobject, Rectangle, DecimalTable,
    FadeIn, FadeOut, FocusOn, AnimationGroup, Succession,Write, ReplacementTransform, Wiggle, Restore, Create,
    UP, DOWN, LEFT, UL, RIGHT,
    TEAL, BLACK, MAROON, RED,
    Scene,
    PI,
)

from .VideoText import VideoText
from ..MovingCode import MovingCode
from ..ListNode import ListNode
from ..MyCurvedLine import MyCurvedLine

from pathlib import Path
ASSETS_DIR = Path(__file__).resolve().parent.parent.parent / "assets"

class ListInsert_SqVideo:
    def __init__(
            self,
            scene: Scene,
    ):
        self.scene = scene
        self.total_text = VideoText()

        PATH_SQ = ASSETS_DIR / "展示代码" / "5ListInsert_Sq.cpp"
        PATH_SQ2 = ASSETS_DIR / "展示代码" / "5ListInsert_Sq2.cpp"
        PATH_SQ3 = ASSETS_DIR / "展示代码" / "5ListInsert_Sq3.cpp"
        self.movingcode2 = MovingCode(PATH_SQ2).set(width = self.scene.camera.frame_width - 3).to_edge(UP, buff = 0.1)
        self.movingcode3 = MovingCode(PATH_SQ3).scale(0.8).to_edge(UP, buff = 0.3)
        self.movingcode1 = MovingCode(PATH_SQ)
        self.movingcode1.set(width = self.scene.camera.frame_width - 3).to_edge(UP, buff = 0.1)


    def first_scene(self):
        Infos = [
            "e_0",
            "e_1",
            r"\cdots",
            r"e_{i-1}",
            r"\cdots",
            r"e_{L.size - 1}",
            ""
        ]
        list_grps = ListNode.get_listnode_grps(Infos, self.scene)
        list_grps[2].tex.scale(0.4)
        list_grps[4].tex.scale(0.4)
        list_grps.to_edge(DOWN, buff = 0.8)
        list_grps.set(width = self.scene.camera.frame_width - 5)

        tex = Tex(r"首地址\\L.base", tex_template = TexTemplateLibrary.ctex).scale(0.4).set_color(TEAL)

        PATH_POINTER = ASSETS_DIR / "ListNode" / "指针.svg"
        pointer = SVGMobject(PATH_POINTER)
        pointer.scale(0.37)
        pointer.rotate(-PI/2)
        pointer.next_to(list_grps[0], LEFT, buff = 0.15)
        pointer.shift(UP*0.3)
        tex.next_to(pointer, DOWN, buff = 0.1)
        tex.shift(LEFT*0.1)

        total_digits = ["0", "1", "", "i-1", "", "L.size-1", ""]
        digits = ListNode.get_array_index(list_grps, total_digits)
        

        array_index = Tex("下标", tex_template = TexTemplateLibrary.ctex).set_color("#FFAA33").scale(0.7)
        array_index.to_edge(DOWN,buff = 0.1)

        curved_line = MyCurvedLine(digits[0].get_center()+DOWN*0.1, array_index.get_center()+UP*0.1, points = 3)

        self.CAPTION4 = Tex(self.total_text.CAPTION4, tex_template = TexTemplateLibrary.ctex)
        self.CAPTION4.scale(0.9)
        self.CAPTION4.set_color("#2176c5")
        self.CAPTION4.next_to(self.movingcode3, DOWN, buff = 0.4)
        caption_line = MyCurvedLine(self.movingcode3[2][1][19].get_center()+DOWN*0.04, self.CAPTION4.get_center()+UP*0.1, points=4)

        self.CAPTION5 = Tex(self.total_text.CAPTION5, tex_template = TexTemplateLibrary.ctex)
        self.CAPTION5.scale(0.9)
        self.CAPTION5.set_color("#2176c5")
        self.CAPTION5.next_to(self.movingcode3, DOWN, buff = 0.4)
        caption_line_copy = MyCurvedLine(self.movingcode3[2][1][19].get_center()+DOWN*0.04, self.CAPTION5.get_center()+UP*0.1, points=4)

        self.scene.play(FadeIn(self.movingcode1), run_time = 1.5)
        self.scene.play(FocusOn(self.movingcode1[2][1][7]))
        self.scene.play(FocusOn(self.movingcode1[2][4][9], run_time = 1.5))
        self.scene.play(FocusOn(self.movingcode1[2][10][12], run_time=1.5))
        self.scene.play(FocusOn(self.movingcode1[2][13][9], run_time=1.5))

        self.scene.wait(5)

        self.scene.play(
            AnimationGroup(
                FadeOut(self.movingcode1[2][1]), 
                FadeOut(self.movingcode1[2][2]), 
                FadeOut(self.movingcode1[2][3]),
            ),
            run_time = 1.5
        )

        self.scene.play(
            AnimationGroup(
                FadeOut(self.movingcode1[2][4]),
                FadeOut(self.movingcode1[2][5]),
                FadeOut(self.movingcode1[2][6]),
                FadeOut(self.movingcode1[2][7]),
                FadeOut(self.movingcode1[2][8]),
            ),
            run_time = 1.5
        )
        self.scene.wait(1.4)
        self.scene.clear()
        self.scene.play(
            FadeIn(self.movingcode3)
        )
        self.scene.wait(1.6)
        

        self.scene.play(
            FadeIn(list_grps)
        )
        self.scene.wait()
        self.scene.play(
            FadeIn(digits),
            Write(self.CAPTION4),
            caption_line.create()
        )
        self.scene.wait()
        self.scene.play(
            curved_line.create(),
            FadeIn(array_index)
        )

        self.scene.wait(5)
        self.scene.play(
            Succession(
                FadeIn(pointer),
                Write(tex)
            )
        )

        self.scene.play(
            caption_line.fadeout(),
            FadeOut(caption_line.arrows)
        )
        self.scene.wait()
        self.scene.play(
            ReplacementTransform(self.CAPTION4, self.CAPTION5),
        )
        self.scene.play(
            caption_line_copy.create()
        )
        self.scene.wait()
        self.scene.play(
            AnimationGroup(
                FadeOut(self.CAPTION5),
                FadeOut(caption_line_copy.arrows),
                caption_line_copy.fadeout()
            )
        )
        
        self.scene.play(
            AnimationGroup(
                FadeOut(pointer),
                FadeOut(tex),
                FadeOut(digits),
            )
        )

        self.scene.play(
            AnimationGroup(
                FadeOut(array_index),
                FadeOut(curved_line.arrows),
                curved_line.fadeout()
            )
        )
        self.scene.play(
            FadeOut(list_grps)
        )

    def second_scene(self):

        reference_rec = Rectangle().set_color(BLACK)
        reference_rec.stretch_to_fit_width(13.5)
        reference_rec.stretch_to_fit_height(4.4)
        reference_rec.to_edge(DOWN, buff = 0)


        Infos = ["1", "2", "3", "4", "5", "NULL"]
        nodes = ListNode().get_listnode_grps(Infos, self.scene)
        # nodes[5].tex.set_opacity(0)
        nodes.scale(0.77)
        nodes.move_to(reference_rec.get_center()).shift(DOWN*0.67)
        single_node = ListNode()
        single_node.set_info("6").set_node_color().shift(DOWN*0.9)

        c = MyCurvedLine(nodes[4].get_top(), nodes[5].get_top()).get_curved_arrows(isflip=True, color = MAROON)
        c.shift(UP*0.5)

        t0 = DecimalTable(
            [[5], [4], [4], [5]],
            row_labels=[
                Tex("i", tex_template = TexTemplateLibrary.ctex), 
                Tex("j", tex_template = TexTemplateLibrary.ctex),
                Tex("L.size - 1",tex_template = TexTemplateLibrary.ctex),
                Tex("position", tex_template = TexTemplateLibrary.ctex),
            ],
            h_buff=1,
            element_to_mobject_config={"num_decimal_places": 0}
        ).set_color(BLACK)
        t0.scale(0.9)
        t0.to_corner(UL, buff = 0.3)
        
        moving_rect = self.movingcode3.get_rect(2)
        moving_rect.to_edge(RIGHT, buff = 0.1)

        self.scene.play(self.movingcode3.animate.to_edge(RIGHT, buff = 0.1))
        self.scene.play(FadeIn(single_node))
        self.scene.wait(1.3)
        self.scene.play(t0.create())

        t0.get_entries()[0].save_state()
        t0.get_entries()[2].save_state()
        self.scene.play(
            t0.get_entries()[0].animate.scale(1.4).set_color(RED),
            Wiggle(t0.get_entries()[0])
        )
        self.scene.wait(0.8)
        self.scene.play(
            Restore(t0.get_entries()[0]),
            t0.get_entries()[2].animate.scale(1.4).set_color(RED),
            Wiggle(t0.get_entries()[2])
        )
        self.scene.wait(0.8)

        self.scene.play(
            Restore(t0.get_entries()[2]),
            FocusOn(t0.get_entries()[4])
        )

        self.scene.wait(2.9)
        self.scene.play(
            FadeIn(moving_rect),
            FocusOn(t0.get_entries()[6])
        )
        self.scene.wait(1.9)

        self.scene.play(
            FadeIn(nodes),
            run_time = 2
        )
        self.scene.wait(3)

        self.scene.play(
            single_node.animate.move_to([nodes[5].get_center()[0], single_node.get_center()[1], 0])
        )
        self.scene.wait(1.7)
        self.scene.play(
            FocusOn(t0.get_entries()[7])
        )
        self.scene.wait(0.4)

        self.scene.play(
            self.movingcode3.transform_remark_rectangle(moving_rect, 3)
        )

        self.scene.wait()
        self.scene.play(
            FocusOn(t0.get_entries()[3])
        )
        self.scene.play(
            FocusOn(t0.get_entries()[7])
        )
        self.scene.wait(2.7)

        nodes[5].save_state()
        nodes[4].save_state()
        nodes[3].save_state()
        single_node.save_state()
        self.scene.play(
            AnimationGroup(
                ReplacementTransform(single_node, nodes[5]),
                nodes[5].animate.change_info("6")
            ),
            self.movingcode3.transform_remark_rectangle(moving_rect, 6)
        )

        self.scene.wait(2)

        self.scene.play(
            Restore(single_node),
            Restore(nodes[5])
        )
        
        self.scene.play(
            FadeOut(moving_rect),
            single_node.animate.move_to([nodes[4].get_center()[0], single_node.get_center()[1], 0])
        )
        self.scene.wait(1.7)

        self.scene.play(
            Succession(
                Create(c),
                AnimationGroup(
                    ReplacementTransform(nodes[4].copy(), nodes[5]),
                    nodes[5].animate.change_info("5"),
                    nodes[4].animate.change_info("NULL")
                )
            )
        )

        self.scene.play(
            AnimationGroup(
                ReplacementTransform(single_node, nodes[4]),
                nodes[4].animate.change_info("6")
            ),
        )
        self.scene.play(
            FadeOut(c)
        )
        self.scene.wait()

        self.scene.play(
            AnimationGroup(
                Restore(single_node),
                Restore(nodes[5]),
                Restore(nodes[4]),
            )
        )
        self.scene.wait()
        self.scene.play(
            single_node.animate.move_to([nodes[2].get_center()[0], single_node.get_center()[1], 0]),
            t0.get_entries()[1].animate.set_value(2),
            t0.get_entries()[7].animate.set_value(2)
        )
        self.scene.wait()


        moving_rect2 = self.movingcode3.get_rect(3)
        self.scene.play(
            Succession(
                FadeIn(moving_rect2),
                AnimationGroup(
                    Create(c),
                    self.movingcode3.transform_remark_rectangle(moving_rect2, 4),
                    t0.get_entries()[3].animate.set_value(3)
                ),
                AnimationGroup(
                    ReplacementTransform(nodes[4].copy(), nodes[5]),
                    nodes[5].animate.change_info("5"),
                    nodes[4].animate.change_info("NULL")
                )

            )
        )
        self.scene.wait(0.7)

        c2 = MyCurvedLine(nodes[3].get_top(), nodes[4].get_top()).get_curved_arrows(isflip=True, color = MAROON)
        c2.shift(UP*0.5)

        self.scene.play(
            Succession(
                AnimationGroup(
                    self.movingcode3.transform_remark_rectangle(moving_rect2, 3),
                    FadeOut(c),                    
                ),
                AnimationGroup(
                    Create(c2),
                    self.movingcode3.transform_remark_rectangle(moving_rect2, 4),
                    t0.get_entries()[3].animate.set_value(2)
                ),
                AnimationGroup(
                    ReplacementTransform(nodes[3].copy(), nodes[4]),
                    nodes[4].animate.change_info("4"),
                    nodes[3].animate.change_info("NULL")
                )
            )
        )
        self.scene.wait(0.7)

        c3 = MyCurvedLine(nodes[2].get_top(), nodes[3].get_top()).get_curved_arrows(isflip=True, color = MAROON)
        c3.shift(UP*0.5)

        self.scene.play(
            Succession(
                AnimationGroup(
                    FadeOut(c2),
                    self.movingcode3.transform_remark_rectangle(moving_rect2, 3),
                ),
                AnimationGroup(
                    Create(c3),
                    self.movingcode3.transform_remark_rectangle(moving_rect2, 4),
                    t0.get_entries()[3].animate.set_value(1)
                ),
                AnimationGroup(
                    ReplacementTransform(nodes[2].copy(), nodes[3]),
                    nodes[3].animate.change_info("3"),
                    nodes[2].animate.change_info("NULL")
                )
            )
        )

        self.scene.wait(0.7)

        self.scene.play(
            AnimationGroup(
                FadeOut(c3),
                Succession(
                    self.movingcode3.transform_remark_rectangle(moving_rect2, 3),
                    AnimationGroup(
                        self.movingcode3.transform_remark_rectangle(moving_rect2, 6),
                        ReplacementTransform(single_node, nodes[2]),
                        nodes[2].animate.change_info("6")
                    )
                ),
            ),
        )
        self.scene.wait(1.5)