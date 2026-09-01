import asyncio
import ssl
import sys

CHUNK_SIZE = 4096


def show(direction, payload):
    print(f'--- {direction} ---')
    print(payload.decode('UTF-8', errors='replace'), end='')
    sys.stdout.flush()


def server_context(certificate_filename, private_key_filename, key_password):
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certificate_filename, private_key_filename, key_password)
    return context


def client_context():
    print('WARNING: the server certificate will not be checked!', file=sys.stderr)
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
    return context


async def relay(reader, writer, direction):
    try:
        while payload := await reader.read(CHUNK_SIZE):
            show(direction, payload)
            writer.write(payload)
            await writer.drain()
    except (ConnectionError, ssl.SSLError):
        pass
    finally:
        writer.close()


async def main(listen_port, target_port, listen_context, target_context):

    async def intercept(client_reader, client_writer):
        server_reader, server_writer = await asyncio.open_connection(
            'localhost', target_port, ssl=target_context
        )
        await asyncio.gather(
            relay(client_reader, server_writer, 'client -> server'),
            relay(server_reader, client_writer, 'server -> client'),
            return_exceptions=True,
        )

    server = await asyncio.start_server(intercept, 'localhost', listen_port, ssl=listen_context)
    print(f'Intercepting localhost:{listen_port} to localhost:{target_port}, in the clear.')
    async with server:
        await server.serve_forever()


def cli_args(command=sys.argv[0], args=sys.argv[1:]):
    match args:
        case (listen_port, target_port, certificate_filename, private_key_filename):
            return int(listen_port), int(target_port), certificate_filename, private_key_filename, None
        case (listen_port, target_port, certificate_filename, private_key_filename, key_password):
            return int(listen_port), int(target_port), certificate_filename, private_key_filename, key_password
        case _:
            raise SystemExit(
                f'Usage: {command} LISTEN_PORT TARGET_PORT CERTIFICATE PRIVATE_KEY [KEY_PASSWORD]'
            )


if __name__ == '__main__':

    listen_port, target_port, certificate_filename, private_key_filename, key_password = cli_args()
    listen_context = server_context(certificate_filename, private_key_filename, key_password)
    try:
        asyncio.run(main(listen_port, target_port, listen_context, client_context()))
    except KeyboardInterrupt:
        pass
