from django.db import models


# Create your models here.
class TimeBasedModel(models.Model):
    class Meta:
        abstract = True

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлено")

class Group(TimeBasedModel):
    class Meta:
        verbose_name = "Поток"
        verbose_name_plural = "Список потоков"

    def __str__(self):
        return self.name

    name = models.CharField(max_length=255, verbose_name="Название потока")
    visible = models.BooleanField(default=False, verbose_name="Скрыктый поток")


class Exam(TimeBasedModel):
    class Meta:
        verbose_name = "Экзамен"
        verbose_name_plural = "Список Экзаменов"

    def __str__(self):
        return self.name
    name = models.CharField(max_length=255, verbose_name="Предмет")


class Event(TimeBasedModel):
    class Meta:
        verbose_name = "Событие"
        verbose_name_plural = "Список событий"

    group = models.ForeignKey(Group, on_delete=models.DO_NOTHING, verbose_name="Поток")
    exam = models.ForeignKey(Exam, on_delete=models.DO_NOTHING, verbose_name="Экзамен")
    date_time = models.DateTimeField(auto_now_add=False, null=False)
    link = models.CharField(max_length=4000, null=True)

# class TelegramUser(TimeBasedModel):
#     class Meta:
#         verbose_name = "Пользователь"
#         verbose_name_plural = "Пользователи"
#
#     id = models.AutoField(primary_key=True)
#     user_id = models.BigIntegerField(unique=True, verbose_name="UserID")
#     name = models.CharField(max_length=255, verbose_name="UserName")
#     user_role = models.CharField(max_length=255, verbose_name="Роль")
#     state = models.IntegerField(verbose_name="Работает?", default=1)
#     phone = models.CharField(max_length=12, unique=True)
#     chat_id = models.BigIntegerField(verbose_name="Чат пользователя", default=0)
#     chanel_id = models.BigIntegerField(verbose_name="Канал пользователя", default=0)
