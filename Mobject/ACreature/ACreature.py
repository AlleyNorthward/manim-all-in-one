from manim import(
    SVGMobject, VGroup, Circle, Line, Mobject,
    AnimationGroup, Succession, MoveAlongPath, Restore, Wait, MoveToTarget,
    RIGHT,
    RED_B, BLACK,
    override_animate,
)
from manim.typing import Point3DLike

import os
from pathlib import Path
ASSDIR = Path(__file__).resolve().parent.parent/"assets"/"A"

# _修改日志
""" ...
    @auther 巷北
    @time 2025.9.11   
    去除了将scene作为参数传入__init__()
    给self.mouth.stretch_to_fig_height()添加判断语句, 以适应多mode嘴巴不同的情况.
    ...
    @auther 巷北
    @time 2025.9.12
    使用A时发现FadeIn()入场存在视觉问题,对原图片进行了修改
    所以层级发生变化,需要对部分代码进行修改.(主要是下标,几乎无影响)
    ...
    @auther 巷北
    @time 2025.9.13
    修改注释,添加_
    进行了危险操作.将MovingCode代码copy到了这里,直接覆盖.后从history中找回,又copy回来. #todo有没有更安全提交、更改代码的方式?
    ...
"""

#_待办
"""
    change_mode(),self.become()可能存在submobjects未更新情况,建议在其之后设计一下,并传入新对象.
"""
class ACreature(SVGMobject):
    # _说明
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

    # _属性
    """
        mode                代表人物造型
        scene               本来不必添加,后来发现不得不在__class__中传入,故设为属性. #弃案 已清除该属性.
        
        body                身体部分   层级结构最下面               由.svg文件而来,自己设计
        eyes                眼睛部分   层级结构在body上面           由SingleEye而来,比例为3b1b设计
        mouth               嘴巴       层级结构在最上面             由.svg文件而来,自己设计
    """

    # _私有方法
    """
        _init_structure()           创建整体结构 body,eyes,mouoth        
        get_svg_file_path()         得到svg路径.封装到内部,通过mode控制,避免用户复杂操作
        _set_submobjects()          重新设立self架构,模仿3b1b,结合ce版本改编而来.#todo可以设置为普通函数
        _draw_eyes()                _init_sturecture()内部私有构造函数之一

        _look_at_animation()        下面这三个是搭配了装饰器,产生动画.
        _restore_eyes_animation()
        _blink_animation()

    """

    # _公有方法
    """
        set_body_color()            这些属于setter和getter,其中setter都return self, 可搭配.animate使用
        get_body_color()
        set_mouth_color()
        get_mouth_color()
        change_mode()
        get_mode()

        look_at()                   这些属于命名配置函数,提供接口给用户,可使用.animate产生动画
        restore_eyes()
        blink()
    """

    # _代码示例
    """
        class ACreatureExample(Scene):
            def construct(self):
                self.camera.background_color = "#ece6e2"
                A = ACreature(self, 'plain')
                self.play(A.animate.blink())
                self.play(A.animate.look_at(UL))
                self.wait()
                self.play(A.animate.look_at(DL))
                self.play(A.animate.move_to(UL))
                self.wait()
                self.play(A.animate.restore_eyes())
                self.play(A.animate.blink())
                self.play(A.animate.flip())
                self.wait()
    """
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

        #_弃案 经过深思熟虑,决定以后将场景对象添加于此,减少不必要麻烦. 于2025.9.11 21:55废弃
        #! 还是存在问题使用self._scene = scene会报错.建议减少将scene传入Mobject避免引发不必要问题.
        #_解决方法 还是妥协吧,创建完对象后就调用self.add()添加场景中.play()时也不会产生问题.也不一定非得这样,
        #_解决方法 灵活添加吧.一切都是因为AnimationGroup与Add可能存在bug导致的.
        # scene.add(self)  废弃

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
        
        # 描述 身体部分对应index为0, 分别为横撇捺
        # 嘴巴为1
        # 右眼为2,3,4 左眼为5,6,7

        #设立身体
        self.body = self[0]
        self.body.set_color(body_color)

        # 设立嘴巴
        self.mouth = self[1]
        #todo 这里是因为微调了嘴巴长度,但是仅仅对'plain'适用.等后续不同mode也可能会灵活调整,随时更改.
        if self.get_mode() == 'plain':
            self.mouth.stretch_to_fit_height(0.125)
        self.mouth.set_color(mouth_color)

        # 初始化眼睛
        self.eyes = self._draw_eyes(eye_stroke_width)
        self.right_eye: SingleEye = self.eyes[0]
        self.left_eye: SingleEye = self.eyes[1]

        self._set_submobjects(self.body, self.eyes, self.mouth)

    def _set_submobjects(self, *mobs):
        self.submobjects.clear()
        self.add(*mobs)

    def _draw_eyes(
            self,
            eye_stroke_width = 1,
    ):
        
        self[5].set_stroke(BLACK, width = eye_stroke_width)
        self[2].set_stroke(BLACK, width = eye_stroke_width)

        right_eye = SingleEye(
            VGroup(self[2],self[3],self[4])
        )

        left_eye = SingleEye(
            VGroup(self[5], self[6], self[7])
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
        # ! 当前对象是由多个组组成的,通过match_style的方式,无法确定是否会对所有的submobjects统一匹配style.可能存在问题.
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
            self.left_eye.animate.look_at(point_or_mobject,),
            self.right_eye.animate.look_at(point_or_mobject,),
            **anim_kwargs
        )
    
    def restore_eyes(self):
        pass

    @override_animate(restore_eyes)
    def _restore_eyes_animation(self, **anim_kwargs):

        return AnimationGroup(
            self.left_eye.animate.restore_pupil(),
            self.right_eye.animate.restore_pupil(),
            **anim_kwargs
        )
    
    def blink(self):
        pass
    
    @override_animate(blink)
    def _blink_animation(self, **anim_kwargs):

        return AnimationGroup(
            # TODO 这里的Add()总是搞不定, 不知道为啥.眼睛总是在身体下方多出来一对
            # TODO 无法解决.感觉可能是因为多组的原因造成的.因为才CreatureEye中
            # TODO 返回的是组中组,这里可能存在问题.

            # HACK 所以生成对象后,必须添加self.add(ACreature())
            # FIXME 待修复

            # INFO 发现是AnimationGroup的问题,与Add一起可能存在问题解决方法是将scene添加到场景中.
            # 直接解决方案是在scene中添加对象.
            # 可是还是为了与manim动画思想保持一致,play与add尽量不共存,虽然没有任何影响.

            # 已解决  妥协了,使用self.add()添加吧.
            self.left_eye.animate.blink(),
            self.right_eye.animate.blink(),
            **anim_kwargs
        )


class SingleEye(VGroup):
    PUPIL_TO_EYE_WIDTH_RATIO = 0.4
    PUPIL_DOT_TO_PUPIL_WIDTH_RATIO = 0.3

    DOWN_OR_UP_RATIO = 0.02

    # _说明
    """
        @auther 巷北
        @time 2025.9.11

            本来这个眼命名为Eye类,因为比例都知道,所以可以直接构建,无需添加额外的东西,并且生成的是一对眼.
            后面等创建了ACreature类的时候,又改变了主意,这个类重命名为SingleEye类, 专门为ACreature类服务,
        经过一系列的修改, 如今必须提供参考眼ref_eye, 其实也就是ACreature中眼睛的相关属性,在这里重新
        画一下,并且能够使用对应动画接口.
            所以说,这个类其实是私有类,不向用户开放.那么在manim底层,肯定也有许多私有类,可以去了解一下.
    """
    # _属性
    """
        pupil                       瞳孔, 是一个组 VGroup(black, dot)
        eye                         眼白
        eyes                        整只眼睛 层级是eye最下面,pupil在上 [eye, pupil] 不确定将瞳孔拆开整合是否更好(如下[eye,black,dot])
        pupil_offset                瞳孔移动偏移量,感觉其实也没必要设为属性
    """
    
    # _私有方法
    """
        _init_eyes()                构建眼睛结构 [eye,pupil(VGroup(black, dot))]
        look()                      看向某处.返回的是移动线,方便MoveAlongPath移动
        _look_animation()           看向某处动画
        _restore()                  瞳孔恢复动画
        _blink_animation()          眨眼动画
    """

    # _公有方法
    """
        look_at()                   看向某处用户接口
        restore_pupil()             恢复瞳孔动画用户接口
        blink()                     眨眼动画接口

    """
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
        pupil_r *= SingleEye.PUPIL_TO_EYE_WIDTH_RATIO

        dot_r = pupil_r
        dot_r *= SingleEye.PUPIL_DOT_TO_PUPIL_WIDTH_RATIO

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
        # TODO 只能瞳孔在中间的时候眨眼.如果看向某处,眨眼的话,存在问题.
        
        if DOWN_OR_UP_RATIO is None:
            DOWN_OR_UP_RATIO = SingleEye.DOWN_OR_UP_RATIO

        self.eyes.save_state()
        self.eyes.generate_target()
        self.eyes.target.stretch(DOWN_OR_UP_RATIO, 1)

    @override_animate(blink)
    def _blink_animation(self, **anim_kwargs):
        self.blink()
        
        return Succession(
            MoveToTarget(self.eyes, run_time = 0.2), 
            Wait(0.04), 
            Restore(self.eyes, run_time = 0.2),
            **anim_kwargs
        )
    




    
        

    






