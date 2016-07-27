from ca_utils import get_output


def parse(name, bare=False, f="-"):
    """ Parse the output from cfssl

    :param name: filename to prefix the certificates
    :param bare: the response from CFSSL is not wrapped in the API standard
        response
    :param f: JSON input, defaults to "-"" which is STDIN
    """
    cmd = ["cfssljson"]
    if bare:
        cmd.append("-bare")
    if f is not "-":
        cmd.append("".join(["-f=", f]))

    cmd.append(name)

    return get_output(" ".join(cmd))
