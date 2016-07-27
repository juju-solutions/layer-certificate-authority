from charmhelpers.core.hookenv import log
from shlex import split

from subprocess import check_call
from subprocess import check_output
from subprocess import CalledProcessError


def install(src, tgt):
    """ This method wraps the bash "install" command """
    return check_call(split('install {} {}'.format(src, tgt)))


def get_output(cmd):
    """ Execute a command on the host. Supports bare string
    input.

    :param cmd: string of the command to Execute
    :returns: The output of the executed command
    """
    try:
        log('Executing: {}'.format(cmd), 'debug')
        out = check_output(split(cmd))
        return out.decode('ascii')
    except CalledProcessError as e:
        log('Error executing command. reason: {}'.format(e.stdout), 'critical')
        return e.stdout
