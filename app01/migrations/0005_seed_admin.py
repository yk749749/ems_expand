from django.db import migrations


def create_default_admin(apps, schema_editor):
    """插入默认管理员：颜楷 / 123456（对应讲义 12.2 的 insert 语句）。"""
    Admin = apps.get_model("app01", "Admin")
    if not Admin.objects.filter(username="颜楷").exists():
        Admin.objects.create(username="颜楷", password="123456")


def delete_default_admin(apps, schema_editor):
    """回滚时删除默认管理员。"""
    Admin = apps.get_model("app01", "Admin")
    Admin.objects.filter(username="颜楷", password="123456").delete()


class Migration(migrations.Migration):

    dependencies = [
        ("app01", "0004_admin"),
    ]

    operations = [
        migrations.RunPython(create_default_admin, delete_default_admin),
    ]
