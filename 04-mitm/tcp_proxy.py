import asyncio
import re
import sys

CHUNK_SIZE = 4096
DUMP_LIMIT = 256
TEXT_LIMIT = 100
# Runs of plain ASCII long enough not to be a coincidence in encrypted noise.
PRINTABLE_RUN = re.compile(rb'[ -~]{8,}')


def printable_text(payload):
    runs = (match.group().decode('ASCII') for match in PRINTABLE_RUN.finditer(payload))
    text = ' | '.join(runs)
    return text if len(text) <= TEXT_LIMIT else f'{text[:TEXT_LIMIT]}...'


def dump(direction, payload):
    print(f'{direction}  {len(payload)} bytes')
    if text := printable_text(payload):
        print(f'    text  {text}')
    shown = payload[:DUMP_LIMIT]
    for offset in range(0, len(shown), 16):
        chunk = shown[offset:offset + 16]
        hexed = ' '.join(f'{byte:02x}' for byte in chunk)
        text = ''.join(chr(byte) if 32 <= byte < 127 else '.' for byte in chunk)
        print(f'    {offset:04x}  {hexed:<47}  {text}')
    if len(payload) > DUMP_LIMIT:
        print(f'    ... {len(payload) - DUMP_LIMIT} more bytes')
    sys.stdout.flush()


async def relay(reader, writer, direction):
    try:
        while payload := await reader.read(CHUNK_SIZE):
            dump(direction, payload)
            writer.write(payload)
            await writer.drain()
    except ConnectionError:
        pass
    finally:
        writer.close()


async def main(listen_port, target_port):

    async def wiretap(client_reader, client_writer):
        server_reader, server_writer = await asyncio.open_connection('localhost', target_port)
        await asyncio.gather(
            relay(client_reader, server_writer, 'client -> server'),
            relay(server_reader, client_writer, 'server -> client'),
            return_exceptions=True,
        )

    server = await asyncio.start_server(wiretap, 'localhost', listen_port)
    print(f'Relaying localhost:{listen_port} to localhost:{target_port}, and reading along.')
    async with server:
        await server.serve_forever()


def cli_args(command=sys.argv[0], args=sys.argv[1:]):
    match args:
        case (listen_port, target_port):
            return int(listen_port), int(target_port)
        case _:
            raise SystemExit(f'Usage: {command} LISTEN_PORT TARGET_PORT')


if __name__ == '__main__':

    listen_port, target_port = cli_args()
    try:
        asyncio.run(main(listen_port, target_port))
    except KeyboardInterrupt:
        pass
