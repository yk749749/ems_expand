from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0006_hash_admin_passwords'),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level', models.SmallIntegerField(choices=[(1, '紧急'), (2, '重要'), (3, '普通')], default=1, verbose_name='级别')),
                ('title', models.CharField(max_length=64, verbose_name='标题')),
                ('detail', models.TextField(verbose_name='详细信息')),
                ('leader', models.ForeignKey(on_delete=models.deletion.CASCADE, to='app01.userinfo', verbose_name='负责人')),
            ],
        ),
    ]
