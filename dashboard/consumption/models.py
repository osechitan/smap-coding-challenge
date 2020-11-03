# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class User(models.Model):
    """User Model"""
    class Meta:
        db_table = 'user'

    area = models.CharField(verbose_name='area', max_length=2)
    tariff = models.CharField(verbose_name='tariff', max_length=2)

    def __str__(self):
        return f'{self.id}'


class Consumption(models.Model):
    """Consuption Model"""
    class Meta:
        db_table = 'consumption'

    user = models.ForeignKey(User,
                             verbose_name='user',
                             on_delete=models.CASCADE)
    datetime = models.DateTimeField(verbose_name='datetime')
    consumption = models.FloatField(verbose_name='consumption')

    def __str__(self):
        return f'{self.id}'
