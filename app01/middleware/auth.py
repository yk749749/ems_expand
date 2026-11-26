# app01/middleware/auth.py
"""登录校验中间件。"""
from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin


class AuthMiddleware(MiddlewareMixin):
    """未登录时统一跳转到登录页面。"""

    def process_request(self, request):
        # 0. 登录页、图片验证码和静态资源不需要登录就能访问
        if (
            request.path_info in ("/login/", "/image/code/")
            or request.path_info.startswith("/static/")
        ):
            return

        # 1. 读取当前访问用户的 session 信息
        #    能读到说明已经登录过，继续访问目标页面
        info_dict = request.session.get("info")
        if info_dict:
            return

        # 2. 没有登录过，重定向到登录页面
        return redirect("/login/")
