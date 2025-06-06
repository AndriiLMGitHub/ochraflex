from django.db import models
from app.models import BlockTemplate, Field, CombinedBlock
from django.conf import settings

# Create your models here.
class SurveyResponse(models.Model):
    LANGUAGES = (
        ('cs', 'Czech Republic'),
        ('de', 'Germany'),
    ) 
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='survey_responses',
        null=True,  # Тепер може бути пустим
        blank=True
    )
    email = models.EmailField(null=True, blank=True)  # Для анонімних користувачів
    block_template = models.ForeignKey(
        BlockTemplate,
        on_delete=models.CASCADE,
        related_name='survey_responses'
    )
    submitted_at = models.DateTimeField(auto_now_add=True)
    language = models.CharField(
        blank=True, null=True, choices=LANGUAGES, max_length=128, default='cs'
    )
    is_deleted = models.BooleanField(default=False)  # Поле для відмітки, чи відповідь видалена
    deleted_at = models.DateTimeField(null=True, blank=True)  # Час, коли було позначено як видалене


    def __str__(self):
        return f"{self.user} - {self.block_template}"

class FieldResponse(models.Model):
    INPUT_METHODS = (
        ('paste', 'Paste'),
        ('keyboard', 'Keyboard'),
        ('unknown', 'Unknown'),
    )
    survey_response = models.ForeignKey(
        SurveyResponse,
        on_delete=models.CASCADE,
        related_name='field_responses'
    )
    field = models.ForeignKey(
        Field,
        on_delete=models.CASCADE,
        null=True,  # Може бути порожнім для DescriptionField
        blank=True,
        related_name='field_responses'
    )
    combined_block = models.ForeignKey(
        CombinedBlock,
        on_delete=models.CASCADE,
        null=True,  # Відповідь може бути пов'язана з CombinedBlock
        blank=True,
        related_name='combined_block_responses'
    )
    value = models.TextField()
    input_time = models.IntegerField(default=0, null=True, blank=True)
    input_method = models.CharField(max_length=128, choices=INPUT_METHODS, blank=True, null=True)

    def __str__(self):
        return f"{self.survey_response} - {self.field} - {self.value[:50]}"
    

class SurveyResponseFavorite(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='favorite_survey_responses'
    )
    survey_response = models.ForeignKey(
        SurveyResponse,
        on_delete=models.CASCADE,
        related_name='favorited_by_users'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'survey_response')

    def __str__(self):
        return f"{self.user} favorite {self.survey_response}"


