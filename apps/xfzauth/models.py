from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from shortuuidfield import ShortUUIDField


class UserManager(BaseUserManager):
    def _creat_user(self, telephone, username, password, **kwargs):
        if not telephone:
            raise ValueError('请输入手机号码！')
        if not username:
            raise ValueError('请输入用户名！')
        if not password:
            raise ValueError('请输入密码！')

        user = self.model(telephone=telephone, username=username, **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, telephone, username, password, **kwargs):
        kwargs['is_superuser'] = False
        return self._creat_user(telephone, username, password, **kwargs)

    def create_superuser(self, telephone, username, password, **kwargs):
        kwargs['is_superuser'] = True
        kwargs['is_staff'] = True
        return self._creat_user(telephone, username, password, **kwargs)


class User(AbstractBaseUser, PermissionsMixin):
    # 为避免用户数量信息泄露，不适用自增长的主键，而是用uuid，但是因为uuid字符太长，可以用shortuuid替换
    # 安装方法：pip install django-shortuuidfield
    uid = ShortUUIDField(primary_key=True)
    telephone = models.CharField(max_length=11, unique=True)
    email = models.EmailField(unique=True, null=True)
    username = models.CharField(max_length=100)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # 设置默认验证字段
    USERNAME_FIELD = 'telephone'

    # 设置后，在创建superuser时会主动要求填写‘USERNAME_FIELD',’REQUIRED_FIELDS'，‘password'
    REQUIRED_FIELDS = ['username']

    # 根据字段，给指定用户发送邮件
    EMAIL_FIELD = 'email'

    object = UserManager()

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username
