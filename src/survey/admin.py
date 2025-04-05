from django.contrib import admin
from .models import SurveyResponse, FieldResponse, SurveyResponseFavorite

# Register your models here.
admin.site.register(FieldResponse)
admin.site.register(SurveyResponseFavorite)

@admin.register(SurveyResponse)
class SeriesResponseAdmin(admin.ModelAdmin):
    list_display = ('user', 'block_template', 'is_deleted',)