
import uuid
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from parler.models import TranslatableModel, TranslatedFields

class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True

    def soft_delete(self):
        self.deleted_at = timezone.now()
        self.save()

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_('Email is required'))
        email = self.normalize_email(email)
        if extra_fields.get('role') == 'ADMIN':
            extra_fields['is_superuser'] = True
            extra_fields['is_staff'] = True
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields['role'] = 'ADMIN'
        return self.create_user(email, password, **extra_fields)

class User(BaseModel, AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    photo = models.ImageField(upload_to='user_photos/', null=True, blank=True)
    address = models.TextField()
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    role = models.CharField(max_length=20, choices=(('CLIENT', 'Client'), ('PROVIDER', 'Provider'), ('ADMIN', 'Admin')), default='CLIENT')

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone', 'address', 'role']

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Client(User):
    class Meta:
        verbose_name = _('Client')
        verbose_name_plural = _('Clients')

    def save(self, *args, **kwargs):
        self.role = 'CLIENT'
        super().save(*args, **kwargs)

class Provider(User):
    skills = models.ManyToManyField('Service', related_name='providers')
    is_approved = models.BooleanField(default=False)

    class Meta:
        verbose_name = _('Provider')
        verbose_name_plural = _('Providers')

    def save(self, *args, **kwargs):
        self.role = 'PROVIDER'
        super().save(*args, **kwargs)

class Admin(User):
    class Meta:
        verbose_name = _('Admin')
        verbose_name_plural = _('Admins')

    def save(self, *args, **kwargs):
        self.role = 'ADMIN'
        self.is_superuser = True
        self.is_staff = True
        super().save(*args, **kwargs)

class Service(TranslatableModel):
    translations = TranslatedFields(
        name=models.CharField(max_length=100),
        description=models.TextField(),
        notes=models.TextField(blank=True)
    )
    category = models.CharField(max_length=50)

    class Meta:
        verbose_name = _('Service')
        verbose_name_plural = _('Services')

    def __str__(self):
        return self.name

class Request(BaseModel):
    STATUS_CHOICES = (
        ('PENDING', _('Pending')),
        ('ACCEPTED', _('Accepted')),
        ('REJECTED', _('Rejected')),
        ('COMPLETED', _('Completed')),
        ('CANCELLED', _('Cancelled')),
        ('EXPIRED', _('Expired')),
    )
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='requests')
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    description = models.TextField()
    location = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    accepted_provider = models.ForeignKey(Provider, on_delete=models.SET_NULL, null=True, blank=True)
    task_date = models.DateTimeField(null=True, blank=True, help_text=_('Date and time when the task should be performed'))

    class Meta:
        verbose_name = _('Request')
        verbose_name_plural = _('Requests')

    def __str__(self):
        return f"Request by {self.client} for {self.service}"

    def is_expired(self):
        if self.task_date and self.task_date < timezone.now():
            self.status = 'EXPIRED'
            self.save()
            return True
        return False

class Response(BaseModel):
    STATUS_CHOICES = (
        ('PENDING', _('Pending')),
        ('ACCEPTED', _('Accepted')),
        ('REJECTED', _('Rejected')),
    )
    request = models.ForeignKey(Request, on_delete=models.CASCADE, related_name='responses')
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE)
    message = models.TextField()
    proposed_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')

    class Meta:
        verbose_name = _('Response')
        verbose_name_plural = _('Responses')

    def __str__(self):
        return f"Response by {self.provider} to {self.request}"