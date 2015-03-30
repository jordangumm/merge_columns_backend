from django.conf.urls import patterns, url

from uploader import views

urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       url(r'^upload$', views.upload_file, name='upload_file'),
                       url(r'^process$', views.process_files, name='process_files'),
)