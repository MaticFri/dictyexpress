from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'dicty.views.index'),
    url(r'^(.*)$', 'dicty.views.others'),
    # url(r'^$', 'dictyExpress.views.home', name='home'),
    # url(r'^dictyExpress/', include('dictyExpress.urls2')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)