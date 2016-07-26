

def sign(csr, ca="ca.pem", ca_key="ca-key.pem", config=None, profile=None,
         hostname=None, subject=None, label=None, remote=None):
    """ Signs a client cert with a host name by a given CA and CA key.

    :param csr:  PEM file for certificate request
    :param ca: CA used to sign the new certificate
    :param ca_key:  CA private key
    :param config: Path to configuration file
    :param profile: Signing profile to use
    :param hostname:  Hostname for the cert, could be a comma-separated
        hostname list
    :param subject: an optional file containing subject information to use
        for the certificate instead of the subject information in the CSR.
    :param label:  Key label to use in remote CFSSL server
    :param remote: Remote CFSSL server
     """

    # Usage of sign:
    # cfssl sign -ca cert -ca-key key [-config config] [-profile profile]
    # [-hostname hostname] CSR [SUBJECT]
    # cfssl sign -remote remote_host [-config config] [-profile profile]
    # [-label label] [-hostname hostname] CSR [SUBJECT]

    pass


def selfsign(hostname, csrjson):
    """ Generate a new self-signed key and signed certificate.

        WARNING: this should ONLY be used for testing. This should never be
        used in production.

        :param hostname: Hostname for the cert
        :param csrjson: JSON file containing the request

    """
    pass


def scan(host, list=False, family=None, scanner=None, timeout=0):
    """ Scan a host for issues.

    :param host: Host(s) to scan (including port)
    :param list: List possible scanners
    :param family: Scanner family regular expression
    :param scanner: Scanner regular expression
    :param timeout: duration (ns, us, ms, s, m, h) to scan each host before
     timing out
    """
    pass


def info(remote, label=None, profile=None, config=None):
    """ Get info about a remote signer.

   :param remote: Remote CFSSL server
   :param label: Key label to use in remote CFSSL server
   :param profile: Signing profile to use
   :param config: Path to configuration file

    """
    # cfssl info -remote remote_host [-label label] [-profile profile]
    # [-label label]  # noqa

    pass


def serve(address="127.0.0.1",
          ca="ca.pem",
          ca_bundle="/etc/cfssl/ca-bundle.crt",
          ca_key="ca-key.pem",
          int_bundle="/etc/cfssl/int-bundle.crt",
          int_dir="/etc/cfssl/intermediates",
          port="8888",
          metadata="/etc/cfssl/ca-bundle.crt.metadata",
          remote=None,
          config=None,
          uselocal=False):
    """ Set up a HTTP server handles CF SSL requests.

      :param address: Address to bind
      :param port: Port to bind
      :param ca: CA used to sign the new certificate
      :param ca-key: CA private key
      :param ca-bundle: Bundle to be used for root certificates pool
      :param int-bundle: Bundle to be used for intermediate certificates pool
      :param int-dir: specify intermediates directory
      :param metadata: Metadata file for
             root certificate presence. The content of the file is a json
             dictionary (k,v): each key k is SHA-1 digest of a root certificate
             while value v is a list of key store filenames.
      :param remote: remote CFSSL server
      :param config: path to configuration file
      :param uselocal: serve local static files as opposed to compiled

    """
    # cfssl serve [-address address] [-ca cert] [-ca-bundle bundle] \
    # [-ca-key key] [-int-bundle bundle] [-int-dir dir] [-port port] \
    # [-metadata file] [-remote remote_host] [-config config] [-uselocal]

    pass


def genkey(csrjson, initca=False, config=None):
    """ Generate a new key and CSR.

    :param csrjson: JSON file containing the request
    :param initca: initialise new CA
    :param config: path to configuration file
    """
    pass


def print_defaults(type):
    """ Print default configurations that can be used as a template.

    :param type: If "list" is used as the TYPE, the list of supported
        types will be printed.
    """
    pass
