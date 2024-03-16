from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

# redirect urls to there target path/files
urlpatterns = [
    # redirect home page
    path('', views.show_page, name='home'),

    # redirect login page
    path('login/', views.login_page, name='login'),

    # redirect signup page
    path('signup/', views.sign_up, name='signup'),

    # redirect create event page
    path('create_event/', views.create_event, name='create_event'),

    # redirect to likeed event page
    path('like_event/<int:event_id>/', views.like_event, name='like_event'),

    # redirect to user-specific events page
    path('user-specific/', views.user_specific, name="specific")
]


# This block of code is typically found in Django projects and is used to serve media files
# during development when the DEBUG mode is enabled. Media files include images, videos, etc.

# The following condition checks if the Django project is running in debug mode.
if settings.DEBUG:

    # If the project is in debug mode, this line adds a URL pattern to the urlpatterns list.
    # This pattern is used to serve media files located in the directory specified by MEDIA_ROOT
    # at the URL specified by MEDIA_URL. This allows direct access to media files via a URL during development.
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

