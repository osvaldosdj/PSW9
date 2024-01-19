from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Apostila(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    titulo = models.CharField(max_length=150)
    arquivos = models.FileField(upload_to='apostilas')
    
    def __str__(self):
        return self.titulo
    

class ViewApostila(models.Model):
    ip = models.GenericIPAddressField()
    apostila = models.ForeignKey(Apostila, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.ip
    
class AvaliacaoApostila(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    AVALIACAO_CHOICES = (('B', 'Bom'), ('R', 'Ruim'), ('P', 'Pode Melhorar'))
    apostila = models.ForeignKey(Apostila, on_delete=models.DO_NOTHING)
    avaliacao = models.CharField(max_length=1, choices=AVALIACAO_CHOICES)

    def __str__(self):
        return self.avaliacao