from django.db import models

class UUID(models.Model):
    id = models.UUIDField()
