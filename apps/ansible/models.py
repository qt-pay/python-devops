from django.db import models

# Create your models here.
__all__ = ['History', 'Project', 'Job', 'Extravars']

ONLINE_STATUS = ((0, '停用'), (1,'激活'))

# 历史任务
class History(models.Model):
    login_user = models.CharField(verbose_name='登录用户', max_length=32)
    src_ip = models.CharField(verbose_name='来源IP', max_length=50)
    task_name = models.CharField(verbose_name='任务类型', max_length=50, blank=True, null=True)
    time_task_start = models.DateTimeField(verbose_name='任务开始时间', null=True, blank=True)
    time_task_finished = models.DateTimeField(verbose_name='任务结束时间', auto_now_add=True)
    cmd_object = models.CharField(verbose_name='操作对象', max_length=50, blank=True, null=True)
    cmd = models.TextField(verbose_name="执行命令",)
    cmd_result = models.CharField(verbose_name="命令结果", max_length=10)
    cmd_detail = models.TextField(verbose_name="结果详情",  null=True, blank=True)
    def __str__(self):
        return self.task_name

    class Meta:
        db_table = 'absible_history'
        verbose_name = '任务历史'
        verbose_name_plural = "任务历史"

class Project(models.Model):
    name = models.CharField(verbose_name='项目标题', max_length=32)
    path = models.CharField(verbose_name='项目路径', max_length=32)
    online_status = models.BooleanField(verbose_name='激活状态',  default=True)
    def __str__(self):
        return self.name

    class Meta:
        db_table = 'absible_project'
        verbose_name = '项目'
        verbose_name_plural = "项目"

class Job(models.Model):
    name = models.CharField(max_length=32, verbose_name='作业名称')
    playbook = models.CharField(verbose_name='playbook剧本', max_length=120, null=True, blank=True)
    project = models.ForeignKey(verbose_name='所属项目', to=Project, on_delete=models.SET_NULL, blank=True, null=True)
    online_status = models.BooleanField(verbose_name='激活状态',  default=True)
    def __str__(self):
        return self.name
    class Meta:
        db_table = 'absible_job'
        verbose_name = '作业'
        verbose_name_plural = "作业"
class Extravars(models.Model):
    name = models.CharField(max_length=50, verbose_name='变量组名', unique=True)
    vers = models.CharField(verbose_name='配置参数',max_length=120, null=True, blank=True )
    job = models.ForeignKey(verbose_name='所属作业', to=Job, on_delete=models.SET_NULL, blank=True, null=True)
    online_status = models.BooleanField(verbose_name='激活状态',  default=True)
    def __str__(self):
        return self.name
    class Meta:
        db_table = 'absible_extravars'
        verbose_name = '任务参数'
        verbose_name_plural = '任务参数'