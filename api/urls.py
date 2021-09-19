from django.urls import path
from api.views import RandomNumberView, download, home, detail, object_detail

app_name = 'api'

urlpatterns = [
    path('object', RandomNumberView.as_view(), name='generate-obj'),
    path('object/<name>', object_detail, name='object-detail'),
    path('download/<name>', download, name='download'),
    path('', home, name='home'),
    path('detail/<name>', detail, name='detail')
]