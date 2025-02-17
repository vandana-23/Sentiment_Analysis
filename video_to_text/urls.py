"""
URL configuration for video_to_text project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include  
from django.conf import settings
from django.conf.urls.static import static 
from videoprocessor import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),  # Root URL points to home view
    path('upload/', views.upload_video, name='upload'),
    # path('success/', views.success, name='success'),
    path('', include('videoprocessor.urls')),  # Include app URLs
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
