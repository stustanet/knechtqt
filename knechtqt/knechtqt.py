import sys
import signal
import asyncio
import time
import subprocess

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from quamash import QEventLoop, QThreadExecutor

from .commandreceiver import CommandReceiver


class KnechtQT:

    def __init__(self, args):
        self.port = args.port
        self.address = args.listen

        self.app = None
        self.window = None
        self.loop = None

    def _close_window(self):
        if self.window:
            self.window.showNormal()
            self.window.hide()
            self.window.close()
            self.window = None

    def show_text(self, text, duration=None):
        if duration is None or duration <= 0:
            duration = 10

        if self.window:
            self._close_window()

        try:
            subprocess.run(['xset', 'dpms', 'force'])
        except FileNotFoundError as e:
            pass

        label = QLabel()
        label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        label.setTextFormat(Qt.RichText)
        label.setWordWrap(True)
        label.setText('<span style="font-size:100px">%s</span>' % text)

        self.window = QMainWindow()
        self.window.setWindowTitle("KnechtQT")
        self.window.setCentralWidget(label)

        self.window.showFullScreen()

        self.loop.call_later(duration, self._close_window)

    def launch(self):
        self.app = QApplication([])
        self.app.setQuitOnLastWindowClosed(False)
        self.loop = QEventLoop(self.app)
        asyncio.set_event_loop(self.loop)

        signal.signal(signal.SIGINT, signal.SIG_DFL)

        with self.loop:
            coro = self.loop.create_server(lambda: CommandReceiver(self),
                                           self.address, self.port)
            server = self.loop.run_until_complete(coro)

            self.loop.run_forever()

            server.close()
            loop.run_until_complete(server.wait_closed())
