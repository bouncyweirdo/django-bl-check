from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField
from django.db import models


class Types:

    STATUS_UNKNOWN = 0
    STATUS_ACTIVE = 1
    STATUS_DOWN = 2

    STATUS_TYPE = (
        (STATUS_UNKNOWN, 'Unknown'),
        (STATUS_ACTIVE, 'Up'),
        (STATUS_DOWN, 'Down'),
    )


class DnsBlacklist(models.Model):
    dns = models.CharField(max_length=500, default=None, blank=True, null=True)
    critical = models.BooleanField(default=False)

    def __str__(self):
        return self.dns


class IpAddress(models.Model):
    user = models.ForeignKey(User)
    address = models.GenericIPAddressField(help_text="Ip address that you want to check.")
    hostname = models.CharField(max_length=500, default=None, blank=True, null=True, help_text="Server hostname where IP is used, for info purposes.")
    rdns = models.CharField(max_length=500, default=None, blank=True, null=True, help_text="Reverse DNS, this field automatically added.")
    status = models.SmallIntegerField(choices=Types.STATUS_TYPE, default=0, help_text="IP status")
    blacklisted = models.BooleanField(default=True, help_text="Unchecked if IP is blacklisted, Checked if IP is clean.")
    critical_blacklisted = models.BooleanField(default=True, help_text="Unchecked if IP is blacklisted in a critical blacklist, Checked if IP is clean.")
    enabled = models.BooleanField(default=True, help_text="If checked, checks will run for this IP.")
    data = JSONField(default={"": ""}, blank=True, null=True, help_text="Info about blacklists")
    last_update = models.DateTimeField(default=None, blank=True, null=True, help_text="Last ip check")
    ssh_port = models.SmallIntegerField(default=22, help_text="Used to check IP accessibility if ping is down, default port 22")

    def __str__(self):
        return self.hostname or self.address

    def reversed_ip(self):
        return '.'.join(self.address.split('.')[::-1])
