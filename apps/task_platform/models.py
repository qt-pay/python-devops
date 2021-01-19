from django.db import models

# Create your models here.
__all__ = ['ScriptProject', 'ScriptFile', 'AnsibleProject', 'AnsiblePlaybook', 'AnsibleParameter', 'TaskRecycle',
           'TaskHistory', 'TaskCrontab']


class ScriptProject(models.Model):
    name = models.CharField(verbose_name='脚本项目标题', max_length=32, unique=True)
    path = models.CharField(verbose_name='脚本项目路径', max_length=32, unique=True)
    src_user = models.CharField(verbose_name="上传用户", max_length=50, null=True, blank=True)
    latest_date = models.DateTimeField(verbose_name='更新时间', auto_now=True)
    create_date = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'task_platform_script_project'
        verbose_name = '脚本分类'
        verbose_name_plural = "脚本分类"


class ScriptFile(models.Model):
    name = models.CharField(verbose_name='任务名称', max_length=32, unique=True)
    file_name = models.CharField(verbose_name='脚本名称', max_length=32, unique=True, null=True, blank=True)
    project = models.ForeignKey(verbose_name='所属脚本项目', to=ScriptProject, on_delete=models.SET_NULL, blank=True,
                                null=True)
    exec_unm = models.IntegerField(verbose_name='执行次数', default=0)
    src_user = models.CharField(verbose_name="上传用户", max_length=50, null=True, blank=True)
    latest_date = models.DateTimeField(verbose_name='更新时间', auto_now=True)
    create_date = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'task_platform_script_file'
        verbose_name = '脚本任务'
        verbose_name_plural = '脚本任务'


class AnsibleProject(models.Model):
    name = models.CharField(verbose_name='项目标题', max_length=32)
    path = models.CharField(verbose_name='项目路径', max_length=32)
    src_user = models.CharField(verbose_name="上传用户", max_length=50, null=True, blank=True)
    online_status = models.BooleanField(verbose_name='激活状态', default=True)
    latest_date = models.DateTimeField(verbose_name='更新时间', auto_now=True)
    create_date = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'task_platform_absible_project'
        verbose_name = 'Ansible项目'
        verbose_name_plural = "Ansible项目"


class AnsiblePlaybook(models.Model):
    name = models.CharField(max_length=32, verbose_name='作业名称')
    exec_unm = models.IntegerField(verbose_name='执行次数', default=0)
    src_user = models.CharField(verbose_name="操作用户", max_length=50, null=True, blank=True)
    file_name = models.CharField(verbose_name='playbook剧本', max_length=120, null=True, blank=True)
    project = models.ForeignKey(verbose_name='所属项目', to=AnsibleProject, on_delete=models.SET_NULL, blank=True,
                                null=True)
    online_status = models.BooleanField(verbose_name='激活状态', default=True)
    latest_date = models.DateTimeField(verbose_name='更新时间', auto_now=True)
    create_date = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'task_platform_absible_playbook'
        verbose_name = 'palybook'
        verbose_name_plural = "palybook"


class AnsibleParameter(models.Model):
    name = models.CharField(max_length=50, verbose_name='变量组名', unique=True)
    param = models.CharField(verbose_name='配置参数', max_length=120, null=True, blank=True)
    playbook = models.ForeignKey(verbose_name='所属作业', to=AnsiblePlaybook, on_delete=models.CASCADE, blank=True,
                                 null=True)
    online_status = models.BooleanField(verbose_name='激活状态', default=True)
    src_user = models.CharField(verbose_name="操作用户", max_length=50, null=True, blank=True)
    latest_date = models.DateTimeField(verbose_name='更新时间', auto_now=True)
    create_date = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'task_platform_absible_parameter'
        verbose_name = 'a任务参数'
        verbose_name_plural = 'a任务参数'


# 定时任务扩展
class TaskCrontab(models.Model):
    name = models.CharField(verbose_name="定时任务名称", max_length=32)
    task_id = models.CharField(verbose_name='定时任务任务ID', max_length=128)
    task_status = models.BooleanField(default=True)
    run_type = models.CharField(verbose_name='执行方式', max_length=128)
    task_lib = models.CharField(verbose_name='任务类型', max_length=128)
    project = models.CharField(verbose_name='项目名称', max_length=128)
    task_hosts = models.TextField(verbose_name='主机列表', )
    task_file = models.CharField(verbose_name='执行脚本', max_length=128)
    hosts_file = models.CharField(verbose_name='hosts文件', max_length=128)
    task_args = models.CharField(verbose_name='参数', max_length=128)
    remarks = models.TextField(verbose_name="定时任务备注", )

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'task_platform_crontab'
        verbose_name = '定时任务'
        verbose_name_plural = '定时任务'


# 回收站
RecycleTaskType = ((0, 'script'), (1, 'playbook'))


class TaskRecycle(models.Model):
    task_type = models.IntegerField(verbose_name='脚本类型script/playbook', choices=RecycleTaskType, null=True, blank=True)
    src_user = models.CharField(verbose_name="操作用户", max_length=50, null=True, blank=True)
    source_name = models.CharField(max_length=50, verbose_name='原任务名', null=True, blank=True)
    source_project_name = models.CharField(max_length=50, verbose_name='原项目名', null=True, blank=True)
    source_project_path = models.CharField(max_length=50, verbose_name='原项目Path', null=True, blank=True)
    source_file_name = models.CharField(max_length=50, verbose_name='原脚本/包名', null=True, blank=True)
    path = models.CharField(max_length=1024, verbose_name='回收站中的路径', null=True, blank=True)

    def __str__(self):
        return self.source_name

    class Meta:
        db_table = 'task_platform_bin'
        verbose_name = '任务回收站'
        verbose_name_plural = '任务回收站'


# 历史任务
HistoryTaskType = ((0, '脚本任务'), (1, '剧本任务'), (2, '定时任务'), (3, '中间调度'))
HistoryRunType = ((0, 'ansible'), (1, 'ssh'),)


class TaskHistory(models.Model):
    src_user = models.CharField(verbose_name="操作用户", max_length=50, null=True, blank=True)
    src_ip = models.GenericIPAddressField(verbose_name="来源IP", max_length=50, null=True, blank=True)

    task_type = models.IntegerField(verbose_name="执行的任务类型", choices=HistoryTaskType, null=True, blank=True)
    task_name = models.CharField(verbose_name='任务名称', max_length=32, null=True, blank=True)
    task_host = models.CharField(verbose_name="目标主机/组", max_length=1020, null=True, blank=True)
    task_id = models.CharField(verbose_name='任务ID', max_length=128, null=True, blank=True)

    crontab_id = models.CharField(verbose_name="定时任务ID", max_length=128, null=True, blank=True)

    task_status = models.CharField(verbose_name='任务状态', max_length=128, null=True, blank=True)
    script_file = models.CharField(verbose_name='执行脚本', max_length=128, null=True, blank=True)
    script_cmd = models.CharField(verbose_name='执行命令', max_length=1024, null=True, blank=True)
    task_code = models.IntegerField(verbose_name='脚本返回状态码', null=True, blank=True)
    task_result = models.TextField(verbose_name='返回结果', null=True, blank=True)
    run_type = models.IntegerField(choices=HistoryRunType, null=True, blank=True)
    run_time = models.IntegerField(verbose_name="脚本运行时长(s)", null=True, blank=True)
    update_time = models.DateTimeField(verbose_name="更新时间", auto_now=True)
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)

    def __str__(self):
        return self.src_user

    class Meta:
        db_table = 'task_platform_history'
        verbose_name = '任务历史'
        verbose_name_plural = '任务历史'
