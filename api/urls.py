from django.conf.urls import url


from . import views


urlpatterns = [
        url(r'^offload/app/(?P<slug>[^/]+)$', views.forwarder.post),
        ]
