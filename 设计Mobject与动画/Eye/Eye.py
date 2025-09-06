from manim import(
    VGroup, Circle, Line, Mobject,
    AnimationGroup, Succession, MoveAlongPath, MoveToTarget, Restore,Add, Wait,
    BLACK, WHITE, 
    RIGHT, 
    override_animate,
)
from manim .typing import Point3DLike

class Eye(VGroup):      
    PUPIL_TO_EYE_WIDTH_RATIO = 0.4
    PUPIL_DOT_TO_PUPIL_WIDTH_RATIO = 0.3

    EYE_RADIUS = 0.2011734163998448 / 2

    DOWN_OR_UP_RATIO = 0.02

    def __init__(
        self,
        pupil_offset = 0.01,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.pupil_offset = pupil_offset

        self.eyes = self._init_eyes()
        self.islooked = False

    def _init_eyes(self):

        new_eye = Circle(radius = Eye.EYE_RADIUS)
        new_eye.set_stroke(width = 1, color = BLACK)
        new_eye.set_fill(color = WHITE, opacity = 1)

        pupil_r = Eye.EYE_RADIUS
        pupil_r *= Eye.PUPIL_TO_EYE_WIDTH_RATIO

        dot_r = pupil_r
        dot_r *= Eye.PUPIL_DOT_TO_PUPIL_WIDTH_RATIO

        black = Circle(radius=pupil_r, color = BLACK)
        dot = Circle(radius=dot_r, color = WHITE)

        dot.shift(black.point_from_proportion(3 / 8) - dot.point_from_proportion(3 / 8))

        new_pupil = VGroup(black, dot)
        new_pupil.set_style(fill_opacity=1, stroke_width=0)
        new_pupil.move_to(new_eye.get_center())

        new_eyes = VGroup(new_eye, new_pupil)

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
        return AnimationGroup(Add(self.eyes), MoveAlongPath(self.pupil, line, **anim_kwargs),)
    
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
            DOWN_OR_UP_RATIO = Eye.DOWN_OR_UP_RATIO

        self.eyes.save_state()
        self.eyes.generate_target()
        self.eyes.target.stretch(DOWN_OR_UP_RATIO, 1)

    @override_animate(blink)
    def _blink_animation(self, **anim_kwargs):
        self.blink()
        
        return AnimationGroup(
            Add(self.eyes),
            Succession(
                MoveToTarget(self.eyes, run_time = 0.2), 
                Wait(0.04), 
                Restore(self.eyes, run_time = 0.2)
            ),
            **anim_kwargs
        )
        


