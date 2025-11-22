from django.core.validators import MinLengthValidator
from django.db import models

class Project(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name="Название проекта")
    description = models.TextField(verbose_name="Описание проекта")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="Тег")
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        related_name="children",
        null=True,
        blank=True
    ) # todo: manytomany связи тегов! не забыть! ⚠️⚠️⚠️

    def __str__(self):
        return self.name

class Task(models.Model):
    STATUS_CHOICES = [
        ('New', 'Новая'),
        ('In Progress', 'В процессе'),
        ('Completed', 'Выполнена'),
        ('On Hold', 'Приостановлена'),
    ]

    PRIORITY_CHOICES = [
        (1, 'Низкий'),
        (2, 'Средний'),
        (3, 'Высокий'),
        (4, 'Критический'),
    ]

    name = models.CharField(
        max_length=255,
        unique=True,
        validators=[MinLengthValidator(10)],
        verbose_name="Название задачи"
    )
    description = models.TextField(blank=True, null=True, verbose_name="Описание задачи")
    status = models.CharField(
        max_length=15,
        choices=STATUS_CHOICES,
        default='New',
        verbose_name="Статус"
    )
    priority = models.PositiveSmallIntegerField(
        choices=PRIORITY_CHOICES,
        verbose_name="Приоритет"
    )
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='tasks',
        verbose_name="Проект"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    deleted_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Дата удаления"
    )
    due_date = models.DateField(
        null=True,
        blank=True,
        verbose_name="Срок выполнения"
    )
    tags = models.ManyToManyField(
        Tag, blank=True,
        related_name='tasks',
        verbose_name="Теги"
    )

    def __str__(self):
        return self.name