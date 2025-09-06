from manim import *
import numpy as np
from typing import List, Tuple, Dict, Optional

# ---------------- Geometry helpers ----------------

def segment_intersection(p1, p2, q1, q2, eps=1e-9):
    """
    Return intersection of segments p1-p2 and q1-q2 as (x,y,u,v)
    where:
      - (x,y) is intersection coordinate
      - u in [0,1] is parameter on segment p1->p2
      - v in [0,1] is parameter on segment q1->q2
    Returns None if parallel/no intersection.
    """
    x1, y1 = p1; x2, y2 = p2
    x3, y3 = q1; x4, y4 = q2
    dx1 = x2 - x1; dy1 = y2 - y1
    dx2 = x4 - x3; dy2 = y4 - y3
    denom = dx1 * dy2 - dy1 * dx2
    if abs(denom) < eps:
        return None
    ux = x3 - x1; uy = y3 - y1
    u = (ux * dy2 - uy * dx2) / denom
    v = (ux * dy1 - uy * dx1) / denom
    if -eps <= u <= 1 + eps and -eps <= v <= 1 + eps:
        xi = x1 + u * dx1
        yi = y1 + u * dy1
        return (xi, yi, u, v)
    return None

# ---------------- Sampling helpers ----------------

def sample_mobject_parametric(m: VMobject, n_samples: int = 400) -> List[Tuple[np.ndarray, float]]:
    """
    Sample a VMobject using point_from_proportion(t) uniformly for t in [0,1].
    Returns list of (point (np.array [x,y,0]), t).
    Note: point_from_proportion relies on VMobject implementation to map proportion -> point.
    """
    pts = []
    if n_samples < 2:
        n_samples = 2
    for i in range(n_samples):
        t = i / (n_samples - 1)
        try:
            p = np.array(m.point_from_proportion(t))
        except Exception:
            # Fallback to get_center if method not present
            p = np.array(m.get_center())
        pts.append((p, t))
    return pts

def build_segments_from_samples(samples: List[Tuple[np.ndarray, float]]):
    """
    From list of (point, t) produce segments list:
    [(p0,p1,t0,t1), ...] where p are 2D tuples (x,y).
    """
    segs = []
    for i in range(len(samples) - 1):
        p0, t0 = samples[i]
        p1, t1 = samples[i + 1]
        segs.append(( (float(p0[0]), float(p0[1])), (float(p1[0]), float(p1[1])), t0, t1 ))
    return segs

# ---------------- Intersection routine ----------------

def intersect_vmobjects(
    A: VMobject,
    B: VMobject,
    n_samples_A: int = 400,
    n_samples_B: int = 400,
    dedupe_eps: float = 1e-3,
) -> List[Dict]:
    """
    Compute approximate intersections between two VMobjects.
    Returns list of dicts: {'xy': (x,y), 'tA': t_on_A, 'tB': t_on_B}
    """
    samplesA = sample_mobject_parametric(A, n_samples_A)
    samplesB = sample_mobject_parametric(B, n_samples_B)
    segsA = build_segments_from_samples(samplesA)
    segsB = build_segments_from_samples(samplesB)

    raw = []
    for (a0, a1, tA0, tA1) in segsA:
        for (b0, b1, tB0, tB1) in segsB:
            res = segment_intersection(a0, a1, b0, b1)
            if res:
                x, y, u, v = res
                # linear interpolate t along the segment
                tA = tA0 + u * (tA1 - tA0)
                tB = tB0 + v * (tB1 - tB0)
                raw.append({'xy': (x, y), 'tA': tA, 'tB': tB})

    # deduplicate by proximity
    unique = []
    for r in raw:
        x, y = r['xy']
        found = False
        for u in unique:
            ux, uy = u['xy']
            if (ux - x) ** 2 + (uy - y) ** 2 <= dedupe_eps ** 2:
                # keep average param values (more robust)
                u['tA'] = (u['tA'] + r['tA']) / 2
                u['tB'] = (u['tB'] + r['tB']) / 2
                found = True
                break
        if not found:
            unique.append(dict(r))
    return unique

# ---------------- Manim Scene demo ----------------

class IntersectionDemo(Scene):
    def construct(self):
        # Example objects: a Circle and an Ellipse (or another Circle) intentionally overlapping
        c1 = Circle(radius=1.5).shift(LEFT * 1)
        c2 = Circle(radius=1.2).shift(RIGHT * 0.2 + UP * 0.3).set_color(BLUE)
        # Or try: c2 = Ellipse(width=2.0, height=1.0).shift(RIGHT*0.2+UP*0.3)

        c1.set_fill(RED, opacity=0.15)
        c2.set_fill(BLUE, opacity=0.15)
        self.add(c1, c2)

        # compute intersections approx
        inters = intersect_vmobjects(c1, c2, n_samples_A=600, n_samples_B=600, dedupe_eps=1e-3)

        # print results
        print("Found intersections:", len(inters))
        print(inters)
        for k, it in enumerate(inters):
            print(k, it)

        # show dots at intersection positions
        dots = VGroup()
        for it in inters:
            x, y = it['xy']
            d = Dot(point=ORIGIN)  # create dot then move (keeps z=0)
            d.move_to(np.array([x, y, 0]))
            d.set_color(YELLOW)
            d.set_z_index(10)
            dots.add(d)
            # annotate with small t-values
            tlabel = Tex(f"tA={it['tA']:.3f}\n tB={it['tB']:.3f}").scale(0.4)
            tlabel.next_to(d, UP + RIGHT * 0.2)
            self.add(tlabel)

        if len(dots) > 0:
            self.play(FocusOn(dots), *[GrowFromCenter(d) for d in dots], run_time=1.2)
        else:
            # no intersections found — show hint
            self.play(Write(Text("No intersections found (increase sampling)")))
        dot = inters[0]['xy']
        print(dot)
        dots = Dot([dot[0], dot[1], 0])
        self.play(FadeIn(dots))
        self.wait(1.5)
