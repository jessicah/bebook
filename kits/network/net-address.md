# BNetAddress
## Constructor and Destructor
::::{abi-group}

:::{cpp:function} BNetAddress::BNetAddress(const char* hostname = NULL, unsigned short port = 0)
:::
:::{cpp:function} BNetAddress::BNetAddress(const struct sockaddr_in& sa)
:::
:::{cpp:function} BNetAddress::BNetAddress(in_addr addr, int port = 0)
:::
:::{cpp:function} BNetAddress::BNetAddress(uint32 addr, int port = 0)
:::
:::{cpp:function} BNetAddress::BNetAddress(const char* hostname, const char* protocol, const char* service)
:::
:::{cpp:function} BNetAddress::BNetAddress(BNetAddress& from)
:::
:::{cpp:function} BNetAddress::BNetAddress(BMessage* archive)
:::
Sets up the {hclass}`BNetAddress` object to refer to the specified address. The
address can be specified in a number of ways:
- By {hparam}`hostname` and {hparam}`port` number. For example, to connect to the HTTP port at www.be.com, you would specify "www.be.com" as the {hparam}`hostname`, and 80 for the {hparam}`port` number.
- By sockaddr_in structure. This structure contains the network family, port number, and IP address that make up the address.
- By IP address and port number. The IP address can be specified either using an in_addr, or by using a uint32. The IP address must be specified in network byte order. See the htonl() function.
- By {hparam}`hostname`, {hparam}`protocol`, and {hparam}`service` name. This causes the port to be looked up in the /etc/services file by matching the protocol (typically "tcp" or "udp") and service name (such as "http" or "ftp") against the entries in the file. See getservbyname() for details on the format of this file.
- By copying an existing {hclass}`BNetAddress`.
- By unflattening an archived {hclass}`BNetAddress` from a {cpp:class}`BMessage`.

After creating your {hclass}`BNetAddress`, you must call
{cpp:func}`~BNetAddress::InitCheck`
to ensure that no errors occurred during setup. You can change the address later by
calling
{cpp:func}`~BNetAddress::SetTo`.
::::

::::{abi-group}

:::{cpp:function} virtual BNetAddress::~BNetAddress()
:::
A typical destructor.
::::

## Member Functions
::::{abi-group}

:::{cpp:function} status_t BNetAddress::InitCheck() const
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
	- The {hclass}`BNetAddress` was constructed without error.
-
	- {cpp:enum}`B_ERROR`
	- An error occurred during construction.
:::
::::

::::{abi-group}

:::{cpp:function} status_t BNetAddress::GetAddr(const char* hostname = NULL, unsigned short* port = NULL) const
:::
:::{cpp:function} status_t BNetAddress::GetAddr(const struct sockaddr_in& sa) const
:::
:::{cpp:function} status_t BNetAddress::GetAddr(in_addr& addr, unsigned short* port = NULL) const
:::
Returns the address represented by the {hclass}`BNetAddress`
object in the format indicated by the form of the function used.
If you don't care about the hostname (in the first form), you can specify
{cpp:enum}`NULL` for the {hparam}`hostname` argument;
if you don't care about the port number, you can specify
{cpp:enum}`NULL` for the {hparam}`port` argument.
:::{list-table}
---
header-rows: 1
---
-
	- Return Code
	- Description
-
	- {cpp:enum}`B_OK`
	- The address was returned successfully.
-
	- {cpp:enum}`B_ERROR`
	- An error occurred fetching the address information.
:::
::::

::::{abi-group}

:::{cpp:function} status_t BNetAddress::SetTo(const char* hostname, const char* protocol, const char* service)
:::
:::{cpp:function} status_t BNetAddress::SetTo(const char* hostname = NULL, unsigned short port = 0)
:::
:::{cpp:function} status_t BNetAddress::SetTo(const struct sockaddr_in& sa)
:::
:::{cpp:function} status_t BNetAddress::SetTo(in_addr addr, int port = 0)
:::
:::{cpp:function} status_t BNetAddress::SetTo(uint32 addr = INADDR_ANY, int port = 0)
:::
Sets the address represented by the {hclass}`BNetAddress` object in the format
indicated by the form of the function used. These formats are described
in the discussion of the constructor.
:::{list-table}
---
header-rows: 1
---
-
	- Return Code
	- Description
-
	- {cpp:enum}`B_OK`
	- The address was set successfully.
-
	- {cpp:enum}`B_ERROR`
	- An error occurred setting the address information.
:::
::::
