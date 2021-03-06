from django.conf.urls.defaults import handler404, handler500, include,\
     patterns, url
from django.conf import settings
from django.conf.urls.i18n import *
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
from dialer_campaign.urls import urlpatterns as urlpatterns_dialer_campaign
from dialer_cdr.urls import urlpatterns as urlpatterns_dialer_cdr
from user_profile.urls import urlpatterns as urlpatterns_user_profile
from voip_app.urls import urlpatterns as urlpatterns_voip_app

from tastypie.api import Api
from api.resources import *

# tastypie api
tastypie_api = Api(api_name='v1')

tastypie_api.register(UserResource())
tastypie_api.register(GatewayResource())
tastypie_api.register(VoipAppResource())
tastypie_api.register(CampaignResource())
tastypie_api.register(PhonebookResource())
tastypie_api.register(BulkContactResource())
tastypie_api.register(CampaignDeleteCascadeResource())
tastypie_api.register(CampaignSubscriberResource())
tastypie_api.register(CallrequestResource())
tastypie_api.register(AnswercallResource())
tastypie_api.register(HangupcallResource())
tastypie_api.register(DialCallbackResource())
tastypie_api.register(CdrResource())


urlpatterns = patterns('',
    # redirect
    #('^$', 'django.views.generic.simple.redirect_to',
    #{'url': '/dialer_campaign/'}),

    # Example:

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # custom admin urls for admin dashboard
    (r'^admin_call_report/$',
     'dialer_campaign.views.admin_call_report'),
    (r'^admin_call_report_graph/$',
     'dialer_campaign.views.admin_call_report_graph'),
    (r'^admin_campaign_report/$',
     'dialer_campaign.views.admin_campaign_report'),
    (r'^admin_campaign_report_graph/$',
     'dialer_campaign.views.admin_campaign_report_graph'),
    (r'^admin_user_report/$',
     'dialer_campaign.views.admin_user_report'),
    (r'^admin_user_report_graph/$',
     'dialer_campaign.views.admin_user_report_graph'),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    
    (r'^api/', include(tastypie_api.urls)),
    
    (r'^i18n/', include('django.conf.urls.i18n')),
    (r'^jsi18n/(?P<packages>\S+?)/$', 'django.views.i18n.javascript_catalog'),

    (r'^admin_tools/', include('admin_tools.urls')),

    #(r'^$', include('dialer_campaign.urls')),
    #(r'^dialer_cdr/', include('dialer_cdr.urls')),
    #(r'^user_profile/', include('user_profile.urls')),

    (r'^static/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.STATIC_ROOT}),
        
    (r'^favicon\.ico$', 'django.views.generic.simple.redirect_to', {'url': 'static/newfies/images/favicon.png'}),
    
    (r'^sentry/', include('sentry.web.urls')),
)

urlpatterns += urlpatterns_dialer_campaign
urlpatterns += urlpatterns_dialer_cdr
urlpatterns += urlpatterns_user_profile
urlpatterns += urlpatterns_voip_app

handler404 = 'urls.custom_404_view'
handler500 = 'urls.custom_500_view'


def custom_404_view(request, template_name='404.html'):
    """404 error handler which includes ``request`` in the context.

    Templates: `404.html`
    Context: None
    """
    from django.template import Context, loader
    from django.http import HttpResponseServerError

    t = loader.get_template('404.html')  # Need to create a 404.html template.
    return HttpResponseServerError(t.render(Context({
        'request': request,
    })))


def custom_500_view(request, template_name='500.html'):
    """500 error handler which includes ``request`` in the context.

    Templates: `500.html`
    Context: None
    """
    from django.template import Context, loader
    from django.http import HttpResponseServerError

    t = loader.get_template('500.html')  # Need to create a 500.html template.
    return HttpResponseServerError(t.render(Context({
        'request': request,
    })))
