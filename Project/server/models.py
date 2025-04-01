import base64
import uuid
from collections import defaultdict
from django.db import models
from apps.users.models import CustomUser as User
from django_quill.fields import QuillField
from django.conf import settings

from ..company.models import Company

from ..payments.models import Billing


class Server(models.Model):
    '''Это модель физического сервера, на котором могут быть подняты различные сервисы'''
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    billing = models.ForeignKey(Billing, on_delete=models.SET_NULL, null=True, related_name='server')
    tunnel_id = models.CharField(max_length=255, null=True, blank=True)
    access_token = models.CharField(max_length=255, null=True, blank=True)
    tunnel_name = models.CharField(max_length=255, null=True, blank=True)
    tunnel_secret = models.CharField(max_length=255, null=True, blank=True)


class Service(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    PROTOCOL_TYPE_CHOICES = [
        ('ssh', 'SSH'),
        ('rdp', 'RDP'),
    ]
    server = models.ForeignKey(Server, on_delete=models.SET_NULL, null=True, related_name='services')
    protocol = models.CharField(max_length=10, choices=PROTOCOL_TYPE_CHOICES)
    port = models.IntegerField(default=3389)
    status = models.CharField(max_length=255, null=True, blank=True)
    access_url = models.CharField(max_length=255, null=True, blank=True)
    dns_record_id = models.CharField(max_length=255, default='None', blank=True)

    def __str__(self):
        return self.protocol

    @staticmethod
    def get_user_servers(user):
        service = Service.objects.filter(group__users=user).select_related('group__company').distinct()
        return service

    @staticmethod
    def get_services_by_company(company):
        services = Service.objects.filter(group__company=company).select_related('group', 'server').distinct()
        return services


class Credentials(models.Model):
    server = models.ForeignKey(Server, on_delete=models.CASCADE, null=True, related_name='credentials')
    account_tag = models.CharField(max_length=255, null=True, blank=True)
    tunnel_id = models.CharField(max_length=255, null=True, blank=True)
    tunnel_name = models.CharField(max_length=255, null=True, blank=True)
    tunnel_secret = models.CharField(max_length=255, null=True, blank=True)
