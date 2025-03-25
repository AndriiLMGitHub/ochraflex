import uuid
from django.db import models
from django.conf import settings


class BlockTemplate(models.Model):
    LANGUAGES = (
        ('cs', 'Czech Republic'),
        ('de', 'Germany'),
    )  # Модель для зберігання шаблонів блоків
    user = models.ForeignKey(
        # Користувач, з яким прив’язаний шаблон
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='block_templates')
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=255)  # Назва блоку
    description = models.TextField(blank=True, null=True)  # Опис блоку
    language = models.CharField(
        blank=True, null=True, choices=LANGUAGES, max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)  # Дата створення
    library_templates = models.ManyToManyField('LibraryTemplate', blank=True)

    def __str__(self):
        return self.name


class DescriptionField(models.Model):
    # Використовується для зберігання описів полів
    block_template = models.ForeignKey(
        BlockTemplate,
        on_delete=models.CASCADE,
        related_name='description_fields',
        null=True,
        blank=True
    )
    title = models.CharField(max_length=128, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    is_combined = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Field(models.Model):
    TEXT = 'text'
    SELECT = 'select'
    TEXTAREA = 'textarea'
    CHECKBOX = 'checkbox'
    RADIO = 'radio'
    NUMBER = 'number'
    DATE = 'date'
    MIN_LENGTH = 'min_length'
    MAX_LENGTH = 'max_length'
    MIN = 'min'
    MAX = 'max'
    BOOLEAN = 'boolean'
    PHONE = 'phone'
    BUTTON = 'button'

    FIELD_TYPES = [
        (TEXT, 'Text'),
        (TEXTAREA, 'Textarea'),
        (NUMBER, 'Number'),
        (SELECT, 'Select'),
        (CHECKBOX, 'Checkbox'),
        (RADIO, 'Radio'),
        (DATE, 'Date'),
        (BOOLEAN, 'Boolean'),
        (PHONE, 'Phone'),
        (BUTTON, 'Button'),
    ]

    name = models.CharField(max_length=128)  # Назва поля
    field_type = models.CharField(
        max_length=50,
        choices=FIELD_TYPES
    )  # Тип поля
    # Варіанти відповіді для select/radio/checkbox
    options = models.JSONField(blank=True, null=True, default=list)
    static_value = models.CharField(
        max_length=1000, null=True, blank=True)
    max_symbols = models.PositiveIntegerField(default=3, null=True, blank=True)
    max_numbers = models.PositiveBigIntegerField(
        default=3, null=True, blank=True)
    help_info = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )  # Додаткова інформація
    is_required = models.BooleanField(default=False)  # Чи є поле обов’язковим
    extra_tag = models.CharField(max_length=255, blank=True, null=True)
    is_combined = models.BooleanField(default=False)
    block_template = models.ForeignKey(
        BlockTemplate,
        on_delete=models.CASCADE,
        related_name='fields',
        null=True,
        blank=True
    )

    def __str__(self):
        return self.name


class CombinedBlock(models.Model):
    block_template = models.ForeignKey(
        BlockTemplate,
        on_delete=models.CASCADE,
        related_name='combined_blocks',
        null=True,
        blank=True
    )
    description_field = models.ForeignKey(
        DescriptionField,
        on_delete=models.CASCADE,
        related_name='combined_blocks',
        null=True,
        blank=True,
    )
    fields = models.ManyToManyField(
        Field,
        related_name='duplicates',
        blank=True,
    )
    allow_dublicate = models.BooleanField(default=False)

    # def __str__(self):
    #     return self.description_field


class LibraryTemplate(models.Model):
    user = models.ForeignKey(
        # Користувач, з яким прив’язаний шаблон
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='library_templates',
        blank=True,
        null=True
    )
    name = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )  # Назва шаблону
    description = models.TextField(blank=True, null=True)  # Опис шаблону
    created_at = models.DateTimeField(auto_now_add=True)  # Дата створення
    field = models.ForeignKey(
        Field,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='library_templates'
    )
    description_field = models.ForeignKey(
        DescriptionField,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='library_templates'
    )
    combined_block = models.ForeignKey(
        CombinedBlock,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='library_templates'
    )
