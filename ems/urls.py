"""
URL configuration for ems project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path, re_path
from django.views.static import serve

from app01 import views

urlpatterns = [
    # 开发环境下由 Django 提供 media 文件访问（生产应交由 Nginx 等处理）
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}, name='media'),

    # 登录与注销
    path('login/', views.login),

    path('image/code/', views.image_code),

    path('logout/', views.logout),

    # 管理员
    path('admin/list/', views.admin_list),

    path('admin/add/', views.admin_add),

    path('admin/<int:nid>/edit/', views.admin_edit),

    path('admin/delete/', views.admin_delete),

    path('admin/<int:nid>/reset/', views.admin_reset_password),

    # 部门
    path('depart/list/', views.depart_list),

    path('depart/add/', views.depart_add),

    path('depart/delete/', views.depart_delete),

    path('depart/<int:nid>/edit/', views.depart_edit),

    # 批量导入部门（Excel）
    path('depart/multi/', views.depart_multi),

    # 用户列表
    path('user/list/', views.user_list),

    path('user/model/form/add/', views.user_model_form_add),

    path('user/<int:nid>/edit/', views.user_edit),

    path('user/delete/', views.user_delete),

    # 靓号列表
    path('pretty/list/', views.pretty_list),

    path('pretty/add/', views.pretty_add),

    path('pretty/<int:nid>/edit/', views.pretty_edit),

    path('pretty/delete/', views.pretty_delete),

    # 任务管理
    path('task/list/', views.task_list),

    path('task/ajax/', views.task_ajax),

    path('task/add/', views.task_add),

    path('task/<int:nid>/edit/', views.task_edit),

    path('task/delete/', views.task_delete),

    # 订单管理
    path('order/list/', views.order_list),

    path('order/add/', views.order_add),

    path('order/delete/', views.order_delete),

    path('order/detail/', views.order_detail),

    path('order/edit/', views.order_edit),

    # 数据统计
    path('chart/list/', views.chart_list),

    path('chart/bar/', views.chart_bar),

    path('chart/pie/', views.chart_pie),

    path('chart/line/', views.chart_line),

    path('chart/highcharts/', views.highcharts),

    # 文件上传
    path('upload/list/', views.upload_list),

    path('upload/form/', views.upload_form),

    path('upload/modal/form/', views.upload_modal_form),

    # 头像预览
    path('tt/', views.tt),

    path('tt/delete/', views.tt_delete),

    # 城市列表
    path('city/list/', views.city_list),

    path('city/add/', views.city_add),

    # Django 自带的 admin 放在最后，避免它的 catch-all 规则抢先匹配 /admin/...
    path('admin/', admin.site.urls),
]
