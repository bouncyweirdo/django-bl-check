from __future__ import absolute_import

from celery.task import task

import shlex
import subprocess
import socket
from dns import resolver

from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist

from .models import Types, DnsBlacklist, IpAddress


@task()
def check_bl(address):
    data = dict()
    blacklist_hosts = DnsBlacklist.objects.all()
    blacklisted = True
    critical_blacklisted = True
    for bl in blacklist_hosts:
        try:
            my_resolver = resolver.Resolver()
            query = '.'.join(reversed(str(address).split("."))) + "." + bl.dns
            answers = my_resolver.query(query, "A")
            answer_txt = my_resolver.query(query, "TXT")
            data[bl.dns] = 'IP: {} IS listed in {} ({}: {})'.format(address, bl, answers[0], answer_txt[0])
            blacklisted = False
            if bl.critical:
                critical_blacklisted = False
        except:
            continue

    try:
        ip = IpAddress.objects.get(address=address)
    except ObjectDoesNotExist:
        return False

    ip.blacklisted = blacklisted
    ip.critical_blacklisted = critical_blacklisted
    ip.data = data
    ip.save()


@task()
def check_ip_status(address):
    rdns = None
    cmd = shlex.split("ping -c1 {}".format(address['address']))
    try:
        output = subprocess.check_output(cmd)
    except subprocess.CalledProcessError:
        status = Types.STATUS_DOWN
    else:
        status = Types.STATUS_ACTIVE

    if status == Types.STATUS_DOWN:
        client_socket = socket.socket()
        client_socket.settimeout(4)
        try:
            client_socket.connect((address['address'], address['ssh_port']))
        except socket.error:
            status = Types.STATUS_DOWN
        else:
            status = Types.STATUS_ACTIVE
        client_socket.close()

    if status == Types.STATUS_ACTIVE:
        try:
            rdns = socket.gethostbyaddr(address['address'])[0]
        except:
            pass

    try:
        ip = IpAddress.objects.get(address=address['address'])
    except ObjectDoesNotExist:
        return False

    ip.status = status
    ip.rdns = rdns
    ip.last_update = timezone.now()
    ip.save()
