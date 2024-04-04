# Simon's Chat client - A Very Simple and Unsafe Chat Client

## Overview

This project showcases a simple chat application designed to illustrate core concepts of network programming, concurrency, and design patterns within a minimalistic framework. It serves as an educational tool for those looking to understand the basics of creating networked applications with C and Python.
Additionally, this intentionally simplistic chat client will serve as a testing ground for exploring various exploit techniques in the future, enhancing understanding of security vulnerabilities within networked applications.

### Server

The used server used by the client is inspired by "Network Programming with C" by Van Winkel, highlighting the essentials of socket programming in C. It's a straightforward implementation aimed at demonstrating how to handle client connections, data transmission, and concurrency through multi-threading, laying the foundation for more complex networked applications with
no transmission checks on completeness.

### Client

On the client side, the application is developed in Python, making use of `raylibpy` for the graphical user interface. This part of the project illustrates how Python applications can integrate with libraries to handle real-time graphical updates, user input, and network communication effectively. The application dynamically manages its dependencies, ensuring a smooth setup and execution process for the user.

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

