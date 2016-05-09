# Holoscanner Server

This project contains the server for the Holoscanner project. The server is
actually split into three different servers

 1. The game server - Handles connections to the individual Hololense clients.
 2. The relay server - Handles connections to a WebSocket viewer for looking at the status of the mesh.
 3. The web server.

## Dependencies

 * Python 3.5+
 * Flask - For the web server
 * Autobahn Python - For websocket connections
 * protobuf.js (included)
 * three.js (included)
 * jquery (included)

## Installation

Install a virtualenv. Pyenv is recommended.

```
pyenv install 3.5.1
pyenv virtualenv 3.5.1 holoscanner-env
```

# Running

Activate the virtualenv.
```
pyenv activate holoscanner-env
```

The environment script must also be run

```
. env.fish
```
for fish:

or

```
. env.sh
```
for POSIX based shells:

The game server and relay server are launched together with
```
python -m holoscanner.server
```

The web server must be launched separately with

```
python -m holoscanner.viewer.server
```

