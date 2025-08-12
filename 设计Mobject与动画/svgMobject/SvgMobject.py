from manim import (
    SVGMobject, Tex, VGroup, VMobject, TexTemplateLibrary,Circle,
    UP, DOWN, LEFT, RIGHT, BLACK
)
import numpy as np
from typing import Optional
class MySvgMobject(VMobject):
    pre_mob = []
    def __init__(
            self,
            svg:SVGMobject,
            title,
            **kwargs
    ):
        super().__init__(**kwargs)
        self.rec = svg[0]
        self.cir = VGroup(svg[1], svg[2])
        self.line = svg[3]
        self.pra_cir = svg[4]
        self.me_cir = svg[6]
        # 设计间隔宽度
        self.cir_dis = np.linalg.norm(svg[3].get_center() - svg[5].get_center())-0.15
        # self.buff = 0.1

        # 初始化图形
        self._init_mobject(title)

    def _init_mobject(self, text = ""):
        dis = np.linalg.norm(self.rec.get_top() - self.line.get_center()) 
        self.rec.stretch_to_fit_height(dis)
        self.line.next_to(self.rec, UP, buff = -dis)

        tex = Tex(text,tex_template = TexTemplateLibrary().ctex).scale(0.4).set_color(BLACK)
        cir_text = VGroup(self.cir, tex).arrange(RIGHT, buff = 0.05)
        cir_text.move_to(self.rec.get_center())
        # cir_text.shift(UP*self.buff/2)

        self.add(VGroup(self.rec,self.line,cir_text))
        # 记录rec的总长度
        self.total_dis = np.linalg.norm(self.rec.get_top() - self.rec.get_bottom())

    def _set_new_total_dis(self):
        self.total_dis += self.cir_dis
    
    def _stretch_rec_height(self):
        origin_rec = self.rec.get_top()
        rec_copy = self.rec.copy().stretch_to_fit_height(self.total_dis)
        stretch_rec = rec_copy.get_top()
        ori_str_dis = np.linalg.norm(origin_rec - stretch_rec)
        self.rec.stretch_to_fit_height(self.total_dis)
        self.rec.shift(DOWN*ori_str_dis)

    def _design_cir_text(self,cir:Optional[Circle] = None, text = "",first_mob :Optional[Circle] = None):
            if cir is None:
                 cir = self.pra_cir.copy()
                 reference_line = self.line
            else:
                 reference_line = self.method_line
            pra_cir_copy = cir
            pra_cir_text = Tex(
                 text,
                 tex_template = TexTemplateLibrary().ctex
            ).scale(0.38).set_color(BLACK)
            if first_mob is None:
                pra_cir_copy.next_to(self.rec,LEFT, buff = -0.3)
                pra_cir_copy.move_to([pra_cir_copy.get_center()[0], reference_line.get_center()[1] - self.cir_dis /2, 0])
            else:
                 pra_cir_copy.move_to(first_mob)
                 pra_cir_copy.shift(DOWN*self.cir_dis)

            pra_cir_text.next_to(pra_cir_copy, RIGHT, buff = 0.1)
            pra_cir_grps = VGroup(pra_cir_copy, pra_cir_text)
            return pra_cir_grps
    
    def _add_line(self, last_mob:Optional[Circle] = None):
        self.method_line = self.line.copy()
        self.method_line.move_to([self.rec.get_center()[0], last_mob.get_center()[1] - self.cir_dis/2, 0])
        # self.method_line.shift(UP*self.buff)
        
    def _design_method_cir_text(self, text = "", first_mob:Optional[Circle] = None):
        return self._design_cir_text(self.me_cir.copy(), text = text, first_mob=first_mob)

    def add_information(self, ismethod = False, islast = False,text = "", first_mob:Optional[Circle] = None):
        self._set_new_total_dis()
        self._stretch_rec_height()
    
        if not ismethod:
            mob = self._design_cir_text(text=text, first_mob=first_mob)
        else:
            mob = self._design_method_cir_text(text = text,first_mob=first_mob)

        if islast:
            self._add_line(mob[0])
            self.add(self.method_line)
        MySvgMobject.pre_mob.append(mob[0])

        self.add(mob)
        return self

        
        
         

        