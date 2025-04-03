from django.urls import path
from . import views

urlpatterns = [
    path('<str:uuid>/submit/', views.submit_survey_response, name='submit_survey'),
    path('<str:uuid>/detail/<str:response_id>/', views.survey_detail_view, name='survey_detail'),
    path('<str:uuid>/generate-partial-pdf/<str:response_id>/', views.generate_partial_pdf, name='generate_partial_pdf'),
    path('<str:id>/choose/language/', views.choose_language_questionare_view, name='choose_language_questionare'),
    #Delete survey
    path('<str:survey_id>/delete/', views.delete_survey_view, name='delete_survey'),
    path('test/url/<str:uuid>/<str:response_id>/', views.test_pdf_view, name='test_pdf'),
    path('test/url/more/<str:uuid>/<str:response_id>/', views.my_view, name='my_view')
]