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
import uuid


@when_not('certificate-authority.apikey.available')
def generate_api_key():
    """ To secure API requests, we will generate an API key and store
    it in unitdata for later access. """
    # TODO: Create an action to regenerate this API key in the event of
    # compromise
    status_set('maintenance', 'Generating API security key')
    raw = str(uuid.uuid1())
    api_key = raw.replace('-', '')
    db = kv()
    db.set('cfssl.apikey', api_key)
    set_state('certificate-authority.apikey.available')


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
@when_not('certificate-authority.ca.placed')
def initialize_ca():
    """ Initialize the certificate authority with keys """
    # write out the CA CSR json to the primary store
    render('csr_ca.json', '/etc/cfssl/csr_ca.json', config())
    # Generate the CA CSR from CFSSL and capture output
    response = cfssl.gencert('/etc/cfssl/csr_ca.json', initca=True)
    temp = NamedTemporaryFile(suffix='.json')

    # write out the response to a temporary file, and generate the certificates
    # from the response json.
    # TODO: Red October integration to keep our CA Key from being unencrypted
    # on disk.
    with open(temp.name, 'w') as fp:
        fp.write(response)
        # when we are in context, we need to flush the buffer to actually write
        fp.flush()
        # Generate TLS keys from the JSON response
        cfssljson.parse("/etc/cfssl/ca", bare=True, f=temp.name)

    set_state('certificate-authority.ca.placed')


@when('certificate-authority.ca.placed')
@when_not('certificate-authority.policy.placed')
def initialize_default_policy():
    """ Configure CFSSL with default signing policies. This initializes a few
    different configurations for generating certificates """
    db = kv()
    apikey = db.get('cfssl.apikey')
    # render the default 5 year policies
    render(config('default_policy'), '/etc/cfssl/policy.json',
           {'apikey': apikey})
    set_state('certificate-authority.policy.placed')


@when('config.default_policy.changed', 'certificate-authority.policy.placed')
def react_to_policy_change():
    initialize_default_policy()
