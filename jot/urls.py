from django.conf.urls import patterns, url

urlpatterns = patterns('jot',
                       url(r'^get-objects-for/(?P<ct_id>\d+)?$',
                           'views.get_objects_for_fk',
                           name="jot_get_objects"),
                       )
