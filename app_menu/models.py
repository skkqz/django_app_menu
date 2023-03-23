from django.db import models


class Menu(models.Model):
    """
    Модель древовидного меню
    """
    name = models.CharField(max_length=50)
    url = models.CharField(max_length=100)
    parent = models.ForeignKey('self', null=True, blank=True,
                               related_name='children', on_delete=models.CASCADE)

    def __str__(self):
        return self.name
