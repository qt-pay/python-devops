# Generated by Django 2.2.2 on 2021-01-09 17:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0013_remove_taskscript_script_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='taskscript',
            name='script_name',
            field=models.CharField(blank=True, max_length=32, null=True, unique=True, verbose_name='脚本名称'),
        ),
    ]