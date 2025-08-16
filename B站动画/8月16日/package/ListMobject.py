from manim import(
    VMobject, DecimalNumber, Text, VGroup,
    RIGHT, DOWN, LEFT,
    Scene
)
class ListMobject(VMobject):
    def __init__(
            self,
            origin_list = None,
            **kwargs
    ):
        super().__init__(**kwargs)
        if origin_list is None:
            origin_list = [1,2,3,4]

        self.origin_list = origin_list

        self.first = DecimalNumber(self.origin_list[0], num_decimal_places=0)
        self.second = DecimalNumber(self.origin_list[1], num_decimal_places=0)
        self.third = DecimalNumber(self.origin_list[2], num_decimal_places=0)
        self.fourth = DecimalNumber(self.origin_list[3], num_decimal_places=0)

        self.frame1 = Text("[")
        self.frame2 = Text("]")

        self._comma = Text(",")

        self.information = {}
        # self._set_information()
    def get_list_Mobject(self):
        grps = VGroup(
            self.frame1,
            self.first,
            self._comma.copy(),
            self.second,
            self._comma.copy(),
            self.third,
            self._comma.copy(),
            self.fourth,
            self.frame2
        )
        grps.arrange(RIGHT, buff = 0.15)
        grps[2].shift(DOWN*0.15)
        grps[4].shift(DOWN*0.15)
        grps[6].shift(DOWN*0.15)
        grps[0].shift(RIGHT*0.1)
        grps[8].shift(LEFT*0.1)
        return grps
    
    
    # def _set_information(self):
    #     self.information[1] = self.first
    #     self.information[2] = self.second
    #     self.information[3] = self.third
    #     self.information[4] = self.fourth

    def change_number_animation(self, scene:Scene, l:list):
        # scene.play(self.information[list_number].animate.set_value(number), run_time = 0.7)
        # 考虑到传入的列表可能为1个数,可能为两个数,可能为3个数,等等,

        # 去除多余的0
        if 0 in l:
            l = dict.fromkeys(l)
            l = list(l)
            l.remove(0)

        while(len(l) < 4):
            l.append(0)
        scene.play(
            self.first.animate.set_value(l[0]),
            self.second.animate.set_value(l[1]),
            self.third.animate.set_value(l[2]),
            self.fourth.animate.set_value(l[3]),
            run_time = 0.7
        )
        
