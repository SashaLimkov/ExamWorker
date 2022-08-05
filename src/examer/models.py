from asgiref.sync import sync_to_async, async_to_sync
from django.db import models

# Create your models here.
from bot.config.loader import bot
from bot.utils.date_time_worker import date_time_formater
from bot.utils.notifier import send_new_time


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

    def save(self, *args, **kwargs):
        visible_changed = False
        if not self.pk:  # new object
            visible_changed = True
        else:
            orig_obj = Group.objects.get(pk=self.pk)
            if orig_obj.visible != self.visible:
                visible_changed = True
        if visible_changed:
            orig_obj = Group.objects.get(pk=self.pk)
            users = UserSubscriptions.objects.filter(group=orig_obj).all()
            text = f"Поток {orig_obj.name} закрыт." \
                   f"\nНапишите /start"
            for user in users:
                send_new_time(user.user.chat_id, text)
                user.user.user_exam.delete()
                user.delete()

        super(Group, self).save(*args, **kwargs)


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

    group = models.ForeignKey(Group, on_delete=models.CASCADE, verbose_name="Поток", related_name="get_events")
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, verbose_name="Экзамен")
    date_time = models.DateTimeField(auto_now_add=False, null=False)
    link = models.CharField(max_length=4000)

    def save(self, *args, **kwargs):
        time_changed = False
        if not self.pk:  # new object
            time_changed = True
        else:
            orig_obj = Event.objects.get(pk=self.pk)
            if orig_obj.date_time != self.date_time:
                time_changed = True
        if time_changed:
            try:
                orig_obj = Event.objects.get(pk=self.pk)
                users = UserExams.objects.filter(event=orig_obj).all()
                date_time = date_time_formater(str(orig_obj.date_time))
                text = f"Дата и/или время экзамена {orig_obj.exam} потока {orig_obj.group} изменились. \nНовая дата и время {date_time}" \
                   f"\nНапишите /start"
                for user in users:
                    send_new_time(user.user.chat_id, text)
            except:
                pass
        super(Event, self).save(*args, **kwargs)

    def __str__(self):
        return f"Экзамен по предмету {self.exam.name} потока {self.group.name}"


class UserSubscriptions(TimeBasedModel):
    class Meta:
        verbose_name = "Подписки Пользователей"
        verbose_name_plural = "Подписки Пользователей"

    user = models.OneToOneField("TelegramUser", on_delete=models.CASCADE, verbose_name="Пользователь")
    group = models.ForeignKey(Group, on_delete=models.CASCADE, verbose_name="Поток")


class UserExams(TimeBasedModel):
    class Meta:
        verbose_name = "Экзамены Пользователей"
        verbose_name_plural = "Экзамены Пользователей"

    user = models.OneToOneField("TelegramUser", on_delete=models.CASCADE, verbose_name="Пользователь", related_name="user_exam")
    event = models.ForeignKey(Event, on_delete=models.CASCADE, verbose_name="Проводимый экзамен")


class TelegramUser(TimeBasedModel):
    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.name

    chat_id = models.BigIntegerField(unique=True, verbose_name="UserID")
    name = models.CharField(max_length=255, verbose_name="Имя Пользователя")
    phone_number = models.CharField(max_length=30, verbose_name="Номер телефона")
