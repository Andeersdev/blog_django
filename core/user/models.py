from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class CustomUserManager(BaseUserManager):

    def create_user(self, full_names, email, password, image=None):
        if not email:
            raise ValueError('Please, enter email.')
        user = self.model(full_names=full_names,
                          email=self.normalize_email(email), image=image)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, full_names, email, password):
        user = self.create_user(full_names, email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user


class User(AbstractBaseUser):

    full_names = models.CharField(max_length=150)
    email = models.EmailField(max_length=150, unique=True)
    password = models.CharField(max_length=150)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    image = models.ImageField(upload_to='user/', null=True, blank=True)
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_names', 'password']

    class Meta:
        db_table = 'user'

    def __str__(self) -> str:
        return self.full_names

    def has_perm(self, app_label) -> bool:
        return self.is_superuser

    def has_module_perms(self, perm, object=None) -> bool:
        return self.is_superuser
