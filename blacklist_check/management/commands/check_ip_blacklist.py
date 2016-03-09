import sys
import os
import socket
import dns.resolver

from django.core.management.base import BaseCommand

from .models import IpAddress, DnsBlacklist
from .utils import check_bl


class Command(BaseCommand):
    help = 'Check IP blacklist'

    def handle(self, *args, **options):
        ips = IpAddress.objects.filter(enabled=True)
        for ip in ips:
            check_bl(ip)
