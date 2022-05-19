import os
import subprocess

from channels.generic.websocket import JsonWebsocketConsumer


class TerminalConsumer(JsonWebsocketConsumer):
    def connect(self):
        self.accept()
        self.send_json({'output': f'{os.getcwd()}>\n'})

    def disconnect(self, code):
        self.close()

    def receive_json(self, content, **kwargs):
        cmd: str = content['cmd']
        result = ''
        if cmd.startswith('cd'):
            try:
                os.chdir(cmd[3:])
            except OSError:
                result = 'The filename, directory name, or volume label syntax is incorrect.\n'
        else:
            try:
                result = subprocess.check_output(cmd, shell=True).decode('ascii')
            except subprocess.CalledProcessError:
                result = f'"{cmd}" is not recognized as an internal or external command,operable program or batch file.\n'
        self.send_json({'output': f'{result}{os.getcwd()}>\n'})
