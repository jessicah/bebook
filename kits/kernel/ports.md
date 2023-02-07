# Ports
## Port Functions
::::{abi-group}


:::{cpp:function} port_id Ports::create_port(int32 queue_length, const char* name)
:::
Creates a new port and returns its port_id number. The port's name is set
to {hparam}`name` and the length of its message queue is set to {hparam}`queue_length`.
Neither the name nor the queue length can be changed once they're set.
The name shouldn't exceed {cpp:enum}`B_OS_NAME_LENGTH` (32) characters.
In setting the length of a port's message queue, you're telling it how
many messages it can hold at a time. When the queue is filled—when
it's holding queue_length messages—subsequent invocations of
{cpp:func}`~write::port`
(on that port) block until room is made in the queue (through calls to
{cpp:func}`~read::port`)
for the additional messages. Once the queue length is set by
create_port(), it can't be changed.
This function sets the owner of the port to be the team of the calling
thread. Ownership can subsequently be transferred through the
{cpp:func}`~set::port`
function. When a port's owner dies (when all the threads
in the team are dead), the port is automatically deleted. If you want to
delete a port prior to its owner's death, use the
{cpp:func}`~delete::port`
function.
:::{list-table}
---
header-rows: 1
---
-
	- Return Code
	- Description
-
	- {cpp:enum}`B_BAD_VALUE`
	- {hparam}`queue_length` is too big or less than zero.
-
	- {cpp:enum}`B_NO_MORE_PORTS`.
	- The system couldn't allocate another port.
:::
::::

::::{abi-group}


:::{cpp:function} status_t Ports::close_port(port_id port)
:::
Closes the port so no more messages can be written to it. After you close
a port, you can call
{cpp:func}`~read::port`
on it, but a
{cpp:func}`~write::port`
call will return {cpp:enum}`B_BAD_PORT_ID`. You can't reopen a closed port; you call this
function so you can read through a port's unread messages prior to
deleting the port, while ensuring that no new messages will show up.
After you've read the messages, you should call
{cpp:func}`~delete::port`
on {hparam}`port`.
:::{list-table}
---
header-rows: 1
---
-
	- Return Code
	- Description
-
	- {cpp:enum}`B_OK`.
	- {hparam}`port` is now closed.
-
	- {cpp:enum}`B_BAD_PORT_ID`.
	- {hparam}`port` doesn't identify an open port.
:::
::::

::::{abi-group}


:::{cpp:function} status_t Ports::delete_port(port_id port)
:::
Deletes the given {hparam}`port`. The port's message queue doesn't have to be
empty—you can delete a port that's holding unread messages. Threads
that are blocked in
{cpp:func}`~read::port`
or
{cpp:func}`~write::port`
calls on the port are
automatically unblocked (and return {cpp:enum}`B_BAD_SEM_ID`).
The thread that calls delete_port() doesn't have to be a member of the
team that owns the port; any thread can delete any port.
:::{list-table}
---
header-rows: 1
---
-
	- Return Code
	- Description
-
	- {cpp:enum}`B_OK`.
	- The port was deleted.
-
	- {cpp:enum}`B_BAD_PORT_ID`.
	- {hparam}`port` isn't a valid port.
:::
::::

::::{abi-group}


:::{cpp:function} port_id Ports::find_port(const char* port_name)
:::
Returns the port_id of the named port.
{hparam}`port_name` should be no longer than
32 characters ({cpp:enum}`B_OS_NAME_LENGTH`).
:::{list-table}
---
header-rows: 1
---
-
	- Return Code
	- Description
-
	- {cpp:enum}`B_NAME_NOT_FOUND`.
	- {hparam}`port_name` doesn't name an existing port.
:::
::::

::::{abi-group}



:::{cpp:function} status_t Ports::get_port_info(port_id port, port_info* info)
:::
:::{cpp:function} status_t Ports::get_next_port_info(team_id team, uint32* cookie, port_info* info)
:::
Copies information about a particular {hparam}`port`
into the port_info structure
designated by {hparam}`info`. The first version of the function designates the port
directly, by port_id.
The get_next_port_info() version lets you step through the list of a
team's ports through iterated calls on the function. The {hparam}`team` argument
identifies the team you want to look at; a {hparam}`team` value of 0 means the team
of the calling thread. The {hparam}`cookie` argument is a placemark; you set it to
0 on your first call, and let the function do the rest. The function
returns {cpp:enum}`B_BAD_VALUE` when there are no more ports to visit:
:::{code}
/* Get the port_info for every port in this team. */
port_info info;
int32 cookie = 0;
while (get_next_port_info(0, &cookie, &info) == B_OK)
   ...
:::
The information in the port_info structure is guaranteed to be internally
consistent, but the structure as a whole should be considered to be
out-of-date as soon as you receive it. It provides a picture of a port as
it exists just before the info-retrieving function returns.
:::{list-table}
---
header-rows: 1
---
-
	- Return Code
	- Description
-
	- {cpp:enum}`B_OK`.
	- The port was found; {hparam}`info` contains valid information.
-
	- {cpp:enum}`B_BAD_VALUE`.
	- {hparam}`port` doesn't identify an existing port, {hparam}`team` doesn't identify an existing team, or there are no more ports to visit.
:::
::::

::::{abi-group}



:::{cpp:function} ssize_t Ports::port_buffer_size(port_id port)
:::
:::{cpp:function} ssize_t Ports::port_buffer_size_etc(port_id port, uint32 flags, bigtime_t timeout)
:::
These functions return the length (in bytes) of the message buffer that's
at the head of port's message queue. You call this function in order to
allocate a sufficiently large buffer in which to retrieve the message
data.
The port_buffer_size() function blocks if the port is currently empty. It
unblocks when a
{cpp:func}`~write::port`
call gives this function a buffer to measure
(even if the buffer is 0 bytes long), or when the port is deleted.
The port_buffer_size_etc() function lets you set a limit on the amount of
time the function will wait for a message to show up. To set the limit,
you pass {cpp:enum}`B_TIMEOUT` as the flags argument, and set timeout to the amount
of time, in microseconds, that you're willing to wait.
:::{list-table}
---
header-rows: 1
---
-
	- Return Code
	- Description
-
	- {cpp:enum}`B_BAD_PORT_ID`.
	- port doesn't identify an existing port, or the port was deleted while the function was blocked.
-
	- {cpp:enum}`B_TIMED_OUT`.
	- The timeout limit expired.
-
	- {cpp:enum}`B_WOULD_BLOCK`
	- You asked for a timeout of 0, but there are no messages in the queue.
:::
See also:
{cpp:func}`~read::port`
::::

::::{abi-group}


:::{cpp:function} int32 Ports::port_count(port_id port)
:::
Returns the number of messages that are currently in port's message
queue. This is the number of messages that have been written to the port
through calls to
{cpp:func}`~write::port`
but that haven't yet been picked up through corresponding
{cpp:func}`~read::port`
calls.
:::{admonition} Warning
:class: warning
This function is provided mostly as a convenience and a semi-accurate
debugging tool. The value that it returns is inherently undependable:
There's no guarantee that additional
{cpp:func}`~read::port` or
{cpp:func}`~write::port`
calls won't change the count as this function is returning.
:::
:::{list-table}
---
header-rows: 1
---
-
	- Return Code
	- Description
-
	- {cpp:enum}`B_BAD_PORT_ID`
	- {hparam}`port` doesn't identify an existing port.
:::
See also:
{cpp:func}`~get::port`
::::

::::{abi-group}



:::{cpp:function} ssize_t Ports::read_port(port_id port, int32* msg_code, void* msg_buffer, size_t buffer_size)
:::
:::{cpp:function} ssize_t Ports::read_port_etc(port_id port, int32* msg_code, void* msg_buffer, size_t buffer_size, uint32 flags, bigtime_t timeout)
:::
These functions remove the message at the head of {hparam}`port`'s message queue
and copy the messages's contents into the {hparam}`msg_code` and {hparam}`msg_buffer`
arguments. The size of the {hparam}`msg_buffer` buffer, in bytes, is given by
{hparam}`buffer_size`. It's up to the caller to ensure that the message buffer is
large enough to accommodate the message that's being read. If you want a
hint about the message's size, you should call
{cpp:func}`~port::buffer`
before calling this function.
If {hparam}`port`'s message queue is empty
when you call read_port(), the function
will block. It returns when some other thread writes a message to the
port through
{cpp:func}`~write::port`.
A blocked read is also unblocked if the port is deleted.
The read_port_etc() function lets you set a limit on the amount of time
the function will wait for a message to show up. To set the limit, you
pass {cpp:enum}`B_TIMEOUT` as the {hparam}`flags`
argument, and set timeout to the amount of
time, in microseconds, that you're willing to wait.
A successful call returns the number of bytes that were written into the
{hparam}`msg_buffer` argument.
:::{list-table}
---
header-rows: 1
---
-
	- Return Code
	- Description
-
	- {cpp:enum}`B_BAD_PORT_ID`.
	- {hparam}`port` doesn't identify an existing port, or the port was deleted while the function was blocked.
-
	- {cpp:enum}`B_TIMED_OUT`.
	- The timeout limit expired.
-
	- {cpp:enum}`B_WOULD_BLOCK`.
	- You asked for a timeout of 0, but there are no messages in the queue.
:::
::::

::::{abi-group}


:::{cpp:function} status_t Ports::set_port_owner(port_id port, team_id team)
:::
Transfers ownership of the designated port to team. A port can only be
owned by one team at a time; by setting a port's owner, you remove it
from its current owner.
There are no restrictions on who can own a port, or on who can transfer
ownership. In other words, the thread that calls set_port_owner() needn't
be part of the team that currently owns the port, nor must you only
assign ports to the team that owns the calling thread (although these two
are the most likely scenarios).
Port ownership is meaningful for one reason: When a team dies (when all
its threads are dead), the ports that are owned by that team are freed.
Ownership, otherwise, has no significance—it carries no special
privileges or obligations.
To discover a port's owner, use the
{cpp:func}`~get::port`
function.
:::{list-table}
---
header-rows: 1
---
-
	- Return Code
	- Description
-
	- {cpp:enum}`B_OK`.
	- Ownership was successfully transferred.
-
	- {cpp:enum}`B_BAD_PORT_ID`.
	- {hparam}`port` doesn't identify a valid port.
-
	- {cpp:enum}`B_BAD_TEAM_ID`.
	- {hparam}`team` doesn't identify a valid team.
:::
::::

::::{abi-group}



:::{cpp:function} status_t Ports::write_port(port_id port, int32 msg_code, void* msg_buffer, size_t buffer_size)
:::
:::{cpp:function} status_t Ports::write_port_etc(port_id port, int32 msg_code, void* msg_buffer, size_t buffer_size, uint32 flags, bigtime_t timeout)
:::
These functions place a message at the tail of port's message queue. The
message consists of {hparam}`msg_code` and
{hparam}`msg_buffer`:
:::{list-table}
---
header-rows: 1
---
-
	- Parameter
	- Description
-
	- msg_code
	- Holds the "message code." This is a mask, flag, or other predictable value that gives a general representation of the message.
-
	- msg_buffer
	- Is a pointer to a buffer that can be used to supply additional information. You pass the length of the buffer, in bytes, as the value of the {hparam}`buffer_size` argument. The buffer can be arbitrarily long.
:::
If the port's queue is full when you call write_port(),
the function will block. It returns when a
{cpp:func}`~read::port`
call frees a slot in the queue for the new message. A blocked
write_port() will also return if the target
port is deleted or closed.
The write_port_etc() function lets you set a limit on the amount of time
the function will wait for a free queue slot. To set the limit, you pass
{cpp:enum}`B_TIMEOUT` as the {hparam}`flags`
argument, and set timeout to the amount of time,
in microseconds, that you're willing to wait.
:::{list-table}
---
header-rows: 1
---
-
	- Return Code
	- Description
-
	- {cpp:enum}`B_OK`.
	- 
The port was successully written to.

-
	- {cpp:enum}`B_BAD_PORT_ID`.
	- {hparam}`port` doesn't identify an open port, or the port was deleted while the function was blocked.
-
	- {cpp:enum}`B_TIMED_OUT`.
	- The timeout limit expired.
-
	- {cpp:enum}`B_WOULD_BLOCK`.
	- You asked for a timeout of 0, but there are no free slots in the message queue.
:::
::::

## Port Structures and Constants
::::{abi-group}


:::{code}
struct {
    port_id port;
    team_id team;
    char name[B_OS_NAME_LENGTH];
    int32 capacity;
    int32 queue_count;
    int32 total_count;
} port_info
:::
The port_info structure provides information about a port. You retrieve
one of these structures through
{cpp:func}`~get::port` or
{cpp:func}`~get::next`.
:::{list-table}
---
header-rows: 1
---
-
	- Field
	- Description
-
	- port.
	- The port_id number of the port.
-
	- team.
	- The team_id of the port's owner.
-
	- name.
	- The name assigned to the port.
-
	- capacity.
	- The length of the port's message queue.
-
	- queue_count.
	- The number of messages currently in the queue.
-
	- total_count.
	- The total number of message that have been read from the port.
:::
Note that the total_count number doesn't
include the messages that are currently in the queue.
::::
