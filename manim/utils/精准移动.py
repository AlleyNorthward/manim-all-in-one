from manim import (
    Mobject, 
    ORIGIN,
    np,
)
from manim.typing import Point3DLike, Vector3D

def set_position(
        self, 
        point_or_mobject: Point3DLike | Mobject, 
        anchor = ORIGIN,
        buff = 0,
        coor_mask: Vector3D = np.array([1, 1, 1]),
):
    if isinstance(point_or_mobject, Mobject):
        target = point_or_mobject.get_center()
    else:
        target = point_or_mobject
        
    move_mob = self.get_critical_point(anchor)

    direction_vector = target - move_mob
    direction_vector_length = np.linalg.norm(direction_vector)
    unit_direction_vector = direction_vector / direction_vector_length
    small_move_vector = unit_direction_vector * buff

    self.shift((direction_vector - small_move_vector) * coor_mask)
    return self
