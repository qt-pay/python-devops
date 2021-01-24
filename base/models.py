from django.db import models


# 基类
class BaseModel(models.Model):

    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='变更时间')
    remark = models.CharField(max_length=1024, null=True, blank=True, verbose_name='备注')

    class Meta:
        abstract = True
        ordering = ['-id']

    # def get_table_info(self):
    #     """
    #     获取table表
    #     """
    #     data = deal_fields_Table(self._meta.fields, True, True, 2, None, None, None)
    #     return data


def JSONFieldDefault():
    return {}


def JSONMulFieldDefault():
    return []

