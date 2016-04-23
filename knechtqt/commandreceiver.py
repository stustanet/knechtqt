import asyncio
import re


class CommandReceiver(asyncio.Protocol):

    LINEBUF_MAX = 1024 * 512

    def __init__(self, knechtqt):
        self.buf = bytearray()
        self.knechtqt = knechtqt
        self.peername = None

    def connection_made(self, transport):
        self.transport = transport
        self.peername = transport.get_extra_info('peername')

    def data_received(self, data):
        if len(self.buf) + len(data) > self.LINEBUF_MAX:
            self.transport.write(b'too much!\n')
            self.close()
            return

        self.buf += data

        npos = self.buf.find(b"\n")
        if npos != -1:
            self.transport.write(b"yay!\n")
            self.transport.close()
            self._process_command(self.buf.decode())

    def _process_command(self, command):
        regex = re.compile(r'^(?:([0-9]+):)?(.*)$')
        match = regex.match(command)

        if match:
            text = match.group(2)
            duration = match.group(1)
            if duration and duration.isdigit():
                duration = int(duration)
            else:
                duration = None

            self.knechtqt.show_text(text, duration)
        else:
            print('Should never reach this point')

    def connection_lost(self, exc):
        pass
