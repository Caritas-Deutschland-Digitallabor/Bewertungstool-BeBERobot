from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', lambda req: redirect('/bewertungstool/')),
    path('admin/', admin.site.urls),
    path('bewertungstool/', include('polls_cms_integration.urls', namespace="polls")), # Link all the other urls that are in the polls_cms_integration url file
    # Rute to all the pages related with reseting the password
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="password/password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password/password_reset_complete.html'), name='password_reset_complete'),
    # Rute to all the pages related with the confirmation of email
    path('email_sent/', auth_views.PasswordResetDoneView.as_view(template_name='confirmation_email/email_sent.html'), name='email_sent'),
    path('email_confirmed/', auth_views.PasswordResetDoneView.as_view(template_name='confirmation_email/email_confirmed.html'), name='email_confirmed'),
    path('link_invalid/', auth_views.PasswordResetDoneView.as_view(template_name='confirmation_email/link_invalid.html'), name='link_invalid'),

]

if settings.DEBUG:
    urlpatterns.extend(static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))

urlpatterns.append(path('', include('cms.urls')))

# the new django admin sidebar is bad UX in django CMS custom admin views.
admin.site.enable_nav_sidebar = False
