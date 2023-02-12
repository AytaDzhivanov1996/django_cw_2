from django.conf import settings
from django.db import models
from django.utils.datetime_safe import date


class Client(models.Model):
    NULLABLE = {'blank': True, 'null': True}

    created_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='пользователь',
                                     **NULLABLE)
    email = models.EmailField(max_length=250, verbose_name='контактный e-mail')
    full_name = models.CharField(max_length=250, verbose_name='фио')
    comment = models.TextField(verbose_name='комментарий', **NULLABLE)

    def __str__(self):
        return f'{self.full_name}'


class Mailing(models.Model):
    NULLABLE = {'blank': True, 'null': True}

    PERIOD_ONCE_DAY = 'once_a_day'
    PERIOD_ONCE_WEEK = 'once_a_week'
    PERIOD_ONCE_MONTH = 'once_a_month'
    PERIODS = (
        ('once_a_day', 'раз в день'),
        ('once_a_week', 'раз в неделю'),
        ('once_a_month', 'раз в месяц')
    )
    STATUS_COMPLETED = 'completed'
    STATUS_CREATED = 'created'
    STATUS_LAUNCHED = 'launched'
    STATUS_DEACTIVATED = 'deactivated'
    STATUSES = (
        ('completed', 'завершена'),
        ('created', 'создана'),
        ('launched', 'запущена'),
        ('deactivated', 'деактивирована')
    )

    created_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь',
                                     **NULLABLE)
    client = models.ForeignKey('coursach.Client', verbose_name='Клиент', on_delete=models.SET_NULL, null=True)
    message = models.ForeignKey('coursach.Letter', verbose_name='Сообщение', on_delete=models.SET_NULL, null=True)
    time_of_mailing = models.TimeField(verbose_name='Время рассылки', **NULLABLE)
    periodicity = models.CharField(choices=PERIODS, default=PERIOD_ONCE_WEEK, max_length=50,
                                   verbose_name='Периодичность')
    mailing_status = models.CharField(choices=STATUSES, default=STATUS_COMPLETED, max_length=50,
                                      verbose_name='Статус рассылки')
    start_date = models.DateField(default=date.today, verbose_name='Начальная дата')
    end_date = models.DateField(default=date.today, verbose_name='Конечная дата')

    class Meta:
        permissions = [
            ('deactivate',
             'Can deactivate mailing')
        ]


class Letter(models.Model):
    NULLABLE = {'blank': True, 'null': True}

    created_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='пользователь',
                                     **NULLABLE)
    letter_topic = models.CharField(max_length=350, verbose_name='Тема письма')
    letter_body = models.TextField(verbose_name='Тело письма')

    def __str__(self):
        return f'{self.letter_topic}'


class MailingTry(models.Model):
    NULLABLE = {'blank': True, 'null': True}

    date = models.DateTimeField(auto_now_add=True, verbose_name='дата и время попытки')
    status = models.CharField(max_length=50, verbose_name='статус попытки')
    answer = models.CharField(max_length=250, verbose_name='ответ почтового сервера', **NULLABLE)
