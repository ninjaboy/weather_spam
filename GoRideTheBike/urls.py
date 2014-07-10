from django.conf.urls import patterns, include, url
from GoRideTheBike import views

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'GoRideTheBike.views.home', name='home'),
    # url(r'^GoRideTheBike/', include('GoRideTheBike.GoRideTheBike.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^$',views.index, name = 'index'),
    url(r'^today/',views.today, name='today'),
    url(r'^tomorrow/',views.tomorrow, name = 'tomorrow'),
    url(r'^work_instruction/',views.work_instruction, name = 'work_instruction'),

)
