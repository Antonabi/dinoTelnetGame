import socketserver
import threading
import time
from rich import print
from game import Game


# ansi codes used
CURSOR_INVIS_CODE = "\033[?25l"
CURSOR_VISIBLE_CODE = "\033[?25h"
RESET_CODE = f"\033[2J \033[3J \033[H {CURSOR_INVIS_CODE}\n"

# other useful stuff
JUMP_MESSAGE_TELNET = "\r\n"
JUMP_MESSAGE_NETCAT = "\n"


class ServerHandler(socketserver.BaseRequestHandler):
    def handle(self):
        print(f"Connection to {self.client_address} established")
        try:
            self.game = Game()

            self.highscore = 0

            # a new thread that sends messages
            sendThread = threading.Thread(target=self.sendMessages)
            sendThread.daemon = True # kill the send thread if the main thread is killed
            sendThread.start()

            # recieve messages from the client
            while True:
                data = self.request.recv(1024)
                if not data:
                    print(f"Connection to {self.client_address} closed")
                    break
                if data.decode() == JUMP_MESSAGE_TELNET or data.decode() == JUMP_MESSAGE_NETCAT: # when server receives an empty message (jump)
                    self.printLog("Recieved jump")
                    self.game.jumped = True
                    self.game.started = True # start the game when jumped
                else:
                    self.printLog(f'Recieved something weird: "{data}"')
                

        except ConnectionResetError:
            print(f"Connection aborted to {self.client_address} aborted.")
            self.request.close()
        except (UnicodeDecodeError, OSError):
            self.printLog(f"Got decode error. Client likely wants to disconect. Message: {data}")
            self.request.sendall("Disconnecting...".encode())
            self.request.close()

    def sendMessages(self):
        while True:
            if self.game.started:
                self.game.tick()
                gameView = self.game.window.render()
                try:
                    self.request.sendall(f"{RESET_CODE}Score:{self.game.score}\nHi:{self.highscore}\n{gameView}".encode())
                except OSError:
                    self.request.close()
                if self.game.score > self.highscore:
                    self.highscore = self.game.score
            else:
                try:
                    gameView = self.game.window.render()
                    self.request.sendall(f"{RESET_CODE}Score:{self.game.score}\nHi:{self.highscore}\n{gameView}\nPress Enter To Jump".encode())
                except OSError:
                    self.request.close()
            time.sleep(0.02)

    def printLog(self, message):
        print(f"Client {self.client_address[1]}: {message}")

class ReusableTCPServer(socketserver.ThreadingTCPServer):
    allow_reuse_address = True # to dont have to wait a minute after server stopping the server

def startServer(host="0.0.0.0", port=8042):
    with ReusableTCPServer((host, port), ServerHandler) as server:
        print(f"Started server and listing on {host}:{port}")
        server.serve_forever()

if __name__ == "__main__":
    port = 8042
    host = "0.0.0.0"
    startServer(port=port, host=host)