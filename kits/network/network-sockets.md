# Network Sockets

:::{list-table}
---
header-rows: 0
align: left
widths: auto
---
-
	- Declared In:

	- kit/net/socket.h

-
	- Library:

	- libnet.so


:::

A socket is an entry onto a network. To transmit data to another computer,
you create a socket, tell it how to find the other computer, and then tell
it to send. To receive data, you create a socket, tell it which computer to
listen to (in some cases), and then wait for data to come pouring in.

The socket story starts with the {ref}`socket()` function. The set of
functions you need to call after that depends on the type of socket you're
creating (as explained in {ref}`socket()`).

## socket(), closesocket()









The socket() function returns a token (a non-negative integer) that
represents the local end of a connection to another machine (0 is a valid
socket token).

:::{admonition} Warning
:class: warning
Socket tokens are not file descriptors (this violates the BSD tradition).
:::

Freshly returned, a socket token is abstract and unusable; to put the
token to use, you have to pass it as an parameter to other functions—such
as {ref}`bind()` and {ref}`connect()`—that know how to establish a
connection over the network. The function's parameters, which are examined
in detail in "{ref}`The socket() Parameters`", accept these values:

:::{list-table}
---
header-rows: 1
align: left
widths: auto
---
-
	- Parameter

	- Acceptable Values

-
	- {hparam}`family`

	- {cpp:enumerator}`AF_INET`

-
	- {hparam}`type`

	- {cpp:enumerator}`SOCK_STREAM`, {cpp:enumerator}`SOCK_DGRAM`

-
	- {hparam}`protocol`

	- 0, {cpp:enumerator}`IPPROTO_TCP`, {cpp:enumerator}`IPPROTO_UDP`,
{cpp:enumerator}`IPPROTO_ICMP`


:::

The most typical socket calls are:

:::{code} c
/* Create a stream TCP socket. */
int tcp_socket = socket(AF_INET, SOCK_STREAM, 0);

/* Create a datagram UDP socket. */
int udp_socket = socket(AF_INET, SOCK_DGRAM, 0);
:::

ICMP messages are normally sent through "raw" sockets; however, the
Network Kit doesn't currently support raw sockets, so you should use a
datagram socket instead:

:::{code} c
/* Create a datagram icmp socket. */
long icmp_socket = socket(AF_INET, SOCK_DGRAM, IPPROTO_ICMP);
:::

closesocket() closes a socket's connection (if it's the type of socket
that can hold a connection) and frees the resources that have been assigned
to the socket. When you're done with the sockets that you've created, you
should pass each socket token to closesocket(). No socket is exempt from
the need to be closed. This extends to sockets that are created for you by
the {ref}`accept()` function.

### The socket() Parameters

socket()'s three parameters, all of which take predefined constants as
values, describe the type of communication the socket can handle:

:::{list-table}
---
header-rows: 1
align: left
widths: auto
---
-
	- Parameter

	- Description

-
	- family
	- Describes the network address format that the socket understands.
		Currently, it must be {cpp:enumerator}`AF_INET` (the Internet address
		format).
-
	- type
	- Describes the persistence of the connection that can be formed through
		this socket. It must be either {cpp:enumerator}`SOCK_STREAM` or
		{cpp:enumerator}`SOCK_DGRAM`. {cpp:enumerator}`SOCK_STREAM` means the
		connection (which is formed through a {ref}`connect()` or {ref}`bind()`
		call) remains open until told to close. {cpp:enumerator}`SOCK_DGRAM`
		describes a datagram socket that's only open while data is being sent or
		received (typically through {ref}`sendto()` and {ref}`recvfrom()`). It's
		closed at all other times. Keep in mind that you still have to call
		closesocket() on a datagram socket when you're done with it.
-
	- protocol
	- Describes the messaging protocol, which is closely related to the socket
		type. Although there are four acceptable values (0,
		{cpp:enumerator}`IPPROTO_TCP`, {cpp:enumerator}`IPPROTO_UDP`, and
		{cpp:enumerator}`IPPROTO_ICMP`), the only values that you should actually
		use are 0 or {cpp:enumerator}`IPPROTO_ICMP`. 0 tells the socket to choose
		the correct protocol based on the socket type: If you set the type to
		{cpp:enumerator}`SOCK_STREAM`, then a protocol of 0 automatically sets the
		messaging protocol to {cpp:enumerator}`IPPROTO_TCP`. Similarly,
		{cpp:enumerator}`IPPROTO_UDP` is the correct protocol for
		{cpp:enumerator}`SOCK_DGRAM`. It's an error to ask for a "udp stream" or a
		"tcp datagram."

:::

### Sorts of Sockets

There are only two socket type constants: {cpp:enumerator}`SOCK_STREAM`
and {cpp:enumerator}`SOCK_DGRAM`. However, if we look at the way sockets
are used, we see that there are really five different categories of
sockets, as illustrated below.

The labelled ovals represent individual computers that are attached to the
network. The solid circles represent individual sockets. The numbers near
the sockets are keys to the socket categories, which are:

1.    The stream listener socket. A stream listener socket provides access to a
service that's running on the "listener" machine (you might want to think
of the machine as a "server.") The listener socket waits for client
machines to "call in" and ask to be served. In order to listen for clients,
the listener must call {ref}`bind()`, which "binds" the socket to an IP
address and machine-specific port, and then {ref}`listen()`. Thus primed,
the socket waits for a client message to show up by sitting in an
{ref}`accept()` call.

2.    The stream client socket. A stream client socket asks for service from a
server machine by attempting to connect to the server's listener socket. It
does this through the {ref}`connect()` function. A stream client can be
bound (you can call {ref}`bind()` on it), but it's not mandatory.

3.    The "accept" socket. When a stream listener hears a client in an
{ref}`accept()` call, the function call creates yet another socket called
the "accept" socket. Accept sockets are valid sockets, just like those you
create through socket(). In particular, you have to remember to close
accept sockets (through closesocket()) just as you would the sockets you
explicitly create. Note that you can't bind an accept socket—the socket is
bound automatically by the system.

4.    The datagram receiver socket. A datagram receiver socket is sort of like a
stream listener: It calls {ref}`bind()` and waits for "senders" to send
messages to it. Unlike the stream listener, the datagram receiver doesn't
call {ref}`listen()` or {ref}`accept()`. Furthermore, when a datagram
sender sends a message to the receiver, there's no ancillary socket created
to handle the message (there's no UDP analog to the TCP accept socket).

5.    The datagram sender socket. A datagram sender is the simplest type of
socket—all it has to do is identify a datagram receiver and send messages
to it, through the {ref}`sendto()` function. Binding a datagram sender
socket is optional.

TCP communication is two-way. Once the link between a client and the
listener has been established (through
{ref}`bind()`/{ref}`listen()`/{ref}`accept()` on the listener side, and
{ref}`connect()` on the client side), the two machines can talk to each
other through respective and complementary {ref}`send()` and {ref}`recv()`
calls.

Communication along a UDP path, on the other hand, is one-way. The
datagram sender can send messages (through {ref}`sendto()`), and the
datagram receiver can receive them (through {ref}`recvfrom()`), but the
receiver can't send message back to the sender. However, you can simulate a
two-way UDP conversation by binding both sockets. This doesn't change the
definition of the UDP path, or the capabilities of the two types of
datagram sockets, it simply means that a bound datagram socket can act as a
receiver (it can call {ref}`recvfrom()`) or as a sender (it can call
{ref}`sendto()`).

:::{admonition} Note
:class: note
To be complete, it should be mentioned that datagram sockets can also
invoke {ref}`connect()` and then pass messages through {ref}`send()` and
{ref}`recv()`. The datagram use of these functions is a convenience; its
advantages are explained in the description of the {ref}`sendto()`
function.
:::

Upon failure, socket() returns a negative value and sets {hparam}`errno`
to…

:::{list-table}
---
header-rows: 1
align: left
widths: auto
---
-
	- Return Code

	- Description

-
	- {cpp:enumerator}`EAFNOSUPPORT`
	- {hparam}`format` was other than {cpp:enumerator}`AF_INET`.
-
	- {cpp:enumerator}`EPROTOTYPE`
	- {hparam}`type` and {hparam}`protocol` mismatch.
-
	- {cpp:enumerator}`EPROTONOSUPPORT`
	- Unrecognized {hparam}`type` or {hparam}`protocol` value.

:::

closesocket() returns a negative value if its parameter is invalid.

## bind()





The bind() function creates an association between a socket and an
"interface," where an interface is a combination of an IP address and a
port number. Binding is, primarily, useful for receiving messgaes: When a
message sender (whether it's a stream client or a datagram sender) sends a
message, it tags the message with an IP address and a port number. The
receiving machine—the machine with the tagged IP address—delivers the
message to the socket that's bound to the tagged port.

The necessity of the bind operation depends on the type of socket;
referring to the five categories of sockets enumerated in the
{ref}`socket()` function description (and illustrated in the charming
diagram found there), the "do I need to bind?" question is answered thus:

1.    Stream listener sockets must be bound. Furthermore, after binding a
listener socket, you must then call listen() and, when a client calls,
{ref}`accept()`.

2.    Stream client sockets can be bound, but they don't have to be. If you're
going to bind a client socket, you should do so before you call
{ref}`connect()`. The advantages of binding a stream client escape me at
the moment. In any case, the client doesn't have to bind to the same port
number as the listener—the listener's binding and the client's binding are
utterly separate entities (let alone that they are on different machines).
However, the client does connect to the interface that the listener is
bound to.

3.    Stream attach sockets must not be bound.

4.    Datagram receiver sockets must be bound.

5.    Datagram sender sockets don't have to be bound… but if you're going to
turn around and use the socket as a receiver, then you'll have to bind it.

Once you've bound a socket, you can't unbind it. If you no longer want the
socket to be bound to its interface, the only thing you can do is close the
socket ({ref}`closesocket()`) and start all over again.

Also, a particular interface can be bound by only one socket at a time and
a single socket can only bind to one interface at a time. If your socket
needs to bind to more than one interface, you need to create more than one
socket and bind each one separately. An example of this is given later in
this function description.

:::{admonition} Warning
:class: warning
The 1-to-1 binding differs with the BSD socket implementation, which
expects a socket to be able to bind to more than one interface. Consider it
a bug that will be fixed in a subsequent release.
:::

### The bind() Parameters

bind()'s first parameter is the socket that you're attempting to bind.
This is, typically, a socket of type {cpp:enumerator}`SOCK_STREAM`. The
interface parameter is the address/port combination (or "interface") to
which you're binding the socket. The parameter is typed as a
{htype}`sockaddr` structure, but, in reality, you have to create and pass a
{htype}`sockaddr_in` structure cast as a {htype}`sockaddr`. The
{htype}`sockaddr_in` structure is defined as:

:::{code} c
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
align: left
widths: auto
---
-
	- Field

	- Description

-
	- sin_family
	- Is the same as the address format constant that used to create the socket
		(the first parameter to {ref}`connect()`). Currently, it's always
		{cpp:enumerator}`AF_INET`.
-
	- sin_port
	- Is the port number that the socket will bind to, given in network byte
		order. Valid port numbers are between 1 and 65535; numbers up to 1024 are
		reserved for services such as ftp and telnet. If you're not implementing a
		standard service, you should choose a port number greater than 1024. The
		actual value of the port number is meaningless, but keep in mind that the
		port number must be unique for a particular address; only one socket can be
		bound to a particular address/port combination.

		:::{admonition} Note
		:class: note
		Currently, there's no system-defined mechanism for allowing a
		client/sender machine to ask a listener/receiver machine for its port
		numbers. Therefore, when you create a networked application, you either
		have to hard-code the port numbers or, better yet, provide default port
		numbers that the user (or a system administrator) can easily change.
		:::
-
	- sin_addr
	- Is an {htype}`in_addr` structure that stores, in its {htype}`s_addr`
		field, the IP address of the socket's machine. As always, the address is in
		network byte order. You can use an address of 0 to tell the binding
		mechanism to find an address for you. By convention, binding to address 0
		(which is conveniently symbolized by the {cpp:enumerator}`INADDR_ANY`
		address) means that you want to bind to every address by which your
		computer is known, including the "loopback" (address 127.0.0.1, or the
		constant {cpp:enumerator}`INADDR_LOOPBACK`).

		:::{admonition} Warning
		:class: warning
		The BeOS does not currently implement global binding. When you bind to
		{cpp:enumerator}`INADDR_ANY`, the bind() function binds to the first
		available interface (where "availability" means the address/port
		combination is currently unbound). Internet interfaces are considered
		before the loopback interface. If you want to bind to all interfaces, you
		have to create a separate socket for each. An example of this is given
		later.
		:::
-
	- sin_zero
	- Is padding. To be safe, you should fill it with zeros.

:::

The {hparam}`size` parameter is the size, in bytes, of the second
parameter.

If the bind() call is successful, the {hparam}`interface` parameter is set
to contain the actual address that was used. If the socket can't be bound,
the function returns a negative value, and sets the global {hparam}`errno`
to {cpp:enumerator}`EABDF` if the {hparam}`socket` parameter is invalid;
for all other errors, {hparam}`errno` is set to -1.

The following example shows a typical use of the bind() function. The
example uses the fictitious gethostaddr() function that's defined in the
description of the gethostname() function.

:::{code} c
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
bind to address 0) isn't currently implemented. Thus, if the gethostaddr()
call fails in the example, the socket will be bound to the first address by
which the local computer is known.

But let's say that you really do want to bind to all interfaces. To do
this, you have to create separate sockets for each interface, then call
bind() on each one. In the example below we create a series of sockets and
then bind each one to an interface that specifies address 0. In doing this,
we depend on the "first available interface" rule to find the next
interface for us. Keep in mind that a successful bind() rewrites the
contents of the {htype}`sockaddr` parameter (most importantly, it resets
the 0 address component). Thus, we have to reinitialize the structure each
time through the loop:

:::{code} c
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

To ask a socket about the address and port to which it is bound you use
the getsockname() function, described later in this section.

Upon failure, bind() returns a negative value and sets {hparam}`errno` to…

:::{list-table}
---
header-rows: 1
align: left
widths: auto
---
-
	- Return Code

	- Description

-
	- {cpp:enumerator}`EABDF`
	- The {hparam}`socket` parameter is invalid.
-
	- {cpp:enumerator}`B_ERROR`
	- All other errors.

:::

## connect()





The meaning of the connect() function depends on the type of socket that's
passed as the first parameter:

-   If it's a stream client, then connect() attempts to form a connection to
the socket that's specified by {hparam}`remote_interface`. The remote
socket must be a bound stream listener. A client socket can only be
connected to one listener at a time. Note that you can't call connect() on
a stream listener.

-   If it's a datagram socket (either a sender or a receiver), connect()
simply caches the {hparam}`remote_interface` information in anticipation of
subsequent {ref}`send()` and {ref}`recv()` calls. By using connect(), a
datagram avoids the fuss of filling in the remote information that's needed
by the "normal" datagram message functions, {ref}`sendto()` and
{ref}`recvfrom()`. Note that a datagram may only call {ref}`send()` and
{ref}`recv()` if it has first called connect().

The {hparam}`remote_interface` parameter is a pointer to a
{htype}`sockaddr_in` structure cast as a {htype}`sockaddr` pointer. The
{hparam}`remote_size` value gives the size of {hparam}`remote_interface`.
See the {ref}`bind()` function for a description of the
{htype}`sockaddr_in` structure.

Currently, you can't disconnect a connected socket. If you want to connect
to a different listener, or reset a datagram's interface information, you
have to close the socket and start over.

When you attempt to connect() a stream client, the listener must respond
with an {ref}`accept()` call. Having gone through this dance, the two
sockets can then pass messages to each other through complementary
{ref}`send()` and {ref}`recv()` calls. If the listener doesn't respond
immediately to a client's attempt to connect, the client's connect() call
will block. If the listener doesn't respond within (about) a minute, the
connection will time out. If the listener's acceptance queue is full, the
client will be refused and connect() will return immediately.

If the socket is in no-block mode (as set through setsockopt()), and
blocking would occur otherwise, connect() returns immediately with a result
of {cpp:enumerator}`EWOULDBLOCK`.

Upon failure, connect() returns a negative number and sets {hparam}`errno`
to…

:::{list-table}
---
header-rows: 1
align: left
widths: auto
---
-
	- Return Code

	- Description

-
	- {cpp:enumerator}`EWOULDBLOCK`
	- The connection attempt would block.
-
	- {cpp:enumerator}`EISCONN`
	- The socket is already connected.
-
	- {cpp:enumerator}`ECONNREFUSED`
	- The listener rejected the connection.
-
	- {cpp:enumerator}`ETIMEDOUT`
	- The connection attempt timed out.
-
	- {cpp:enumerator}`ENETUNREACH`
	- The client can't get to the network.
-
	- {cpp:enumerator}`EBADF`
	- The {hparam}`socket` parameter is invalid.
-
	- {cpp:enumerator}`B_ERROR`
	- All other errors.

:::

## getpeername(), getsockname()









getsockname() returns, by reference in {hparam}`interface`, a
{htype}`sockaddr_in` structure that contains the interface information for
the bound socket given by {hparam}`socket`.

getpeername() returns, in the structure pointed to by the
{hparam}`interface` parameter, a {htype}`sockaddr_in` structure that
describes the remote interface to which the socket is connected.

In both cases, the *{hparam}`size` parameter gives the size of the
{hparam}`interface` structure; *{hparam}`size` is reset, on the way out, to
the size of the {hparam}`interface` parameter as it's passed back. Note
that the {htype}`sockaddr_in` pointer that you pass as the second parameter
must be cast as a pointer to a {htype}`sockaddr` structure:

:::{code} c
struct sockaddr_in interface;
int size = sizeof(interface);

/* We'll assume "sock" is a valid socket token. */
if (getsockname(sock, (struct sockaddr*) &interface, &size) < 0)
   /* error */
:::

Upon failure, getsockname() and getpeername() return negative numbers and
set {hparam}`errno` to…

:::{list-table}
---
header-rows: 1
align: left
widths: auto
---
-
	- Return Code

	- Description

-
	- {cpp:enumerator}`EINVAL`
	- The *{hparam}`size` value (going in) wasn't big enough.
-
	- {cpp:enumerator}`EBADF`
	- The {hparam}`socket` parameter is invalid.
-
	- {cpp:enumerator}`B_ERROR`
	- All other errors.

:::

## listen(), accept()









After you've bound a stream listener socket to an interface (through
{ref}`bind()`), you then tell the socket to start listening for clients
that are trying to connect. You then pass the socket to accept() which
blocks until a client connects to the listener (the client does this by
calling {ref}`connect()`, passing it a description of the interface to
which the listener is bound).

When accept() returns, the value that it returns directly is a new socket
token; this socket token represents an "accept" socket that was created as
a proxy (on the local machine) for the client. To receive a message from
the client, or to send a message to the client, the listener must pass the
accept socket to the respective stream messaging functions, {ref}`recv()`
and {ref}`send()`.

A listener only needs to invoke listen() once; however, it can accept more
than one client at a time. Often, a listener will spawn an "accept" thread
that loops over the accept() call.

:::{admonition} Note
:class: note
Only stream listeners need to invoke listen() and accept(). None of the
other socket types (enumerated in the {ref}`socket()` description) need to
call these functions.
:::

listen() takes two parameters: The first is the socket that you want to
have start listening. The second is the length of the listener's
"acceptance count." This is the number of clients that the listener is
willing to accept at a time. If too many clients try to connect at the same
time, the excess clients will be refused—the connection isn't automatically
retried later.

After the listener starts listening, it must process the client
connections within a certain amount of time, or the connection attempts
will time out.

If listen() succeeds, the function returns 0; otherwise it returns a
negative result and sets the global {hparam}`errno` to a descriptive
constant. Currently, the only {hparam}`errno` value that listen() uses,
other than -1, is {cpp:enumerator}`EBADF`, which means the socket parameter
is invalid.

The parameters to accept() are the socket token of the listener
({hparam}`socket`), a pointer to a {htype}`sockaddr_in` structure cast as a
{htype}`sockaddr` structure ({hparam}`client_interface`), and a pointer to
an integer that gives the size of the {hparam}`client_interface` parameter
({hparam}`client_size`).

The {hparam}`client_interface` structure returns interface information (IP
address and port number) of the client that's attempting to connect. See
the {ref}`bind()` function for an examination of the {htype}`sockaddr_in`
structure.

The *{hparam}`client_size` parameter is reset to give the size of
{hparam}`client_interface` as it's passed back by the function.

The value that {hparam}`accept()` returns directly is a token that
represents the accept socket. After checking the token value (where a
negative result indicates an error), you must cache the token so you can
use it in subsequent {ref}`send()` and {ref}`recv()` calls.

When you're done talking to the client, remember to call
{ref}`closesocket()` on the accept socket that accept() returned. This
frees a slot in the listener's acceptance queue, allowing a possibly
frustrated client to connect to the listener.

Upon failure, listen() and accept() return < 0 and set {hparam}`errno` to…

:::{list-table}
---
header-rows: 1
align: left
widths: auto
---
-
	- Return Code

	- Description

-
	- {cpp:enumerator}`EBADF`
	- The {hparam}`socket` parameter is invalid.
-
	- {cpp:enumerator}`EINVAL`
	- (accept() only) The listener socket isn't bound.
-
	- {cpp:enumerator}`EBADF`
	- (accept() only) The acceptance queue is full.
-
	- {cpp:enumerator}`B_ERROR`
	- All other errors.

:::

## select()





The select() function returns information about selected sockets. The
{hparam}`socket_range` parameter tells the function how many sockets to
check: It checks socket numbers up to ({hparam}`socket_range` - 1).
Traditionally, the {hparam}`socket_range` parameter is set to 32.

The {htype}`fd_set` structure that types the next three parameters is a
32-bit mask that encodes the sockets that you're interested in; this
refines the range of sockets that was specified in the first parameter. You
should use the FD_OP() macros to manipulate the structures that you pass
in:

:::{list-table}
---
header-rows: 1
align: left
widths: auto
---
-
	- Macro

	- Description

-
	- FD_ZERO(set)
	- Clears the mask given by set.
-
	- FD_SET(socket, set)
	- Adds a socket to the mask.
-
	- FD_CLEAR(socket, set)
	- Clears a socket from the mask.
-
	- FD_ISSET(socket, set)
	- Returns non-zero if the given socket is already in the mask.

:::

The function passes socket information back to you by resetting the three
{htype}`fd_set` parameters. The parameters themselves represent the types
of information that you can check:

:::{list-table}
---
header-rows: 1
align: left
widths: auto
---
-
	- Field

	- Description

-
	- read_bits
	- Tells you if a socket is "ready to read." In other words, it tells you if
		a socket has a in-coming message waiting to be read.
-
	- write_bits
	- Tells you if a socket is "ready to write."
-
	- exception_bits
	- Tells you if there's an exception pending on the socket.

:::

:::{admonition} Warning
:class: warning
Currently, only {hparam}`read_bits` is implemented. You should pass
{cpp:expr}`NULL` as the {hparam}`write_bits` and {hparam}`exception_bits`
parameters.
:::

select() doesn't return until at least one of the
{htype}`fd_set`-specified sockets is ready for one of the requested
operations. To avoid blocking forever, you can provide a time limit in the
final parameter, passed as a {htype}`timeval` structure.

In the following example, we check if a given datagram socket has a
message waiting to be read. The select() times out after two seconds:

:::{code} c
bool can_read_datagram(int s)
{
   struct timeval tv;
   struct fd_set fds;

   tv.tv_sec = 2;
   tv.tv_usec = 0;

   /* Initialize (clear) the socket mask. */
   FD_ZERO(&fds);

   /* Set the socket in the mask. */
   FD_SET(s, &fds);
   select(32, &fds, NULL, NULL, &tv);

   /* If the socket is still set, then it's ready to read. */
   return FD_ISSET(s, &fds);
}
:::

:::{list-table}
---
header-rows: 1
align: left
widths: auto
---
-
	- Return Code

	- Description

-
	- -1
	- select() failed.
-
	- 0
	- select() timed out.
-
	- 1
	- Any of the selected sockets was found to be ready.

:::

## send(), recv()









These functions are used to send data to a remote socket, and to receive
data that was sent by a remote socket. send() and recv() calls must be
complementary: after socket A sends to socket B, socket B needs to call
recv() to pick up the data that A sent. send() sends its data and returns
immediately. recv() will block until it has some data to return.

The send() and recv() functions can be called by stream or datagram
sockets. However, there are some differences between the way the functions
work when used by these two types of socket:

-   For a stream listener and a stream client to transmit messages, the
listener must have previously called {ref}`bind()`, {ref}`listen()`,
{ref}`accept()`, and the client must have called {ref}`connect()`. Having
been properly connected, the two sockets can send and receive as if they
were peers.

-   For stream sockets, send() and recv() can both block: send() blocks if the
amount of data that's sent overwhelms the receiver's ability to read it,
and recv() blocks if there's no message waiting to be read. You can tell
these functions to be non-blocking by setting the sending socket's no-block
socket option (see {ref}`setsockopt()`).

-   If you want to call send() or recv() through a datagram socket, you must
first {ref}`connect()` the socket. In addition, a receiving datagram socket
must also be bound to an interface (through {ref}`bind()`). See the
{ref}`connect()` description for more information on what that function
means to a datagram socket.

-   Datagram sockets never block on send(), but they can block in a recv()
call. As with stream sockets, you can set a datagram socket to be
non-blocking (for the recv(), as well as for {ref}`recvfrom()`) through
{ref}`setsockopt()`.

### The Parameters

The parameters to send() and recv() are:

:::{list-table}
---
header-rows: 1
align: left
widths: auto
---
-
	- Parameter

	- Description

-
	- socket
	- Is, for datagrams and stream client sockets, the local socket token. In
		other words, when a datagram or stream client wants to send or receive
		data, it passes its own socket token as the first parameter. The recipient
		of a send(), or the sender of a recv() is, for these sockets, already
		known: It's the socket that's identified by the previous {ref}`connect()`
		call.

		For a stream listener, {hparam}`socket` is the "accept socket" that was
		previously returned by an {ref}`accept()` call. A stream listener can send
		and receive data from more than one client at the same time (or, at least,
		in rapid succession).
-
	- buf
	- Is a pointer to the data that's being sent, or is used to hold a copy of
		the data that was received.
-
	- size
	- Is the allocated size of {hparam}`buf`, in bytes.
-
	- flags
	- Is currently unused. For now, set it to 0.

:::

A successful send() returns the number of bytes that were sent; a
successful recv() returns the number of bytes that were received. Upon
failure, the functions return negative numbers and set {hparam}`errno` to…

:::{list-table}
---
header-rows: 1
align: left
widths: auto
---
-
	- Return Code

	- Description

-
	- {cpp:enumerator}`EWOULDBLOCK`
	- The call would block on a non-blocking socket.
-
	- {cpp:enumerator}`EINTR`
	- The local socket was interrupted.
-
	- {cpp:enumerator}`ECONNRESET`
	- The remote socket disappeared (send() only).
-
	- {cpp:enumerator}`ENOTCONN`
	- The socket isn't connected.
-
	- {cpp:enumerator}`EADDRINUSE`
	- The interface is busy (datagram sockets only).
-
	- {cpp:enumerator}`EBADF`
	- The {hparam}`socket` parameter is invalid.
-
	- {cpp:enumerator}`B_ERROR`
	- All other errors.

:::

## sendto(), recvfrom()









These functions are used by datagram sockets (only) to send and receive
messages. The functions encode all the information that's needed to find
the recipient or the sender of the desired message, so you don't need to
call {ref}`connect()` before invoking these functions. However, a datagram
socket that wants to receive messages must first call {ref}`bind()` (in
order to fix itself to an interface that can be specified in a remote
socket's sendto() call).

The four initial parameters to these function are similar to those for
{ref}`send()` and {ref}`recv()`; the additional parameters are the
interface specifications:

-   For sendto(), the {hparam}`to` parameter is a {htype}`sockaddr_in`
structure pointer (cast as a pointer to a {htype}`sockaddr` structure) that
specifies the interface of the remote socket that you're sending to. The
{hparam}`toLen` parameter is the size of the {hparam}`to` parameter.

-   For recvfrom(), the {hparam}`from` parameter returns the interface for the
remote socket that sent the message that recvfrom() received.
*{hparam}`fromLen` is set to the size of the from structure. As always, the
interface structure is a {htype}`sockaddr_in` cast as a pointer to a
{htype}`sockaddr`.

sendto() never blocks. recvfrom(), on the other hand, will block until a
message arrives, unless you set the socket to be non-blocking through the
{ref}`setsockopt()` function.

You can broadcast a message to all interfaces that can be found by setting
sendto()'s target address to {cpp:enumerator}`INADDR_BROADCAST`.

As an alternative to these functions, you can call {ref}`connect()` on a
datagram socket and then call {ref}`send()` and {ref}`recv()`. The
{ref}`connect()` call caches the interface information provided in its
parameters, and uses this information the subsequent {ref}`send()` and
{ref}`recv()` calls to "fake" the analogous sendto() and recvfrom()
invocations. For sending, the implication is obvious: The target of the
{ref}`send()` is the interface supplied in the {ref}`connect()`. The
implication for receiving bears description: when you {ref}`connect()` and
then call {ref}`recv()` on a datagram socket, the socket will only accept
messages from the interface given in the {ref}`connect()` call.

You can mix sendto()/recvfrom() calls with {ref}`send()`/{ref}`recv()`. In
other words, connecting a datagram socket doesn't prevent you from calling
sendto() and recvfrom().

A successful sendto() returns the number of bytes that were sent; a
successful recvfrom() returns the number of bytes that were received. Upon
failure, the functions return negative numbers and set {hparam}`errno` to…

:::{list-table}
---
header-rows: 1
align: left
widths: auto
---
-
	- Return Code

	- Description

-
	- {cpp:enumerator}`EWOULDBLOCK`
	- The call would block on a non-blocking socket.
-
	- {cpp:enumerator}`EINTR`
	- The local socket was interrupted.
-
	- {cpp:enumerator}`EBADF`
	- The {hparam}`socket` parameter is invalid.
-
	- {cpp:enumerator}`EADDRNOTAVAIL`
	- The specified interface is unrecognized.
-
	- {cpp:enumerator}`B_ERROR`
	- All other errors.

:::

## setsockopt()





setsockopt() lets you set certain options that are associated with a
socket. Currently, the Network Kit only recognizes one option: It lets you
declare a socket to be blocking or non-blocking. A blocking socket will
block in a {ref}`recv()` or {ref}`recvfrom()` call if there's no data to
retrieve.

A blocking socket will block in a {ref}`send()` or {ref}`sendto()` call if
the send would overrun the network's ability to keep up with the data.

A non-blocking socket returns immediately, even if it comes back
empty-handed or is unable to send the data.

The function's parameters are:

:::{list-table}
---
header-rows: 1
align: left
widths: auto
---
-
	- Parameter

	- Description

-
	- socket
	- Is the socket that you're attempting to affect.
-
	- level
	- Is a constant that indicates where the option is enforced. Currently,
		level should always be {cpp:enumerator}`SOL_SOCKET`.
-
	- option
	- Is a constant that represents the option you're interested in. The only
		option constant that does anything right now is
		{cpp:enumerator}`SO_NONBLOCK`. (Two other
		constants—{cpp:enumerator}`SO_REUSEADDR` and {cpp:enumerator}`SO_DEBUG`—are
		recognized, but they aren't currently implemented.)
-
	- data
	- Points to a buffer that's used to toggle or otherwise inform the option.
		For the {cpp:enumerator}`SO_NONBLOCK` option (and other boolean options),
		you fill the buffer with zeroes if you want to turn the option off (the
		socket will block), and non-zeros if you want to turn it on (the socket
		won't block). In the case of a boolean option, a single byte of
		zero/non-zero will do.
-
	- size
	- Is the size of the {hparam}`data` buffer.

:::

Upon failure, setsockopt() returns a negative number and sets
{hparam}`errno` to…

:::{list-table}
---
header-rows: 1
align: left
widths: auto
---
-
	- Return Code

	- Description

-
	- {cpp:enumerator}`EINTR`
	- The local socket was interrupted.
-
	- {cpp:enumerator}`EBADF`
	- The {hparam}`socket` parameter is invalid.
-
	- {cpp:enumerator}`ENOPROTOOPT`
	- Unknown option.

:::
