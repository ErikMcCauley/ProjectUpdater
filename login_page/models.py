from django.db import models

class projects(models.Model):
    projectCode = models.TextField()
    cleaved = models.TextField()
    purified = models.TextField()
    AAA = models.TextField()
    totalProjects = models.TextField()

    def __str__(self):
        return '%s %s %s %s %s' % (self.projectCode, self.cleaved, self.purified,self.AAA,self.totalProjects)

"""
from -APPNAME-.models import -MODELCLASS-
-INSTOBJECT- = -MODELCLASS-(-feild to enter- = "-ENTRY-", cont)
instobect.save()


"""