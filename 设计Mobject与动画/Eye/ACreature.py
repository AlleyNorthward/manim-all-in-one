from manim import*
from manim.typing import Point3DLike
from CreatureEye import CreatureEye

import os
from pathlib import Path
ASSDIR = Path(__file__).resolve().parent/"assets"/"creature"

class ACreature(SVGMobject):
    """
        @auther: 巷北
        @time: 2025.9.9  22:43

            这个代码是模仿3b1b实现的.
            写这个的目的是担心别人说抄袭什么的,这里叠层buff.
            之前看3b1b的视频,看到了小人物pi,当时在想怎么实现的.后面学习manim的时候,
        也一直在思考这个问题.我知道3b1b源码中有,可是当时刚学习,且学习的ce版本,gl我
        内心感觉看不太懂.而且当时对源代码路径不太熟悉,所以也找不到代码在哪.
            随着学习的深入,我慢慢也开始做视频了.做了第一个数据结构视频后发现,制作时,
        中间缺少互动对象,要是有个小人物就好了.
            后来开学,音频没办法录制,只能专注于代码,所以抽出来两天深入学习ai,学会了制图
        并且解决了很多问题,最终两三天的时间,设计出来了我自己的ACreature.
            当然,我先设计了眼睛,因为看3b1b的源代码,发现眼睛并不是svg图,而是按照比例写好了的.
        所以我也按照比例,设计了Eye类,并且完善了ce版本的眨眼、看向某方的动画.动画是完全自己写的,
        因为ce版本跟gl版本不太一样.
            现在我设计完初版本的ACreature, 身体部分按照某字体更改的,然后添加了自己的创意,嘴巴
        也是自己画的.目前需要写代码,实现Mobject创建以及动画部分.
            之前学习的时候,没亲自学习过3b1b的源代码(跟着别人学,而别人在所难免地受到3b1b的影响),
        所以这次打算学习一下3b1b的代码,看看哪些有自己不熟悉的python知识点,并且看看gl跟ce的不同.
        逻辑部分肯定自己写,看别人的我也不愿意看.主要是学习架构(比如从用户输入角度来看, 输入mode
        比输入path好太多了.我之前自己设计时,总会让用户(其实就是我自己,但站在面向对象设计角度来看,
        大众观念一定要有)输入path,我自己能明白可是别人可能无法明白).
            还有就是看了3b1b的change_mode()部分,明白了__class__()的含义.之前从未用过,但光从书
        上看的话,真不如这里实战应用理解的深刻.
            等等等等.
            所以模仿也好,抄袭也罢,我最初的目的是学习3b1b的源码的,所以前面说的也很难避免.
            有很多"借口"我也不多说了.
            希望大家理解~
    """
    # 本来打算作为基类, TeacherCreature和StudentCreature分别代表
    # 老师和学生人物.可是对比下发现学生有些丑.所以还是模仿3b1b,老师
    # 和学生用flip转换,这样节省了不少事,设计层面也方便了很多.

    def __init__(
            self,
            mode = 'plain',
            body_color = RED_B,
            mouth_color = BLACK,
            eye_stroke_width = 1,
            **kwargs
    ):
        self.mode = mode
        super().__init__(file_name = self.get_svg_file_path(mode), **kwargs)

        # 解析时,stroke_width会存在为None的可能, 最后调用match_style()会报错
        # 这里提前避免一下
        self.stroke_width = 0 if self.stroke_width is None else self.stroke_color
        self._init_structure(
            body_color,
            mouth_color,
            eye_stroke_width
        )

    def get_svg_file_path(self, mode):
        PATH_FILE = os.path.join(ASSDIR, f'{mode}.svg')

        # 异常几乎没写过.看看3b1b怎么写的, 学习一下.
        if not os.path.exists(PATH_FILE):
            PATH_FILE = os.path.join(ASSDIR, "plain.svg")
        return PATH_FILE
    
    def _init_structure(
            self,
            body_color = RED_B,
            mouth_color = BLACK,
            eye_stroke_width = 1,
    ):
        
        # 描述 身体部分对应index为0,1,2, 分别为横撇捺
        # 嘴巴为3
        # 右眼为4,5,6 左眼为7,8,9

        #设立身体
        self.body = VGroup(
            self[0],
            self[1],
            self[2]
        )
        self.body.set_color(body_color)

        # 设立嘴巴
        self.mouth = self[3]
        self.mouth.stretch_to_fit_height(0.125)
        self.mouth.set_color(mouth_color)

        # 初始化眼睛
        self.eyes = self._draw_eyes(eye_stroke_width)
        self.right_eye: CreatureEye = self.eyes[0]
        self.left_eye: CreatureEye = self.eyes[1]

        self._set_submobjects(self.body, self.eyes, self.mouth)

    def _set_submobjects(self, *mobs):
        self.submobjects.clear()
        self.add(*mobs)

    def _draw_eyes(
            self,
            eye_stroke_width = 1,
    ):
        
        self[7].set_stroke(BLACK, width = eye_stroke_width)
        self[4].set_stroke(BLACK, width = eye_stroke_width)

        right_eye = CreatureEye(
            VGroup(self[4],self[5],self[6])
        )

        left_eye = CreatureEye(
            VGroup(self[7], self[8], self[9])
        )

        return VGroup(right_eye, left_eye)
    
    def set_body_color(self, color = RED_B):
        self.body.set_color(color)

        # 这里虽然是set,return self的目的是方便.animate生成动画.
        return self
    
    def get_body_color(self):
        return self.body.get_color()
    
    def set_mouth_color(self, color = BLACK):
        self.mouth.set_color(color)
        return self
    
    def get_mouth_color(self):
        return self.mouth.get_color()
    
    def change_mode(self, mode):
        new_self = self.__class__(mode = mode)
        new_self.match_style(self)
        new_self.match_height(self)

        new_self.move_to(self.get_center())
        # TODO 这里需要设计看向方向
        self.become(new_self)
        self.mode = mode
        return self
    
    def get_mode(self):
        return self.mode
    
    # Eyes Animation 
    def look_at(slef):
        pass

    @override_animate(look_at)
    def _look_at_animation(self, point_or_mobject:Point3DLike = RIGHT, **anim_kwargs):
        return AnimationGroup(
            # Add(self),
            self.left_eye.animate.look_at(point_or_mobject,),
            self.right_eye.animate.look_at(point_or_mobject,),
            **anim_kwargs
        )
    
    def restore_eyes(self):
        pass

    @override_animate(restore_eyes)
    def _restore_eyes_animation(self, **anim_kwargs):

        return AnimationGroup(
            # Add(self),
            self.left_eye.animate.restore_pupil(),
            self.right_eye.animate.restore_pupil(),
            **anim_kwargs
        )
    
    def blink(self):
        pass
    
    @override_animate(blink)
    def _blink_animation(self, isaddbody = False, **anim_kwargs):

        return AnimationGroup(
            # TODO 这里的Add()总是搞不定, 不知道为啥.眼睛总是在身体下方多出来一对
            # TODO 无法解决.感觉可能是因为多组的原因造成的.因为才CreatureEye中
            # TODO 返回的是组中组,这里可能存在问题.

            # HACK 所以生成对象后,必须添加self.add(ACreature())
            # FIXME 待修复

            # Add(self),
            self.left_eye.animate.blink(),
            self.right_eye.animate.blink(),
            **anim_kwargs
        )

    


class CreatureEye(VGroup):      
    PUPIL_TO_EYE_WIDTH_RATIO = 0.4
    PUPIL_DOT_TO_PUPIL_WIDTH_RATIO = 0.3

    DOWN_OR_UP_RATIO = 0.02

    def __init__(
        self,
        ref_eye = None,
        pupil_offset = 0.01,
        **kwargs
    ):
        if ref_eye is None:
            print(
                """
                    目前不支持单独产生眼睛,需要输入参考眼,以方便配置.
                """
            )
        eye_radius = ref_eye[0].width / 2

        super().__init__(**kwargs)
        self.pupil_offset = pupil_offset

        self.eyes = self._init_eyes(
            eye_radius,
            ref_eye[0],
            ref_eye[1],
            ref_eye[2]
        )
        self.islooked = False

    def _init_eyes(
        self,
        eye_radius,
        eye:Circle,
        black_pupil:Circle,
        white_pupil:Circle,
    ):

        new_eye = Circle(radius = eye_radius)
        new_eye.match_style(eye)

        pupil_r = eye_radius
        pupil_r *= CreatureEye.PUPIL_TO_EYE_WIDTH_RATIO

        dot_r = pupil_r
        dot_r *= CreatureEye.PUPIL_DOT_TO_PUPIL_WIDTH_RATIO

        black = Circle(radius=pupil_r)
        black.match_style(black_pupil)
        dot = Circle(radius=dot_r)
        dot.match_style(white_pupil)

        dot.shift(black.point_from_proportion(3 / 8) - dot.point_from_proportion(3 / 8))

        new_pupil = VGroup(black, dot)
        new_pupil.move_to(new_eye.get_center())

        new_eyes = VGroup(new_eye, new_pupil)
        new_eyes.move_to(eye.get_center())
        self.eye = new_eye
        self.pupil = new_pupil

        self.add(new_eye)
        self.add(self.pupil)

        return new_eyes


    def look(self, point:Point3DLike = RIGHT,) -> Line:
        pupil_radius = self.pupil.width / 2
        eye_radius = self.eye.width / 2
        pupil_move_dis = (eye_radius - pupil_radius) + self.pupil_offset

        ref_line = Line(self.eye.get_center(), point)

        end_vec = ref_line.point_from_proportion(pupil_move_dis / ref_line.get_length())

        if self.islooked:
            start_vec = self.pupil.get_center()
        else:
            start_vec = self.eye.get_center()
        
        ref_line = Line(start_vec, end_vec)

        return ref_line
        

    def look_at(self, point_or_mobject):
         
        if isinstance(point_or_mobject, Mobject):
            point = point_or_mobject.get_center()

        else:
            point = point_or_mobject

        ref_line = self.look(point)
        self.islooked = True

        return ref_line

    @override_animate(look_at)
    def _look_animation(self, point_or_mobject:Point3DLike = RIGHT, **anim_kwargs):
        line = self.look_at(point_or_mobject)
        return MoveAlongPath(self.pupil, line, **anim_kwargs)
    
    def restore_pupil(self):
        self.islooked = False
        ref_line = Line(self.pupil.get_center(), self.eye.get_center())

        return ref_line

    @override_animate(restore_pupil)
    def _restore(self, **anim_kwargs):
        ref_line = self.restore_pupil()
        return MoveAlongPath(self.pupil, ref_line, **anim_kwargs)
    
    def blink(self, DOWN_OR_UP_RATIO = None):
        if DOWN_OR_UP_RATIO is None:
            DOWN_OR_UP_RATIO = CreatureEye.DOWN_OR_UP_RATIO

        self.eyes.save_state()
        self.eyes.generate_target()
        self.eyes.target.stretch(DOWN_OR_UP_RATIO, 1)

    @override_animate(blink)
    def _blink_animation(self, **anim_kwargs):
        self.blink()
        
        return AnimationGroup(
            Succession(
                MoveToTarget(self.eyes, run_time = 0.2), 
                Wait(0.04), 
                Restore(self.eyes, run_time = 0.2)
            ),
            **anim_kwargs
        )
    
        

    





