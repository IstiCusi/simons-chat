#!/usr/bin/env python3

import re
from enum import Enum
from typing import Optional
import argparse
import threading
import socket
import time
import subprocess
import pkg_resources
import sys


# python_version = sys.version_info
# python_major = python_version.major
# python_minor = python_version.minor

# venv_dir = os.path.expanduser(f'~/.chat/venv/py{python_major}.{python_minor}')

# if not os.path.exists(venv_dir):
#     subprocess.check_call([sys.executable, '-m', 'venv', venv_dir])

# venv_lib = os.path.join(venv_dir, 'lib', f'python{python_major}.{python_minor}', 'site-packages')
# sys.path.append(venv_lib)

required = {"raylib-py"}
installed = {pkg.key for pkg in pkg_resources.working_set}
missing = required - installed

if missing:
    print("The following packages will be installed now", missing)
    python = sys.executable
    subprocess.check_call(
        [python, "-m", "pip", "install", *missing], stdout=subprocess.DEVNULL
    )

import raylibpy

raylibpy.set_trace_log_level(raylibpy.LOG_NONE)


def parse_arguments():
    parser = argparse.ArgumentParser(description="Connect to a chat server.")
    parser.add_argument(
        "--host",
        type=str,
        default="localhost",
        help="Hostname or IP address of the chat server",
    )
    parser.add_argument(
        "--port", type=int, default=1602, help="Port number of the chat server"
    )
    return parser.parse_args()


class MsgType(Enum):
    ME = 1
    FRIEND = 2


class ChatNetworkHandler:

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket: Optional[socket.socket] = None
        self.observers = []
        self.connected = False

    def connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.socket.connect((self.host, self.port))
            threading.Thread(target=self.receive_message_loop,
                             daemon=True).start()
            self.connected = True
        except:
            print("Server could not be reached -- please use /connect in GUI")
            self.connected = False

    def is_connected(self):
        assert self.socket is not None, "Socket not initialized"
        return self.connected

    def send_message(self, message):
        assert self.socket is not None, "Socket not initialized"
        self.socket.sendall(message.encode())

    def receive_message_loop(self):
        assert self.socket is not None, "Socket not initialized"
        try:
            while True:
                message = self.socket.recv(4096).decode()
                if message:
                    self.notify_observers(message)
                else:
                    break
        finally:
            self.socket.close()

    def register_observer(self, observer):
        if observer not in self.observers:
            self.observers.append(observer)

    def notify_observers(self, message):
        for observer in self.observers:
            observer.update(message)

    def close(self):
        assert self.socket is not None, "Socket not initialized"
        self.socket.close()


class ChatClient:

    def __init__(self, network_address="localhost", port=1602):
        self.screen_width = 1210
        self.screen_height = 450

        raylibpy.init_window(
            self.screen_width, self.screen_height, "Simon's chat")
        raylibpy.set_target_fps(60)

        self.font = raylibpy.load_font("./Font.ttf")
        raylibpy.set_texture_filter(
            self.font.texture, raylibpy.TEXTURE_FILTER_TRILINEAR
        )
        self.font_size = self.font.base_size
        self.char_width = raylibpy.measure_text_ex(
            self.font, "A", self.font_size, 1)[0]
        self.max_length = (int)(self.screen_width / self.char_width) - 7

        self.network_address = network_address
        self.port = port

        self.network_handler = ChatNetworkHandler(network_address, port)
        self.network_handler.register_observer(self)

        self.messages = []

        self.input_text = ""
        self.cursor_position = 0
        self.cursor_visible = True

        self.last_blink_time = time.time()
        self.blink_interval = 0.5

        self.backspace_pressed = False
        self.backspace_timer = 0
        self.backspace_delay = 0.07
        self.last_backspace_time = time.time()

    def handle_input(self):
        max_length = self.max_length
        key = raylibpy.get_char_pressed()
        while key > 0:
            if key >= 32 and key <= 125:
                if (
                    len(self.input_text) < max_length
                    or self.cursor_position < max_length
                ):
                    self.input_text = (
                        self.input_text[: self.cursor_position]
                        + chr(key)
                        + self.input_text[self.cursor_position:]
                    )
                    self.cursor_position += 1
            key = raylibpy.get_char_pressed()

    def handle_cursor_movement(self):
        if raylibpy.is_key_pressed(raylibpy.KEY_RIGHT):
            if self.cursor_position < len(self.input_text):
                self.cursor_position += 1
        elif raylibpy.is_key_pressed(raylibpy.KEY_LEFT):
            if self.cursor_position > 0:
                self.cursor_position -= 1

    def handle_backspace(self):
        current_time = time.time()
        if raylibpy.is_key_down(raylibpy.KEY_BACKSPACE):
            if (
                not self.backspace_pressed
                or current_time - self.last_backspace_time > self.backspace_delay
            ):
                if self.cursor_position > 0:
                    self.input_text = (
                        self.input_text[: self.cursor_position - 1]
                        + self.input_text[self.cursor_position:]
                    )
                    self.cursor_position -= 1
                    self.last_backspace_time = current_time
                self.backspace_pressed = True
        else:
            self.backspace_pressed = False

    def handle_enter(self):
        if (
            raylibpy.is_key_pressed(raylibpy.KEY_ENTER)
            and self.input_text.strip() != ""
        ):
            self.send_message(self.input_text)
            self.input_text = ""
            self.cursor_position = 0

    def update_cursor_blink(self):
        if time.time() - self.last_blink_time > self.blink_interval:
            self.cursor_visible = not self.cursor_visible
            self.last_blink_time = time.time()

    def draw(self):
        raylibpy.begin_drawing()

        raylibpy.clear_background(raylibpy.RAYWHITE)

        for i, message in enumerate(self.messages[-12:]):
            text_color = raylibpy.BLACK if message[1] == MsgType.ME else raylibpy.GRAY
            raylibpy.draw_text_ex(
                self.font,
                message[0],
                raylibpy.Vector2(20, 10 + i * 30),
                self.font_size,
                1,
                text_color,
            )

        raylibpy.draw_rectangle(
            10, self.screen_height - 50, self.screen_width - 20, 40, raylibpy.DARKBLUE
        )
        raylibpy.draw_text_ex(
            self.font,
            self.input_text,
            raylibpy.Vector2(20, self.screen_height - 45),
            self.font_size,
            1,
            raylibpy.YELLOW,
        )

        if self.cursor_visible:
            cursor_x = (
                20
                + raylibpy.measure_text_ex(
                    self.font,
                    self.input_text[: self.cursor_position],
                    self.font_size,
                    1,
                ).x
            )
            raylibpy.draw_rectangle(
                int(cursor_x),
                self.screen_height - 45,
                self.char_width,
                30,
                raylibpy.PINK,
            )
            if self.cursor_position < len(self.input_text):
                letter_under_cursor = self.input_text[self.cursor_position]
                raylibpy.draw_text_ex(
                    self.font,
                    letter_under_cursor,
                    raylibpy.Vector2(int(cursor_x), self.screen_height - 45),
                    self.font_size,
                    1,
                    raylibpy.WHITE,
                )

        raylibpy.end_drawing()

    def update(self, message):
        self.messages.append([message, MsgType.FRIEND])

    def connect_to_server(self):
        self.network_handler.connect()
        if not self.network_handler.is_connected():
            message = "*** Not connected ***"
        else:
            message = "*** Connected  ***"
        self.messages.append([message, MsgType.ME])

    def parse_command(self, message):
        connect_pattern = r"/connect\s+(\S+:\d+)"
        beep_pattern = r"/beep"

        connect_match = re.match(connect_pattern, message)
        beep_match = re.match(beep_pattern, message)

        if connect_match:
            command = "connect"
            argument = connect_match.group(1)
        elif beep_match:
            command = "beep"
            argument = None
        else:
            command = None
            argument = None

        return command, argument

    def handle_commands(self, tokens):
        command = tokens[0]
        if command == "connect":
            print(tokens[0])
            print(tokens[1])
        elif command == "beep":
            pass

    def send_message(self, message):
        tokens = self.parse_command(message)
        if tokens and tokens[0]:
            self.handle_commands(tokens)
            message = "*** Executed ***"
        elif self.network_handler.is_connected():
            self.network_handler.send_message(message)
        else:
            message = "*** Not connected ***"

        self.messages.append([message, MsgType.ME])

    def run(self):
        while not raylibpy.window_should_close():
            self.handle_input()
            self.handle_backspace()
            self.handle_cursor_movement()
            self.handle_enter()
            self.update_cursor_blink()
            self.draw()
        raylibpy.close_window()


if __name__ == "__main__":

    args = parse_arguments()
    client = ChatClient(network_address=args.host, port=args.port)
    client.connect_to_server()
    client.run()
