from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager, User
from django.utils.translation import ugettext_lazy as _
# from apps.rbac.models import Roles
# Create your models here.
__all__ = ['UserProfile','Department']


# 定义管理类
class UserManager(BaseUserManager):
    use_in_migrations = True
    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)  # 创建对象 UserProfile(email='', password='')
        user.set_password(password)  # 把密码加密
        user.save(using=self._db)  # 保存到数据库
        return user
    # 创建普通用户
    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    # 创建超级用户
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(email, password, **extra_fields)
# 定义部门
class Department(models.Model):
    title = models.CharField(max_length=32, verbose_name="部门名称")
    count = models.IntegerField(verbose_name="人数", default=0)

    def __str__(self):
        return self.title
    class Meta:
        db_table = 'user_department'
        verbose_name = '部门管理'
        verbose_name_plural = "部门管理"
# 定义UserProfile这个类的管理类
#
class UserProfile(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField('邮箱', max_length=255,unique=True, db_index=True)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('是否允许用户登录admin站点.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    name = models.CharField(verbose_name='名字',max_length=32, db_index=True)
    department = models.ForeignKey(verbose_name='部门',to='Department',  blank=True, null=True, on_delete=models.SET_NULL)
    roles =  models.ManyToManyField(verbose_name='角色',to='rbac.Roles', blank=True)
    phone = models.CharField(verbose_name='手机号码', max_length=32,  blank=True, null=True)
    remarks = models.TextField(verbose_name='备注', blank=True, null=True, default=None)
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'  # 用来唯一确定auth中的用户
    REQUIRED_FIELDS = ['name']  # auth指定除了上面两个配置项的字段还有那些字段要必填

    class Meta:
        db_table = 'user_profile'
        verbose_name = '用户表'
        verbose_name_plural = "用户表"
    #
    def get_full_name(self):
        # The user is identified by their email address
        return self.name

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):  # __unicode__ on Python 2
        return self.name
    # 给项目添加管理类
    objects = UserManager()