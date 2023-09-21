from django.db import models

# Create your models here.
class BusStations(models.Model):
    terminal_name = models.CharField(max_length=256, null=True, blank=True)
    terminal_code = models.IntegerField(null=True,blank=True)

    def __str__(self):
        return str(self.terminal_code) + ':' + str(self.terminal_name)


