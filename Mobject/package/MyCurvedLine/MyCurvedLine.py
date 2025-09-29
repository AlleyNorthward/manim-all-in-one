from manim import *

# 修改日志

"""
    @auther 巷北
    @time 2025.9.29
    第三次更新吧.主要目的并不是能用,而是练习python.上一次更新的时候,引入的是
    __class__,跟3b1b学习的,应用在这里也并不是太符合,虽然能达到想要的效果.这次
    跟manim底层学习了一个设计模式,感觉应用在这里还是很合适的.而且极具一般性,后
    续可以根据逻辑再次创造其他的弯曲箭头,前提是需要包含一些必要的属性,而且要尽力
    避免创造新的属性(就是接口类中用到的属性要存在,不要提供新的属性给接口类).
    因为要用到manim初始的类,所以需要再继承一下,切换接口,方便适配.另外,尽量要做到
    参数一致性,否则后续可能会多添加判断语句,以适配多种可能性.
    
    整体结构再强调一下.线的种类,继承自VMobject,包括self.path,self.arrows,其中,
    路径是单一路径,self.arrows不添加到VMobject的submobjects,这样方便管理,统一
    配色.接下来,生成器类,继承自VGroup,内部仅包含self.path(路径),self.arrows(箭头),
    初始化之后,提供动画接口,配色接口,便于生成各类的箭头.
"""

class CurvedThinLine(VMobject):
    # 说明
    """
        @auther 巷北
        @time 2025.9.29
        这个类名,看起来有些长,有些奇怪,主要是为了避免日后跟manim更新的新对象
        起名冲突,所以才选择了个怪异的名字.而设计模式中,这个类是默认类,用户调用
        的时候,不需要主动填写这个类名,但是有权修改这个类.
    """
    def __init__(
            self,
            start, 
            end,
            points = 4,
            thickness = 0.45,
            path_color = MAROON,
            arrow_color = TEAL,
            arrow_degrees = 20*DEGREES,
            arrow_length = 0.3,
            stroke_opacity = 0.7,
            buff = 0.05,
            **kwargs
    ):

        start = start + DOWN * buff + RIGHT * buff
        end = end + LEFT * buff + UP * buff
        super().__init__(**kwargs)

        self.path = self._generate_points(start, end, path_color, thickness, points).set_stroke(opacity = stroke_opacity)
        self.arrow = self._set_arrows(arrow_length, arrow_degrees, arrow_color).set_stroke(opacity = stroke_opacity)

        # 下面的这些, 有些赘余, 但是方便全局访问, 属于specific_attributes. 果然,不需要了.因为下面内容是具体的值,我们获取的是键名列表.
        # 不删除,注释掉了,警示一下

        # self.points = points
        # self.thickness = thickness
        # self.arrow_degrees = arrow_degrees
        # self.arrow_length = arrow_length
    
    def _get_curved_points(
            self,
            start,
            end,
            thickness,
            points
    ):
        uv = normalize(end - start)
        nv = rotate_vector(uv, 90*DEGREES) * thickness
        zz = [nv, -nv]

        return [
            np.array(
                interpolate(start, end, i/ points)
            ) + zz[i % 2]
            for i in range(1, points)
        ]

    def _generate_points(
            self,
            start,
            end,
            path_color,
            thickness,
            points,
    ):

        points = self._get_curved_points(start, end, thickness, points)
        self.set_points_smoothly([start, *points, end])
        self.set_color(path_color)
        return self
    
    def _set_arrows(
            self,
            arrow_length,
            arrow_degrees,
            arrow_color
    ):
        tangentline = TangentLine(self.path, 1)
        tangentline.set_length(arrow_length)
        tangentline.rotate(-arrow_degrees)
        tangentline.shift(tangentline.get_unit_vector()* -tangentline.get_length() / 2)

        tangentline2 = tangentline.copy()
        tangentline2.rotate(arrow_degrees * 2 + 5 * DEGREES, about_point=tangentline2.get_end())

        arrows = VGroup(tangentline, tangentline2)
        arrows.set_color(arrow_color)

        return arrows
    
    # 下面是接口方法.虽然属性命名要求一致,但还是提供下面这些统一接口,方便调用.
    def get_path(self):
        return self.path
    def get_arrow(self):
        return self.arrow
    def get_specific_attributes(self):
        return ["points", "thickness", "arrow_degrees", "arrow_length"]

class CurvedSingleArrow(CurvedArrow):
    def __init__(
            self,
            start,
            end,
            path_color = MAROON,
            arrow_color = TEAL,
            buff = 0.05,
            angle = TAU / 4,
            **kwargs           
    ):
        start = start + DOWN * buff + RIGHT * buff
        end = end + LEFT * buff + UP * buff
        super().__init__(start_point = start, end_point = end, angle = angle, **kwargs)

        self.arrow = self.get_tip().set_color(arrow_color)
        self.remove(self.arrow)

        self.path = self.set_color(path_color)

    def get_path(self):
        return self
    def get_arrow(self):
        return self.arrow
    def get_specific_attributes(self):
        return ["angle"]
    
class CurvedArrowBuilder(VGroup):
    # 说明
    """
        @auther 巷北
        @time 2025.9.29 13:02
        这个是曲线生成器,目前只能生成CurvedPathWithArrow,CurvedArrow.可以自定义,
        但是需要遵循基本范式,否则不满足需求.思考了一下,接口不统一,还是比较麻烦的.
        需要统一一下接口,供该类调用.
        未具备一般性,隐去所有专一属性,仅暴露共有属性.专一属性全部由**kwargs接收,
        用户可以通过curvedline_class,找到对应的类,从而确定具体属性,而这里不统一
        显示.
    """
    def __init__(
            self,
            start,
            end,
            curvedline_class = CurvedThinLine,
            path_color = MAROON,
            arrow_color = TEAL,
            buff = 0.05,
            **kwargs
    ):  
        """
            因为继承了VGroup,所以**kwargs包括两部分,一部分是VGroup中的,
            一部分是curvedline_class中的.我们需要将特立独行的属性给去除
            掉,否则都传**kwargs的话,就会存在问题.所以我需要解决这个问题
            思想是,对应类,添加一个get_attributes的方法,在这个Builder中,
            添加一个delete_attributes方法,重新归整一下kwargs,然后再传入
            super之中.
        """
        self.curvedline = curvedline_class(
            start = start,
            end = end,
            path_color = path_color,
            arrow_color = arrow_color,
            buff = buff, 
            **kwargs
        )
        kwargs = self.delete_specific_attributes(kwargs)
        super().__init__(**kwargs)

        self.add(self.path, self.arrow)

    @property
    def path(self):
        return self.curvedline.get_path()
    
    @property
    def arrow(self):
        return self.curvedline.get_arrow()
    
    def get_available_classes(self):
        # 说明
        "返回的是可以使用的类的类型,方便curvedline_class调用"
        return [CurvedThinLine, CurvedSingleArrow]
    
    @property
    def specific_attributes(self):
        return self.curvedline.get_specific_attributes()
    
    def delete_specific_attributes(self, kwargs: dict):
        return {k: v for k, v in kwargs.items() if k not in self.specific_attributes}

    @override_animation(Create)
    def _create(self, run_time = 2):
        
        #todo 这里时间的设计,怎么说呢,假如后续有其他类型,需要再去进行调整
        run_time = 1 if isinstance(self, CurvedSingleArrow) else run_time

        return Succession(
            Create(self.path, run_time = run_time * 3 / 4),
            FadeIn(self.arrow, run_time = run_time / 4)
        )
    
    @override_animation(Uncreate)
    def _uncreate(self, run_time = 2):

        return AnimationGroup(
            Uncreate(self.path, run_time = run_time),
            FadeOut(self.arrow, run_time = run_time)
        )

    

    