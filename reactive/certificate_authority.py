from charms.reactive import when
from charms.reactive import when_not
from charms.reactive import set_state
from charms.templating.jinja2 import render
from charmhelpers.core.hookenv import config
from charmhelpers.core.hookenv import resource_get
from charmhelpers.core.hookenv import status_set
from charmhelpers.core.unitdata import kv

from ca_utils import install

from tempfile import NamedTemporaryFile

import cfssl
import cfssljson


@when_not('certificate-authority.installed')
def install_cfssl():
    """ Install the CFSSL binaries """
    status_set('maintenance', 'Installing CFSSL.')
    # Resources are used to deliver the CA binary bits
    cfssl_bin = resource_get('cfssl')
    cfssl_json_bin = resource_get('cfssljson')

    if not cfssl_bin or not cfssl_json_bin:
        status_set('blocked', 'Missing resources. See: README.md.')
        return

    install(cfssl_bin, '/usr/local/bin/cfssl')
    install(cfssl_json_bin, '/usr/local/bin/cfssljson')

    set_state('certificate-authority.installed')


@when('certificate-authority.installed')
@when_not('certificate-authority.initialized')
def initialize_ca():
    """ Initialize the certificate authority with keys """
    render('csr_ca.json', '/etc/cfssl/csr_ca.json', config())
    response = cfssl.gencert('/etc/cfssl/csr_ca.json', initca=True)
    temp = NamedTemporaryFile(suffix='.json')

    # write out the response to a temporary file, and generate the certificates
    # from the response json.
    with open(temp.name, 'w') as fp:
        fp.write(response)
        # when we are in context, we need to flush the buffer to actually write
        fp.flush()
        # Generate TLS keys from the JSON response
        cfssljson.parse("ca", bare=True, f=temp.name)
