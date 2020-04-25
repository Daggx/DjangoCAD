from django.db import models

# Create your models here.


class Patient(models.Model):
    last_name = models.CharField(max_length=50, null=True, blank=True)
    first_name = models.CharField(max_length=50, null=True, blank=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    gender = models.CharField(
        max_length=1, choices=GENDER_CHOICES, null=True, blank=True)
    email = models.EmailField(
        max_length=254, unique=True, null=True, blank=True)
    Address = models.CharField(
        max_length=100, default=None, null=True, blank=True)

    def __str__(self):
        if self.last_name != None:
            return self.last_name + ' ' + self.first_name
        return 'patient irm :' + str(self.id)


class IRM(models.Model):
    id_patient = models.OneToOneField(Patient, on_delete=models.CASCADE)
    irm_pic = models.ImageField(default='default.jpg', upload_to='irm_pics')
    IRM_CATEGORIES = (
        ('F1', 'F1'),
        ('F2', 'F2'),
        ('F3', 'F3'),
    )
    irm_categorie = models.CharField(
        max_length=2, choices=IRM_CATEGORIES, null=True, blank=True)
    irm_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return 'IRM Patient  : ' + str(self.id_patient.id)
