# app01/utils/form.py
"""业务表单：用户表单、靓号表单与管理员表单。"""
from django import forms

from app01 import models
from app01.utils.bootstrap import BootstrapModelForm
from app01.utils.encrypt import md5


class UserModelForm(BootstrapModelForm):
    """用户新建/编辑表单。"""

    class Meta:
        # 指定该表单对应的数据库模型
        model = models.UserInfo
        # 需要在页面上展示的字段列表
        fields = ["name", "password", "age", "account", "create_time", "gender", "depart"]


class PrettyModelForm(BootstrapModelForm):
    """靓号新建/编辑表单。"""

    class Meta:
        # 指定该表单对应的数据库模型
        model = models.PrettyNum
        # 需要在页面上展示的字段列表
        fields = ["mobile", "price", "level", "status"]

    def clean(self):
        """校验：状态为“已占用”时，手机号不能重复。"""
        # 先调用父类的 clean，拿到已经校验通过的数据
        cleaned_data = super().clean()
        mobile = cleaned_data.get("mobile")
        status = cleaned_data.get("status")

        # 仅当状态为“已占用”(1) 且手机号填写了内容时，才校验号码是否重复
        if mobile and status == 1:
            # 在全表范围内查询是否存在相同手机号的记录（不区分对方状态）
            queryset = models.PrettyNum.objects.filter(mobile=mobile)
            # 编辑场景下需要排除当前正在修改的这条记录本身
            if self.instance and self.instance.pk:
                queryset = queryset.exclude(pk=self.instance.pk)
            # 已存在则把错误信息挂到 mobile 字段上
            if queryset.exists():
                self.add_error("mobile", "该手机号已被占用，号码不能重复")

        return cleaned_data


class AdminModelForm(BootstrapModelForm):
    """管理员新建表单：用户名、密码、确认密码。"""

    # 确认密码不是数据库字段，只在表单层面添加，不需要修改 models.py
    confirm_password = forms.CharField(
        label="确认密码",
        widget=forms.PasswordInput(render_value=True),
    )

    class Meta:
        # 指定该表单对应的数据库模型
        model = models.Admin
        # 新建时需要填写用户名和密码
        fields = ["username", "password"]
        widgets = {
            # 密码框输入内容以圆点显示，校验失败时保留输入
            "password": forms.PasswordInput(render_value=True),
        }

    field_order = ["username", "password", "confirm_password"]

    def clean(self):
        """校验两次输入的密码是否一致。"""
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error("confirm_password", "密码不一致")

        return cleaned_data

    def save(self, commit=True):
        """保存前把密码转换为 MD5。"""
        admin = super().save(commit=False)
        admin.password = md5(admin.password)
        if commit:
            admin.save()
        return admin


class AdminEditForm(BootstrapModelForm):
    """管理员编辑表单（只允许修改用户名，密码通过“重置密码”修改）。"""

    class Meta:
        model = models.Admin
        fields = ["username"]


class AdminResetPasswordForm(BootstrapModelForm):
    """管理员重置密码表单。"""

    # 确认密码不是数据库字段，只在表单层面添加
    confirm_password = forms.CharField(
        label="确认密码",
        widget=forms.PasswordInput(render_value=True),
    )

    class Meta:
        model = models.Admin
        fields = ["password"]
        widgets = {
            # 密码框输入内容以圆点显示，校验失败时保留输入
            "password": forms.PasswordInput(render_value=True),
        }

    field_order = ["password", "confirm_password"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # GET 打开页面时不要把数据库里的旧密码哈希回显到输入框
        self.initial["password"] = ""
        self.initial["confirm_password"] = ""

    def clean(self):
        """校验两次密码是否一致，并检查新密码是否与旧密码相同。"""
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error("confirm_password", "密码不一致")

        # 去数据库校验：当前修改的密码不能和原来的密码相同
        if password and self.instance and self.instance.pk:
            old_password = (
                models.Admin.objects.filter(pk=self.instance.pk)
                .values_list("password", flat=True)
                .first()
            )
            if old_password and md5(password) == old_password:
                self.add_error("password", "不能与以前的密码相同")

        return cleaned_data

    def save(self, commit=True):
        """保存前把新密码转换为 MD5。"""
        admin = super().save(commit=False)
        admin.password = md5(admin.password)
        if commit:
            admin.save()
        return admin
