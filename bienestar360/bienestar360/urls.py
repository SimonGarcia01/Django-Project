from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

app_name = "login"
urlpatterns = [
    path('', RedirectView.as_view(url='/login/'), name='home'),
    path('', include('login.urls', namespace="login")),
    path('admin/', admin.site.urls),
    path('homepageCADI/', include(('homepageCADI.urls', 'homepageCADI'), namespace='homepageCADI')),
    path('homepageUser/', include(('homepageUser.urls', 'homepageUser'), namespace="homepageUser")),
    path("activities/", include("activities.urls")),
    path('tournaments/', include('tournaments.urls')),
    path('social_projects/', include(('social_projects.urls', 'social_projects'), namespace='social_projects')),
    path('preferences/', include(('UserPreference.urls', 'UserPreference'), namespace='UserPreference')),
    path('reportsAndStats/', include(('reportsAndStats.urls', 'reportsAndStats'), namespace='reportsAndStats')),

]
