from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
9


def index(request):
    if request.user.is_authenticated:
        return redirect('questionnaires')
    else:
        return redirect('signin')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('account/', include('account.urls')),
    path('dashboard/', include('app.urls')),
    path('dashboard/survey/', include('survey.urls')),
]
