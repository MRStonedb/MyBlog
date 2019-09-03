"""
django class-based view 原理：
    将function view里面的分支语句(if method == "POST":elif method == "GET")抽出来独立到函数as_view中，
    通过动态获取当前请求HTTP Method对应的方法来处理对应的请求

"""

# 伪代码
class View():
    @classmethod
    def as_view(cls, **initkwargs):
        def view(request, *args, **kwargs):
            self = cls(**initkwargs)
            handler = getattr(self, request.method.lower())
            if handler:
                return handler(request)
            else:
                raise Exception("Method Not Allow")
        return view