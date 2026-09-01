import sys

import requests

from lib import std_io


def cli_args(command=sys.argv[0], args=sys.argv[1:]):
    match args:
        case (url,):
            return url, True
        case (url, '--no-ca-check'):
            return url, False
        case (url, ca_certificate_filename):
            return url, ca_certificate_filename
        case _:
            raise SystemExit(f'Usage: {command} URL [CA_CERTIFICATE|--no-ca-check]')


if __name__ == '__main__':

    url, verify = cli_args()
    try:
        response = requests.get(url, verify=verify)
    except requests.exceptions.SSLError as error:
        raise SystemExit(f'Refused: {error}')
    except requests.exceptions.ConnectionError as error:
        raise SystemExit(f'Could not connect to {url}: {error}')
    std_io.write_text(response.status_code, lead='Status: ')
    std_io.write_text(response.text.strip(), lead='Body: ')
