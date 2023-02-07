# Network Sockets
## socket(), closesocket()
::::{abi-group}

socket()'s three parameters, all of which take predefined constants as
values, describe the type of communication the socket can handle:
:::{list-table}
---
header-rows: 1
---
-
	- Parameter
	- Description
-
	- family
	- Describes the network address format that the socket understands. Currently, it must be {cpp:enum}`AF_INET` (the Internet address format).
-
	- type
	- Describes the persistence of the connection that can be formed through this socket. It must be either {cpp:enum}`SOCK_STREAM` or {cpp:enum}`SOCK_DGRAM`. {cpp:enum}`SOCK_STREAM` means the connection (which is formed through a {ref}`connect()` or {ref}`bind()` call) remains open until told to close. {cpp:enum}`SOCK_DGRAM` describes a datagram socket that's only open while data is being sent or received (typically through {ref}`sendto()` and {ref}`recvfrom()`). It's closed at all other times. Keep in mind that you still have to call closesocket() on a datagram socket when you're done with it.
-
	- protocol
	- Describes the messaging protocol, which is closely related to the socket type. Although there are four acceptable values (0, {cpp:enum}`IPPROTO_TCP`, {cpp:enum}`IPPROTO_UDP`, and {cpp:enum}`IPPROTO_ICMP`), the only values that you should actually use are 0 or {cpp:enum}`IPPROTO_ICMP`. 0 tells the socket to choose the correct protocol based on the socket type: If you set the type to {cpp:enum}`SOCK_STREAM`, then a protocol of 0 automatically sets the messaging protocol to {cpp:enum}`IPPROTO_TCP`. Similarly, {cpp:enum}`IPPROTO_UDP` is the correct protocol for {cpp:enum}`SOCK_DGRAM`. It's an error to ask for a "udp stream" or a "tcp datagram."
:::
::::

::::{abi-group}

There are only two socket type constants:
{cpp:enum}`SOCK_STREAM` and {cpp:enum}`SOCK_DGRAM`.
However, if we look at the way sockets are used, we see that there are
really five different categories of sockets, as illustrated below.
The labelled ovals represent individual computers that are attached to
the network. The solid circles represent individual sockets. The numbers
near the sockets are keys to the socket categories, which are:
The stream listener socket. A stream listener socket provides access to a service that's running on the "listener" machine (you might want to think of the machine as a "server.") The listener socket waits for client machines to "call in" and ask to be served. In order to listen for clients, the listener must call bind(), which "binds" the socket to an IP address and machine-specific port, and then listen(). Thus primed, the socket waits for a client message to show up by sitting in an accept() call.The stream client socket. A stream client socket asks for service from a server machine by attempting to connect to the server's listener socket. It does this through the connect() function. A stream client can be bound (you can call bind() on it), but it's not mandatory.The "accept" socket. When a stream listener hears a client in an accept() call, the function call creates yet another socket called the "accept" socket. Accept sockets are valid sockets, just like those you create through socket(). In particular, you have to remember to close accept sockets (through closesocket()) just as you would the sockets you explicitly create. Note that you can't bind an accept socket—the socket is bound automatically by the system.The datagram receiver socket. A datagram receiver socket is sort of like a stream listener: It calls bind() and waits for "senders" to send messages to it. Unlike the stream listener, the datagram receiver doesn't call listen() or accept(). Furthermore, when a datagram sender sends a message to the receiver, there's no ancillary socket created to handle the message (there's no UDP analog to the TCP accept socket).The datagram sender socket. A datagram sender is the simplest type of socket—all it has to do is identify a datagram receiver and send messages to it, through the sendto() function. Binding a datagram sender socket is optional.
TCP communication is two-way. Once the link between a client and the
listener has been established (through
{ref}`bind()`/{ref}`listen()`/{ref}`accept()`
on the listener side, and
{ref}`connect()`
on the client side), the two machines can
talk to each other through respective and complementary
{ref}`send()` and
{ref}`recv()`
calls.
Communication along a UDP path, on the other
hand, is one-way. The datagram sender can send messages (through
{ref}`sendto()`),
and the datagram receiver can receive them (through
{ref}`recvfrom()`),
but the receiver can't
send message back to the sender. However, you can simulate a two-way UDP
conversation by binding both sockets. This doesn't change the definition
of the UDP path, or the capabilities of the two types of datagram
sockets, it simply means that a bound datagram socket can act as a
receiver (it can call
{ref}`recvfrom()`)
or as a sender (it can call
{ref}`sendto()`).
:::{admonition} Note
:class: note
To be complete, it should be mentioned that datagram sockets can also
invoke
{ref}`connect()`
and then pass messages through
{ref}`send()` and
{ref}`recv()`.
The datagram use of these functions is a convenience; its advantages are
explained in the description of the
{ref}`sendto()`
function.
:::
::::

## bind()
::::{abi-group}

bind()'s first parameter is the socket that you're attempting to bind.
This is, typically, a socket of type {cpp:enum}`SOCK_STREAM`. The interface parameter
is the address/port combination (or "interface") to which you're binding
the socket. The parameter is typed as a sockaddr structure, but, in
reality, you have to create and pass a sockaddr_in structure cast as a
sockaddr. The sockaddr_in structure is defined as:
:::{code}
struct sockaddr_in {
   unsigned short sin_family;
   unsigned short sin_port;
   struct in_addr sin_addr;
   char sin_zero[4];
};
:::
:::{list-table}
---
header-rows: 1
---
-
	- Field
	- Description
-
	- sin_family
	- Is the same as the address format constant that used to create the socket (the first parameter to {ref}`connect()`). Currently, it's always {cpp:enum}`AF_INET`.
-
	- sin_port
	- Is the port number that the socket will bind to, given in network byte order. Valid port numbers are between 1 and 65535; numbers up to 1024 are reserved for services such as ftp and telnet. If you're not implementing a standard service, you should choose a port number greater than 1024. The actual value of the port number is meaningless, but keep in mind that the port number must be unique for a particular address; only one socket can be bound to a particular address/port combination.NoteCurrently, there's no system-defined mechanism for allowing a client/sender machine to ask a listener/receiver machine for its port numbers. Therefore, when you create a networked application, you either have to hard-code the port numbers or, better yet, provide default port numbers that the user (or a system administrator) can easily change.
-
	- sin_addr
	- Is an in_addr structure that stores, in its s_addr field, the IP address of the socket's machine. As always, the address is in network byte order. You can use an address of 0 to tell the binding mechanism to find an address for you. By convention, binding to address 0 (which is conveniently symbolized by the {cpp:enum}`INADDR_ANY` address) means that you want to bind to every address by which your computer is known, including the "loopback" (address 127.0.0.1, or the constant {cpp:enum}`INADDR_LOOPBACK`).WarningThe BeOS does not currently implement global binding. When you bind to INADDR_ANY, the bind() function binds to the first available interface (where "availability" means the address/port combination is currently unbound). Internet interfaces are considered before the loopback interface. If you want to bind to all interfaces, you have to create a separate socket for each. An example of this is given later.
-
	- sin_zero
	- Is padding. To be safe, you should fill it with zeros.
:::
The {hparam}`size` parameter is the size, in
bytes, of the second parameter.
If the bind() call is successful, the
{hparam}`interface` parameter is set to contain the actual
address that was used. If the socket can't be bound, the function returns a
negative value, and sets the global
errno to {cpp:enum}`EABDF`
if the {hparam}`socket` parameter is invalid; for all other
errors, errno is set to
-1.
The following example shows a typical use of the bind() function. The
example uses the fictitious gethostaddr() function that's defined in the
description of the gethostname() function.
:::{code}
struct sockaddr_in sa;
int sock;
long host_addr;
/* Create the socket. */
if ((sock = socket(AF_INET, SOCK_STREAM, 0)) < 0) {
   /* error */
}
/* Set the address format for the imminent bind. */
sa.sin_family = AF_INET;
/* We'll choose an arbitrary port number translated to network byte
order. */
sa.sin_port = htonl(2125);
/* Get the address of the local machine. If the address can't
* be found (the function looks it up based on the host name),
* then we use address INADDR_ANY.
*/
if ((host_addr = (ulong) gethostaddr()) == -1) {
   host_addr = INADDR_ANY;
}
sa.sin_addr.s_addr = host_addr;
/* Clear sin_zero. */
memset(sa.sin_zero, 0, sizeof(sa.sin_zero));
/* Bind the socket. */
if (bind(sock, (struct sockaddr*) &sa, sizeof(sa)) < 0) {
   /* error */
}
:::
As mentioned earlier, the bind-to-all-interfaces convention (by asking to
bind to address 0) isn't currently implemented. Thus, if the
gethostaddr()
call fails in the example, the socket will be bound to the
first address by which the local computer is known.
But let's say that you really do want to bind to all interfaces. To do
this, you have to create separate sockets for each interface, then call
bind() on each one. In the example below we create a series of sockets
and then bind each one to an interface that specifies address 0. In doing
this, we depend on the "first available interface" rule to find the next
interface for us. Keep in mind that a successful bind() rewrites the
contents of the sockaddr parameter (most importantly, it resets the 0
address component). Thus, we have to reinitialize the structure each time
through the loop:
:::{code}
/* Declare an array of sockets. */
#define MAXSOCKETS 4
int socks[MAXSOCKETS];
int sockN;
int bind_res;
struct sockaddr_in sock_addr;
for (sockN = 0; sockN < MAXSOCKETS; sockN++)
{
   (socks[sockN] = socket(AF_INET, SOCK_STREAM, 0));
   if (socks[sktr] < 0) {
      perror("socket");
      goto sock_error;
   }
   /* Initialize the structure. */
   sa.sin_family = AF_INET;
   sa.sin_port = htonl(2125);
   sa.sin_addr.s_addr = 0;
   memset(sa.sin_zero, 0, sizeof(sa.sin_zero));
   bind_res = bind(socks[sockN],
               (struct sockaddr*) &sa,
               sizeof(sa));
   /* A bind error means we've run out of addresses. */
   if (bind_res < 0) {
      closesocket(socks[sockN--]);
      break;
   }
}
/* Use the bound socket (listen, accept, recv/send). */
...
sock_error:
   for (;sockN >=0 sockN--)
      closesocket(socks[sockN]);
:::
::::

## connect()
## getpeername(), getsockname()
## listen(), accept()
## select()
## send(), recv()
::::{abi-group}

The parameters to send() and recv() are:
:::{list-table}
---
header-rows: 1
---
-
	- Parameter
	- Description
-
	- socket
	- Is, for datagrams and stream client sockets, the local socket token. In other words, when a datagram or stream client wants to send or receive data, it passes its own socket token as the first parameter. The recipient of a send(), or the sender of a recv() is, for these sockets, already known: It's the socket that's identified by the previous {ref}`connect()` call.For a stream listener, {hparam}`socket` is the "accept socket" that was previously returned by an {ref}`accept()` call. A stream listener can send and receive data from more than one client at the same time (or, at least, in rapid succession).
-
	- buf
	- Is a pointer to the data that's being sent, or is used to hold a copy of the data that was received.
-
	- size
	- Is the allocated size of {hparam}`buf`, in bytes.
-
	- flags
	- Is currently unused. For now, set it to 0.
:::
::::

## sendto(), recvfrom()
## setsockopt()