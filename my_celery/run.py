import os
from celery import Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'devops.settings')  # 设置django环境
# 启动命令 celery -A my_celery.run worker -l info

# 创建实例

app = Celery('test')
app.config_from_object('django.conf:settings', namespace='CELERY')

# 加载任务
app.autodiscover_tasks([
    'my_celery.script_task',
    'my_celery.playbook_task',
    'my_celery.paramiko_task',
])
