from django.db import models


# Create your models here.
class Department(models.Model):
    title = models.CharField(verbose_name='标题', max_length=32)

    def __str__(self):
        return self.title


class UserInfo(models.Model):
    name = models.CharField(verbose_name='姓名', max_length=16)
    password = models.CharField(verbose_name='密码', max_length=64)
    age = models.IntegerField(verbose_name='年龄')
    account = models.DecimalField(verbose_name='账户余额', max_digits=10, decimal_places=2, default=0)
    # 表关联
    depart = models.ForeignKey(verbose_name='部门', to=Department, to_field='id', on_delete=models.CASCADE)


class PrettyNum(models.Model):
    mobile = models.CharField(verbose_name='号码', max_length=11)
    price = models.IntegerField(verbose_name='价格', default=0)
    level_choices = (
        (1, "1级"),
        (2, "2级"),
        (3, "3级"),
        (4, "4级"),
    )
    level = models.IntegerField(verbose_name='级别', choices=level_choices, default=1)
    status_choices = (
        (1, "已占用"),
        (2, "未使用"),
    )
    status = models.SmallIntegerField(verbose_name='状态', choices=status_choices, default=2)


class Admin(models.Model):
    username = models.CharField(verbose_name="用户名", max_length=32)
    password = models.CharField(verbose_name="密码", max_length=64)