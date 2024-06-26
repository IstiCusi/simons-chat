# Simon's Chat Client - A Very Simple and Unsafe Chat Client

## Overview

This project showcases a simple chat application designed to illustrate core concepts of network programming, concurrency, and design patterns within a minimalistic framework. It serves as an educational tool for those looking to understand the basics of creating networked applications with C and Python.
Additionally, this intentionally simplistic chat client will serve as a testing ground for exploring various exploit techniques in the future, enhancing understanding of security vulnerabilities within networked applications.

Simon's Chat, born from my son Simon's deepest desire, is not just any chat client. It's a bespoke haven for him and his buddies, untouched by the commercial fray. Crafted with a dash of humor, it's as independent as it gets, with one tiny, laughable catch: it's encryption-free, so dad can always tune in to the latest gossip—family bonding at its finest, or as we like to call it, 'open-source parenting'.

### Server

The used server used by the client is inspired by "Network Programming with C" by Van Winkel, highlighting the essentials of socket programming in C.
It's a straightforward implementation aimed at demonstrating how to handle client connections, data transmission, and concurrency through
multi-threading, laying the foundation for more complex networked applications with transmission checks on completeness and safety.

### Client

On the client side, the application is developed in Python, making use of `raylibpy` for the graphical user interface. This part of the project illustrates how Python applications can integrate with libraries to handle real-time graphical updates, user input, and network communication effectively. The application dynamically manages its dependencies, ensuring a smooth setup and execution process for the user.
Start the client with:

```bash
./chat.py --host <host ip> --port <tcp port>
```
or with, implying the standard port 1602, 

```bash
./chat.py --host <host ip>
```
or, implying the standard port and localhost, with 

```bash
./chat.py
```

## Key Concepts

- **Network Programming**: Utilizes sockets for communication between the chat server and client, adhering to TCP for reliable data transmission.
- **Concurrency**: Employs threading on both the server and client sides to manage multiple connections and perform tasks like sending, receiving, and rendering messages concurrently.
- **Observer/Observable Pattern**: Implemented in the Python client to update the chat interface in response to new messages, demonstrating decoupled communication between application components.
- **Dynamic Dependency Management**: The Python client automatically installs missing packages, highlighting a user-friendly approach to dependency resolution.

## Installation and Usage

To run the server, compile `server.c` using a C compiler (e.g., `gcc`) and execute the resulting binary. The client can be run with Python after ensuring `raylibpy` and any other dependencies are installed. Note that the application automatically installs Python dependencies upon startup.

### Font

FiraCode is used in the chat interface, chosen for its readability and support for programming ligatures, enhancing the visual presentation of the chat.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Server inspired by "Network Programming with C" by Van Winkel.
- FiraCode font used for enhancing the chat interface's readability.

## TODOs

- Unit testing soon
- Correct connection checking
- UDP data transfer class as proxy 
- TCP data transfer class as proxy 
- Factory to produce such proxies
- Better message handling
- Packaging of executables for windows and linux
- Add docstrings
- UML/SysML Produce Wiki with activity, class diagrams etc
- Scoping
- Add client names
- Add recieve confirmation by header and markers
- Add file transfer and /event (ringing at the reciever)
- Add encryption
- Add windows support
- Add chat log
- Add better keyboard handling
- Add piping possibility for streaming (e.g. music)
- Add sound
- Extend to hamlib capabilities -- transfer by radios AX.25
- Add password hash
- Add Desktop size and window size independent GUI / all elements scale
- Add Protocol Manager for different server formats
- Add configuration file loading.
- Add picture icons / video icon / sound icon to text queue
- Add direwolf binding 
- Translate client prototype to C++
- Overlay mode for gaming
- scripting (lua ?)
