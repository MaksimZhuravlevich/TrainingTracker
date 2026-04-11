from django.db import models

class MuscleGroup(models.Model):
    name=models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Equipment(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
class Exercise(models.Model):
    name=models.CharField(max_length=50)
    description=models.TextField(blank=True,null=True)
    muscles = models.ManyToManyField(MuscleGroup,related_name='exercises')
    equipment=models.ForeignKey(
        Equipment,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    def __str__(self):
        return self.name
