from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect


# Home redirect (root URL)
def home_redirect(request):
    return redirect('/accounts/login/')


urlpatterns = [
    # Root URL (fixes 404)
    path('', home_redirect),

    # Django Admin
    path('admin/', admin.site.urls),

    # App Routes
    path('accounts/', include('accounts.urls')),
    path('tickets/', include('tickets.urls')),
    path('prediction/', include('prediction.urls')),
    path('reminders/', include('reminders.urls')),
    path('adminpanel/', include('adminpanel.urls')),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)