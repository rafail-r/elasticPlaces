from django.conf.urls import url

from . import views

app_name = 'searchapp'
urlpatterns = [
	url(r'^home', views.search_page, name='search_page'),
    url(r'^results/$', views.search_results, name='search_results'),
    url(r'^details/(?P<_id>\w+)', views.get_by_id, name='get_by_id'),
    url(r'^live_search', views.live_search, name='live_search'),
]