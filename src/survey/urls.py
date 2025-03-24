from django.urls import path
from . import views

urlpatterns = [
    path('<str:uuid>/submit/', views.submit_survey_response, name='submit_survey'),
    path('<str:uuid>/detail/<str:response_id>/', views.survey_detail_view, name='survey_detail'),
    path('<str:uuid>/generate-partial-pdf/', views.generate_partial_pdf, name='generate_partial_pdf'),
]