import datetime

from django.utils import timezone
from django.core.management.base import BaseCommand

from blacklist_check.models import IpAddress, Types
from blacklist_check.tasks import check_ip_status


class Command(BaseCommand):
    help = 'Check IP status and rdns'

    def handle(self, *args, **options):
        ips = IpAddress.objects.filter(enabled=True, status__in=[Types.STATUS_DOWN, Types.STATUS_UNKNOWN]).values('address', 'ssh_port')
        for ip in ips:
            check_ip_status.delay(ip)

        now = timezone.now()
        last_update = now - datetime.timedelta(minutes=5)

        ips = IpAddress.objects.filter(enabled=True, last_update__lte=last_update).values('address', 'ssh_port')
        for ip in ips:
            check_ip_status.delay(ip)
