# Ports

A port is a system-wide message repository into which any thread can copy a buffer of data, and from
which any thread can then retrieve the buffer. This repository is implemented as a
first-in/first-out message queue: A port stores its messages in the order in which they're received,
and it relinquishes them in the order in which they're stored. Each port has its own message queue.

## Creating and Destroying a Port

The {cpp:func}`create_port()` function creates a new port and assigns it a unique, system-wide
`port_id` number. Although ports are accessible to all threads, the `port_id` numbers aren't
disseminated by the operating system---there's no "find_port" function. If you create a port and
want some other thread to be able to write to or read from it, you have to broadcast the `port_id`
to that thread.

A port is owned by the team in which it was created. When a team dies (when all its threads are
killed), the ports that belong to the team are deleted. A team can bestow ownership of its ports to
some other team through the {cpp:func}`set_port_owner()` function.

If you want to explicitly get rid of a port, you call {cpp:func}`delete_port`. You can delete any
port, not just those that are owned by the team of the calling them. When you delete a port, all of
its unread messages are thrown away. If you want to read these messages, but you don't want any new
messages to arrive in the meantime, you should call {cpp:func}`close_port()` before deleting the
port. Note that you can't reopen a closed port; after you get done reading the port's messages,
you're expected to delete the port.

## The Message Queue: Reading and Writing Port Messages

The length of a port's message queue---the number of messages that it can hold at a time---is set
when the port is created.

The functions {cpp:func}`write_port()` and {cpp:func}`read_port()` manipulate a port's message
queue: {cpp:func}`write_port()` places a message at the tail of the port's message queue;
{cpp:func}`read_port()` removes the message at the head of the queue and returns it to the caller.
{cpp:func}`write_port()` blocks if the queue is full; it returns when room is made in the queue by
an invocation of {cpp:func}`read_port()`. Similarly, if the queue is empty, {cpp:func}`read_port()`
blocks until {cpp:func}`write_port()` is called.

You can provide a timeout for your port-writing and port-reading operations by using the
"full-blown" functions {cpp:func}`write_port_etc()` and {cpp:func}`read_port_etc()`. By supplying a
timeout, you can ensure that your port operations won't block forever.

Although each port has its own message queue, all ports share a global "queue slot" pool---there are
only so many message queue slots that can be used by all ports taken cumulatively. If too many port
queues are allowed to fill up, the slot pool will drain, which will cause {cpp:func}`write_port()`
calls on less-than-full ports to block. To avoid this situation, you should make sure that your
{cpp:func}`write_port()` and {cpp:func}`read_port()` calls are reasonably balanced.

The {cpp:func}`write_port()` and {cpp:func}`read_port()` functions are the only way to traverse a
port's message queue. There's no notion of "peeking" at the queue's unread messages, or of erasing
messages that are in the queue.

## Port Messages

A port message---the data that's sent through a port---consists of a "message code" and a "message
buffer". Either of these elements can be used however you like, but they're intended to fit these
purposes:

- A message code (a single four-byte value) should be a mask, flag, or other predictable value that
  gives a general representation of the flavor or import of the message. For this to work, the
  sender and receiver of the message must agree on the meanings of the values that the code can
  take.

- The data in the message buffer can elaborate upon the code, identify the sender of the message, or
  otherwise supply additional information. The length of the buffer isn't restricted. To get the
  length of the message buffer that's at the head of a port's queue, you call the
  {cpp:func}`port_buffer_size()` function.

The message that you pass to {cpp:func}`write_port()` is copied into the port. After
{cpp:func}`write_port()` returns, you may free the message data without affecting the copy that the
port holds.

When you read a port, you have to supply a buffer into which the port mechanism can copy the
message. If the buffer that you supply isn't large enough to accommodate the message, the unread
portion will be lost---the next call to {cpp:func}`read_port()` won't finish reading the message.

You typically allocate the buffer that you pass to {cpp:func}`read_port()` by first calling
{cpp:func}`port_buffer_size()`, as shown below:

:::{code} cpp
char *buf = NULL;
ssize_t size;
int32 code;

/* We'll assume that my_port is valid.
* port_buffer_size() will block until a message shows up.
*/
if ((size = port_buffer_size(my_port)) < B_OK)
   /* Handle the error */

if (size > 0)
   buf = (char *)malloc(size);

if (buf) {
   /* Now we can read the buffer. */
   if (read_port(my_port, &code, (void *)buf, size) < B_OK)
   /* Handle the error */
:::

Obviously, there's a race condition (in the example) between {cpp:func}`port_buffer_size()` and the
subsequent {cpp:func}`read_port()` call---some other thread could read the port in the interim. If
you're going to use {cpp:func}`port_buffer_size()` as shown in the example, you shouldn't have more
than one thread reading the port at a time.

As stated in the example, {cpp:func}`port_buffer_size()` blocks until a message shows up. If you
don't want to (potentially) block forever, you should use the {cpp_func}`port_buffer_size_etc()`
version of the function. As with the other `...etc()` functions, {cpp:func}`port_buffer_size_etc()`
provides a timeout option.
