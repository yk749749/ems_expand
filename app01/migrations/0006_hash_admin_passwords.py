import hashlib

from django.db import migrations


def _is_md5(value):
    """判断字符串是否已经是 32 位 MD5（十六进制）。"""
    return len(value) == 32 and all(char in "0123456789abcdef" for char in value.lower())


def hash_admin_passwords(apps, schema_editor):
    """把管理员表中的明文密码统一转换为 MD5。"""
    Admin = apps.get_model("app01", "Admin")
    for admin in Admin.objects.all():
        password = admin.password or ""
        if not _is_md5(password):
            admin.password = hashlib.md5(password.encode("utf-8")).hexdigest()
            admin.save(update_fields=["password"])


class Migration(migrations.Migration):

    dependencies = [
        ("app01", "0005_seed_admin"),
    ]

    operations = [
        migrations.RunPython(hash_admin_passwords, migrations.RunPython.noop),
    ]
