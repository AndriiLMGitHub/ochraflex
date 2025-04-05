from django.urls import path
from . import views

urlpatterns = [
    path('<str:uuid>/submit/', views.submit_survey_response, name='submit_survey'),
    path('<str:uuid>/detail/<str:response_id>/', views.survey_detail_view, name='survey_detail'),
    path('<str:uuid>/generate-partial-pdf/<str:response_id>/', views.generate_partial_pdf, name='generate_partial_pdf'),
    #Delete survey
    path('<str:survey_id>/delete/', views.delete_survey_view, name='delete_survey'),
    path('response/<str:uuid>/<str:response_id>/', views.test_pdf_view, name='test_pdf'),
    # Favorites
    path('favorites/toggle/<str:survey_response_id>/', views.toggle_favorite, name='toggle_favorite'),
    path('delete/<int:survey_response_id>/', views.delete_survey_response, name='delete_survey_response'),

]