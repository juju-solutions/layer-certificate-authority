from charms.reactive import when
from charms.reactive import when_not
from charms.reactive import set_state
from charmhelpers.core.hookenv import resource_get
from charmhelpers.core.hookenv import status_set
from ca_utils import install

import cfssl


@when_not('certificate-authority.installed')
def install_certificate_authority():
    # Resources are used to deliver the CA binary bits
    cfssl_bin = resource_get('cfssl')
    cfssl_json_bin = resource_get('cfssljson')

    if not cfssl_bin or not cfssl_json_bin:
        status_set('blocked', 'Missing resources. See: README.')
        return

    install(cfssl_bin, '/usr/local/bin/cfssl')
    install(cfssl_json_bin, '/usr/local/bin/cfssljson')

    set_state('certificate-authority.installed')


@when('certificate-authority.installed')
@when_not('certificate-authority.initialized')
def initialize_ca():
    cfssl.sign()
