# BNetEndpoint
## Constructor and Destructor
::::{abi-group}

:::{cpp:function} BNetEndpoint::BNetEndpoint(int protocol = SOCK_STREAM)
:::
:::{cpp:function} BNetEndpoint::BNetEndpoint(const BNetEndpoint& from)
:::
:::{cpp:function} BNetEndpoint::BNetEndpoint(BMessage* archive)
:::
Creates a {hclass}`BNetEndpoint` representing a
network connection endpoint on the local system. After construction, you
must call
{cpp:func}`~BNetEndpoint::InitCheck`
to ensure that no errors occurred during setup.
The {hparam}`protocol` argument lets you specify
whether the {hclass}`BNetEndpoint` will use a stream
socket ({cpp:enum}`SOCK_STREAM`) or a datagram socket
({cpp:enum}`SOCK_DGRAM`).
By default, I/O is blocking and address reusing is off. You can change
these by calling
{cpp:func}`~BNetEndpoint::SetNonBlocking` and
{cpp:func}`~BNetEndpoint::SetReuseAddr`.
::::

::::{abi-group}

:::{cpp:function} virtual BNetEndpoint::~BNetEndpoint()
:::
A typical destructor.
::::

## Member Functions
::::{abi-group}

:::{cpp:function} virtual status_t BNetEndpoint::Bind(const BNetAddress& address)
:::
:::{cpp:function} virtual status_t BNetEndpoint::Bind(int port = 0)
:::
Binds the {hclass}`BNetEndpoint` to a
specific local address. That address can be
specified by using a
{cpp:class}`BNetAddress`
or a simple {hparam}`port` number. This selects
the port that will handle the local end of the connection.
If your {hclass}`BNetEndpoint` is using a stream
protocol and is going to be listening for connections, you must call
{hmethod}`Bind()`.
If your stream {hclass}`BNetEndpoint` is a client,
it doesn't have to call {hmethod}`Bind()` but you can if
you want to. There aren't any significant benefits to doing so,
however.
A stream accept {hclass}`BNetEndpoint`s must not
be bound.
Datagram {hclass}`BNetEndpoint`s that are going to
receive data must be bound; datagram
{hclass}`BNetEndpoint`s that will only be sending data
don't have to be. However, if an endpoint will both send and receive, it
must be bound.
If you don't specify an {hparam}`address` or
{hparam}`port` number, or specify a
{hparam}`port` number of 0,
{hmethod}`Bind()` will bind the
{hclass}`BNetEndpoint` to a random local port. You can
determine which one by calling
{cpp:func}`~BNetEndpoint::LocalAddr`.
The only way to unbind a {hclass}`BNetEndpoint`
from an address or port is to close the endpoint.
:::{list-table}
---
header-rows: 1
---
-
	- Return Code
	- Description
-
	- {cpp:enum}`B_OK`
	- The address was successfully bound to.
-
	- {cpp:enum}`B_ERROR`
	- An error occurred.
:::
::::

::::{abi-group}

:::{cpp:function} virtual void BNetEndpoint::Close()
:::
Closes the connection, if there is one. If there's unread data buffered
up, it's disposed of.
::::

::::{abi-group}

:::{cpp:function} virtual status_t BNetEndpoint::Connect(const BNetAddress& address)
:::
:::{cpp:function} virtual status_t BNetEndpoint::Connect(const char* address, unsigned short port)
:::
Opens a connection to the specified remote system. The system's address
can be specified by either using a
{hclass}`BNetAddress`
or by specifying the IP
address or domain name and port number. For example, to connect to the
Megaburger, Inc. web server, your software would call:
:::{code}
status_t err = myEndpoint->Connect("www.megaburger.com", 80);
if (err != B_OK) {
   /* error occurred */
}
else {
   /* all is well, connection is open */
}
:::
:::{list-table}
---
header-rows: 1
---
-
	- Return Code
	- Description
-
	- {cpp:enum}`B_OK`
	- The connection was opened.
-
	- {cpp:enum}`B_ERROR`
	- An error occurred.
:::
::::

::::{abi-group}

:::{cpp:function} int BNetEndpoint::Error() const
:::
:::{cpp:function} char* BNetEndpoint::ErrorStr() const
:::
{hmethod}`Error()` returns the integer error code for the last send or receive
error. If you receive a {cpp:enum}`B_ERROR` result from a send or receive function,
you can find out the specific error using this function.
{hmethod}`ErrorStr()` returns a pointer to a text string describing the error; this
string isn't yours, so don't try to free() it.
::::

::::{abi-group}

:::{cpp:function} status_t BNetEndpoint::InitCheck() const
:::
Returns a status_t indicating whether or not the object was successfully
instantiated.
:::{list-table}
---
header-rows: 1
---
-
	- Return Code
	- Description
-
	- {cpp:enum}`B_OK`
	- The {hclass}`BNetEndpoint` was constructed without error.
-
	- {cpp:enum}`B_ERROR`
	- An error occurred during construction.
:::
::::

::::{abi-group}

:::{cpp:function} virtual bool BNetEndpoint::IsDataPending(bigtime_t timeout = 0)
:::
Returns {cpp:enum}`true` if there's data waiting to be received, otherwise returns
{cpp:enum}`false`. If you specify a {hparam}`timeout` other than 0, the function will block
until either data is available or the timeout period elapses.
::::

::::{abi-group}

:::{cpp:function} virtual status_t BNetEndpoint::Listen(int backlog = 5)
:::
:::{cpp:function} virtual BNetEndpoint* BNetEndpoint::Accept(int32 timeout = -1)
:::
{hmethod}`Listen()` tells the
{hclass}`BNetEndpoint` to begin listening for incoming
connection attempts on its local port. These attempts are queued; up to
backlog attempts can be in the queue at any time. If more attempts are
backlogged than that, the later attempts will be rejected until there's
room in the queue.
You can accept an incoming connection attempt by calling {hmethod}`Accept()`. If
there are no connection attempts queued up, this function returns {cpp:enum}`NULL`.
If there are connection attempts in the queue, a new {hclass}`BNetEndpoint` object
is created with the connection between your local port and the remote
system opened, and that {hclass}`BNetEndpoint` is returned to you.
The new connection is yours to do with as you please. When you're
finished with the connection, you must delete the returned {hclass}`BNetEndpoint`.
Typically your listener thread will look something like this:
:::{code}
long MyListener(void* data) {
   BNetEndpoint endpoint;
   if (endpoint.InitCheck() < B_OK) {
      return -1;
   }
   /* bind to the desired port */
   endpoint.Bind(portNumber);
   /* listen for connections */
   endpoint.Listen();
   while (keepListening) {
      BNetEndpoint* connect = NULL;
      connect = endpoint.Accept();
      if (connect) {
         /* call a function do the work */
         handle_connection(connect, data);
         delete connect;
      }
   }
   endpoint.Close();
}
:::
:::{list-table}
---
header-rows: 1
---
-
	- Return Code
	- Description
-
	- {cpp:enum}`B_OK`
	- Success.
-
	- {cpp:enum}`B_ERROR`
	- Failure.
:::
::::

::::{abi-group}

:::{cpp:function} const BNetAddress& BNetEndpoint::LocalAddr()
:::
:::{cpp:function} const BNetAddress& BNetEndpoint::RemoteAddr()
:::
These functions return a
{cpp:class}`BNetAddress`
representing the local or remote system on the connection.
{hmethod}`LocalAddr()` returns the address of the local
machine, and {hmethod}`RemoteAddr()` (amazingly enough)
returns the address of the remote system.
If there isn't a remote connection, {hmethod}`RemoteAddr()` will return a
{cpp:class}`BNetAddress`
indicating an IP address of 0.0.0.0.
::::

::::{abi-group}

:::{cpp:function} virtual int32 BNetEndpoint::Receive(const void* buffer, size_t size, int flags = 0)
:::
:::{cpp:function} virtual int32 BNetEndpoint::Receive(BNetBuffer& buffer, size_t size, int flags = 0)
:::
:::{cpp:function} virtual int32 BNetEndpoint::ReceiveFrom(const void* buffer, size_t size, const BNetAddress& from, int flags = 0)
:::
:::{cpp:function} virtual int32 BNetEndpoint::ReceiveFrom(BNetBuffer& buffer, size_t size, const BNetAddress& from, int flags = 0)
:::
{hmethod}`Receive()` receives a buffer of data from the remote end of the
connection. If there's no connection established, {cpp:enum}`B_ERROR` is returned
immediately. Up to {hparam}`size` bytes of data are received.
{hmethod}`ReceiveFrom()` receives the buffer
from the remote system specified by the from
{cpp:class}`BNetAddress`.
{hmethod}`ReceiveFrom()` only works if the connection is
using a datagram protocol.
The first form of each function function sends an arbitrary buffer of the
specified {hparam}`size`, and the second form sends the contents of a
{cpp:class}`BNetBuffer`.
When using a
{cpp:class}`BNetBuffer`,
incoming data is appended to the end of the
buffer, so you can use the same buffer in a loop to buffer incoming data
in chunks until the desired number of bytes have been read.
The {hparam}`flags` argument, which is passed on to
the socket.h
{ref}`recv()` or
{ref}`recvfrom()`
function, is currently unused and must be 0.
When you call these functions in blocking mode (which is the default),
they block until there's data available to receive or a timeout occurs.
The timeout period is set by calling
{cpp:func}`~BNetEndpoint::SetTimeout`.
You can turn on or off blocking by calling
{cpp:func}`~BNetEndpoint::SetNonBlocking`.
If you're in nonblocking mode and
there's no data waiting, these functions return 0 immediately, indicating
that there's no data.
These functions return the number of bytes actually received, or -1 if an
error occurred. You can call
{cpp:func}`~BNetEndpoint::Error`
to get the specific error that occurred.
::::

::::{abi-group}

:::{cpp:function} virtual int32 BNetEndpoint::Send(const void* buffer, size_t size, int flags = 0)
:::
:::{cpp:function} virtual int32 BNetEndpoint::Send(BNetBuffer& buffer, int flags = 0)
:::
:::{cpp:function} virtual int32 BNetEndpoint::SendTo(const void* buffer, size_t size, const BNetAddress& to, int flags = 0)
:::
:::{cpp:function} virtual int32 BNetEndpoint::SendTo(BNetBuffer& buffer, const BNetAddress& to, int flags = 0)
:::
{hmethod}`Send()` sends a buffer of data to the
remote end of the connection. If there's no connection established,
{cpp:enum}`B_ERROR` is returned immediately. In addition, if
the {hclass}`BNetEndpoint` is configured to use a datagram
protocol, this function fails unless
{cpp:func}`~BNetEndpoint::Connect`
has been called, since that function caches the destination address.
{hmethod}`SendTo()` sends the buffer to the remote system specified by the to
{cpp:class}`BNetAddress`.
{hmethod}`SendTo()` only works if the connection is using a datagram
protocol.
The first form of each function function sends an arbitrary buffer of the
specified size, and the second form sends the contents of a
{cpp:class}`BNetBuffer`.
The {hparam}`flags` argument, which is passed on
to the the socket.h
{ref}`send()` or
{ref}`sendto()`
function, is currently unused and must be 0.
These functions return the number of bytes actually sent, or -1 if an
error occurred. You can call
{cpp:func}`~BNetEndpoint::Error`
to get the specific error that occurred.
::::

::::{abi-group}

:::{cpp:function} int BNetEndpoint::SetOption(int32 option, int32 level, const void* data, unsigned int dataSize)
:::
:::{cpp:function} int BNetEndpoint::SetNonBlocking(bool enable = true)
:::
:::{cpp:function} int BNetEndpoint::SetReuseAddr(bool enable = true)
:::
{hmethod}`SetOption()` lets you set any option
for the {hclass}`BNetEndpoint`. This provides
access to the setsockopt() function of the underlying
socket.
{hmethod}`SetNonBlocking()` controls whether
I/O should block or not. If {hparam}`enable` is
{cpp:enum}`true`, the connection will be nonblocking. If
{hparam}`enable` is {cpp:enum}`false`, the
connection will block on I/O calls until the transmission is completed.
{hmethod}`SetReuseAddr()` controls
whether addresses should be reused or not. If
{hparam}`enable` is {cpp:enum}`true`, addresses
will be reused. If {hparam}`enable` is {cpp:enum}`false`, the
connection won't reuse addresses.
These functions return 0 if successful; otherwise they return -1.
::::

::::{abi-group}

:::{cpp:function} status_t BNetEndpoint::SetProtocol(int protocol)
:::
Sets the protocol type for the connection. Possible values for the
protocol argument are {cpp:enum}`SOCK_STREAM` (to use the stream protocol) or
{cpp:enum}`SOCK_DGRAM` (for datagram protocol).
:::{list-table}
---
header-rows: 1
---
-
	- Return Code
	- Description
-
	- {cpp:enum}`B_OK`
	- The protocol was set successfully.
-
	- {cpp:enum}`B_ERROR`
	- An error occurred setting the protocol.
:::
::::

::::{abi-group}

:::{cpp:function} void BNetEndpoint::SetTimeout(bigtime_t timeout)
:::
Sets the timeout for calls to
{cpp:func}`~BNetEndpoint::Receive` and
{cpp:func}`~BNetEndpoint::ReceiveFrom`.
If blocking I/O is in use, and {hparam}`timeout`
microseconds pass, the function will abort
with an error. By default, there's no timeout. You can specify that you
want no timeout by specifying -1.
::::

::::{abi-group}

:::{cpp:function} int BNetEndpoint::Socket() const
:::
Returns the actual socket used by the {hclass}`BNetEndpoint` for data
communications.
::::

## Operators
::::{abi-group}

:::{cpp:function} BNetEndpoint& operator =(const BNetEndpoint& from)
:::
Copies the {hclass}`BNetEndpoint` specified by
{hparam}`from` into the left-side object,
thereby duplicating that object. If {hparam}`from` is connected, the left-side
object will duplicate and open the same connection.
::::
