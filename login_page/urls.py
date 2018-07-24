from django.conf.urls import url, include
from . import views
from login_page.resources import loginResource


login_resource = loginResource()

app_name = "login_page"

urlpatterns = [
    url(r'^$', views.login_view, name="login"),
    url(r'^display/$', views.display, name="display"),
    url(r'^api/', include(login_resource.urls)),

]
