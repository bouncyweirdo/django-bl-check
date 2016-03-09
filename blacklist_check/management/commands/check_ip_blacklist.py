from django.core.management.base import BaseCommand

from blacklist_check.models import IpAddress, Types
from blacklist_check.utils import check_bl


class Command(BaseCommand):
    help = 'Check IP blacklist'

    def handle(self, *args, **options):
        ips = IpAddress.objects.filter(enabled=True, status=Types.STATUS_ACTIVE)
        for ip in ips:
            check_bl(ip)
