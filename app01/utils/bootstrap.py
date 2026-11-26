# app01/utils/bootstrap.py
"""Form / ModelForm 的公共基类：统一给字段添加 Bootstrap 样式。"""
from django import forms


def _apply_bootstrap(fields, exclude_fields=()):
    """给字段添加 form-control 样式，placeholder 默认使用字段的 label。

    :param exclude_fields: 不套 form-control 的字段名（如 FileField 文件框）
    """
    for name, field in fields.items():
        if name in exclude_fields:
            continue

        # 保留控件已有的属性（如 Textarea 的 rows），再补上样式
        attrs = dict(field.widget.attrs)
        attrs["class"] = "form-control"
        attrs["placeholder"] = field.label
        field.widget.attrs = attrs


class BootstrapForm(forms.Form):
    """普通 Form 的基类。"""

    # 子类可覆盖：这些字段不套 form-control（文件上传框需要原样显示）
    bootstrap_exclude_fields = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _apply_bootstrap(self.fields, self.bootstrap_exclude_fields)


class BootstrapModelForm(forms.ModelForm):
    """所有业务 ModelForm 的基类，保持各表单字段样式一致。"""

    bootstrap_exclude_fields = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _apply_bootstrap(self.fields, self.bootstrap_exclude_fields)
