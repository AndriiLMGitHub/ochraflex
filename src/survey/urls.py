from django.urls import path
from . import views

urlpatterns = [
    path('<int:block_id>/submit/', views.submit_survey_response, name='submit_survey'),
    path('<int:block_id>/detail/', views.survey_detail_view, name='survey_detail'),
]