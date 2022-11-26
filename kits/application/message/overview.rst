BMessage
========

A BMessage is a bundle of structured information. Every BMessage contains a
command constant and some number of data fields.

* The command constant is an int32 value that describes, rougly, the purpose of
  the BMessage. It's stored as the public what data member. You always set and
  examine the what value directly, you don't need to call a function. (As a
  convenience, you can set the command constant when you create the BMessage
  object.)
* The data fields are name-type-value triplets. A field is primarily identified
  by name, but you can look for fields by name, type, or a combination of the two.
  The type is encoded as a constant (B_INT32_TYPE, B_STRING_TYPE, etc), and is
  meant to describe the type of value that the field holds. A single field can
  have only one name and one type, but can contain an array of values. Individual
  values in a field are accessible by index.

Neither the command constant nor the data fields are mandatory. You can create a
BMessage that has data but no command, or that only has a command. However,
creating a BMessage that has neither is pointless.

Preparatory Reading
===================

BMessages are used throughout the kits to send data (or notifications) to
another thread, possibly in another application. To understand how BMessages fit
into the messaging system, see :doc:`Messaging </kits/application/messaging>`.

The BMessage class also contributes a number of functions that help define the
scripting system. See "Scripting" for an introduction to this system.

BMessages are also used by a number of classes (BClipboard, BArchivable, and
others) for their ability to store data.

Types of Functions
==================

The BMessage class defines five types of functions:

Data field functions
	These functions either set or retreive the value of a data field. See
	AddData(), FindData(), ReplaceData(), and RemoveName()

Info functions
	These functions retrieve information about the state and contents of the
	BMessage. See IsSystem() and GetInfo()

Messaging functions
	These functions are part of the messaging system. A smaller set of functions
	reports on the status of a received message. For example, IsSourceWaiting()
	tells whether the message sender is waiting for a reply, WasDropped() says
	whether it was dragged and ropped, and DropPoint() says where it was
	dropped.

Scripting functions
	Functions such as AddSpecifier() and PopSpecifier()

Flatenning functions
	The data in a BMessage can be flattened into an untyped stream of bytes. See
	Flatten()

BMessage Ownership
==================

The documentation for the functions that accept or pass back a BMessage object
should tell you who's responsible for deleting the object. Most functions that
accept a BMessage argument copy the object, leaving the called with the
responsibility for deleting the argument. The exceptions i.e. BMessage-accepting
functions that take over ownership of the object are listed below:

Functions that return a BMessage to you usually don't give up ownership; in
general, you don't delete the BMessages that are passed to you. The exceptions,
functions that expect the caller to take over ownership of a passed-back
BMessage are listed below:
