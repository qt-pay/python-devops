# Generated by Django 2.2.2 on 2021-01-01 14:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Menus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=32, verbose_name='菜单名称')),
                ('url', models.CharField(help_text='精确URL与前端匹配不好包含正则', max_length=128, verbose_name='URL')),
                ('pid', models.IntegerField(blank=True, help_text='为0则是一级菜单,指定id则是指定id的二级菜单', null=True, verbose_name='是否为主菜单')),
                ('icon', models.CharField(default='111', help_text='指定显示的icon图标', max_length=32, verbose_name='图标')),
            ],
            options={
                'verbose_name': '菜单表',
                'verbose_name_plural': '菜单表',
                'db_table': 'rbac_menus',
            },
        ),
        migrations.CreateModel(
            name='Permissions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=32, verbose_name='名称')),
                ('url', models.CharField(max_length=128, verbose_name='含正则的URL')),
                ('method', models.CharField(choices=[('GET', 'GET'), ('POST', 'POST'), ('PUT', 'PUT'), ('PATCH', 'PATCH'), ('DELETE', 'DELETE')], default='GET', help_text='请求的类型', max_length=10, verbose_name='请求类型')),
                ('remarks', models.TextField(blank=True, null=True, verbose_name='备注')),
                ('pid', models.IntegerField(blank=True, help_text='0为权限分类指定ID则属于二级', null=True, verbose_name='是否为分类')),
            ],
            options={
                'verbose_name': '权限表',
                'verbose_name_plural': '权限表',
                'db_table': 'rbac_permissions',
            },
        ),
        migrations.CreateModel(
            name='Roles',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=32, unique=True, verbose_name='角色名称')),
                ('remarks', models.TextField(blank=True, default=None, null=True, verbose_name='备注')),
                ('menus', models.ManyToManyField(blank=True, help_text='可以打开那些菜单', to='rbac.Menus', verbose_name='拥有的菜单权限')),
                ('permissions', models.ManyToManyField(blank=True, to='rbac.Permissions', verbose_name='拥有的所有权限')),
            ],
            options={
                'verbose_name': '角色表',
                'verbose_name_plural': '角色表',
                'db_table': '_rbac_roles',
            },
        ),
    ]