Messaging
=========

.. highlight:: cpp

The Application Kit provides a message-passing system that lets your application
send messages to and receives messages from other applications (including the
Be-defined servers and apps), and from other threads in your own application.

The primary messaging classes are:

:cpp:class:`BMessage`
	Represents a message.

:cpp:class:`BHandler`
	Defines hook functions that are called to handle incoming messages

:cpp:class:`BLooper`
	Runs a loop that receives incoming messages and figures out which BHandler
	should handle them.

:cpp:class:`BMessenger`
	Represents a message's destination (a combination of BLooper and BHandler),
	whether it's local or remote. The object is most useful for sending messages
	to other applications--you don't need it for local calls.

The other messaging classes are:

:cpp:class:`BMessageQueue`
	Is a FIFO that holds a BLooper's incoming messages.

:cpp:class:`BMessageFilter`
	Is a device that can examine and (potentially) reject or re-route incoming
	messages.
	
:cpp:class:`BInvoker`
	Is a convenience class that lets you treat a message and its target (the
	BHandler that will handle the message) as a single object.

:cpp:class:`BMessageRunner`
	Lets you send the same message over and over, at regular intervals.

The rest of this chapter looks at...

* The essential features of the four fundamental classes. ("Features of the
fundamental Classes")
* How a BLooper decides which BHandler should handle an incoming message. ("From
Looper to Handler")
* The different methods for sending messages and receiving replies. ("Sending a Message")

and describes how the classes fit together in the messaging system with an
emphasis on what you can do in your application to take part.

Features of the Fundamental Classes
===================================

Looked at collectively, the four fundamental messaging classes comprise a huge
chunk of API. Fortunately, the essential part of this API is pretty small;
that's what we're going to look at here.

The BMessage Class
------------------

In the BMessage class, there's one essential data member, and two essential
functions:

* The what data member is an arbitrary uint32 value that describes
(symbolically) what the message is about. You can set and exame what
directly--you don't have to use functions to get to it. The what value is called
the object's command constant. The BeOS defines some number of command constants
(such as :cpp:enum:`B_QUIT_REQUESTED`, and :cpp:enum:`B_MOUSE_DOWN`), but you'll also be creating
constants of your own. Keep in mind that the constant's value is
meaningless--it's just a code that identifies the "intent" of the message (and
it's only meaningful if the receiver recognizes the constant).

* The two essential functions are :cpp:expr:`AddData()` and :cpp:expr:`FindData()`. These functions add
data to a message you're about to send, and retrieve it from a message you just
received. A :cpp:class:`BMessage` can hold any amount of data; each data item (or "field") is
identified by name, type, and index. For example, you can ask a message for the
third boolean value named "IsEnabled" that it contains. In general, you use
type-specific functions such as :cpp:expr:`Add/FindString()` and :cpp:expr:`Add/FindInt32()` rather than
:cpp:expr:`Add/FindData()`. The query we just posed would actually look like this::
	/* The args are: name, index, value (returned by
	   reference) */
	bool returnValue;
	aMessage.FindBool("IsEnabled", 2, &returnValue);

In summary, a :cpp:class:`BMessage` contains (1) a command constant and (2) a set of data
fields. Every :cpp:class:`BMessage` that's used in the messaging system must have a command
constant, but not every object needs to have data fields. (Other parts of the
BeOS use :cpp:class:`BMessage` s for their data only. The :cpp:class:`BClipboard` object, for example,
ignores a :cpp:class:`BMessage`'s command constant.)

Note: When discussing system-generated :cpp:class:`BMessage` objects, we refer to the object
by its command constant. For example, "a :cpp:enum:`B_MOUSE_DOWN`" means "a :cpp:class:`BMessage` that
has :cpp:enum:`B_MOUSE_DOWN` as its command constant".

Notice that a :cpp:class:`BMessage` doesn't know how to send itself. However, as we'll see
later, it does know how to reply to its sender once it's in the hands of the
recipient.

The BLooper Class
=================

BLooper's role is to receive messages and figure out what to do with them. There
are four parts to this job, embodied in these functions:
