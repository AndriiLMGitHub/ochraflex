from django.contrib import admin
from .models import SurveyResponse, FieldResponse, SurveyResponseFavorite

# Register your models here.
admin.site.register(SurveyResponse)
admin.site.register(FieldResponse)
admin.site.register(SurveyResponseFavorite)