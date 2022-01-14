from datetime import datetime, timedelta

import jwt
from django.conf import settings
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager, PermissionsMixin)
from django.db import models

ROLE_CHOICE = (('educator', 'Педагог'),
               ('psychologist', 'Психолог'),
               ('optometrist', 'Специалист по зрению'),
               ('admin', 'Администратор'))

DIC_ROLE = {'educator': 'Педагог', 'psychologist': 'Психолог', 'optometrist': 'Специалист по зрению', 'admin': 'Администратор'}


class UserManager(BaseUserManager):
    def create_user(self, username, password, role):
        """ Создает и возвращает пользователя с паролем и именем. """
        if username is None:
            raise TypeError('Users must have a username.')
        user = self.model(username=username, role=role)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password, role):
        """ Создает и возввращет пользователя с привилегиями суперадмина. """
        if password is None:
            raise TypeError('Superusers must have a password.')
        user = self.create_user(username, password, role)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(db_index=True, max_length=255, unique=True, verbose_name='Пользователь')
    is_staff = models.BooleanField(default=False, verbose_name="Права администратора")
    role = models.CharField(choices=ROLE_CHOICE, max_length=255, verbose_name='Должность')

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['role']

    objects = UserManager()

    def __str__(self):
        return "{} {}".format(self.username, DIC_ROLE[self.role])

    @property
    def token(self):
        return self._generate_jwt_token()

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

    def _generate_jwt_token(self):
        dt = datetime.now() + timedelta(days=30)

        token = jwt.encode({
            'id': self.pk,
            'exp': dt.utcfromtimestamp(dt.timestamp())  # CHANGE HERE
        }, settings.SECRET_KEY, algorithm='HS256')

        return token

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
