import shlex
import socket
import subprocess

from dns import resolver

from .models import Types


def check_bl(ip, bl):
    data = dict()
    blacklisted = True
    try:
        my_resolver = resolver.Resolver()
        query = '.'.join(reversed(str(ip).split("."))) + "." + bl
        answers = my_resolver.query(query, "A")
        answer_txt = my_resolver.query(query, "TXT")
        data[bl] = 'IP: {} IS listed in {} ({}: {})'.format(ip, bl, answers[0], answer_txt[0])
        blacklisted = False
    except Exception as e:
        pass

    data['blacklisted'] = blacklisted
    return data


def check_ip_status(ip, ssh_port=22):
    cmd = shlex.split("ping -c1 {}".format(ip))
    rdns = None
    try:
        output = subprocess.check_output(cmd)
    except subprocess.CalledProcessError as e:
        status = Types.STATUS_DOWN
    else:
        status = Types.STATUS_ACTIVE

    if status == Types.STATUS_DOWN:
        client_socket = socket.socket()
        client_socket.settimeout(4)
        try:
            client_socket.connect((ip, ssh_port))
        except socket.error:
            status = Types.STATUS_DOWN
        else:
            status = Types.STATUS_ACTIVE
        client_socket.close()

    if status == Types.STATUS_ACTIVE:
        try:
            rdns = socket.gethostbyaddr(ip)[0]
        except Exception as e:
            pass

    return {'status': status, 'rdns': rdns}
