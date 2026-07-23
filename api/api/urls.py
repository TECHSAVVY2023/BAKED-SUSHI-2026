
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import RedirectView

urlpatterns = [
    re_path('', include('landingPage.urls')),
    path('admin/', admin.site.urls),
    path('api/bakedsushi/', include('bakedsushi.urls')),
]

#CATCH-ALL (KEEP LAST)
urlpatterns += [
    re_path(r'^.*$', RedirectView.as_view(url='/', permanent=False)),
]
