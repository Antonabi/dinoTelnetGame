# Dino Telnet Game

This is a (very crappy) version of the [chrome dino game](chrome://dino) completely playable with telnet and netcat.

It could be that this doesn't work on Windows, because ansi codes dont work. (I couldn't test this)

(If you run into any bugs, just open an issue explaining it. This thing is just a messy pile of code. I tried to clean it up its still a bit wonky. Maybe ill rewrite this in the future...)

## Hosting The Server

### Requirements

To get this to work you have to have python installed.
Download it [here](https://www.python.org/downloads/) or if you are on mac with [brew](https://formulae.brew.sh/formula/python@3.12#default).

### Setting Up The Sever

To host the server and try this, just clone this github repo with

```sh
git clone https://github.com/Antonabi/dinoTelnetGame.git
```

then cd into the new folder with

```sh
cd dinoTelnetGame
```

and install the requirements from the `requirements.txt` (or just install `numpy` and `rich`) with:

```sh
pip install -r requirements.txt
```

Now you can just run the server with:

```sh
python3 server.py
```

The server should now be running on host `0.0.0.0` with port `8042`.
To change this, just go into `server.py` and chnage the port and the host at the bottom (line 80).
If I wanted to just host this on my machine and on port `8080` I would do this:

```diff
if __name__ == "__main__":
-   port = 8042
-   host = "0.0.0.0"
+   port = 8080
+   host = "127.0.0.1"
    startServer(port=port, host=host)
```

## Playing The Game

To play the game just connect with telnet:

```sh
telnet [ip] [port]
```

or netcat:

```sh
nc [ip] [port]
```

If you don't have it installed, here is how to:

### Mac

(Install brew [here](https://brew.sh/) if you dont have it)

Netcat:

```sh
brew install netcat
```

Telnet:

```sh
brew install telnet
```

### Windows

Telnet:

[Info here](https://www.redswitches.com/blog/how-to-use-telnet-on-windows#How_to_Enable_Telnet_on_Windows_10)
(Im not sure if this is a good tutorial. I don't use windows.)

```sh
pkgmgr /iu:"TelnetClient"
```

(This shoud work)
