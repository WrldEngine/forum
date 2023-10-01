from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from forum import views

user_patterns = [
    path('', views.user, name='user'),
    path('settings/', views.settings, name='settings')
]

urlpatterns = [
    path('', views.index),
    path('admin/', admin.site.urls),
    path('reg/', views.reg, name='registration'),
    path('auth/', views.auth, name='authorization'),
    path('verify/<str:name>/<str:email>/', views.verify, name='verify'),
    path('user/<str:username>/', include(user_patterns), name='user'),
    path('ask', views.ask_question),
    path('q/<str:subject>/<int:id>/', views.question_details, name='q_details'),
    path('questions/', views.questions),
    path('logout', views.logout_page)
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
