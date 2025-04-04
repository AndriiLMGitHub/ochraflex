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
    path('add_to_favorites/<int:response_id>/', views.add_to_favorites, name='add_to_favorites'),
    path('remove_from_favorites/<int:response_id>/', views.remove_from_favorites, name='remove_from_favorites'),
]