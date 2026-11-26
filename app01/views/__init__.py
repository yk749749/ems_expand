# app01/views/__init__.py
"""视图包：按业务拆分到不同模块，并在这里统一导出。

这样 ems/urls.py 中的 ``from app01 import views`` 及 ``views.xxx`` 写法保持不变。
"""
from app01.views.account import image_code, login, logout
from app01.views.admin import (
    admin_add,
    admin_delete,
    admin_edit,
    admin_list,
    admin_reset_password,
)
from app01.views.chart import (
    chart_bar,
    chart_line,
    chart_list,
    chart_pie,
    highcharts,
)
from app01.views.city import city_add, city_list
from app01.views.depart import (
    depart_add,
    depart_delete,
    depart_edit,
    depart_list,
    depart_multi,
)
from app01.views.order import (
    order_add,
    order_delete,
    order_detail,
    order_edit,
    order_list,
)
from app01.views.pretty import (
    pretty_add,
    pretty_delete,
    pretty_edit,
    pretty_list,
)
from app01.views.task import task_add, task_ajax, task_delete, task_edit, task_list
from app01.views.upload import (
    tt,
    tt_delete,
    upload_form,
    upload_list,
    upload_modal_form,
)
from app01.views.user import (
    user_delete,
    user_edit,
    user_list,
    user_model_form_add,
)

__all__ = [
    "admin_add",
    "admin_delete",
    "admin_edit",
    "admin_list",
    "admin_reset_password",
    "chart_bar",
    "chart_line",
    "chart_list",
    "chart_pie",
    "city_add",
    "city_list",
    "depart_add",
    "depart_delete",
    "depart_edit",
    "depart_list",
    "depart_multi",
    "highcharts",
    "image_code",
    "login",
    "logout",
    "order_add",
    "order_delete",
    "order_detail",
    "order_edit",
    "order_list",
    "pretty_add",
    "pretty_delete",
    "pretty_edit",
    "pretty_list",
    "task_ajax",
    "task_add",
    "task_delete",
    "task_edit",
    "task_list",
    "tt",
    "tt_delete",
    "upload_form",
    "upload_list",
    "upload_modal_form",
    "user_delete",
    "user_edit",
    "user_list",
    "user_model_form_add",
]
