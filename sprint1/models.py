from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.conf import settings
from model_utils import Choices


class UserManager(BaseUserManager):
    def _create_user(self, email, birth_date, password, is_staff, is_superuser, **extra_fields):
        if not email:
            raise ValueError('Email necéssaire pour la création')
        if not birth_date:
            raise ValueError('Pas de date de naissance ! ')

        now = timezone.now()
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            birth_date=birth_date,
            is_staff=is_staff,
            is_active=True,
            is_superuser=is_superuser,
            last_login=now,
            date_joined=now,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, birth_date=None, password=None, **extra_fields):
        return self._create_user(email, password, False, False, **extra_fields)

    def create_superuser(self, email, birth_date, password, **extra_fields):
        user = self._create_user(
            email, birth_date, password, True, True, **extra_fields)
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=254, unique=True, error_messages={
                              'unique': "This email has already been registered."})
    name = models.CharField(max_length=254, null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    birth_date = models.DateField(null=True, blank=True)
    is_doctor = models.BooleanField(default=False)
    is_receptionist = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['birth_date']

    objects = UserManager()

    def get_absolute_url(self):
        return "/users/%i/" % (self.pk)

    def get_email(self):
        return self.email


GRADES = Choices('Resident ', 'Assistant', 'Maître assistant',
                 'Professeur ', 'Chef de service')
SPECIALITES = Choices('Généraliste', 'Neurologue', 'NeuroChirurgien')


class Wilaya(models.Model):
    numero = models.IntegerField(primary_key=True)
    nom = models.CharField(blank=False, null=False, max_length=50)

    def __str__(self):
        return self.nom


class Hopital(models.Model):

    name = models.CharField(blank=False, null=False, max_length=75)
    wilaya = models.ForeignKey(
        Wilaya, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Hopitaux"

    def __str__(self):
        return str(self.wilaya.numero) + " : " + self.name


class Doctor(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='doctor')

    first_name = models.CharField(blank=False, null=False, max_length=255)
    last_name = models.CharField(blank=False, null=False, max_length=255)
    grade = models.CharField(choices=GRADES, blank=False,
                             null=False, max_length=255)
    specialite = models.CharField(
        choices=SPECIALITES, blank=False, null=False, max_length=255)
    hopital = models.ForeignKey(Hopital, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return "Dr. " + self.last_name + " " + self.first_name


class Receptionist(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='receptionist')
    first_name = models.CharField(blank=False, null=False, max_length=255)
    last_name = models.CharField(blank=False, null=False, max_length=255)
    wilaya = models.ForeignKey(Wilaya, on_delete=models.CASCADE, null=True)
    hopital = models.ForeignKey(Hopital, on_delete=models.CASCADE, null=True)

    def __str__(self):

        return self.first_name + " " + self.last_name
