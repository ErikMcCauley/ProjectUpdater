from tastypie.resources import ModelResource
from login_page.models import projects
from tastypie.authorization import Authorization


class loginResource(ModelResource):
    class Meta:
        queryset = projects.objects.all()
        resource_name = 'log'
        authorization = Authorization()
