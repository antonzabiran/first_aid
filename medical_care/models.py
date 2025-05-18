from django.db import models
from django.urls import reverse
from taggit.managers import TaggableManager
from taggit.models import TagBase, GenericTaggedItemBase
from django.utils.text import slugify
from unidecode import unidecode

class CyrillicTag(TagBase):
    class Meta:
        verbose_name = "Медицинский тег"
        verbose_name_plural = "Медицинские теги"

    def slugify(self, tag, i=None):
        # Конвертируем кириллицу в латиницу
        slug = slugify(unidecode(tag))
        if i is not None:
            slug += f"_{i}"
        return slug

class TaggedEmergency(GenericTaggedItemBase):
    tag = models.ForeignKey(
        CyrillicTag,
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_items",
    )

class EmergencyCondition(models.Model):
    title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    protocol = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    tags = TaggableManager(blank=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('medical_care:info', args=[self.slug])

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title, allow_unicode=True)
        super().save(*args, **kwargs)
    

class AssessmentStep(models.Model):
    QUESTION_TYPES = (
        ('binary', 'Да/Нет'),
        ('multiple', 'Выбор из вариантов'),
    )
    
    question = models.CharField("Вопрос", max_length=255)
    question_type = models.CharField("Тип вопроса", max_length=10, choices=QUESTION_TYPES, default='binary')
    emergency = models.ForeignKey(EmergencyCondition, on_delete=models.CASCADE, related_name='steps')
    order = models.PositiveIntegerField("Порядок", default=0)
    yes_next = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='yes_steps')
    no_next = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='no_steps')
    action = models.TextField(blank=True)
    
    # Новое поле для связи вопросов с полями статуса
    STATUS_FIELD_CHOICES = [
        ('consciousness', 'Сознание'),
        ('breathing', 'Дыхание'),
        ('heartbeat', 'Сердцебиение'),
    ]
    status_field = models.CharField(
        max_length=15,
        choices=STATUS_FIELD_CHOICES,
        blank=True,
        null=True,
        verbose_name="Какое поле статуса обновлять"
    )

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.emergency.title} - {self.question}"

class AssessmentChoice(models.Model):
    step = models.ForeignKey(AssessmentStep, on_delete=models.CASCADE, related_name='choices')
    text = models.CharField(max_length=255)
    next_step = models.ForeignKey(AssessmentStep, on_delete=models.SET_NULL, null=True, blank=True, related_name='following_steps')

    def __str__(self):
        return self.text

class PatientStatus(models.Model):
    session_key = models.CharField(max_length=40)
    emergency = models.ForeignKey(EmergencyCondition, on_delete=models.CASCADE)
    consciousness = models.BooleanField(default=False)
    breathing = models.BooleanField(default=False)
    heartbeat = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Status {self.session_key}"

class EmergencyProtocol(models.Model):
    emergency = models.ForeignKey(EmergencyCondition, on_delete=models.CASCADE)
    step = models.ForeignKey(AssessmentStep, on_delete=models.CASCADE)
    order = models.PositiveIntegerField()
    
    class Meta:
        ordering = ['order']

class CPRTimer(models.Model):
    start_time = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    current_phase = models.CharField(
        max_length=12, 
        choices=[('compression', 'Надавливания'), ('ventilation', 'Вдохи')],
        default='compression'
    )
    cycle_count = models.IntegerField(default=0)
    
    def time_elapsed(self):
        return (timezone.now() - self.start_time).total_seconds()


class EmergencyMedia(models.Model):
    emergency = models.ForeignKey(
        'EmergencyCondition', 
        related_name='media', 
        on_delete=models.CASCADE
    )
    image = models.ImageField(upload_to='protocols/')
    description = models.TextField()
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name = 'Медиа-материал'
        verbose_name_plural = 'Медиа-материалы'

    def __str__(self):
        return f"Медиа {self.order} для {self.emergency.title}"