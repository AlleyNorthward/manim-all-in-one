from manim import(
    interpolate_color
)
def interpolate_color_range(*colors):
    # 说明
    """
        @auther 巷北
        @time 2025.9.13
            颜色渐变差值函数.不是原创,稍作修改.
            之前没怎么写过闭包,所以也似懂非懂的(不过一直用着装饰器).看了这个的
        写法后,稍微明白了些.这种闭包函数,内部还有一个函数,而外层函数则返回这个
        内部这个函数.这是基本架构.
            闭包函数相当于两个函数,其外层函数有外层参数,内层函数有内层参数.
            以这个函数为例,外层传参是*colors,而内层传参是alpha.内部可以自由访问
        外层参数*colors,而外层访问不了alpha.
            外层临时变量(比如这里的color_steps、alpha_steps),内层函数无法直接访
        问,需要通过关键字nonlocal,来获取访问权限(通过这个函数来看的).但是如果我们
        只是读取、访问数据,去掉这一行也没问题.但是如果修改值,并且希望外层函数也跟着
        改变,那必须要用nonlocal.有些类似于C++中的&操作.
            关于函数逻辑,后续再说吧.先了解下闭包,一口也吃不成个胖子.
    """

    # 代码示例
    """
            class Example(Scene):
            def construct(self):
                square = Square(fill_opacity=1).scale(2)
                color_palette = interpolate_color_range(RED, TEAL, PINK, GREEN)

                def my_alpha_updater(mob, alpha):
                    color = color_palette(alpha)
                    mob.set_color(color)

                self.play(
                    UpdateFromAlphaFunc(square, my_alpha_updater, run_time=4, rate_func=smooth)
                )
                self.wait()
    """
    partition = len(colors)
    dx = 1 / (partition-1)
    colors_steps = [
        (colors[i],colors[i+1])
        for i in range(partition-1)
    ]
    alpha_steps = [
        (dx * i, dx * (i+1))
        for i in range(partition-1)
    ]
    def f(alpha):
        nonlocal colors_steps, alpha_steps
        for i_count,(c_s,a_s) in enumerate(zip(colors_steps,alpha_steps)):
            if a_s[0] <= alpha <= a_s[1]:
                d_alpha = alpha - dx * i_count
                c_alpha = d_alpha / dx
                return interpolate_color(c_s[0], c_s[1], c_alpha)
    return f


def interpolate_color_range_decorator(*colors):
    # 说明
    """
        @auther 巷北
        @time 2025.9.13 13:22
            在上面的基础上,我将函数更改成了装饰器版本.这样才能起到锻炼的效果,也能有
        更深的理解.如果单纯地看视频、重复地做练习,对我来说一点效果也没有.
            此时有三层函数,我这里就称之为外层,中间层,内层.
        我们先来说说一般地装饰器.一般装饰器,是直接@,比如@decorator.然后将被装饰函数
        传入decorator中.而其内层函数则是实际作用函数.
            那么内层函数实际用途是什么呢?可以拓展传入函数的参数.比如传入参数func,本来
        只能接收两个参数a,b,那么内层函数必须接受参数a,b.也就是如下形式:
        ...
        def wraper(a, b, *args, **kwargs):
            return func(a, b, c, d, *args, **kwargs)
            pass
        ...
            如上所示,返回了新的func,并且多了参数c、d,这也就代表着,如果给func添加了装饰
        器,我们就不需要局限于func只能传入相关参数a、b的限制,而是能传入多参数,abcd.这
        就是内层装饰的意义.当然,关于参数c和d,肯定是根据具体添加的,而不是随意添加.
            关于*args以及**kwargs则是安全考虑.比如你要修改mob的颜色、等其他内容,就不得不
        添加二者,保证安全.不过这里去掉也没问题.但为了安全性,建议加上.

            好了,我们现在知道了,添加装饰器,可以通过内层函数,来拓展func的参数数量.那么外层
        函数有什么用呢?
            如果我们只以函数作为参数,就只需要两层函数装饰器便能解决问题.可如果我们想给装饰器
        添加参数,怎么办?
            再添加一个外层函数就好了,并且能接收待传入装饰器的所有参数.这里我也不再过多解释了,
        内层明白了,外层自然也就明白了.
            至此, 我们也就能明白装饰器的具体原理以及实现效果了.
            而这个函数就是一个非常好的装饰器的例子.忘了来看看就好.结合实践,永远比盲目练习强.
    """

    # 代码示例
    """
            class Example(Scene):
            def construct(self):
                square = Square(fill_opacity=1).scale(2)
                
                @interpolate_color_range_decorator(RED, BLUE, YELLOW)
                def my_alpha_updater(mob, alpha, color):
                    mob.set_color(color)

                self.play(
                    UpdateFromAlphaFunc(square, my_alpha_updater, run_time=4, rate_func=smooth)
                )
                self.wait()
    """
    partition = len(colors)
    dx = 1 / (partition-1)
    colors_steps = [(colors[i], colors[i+1]) for i in range(partition-1)]
    alpha_steps = [(dx * i, dx * (i+1)) for i in range(partition-1)]
    def decorator(f):
        def wrapper(mob, alpha, *args, **kwargs):
            for i_count,(c_s,a_s) in enumerate(zip(colors_steps,alpha_steps)):
                if a_s[0] <= alpha <= a_s[1]:
                    d_alpha = alpha - dx * i_count
                    c_alpha = d_alpha / dx
                    color = interpolate_color(c_s[0], c_s[1], c_alpha)
                    return f(mob, alpha, color, *args, **kwargs)
            return f(mob, alpha, colors[-1], *args, **kwargs)
        return wrapper
    return decorator


