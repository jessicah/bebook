# Scripting

Scripting provides a mechanism for programmatically controlling some other application by sending it
special scripting commands. These commands are defined by the "scripted" application itself. For
example, if you want some other application to be able to tell your application to perform the
"FlipOver" operation, you have to publish the format of the "FlipOver" command. The set of
operations that you want to expose is called a "suite".

Haiku defines some number of suites that correspond to particular classes. For example, all
{cpp:class}`BApplication` objects respond to the commands defined in the "vnd.Be-application" suite.
One of the commands in the suite gives you access to the application's windows. When you've located
the window that you want, you can move it, close it, resize it, and so on, according to the commands
in the "vnd.Be-window" suite.

---

# Basics

The scripting framework defines the following notions: commands, properties, and specifiers. If you
are familiar with AppleScript, these are equivalent to verbs, nouns, and adjectives. Commands act on
a specific instance of a property, as determined by the specifiers.

## Commands

The command conveys the action of a scripting command and is stored in the {cpp:expr}`what` field of
the scripting {cpp:class}`BMessage`. There are six standard commands (defined in `app/Message.h`).

:::{list-table}
---
header-rows: 1
---
-
	- Constant
	- Description
-
	- {cpp:enum}`B_COUNT_PROPERTIES`
	- Counts the number of instances of a property.
-
	- {cpp:enum}`B_CREATE_PROPERTY`
	- Creates a new instance of a property.
-
	- {cpp:enum}`B_DELETE_PROPERTY`
	- Destroys an instance of a property.
-
	- {cpp:enum}`B_GET_PROPERTY`
	- Gets the value of an instance of a property.
-
	- {cpp:enum}`B_SET_PROPERTY`
	- Sets the value of an instance of a property. The `data` field contains the new value of the
	property.
:::

Each of these commands acts on a "property", which is nothing more than a scriptable feature of an
object. As a real world example, the windows owned by an application are properties, as is the title
of each window. The particular interpretation of the command depends upon the property it is acting
on. For example, {cpp:enum}`B_DELETE_PROPERTY`, acting on the "Entry" property of a Tracker window,
causes a file to be moved to the trash. However, the same command acting on the "Selection" property
of the same window removes files from the list of selected items.

Scriptable objects should limit themselves to this set of commands. If an object uses a nonstandard
command, it runs the risk of being unusable by general scripting tools.

## Properties and Specifiers

A property represents a scriptable feature of an object. Properties are named; these names are
strings unique within a class. For example, a {cpp:class}`BWindow` defines properties such as
"Frame", "Title", and "View". The data type of the property and its allowable values are determined
by the property. For example, the window's "Frame" accepts {cpp:enum}`B_RECT_TYPE` values while the
"Title" is a {cpp:enum}`B_STRING_TYPE`.

Sometimes a property is represented by another object. For example, {cpp:class}`BWindow`'s "View"
designates a {cpp:class}`BView`, an object which hsa a set of properties distinct from those of
{cpp:class}`BWindow`.

An object may have more than one instance of a given property. For example, the "Window" property of
{cpp:class}`BApplication`, has as many instances as there are windows in the application. As a
result, there is some ambiguity when you ask for the Window of an application. Instead, it's more
correct to ask for the first Window, of the Window named "Snyder". In other words, a property is not
enough to identify a feature; a specific instance must be picked out as well.

Specifiers are used to target ("specify") particular instances of properties. A specifier is a
{cpp:class}`BMessage` containing the following elements:

- The name of the property in the "property" field, stored as a {cpp:enum}`B_STRING_TYPE`.
- The specifier constant, indicating a method of identifying a specific instance of the property, in
  the {cpp:expr}`what` field along with any necessary supporting fields.

There are seven standard specifier constants (defined in `app/Message.h`):

:::{list-table}
---
header-rows: 1
---
-
	- Constant
	- Description
-
	- {cpp:enum}`B_DIRECT_SPECIFIER`
	- The property name is sufficient specification by itself, usually because there's only one
	instance of the property. If there's more than one value for the property, a
	{cpp:enum}`B_DIRECT_SPECIFIER` would specify them all.
-
	- {cpp:enum}`B_NAME_SPECIFIER`
	- The specifier message has a `name` field of type {cpp:enum}`B_STRING_TYPE` with the name of a
	particular instance of the property.
-
	- {cpp:enum}`B_ID_SPECIFIER`
	- The specifier message has an `id` field with a unique identifying value of type int32 for a
	particular instance of the property.
-
	- {cpp:enum}`B_INDEX_SPECIFIER`
	- The specifier message has an int32 field named `index` with the index to a particular instance
	of the property.
-
	- {cpp:enum}`B_RANGE_SPECIFIER`
	- In addition to an `index` field, the specifier message has an additional int32 field named
	`range`, identifying `range` items beginning at "index."
-
	- {cpp:enum}`B_REVERSE_RANGE_SPECIFIER`
	- The "index" counts from the end of the list backwards. Depending on the kind of data and the
	message protocol, the `range` may extend toward the front of the list from the index or toward
	the end of the lift. In other words, the index works in reverse, the range may or may not.
:::

As with messages, the precise meaning of a given specifier depends upon the context. Additionally,
there may be user-defined (or perhaps more properly object-defined) specifiers. User-defined
specifier constants should be greater than `B_SPECIFIERS_END` to prevent conflicts with
Haiku-defined specifiers.

Specifiers are added to the "specifier" field of a scripting message using
{cpp:func}`BMessage::AddSpecifier()`. There are several variants of this method, including shortcuts
for adding {cpp:enum}`B_DIRECT_SPECIFIER`, {cpp:enum}`B_INDEX_SPECIFIER`,
{cpp:enum}`B_RANGE_SPECIFIER`, and {cpp:enum}`B_NAME_SPECIFIER` specifiers. For all other
specifiers, you must manually construct the specifier and add it to the scripting message with
{cpp:func}`AddSpecifier()`. For example, to add a {cpp:enum}`B_ID_SPECIFIER`:

	BMessage specifier(B_ID_SPECIFIER);	// create a new specifier
	specifier.AddInt32("id", 2827);		// add the id number of the specifier
	message.AddSpecifier(&specifier);	// add the specifier to the message

:::{warning}
You _must_ use {cpp:func}`BMessage::AddSpecifier()` to add specifiers to a {cpp:class}`BMessage`; it
performs additional scripting support work that {cpp:func}`AddMessage()` doesn't.
:::

## The Specifier Stack

In general, an application will not be able to obtain a {cpp:class}`BMessenger` for the target
object; instead, it'll have to settle for a {cpp:class}`BMessenger` targeting the
{cpp:class}`BApplication` of the program containing the desired object. In these cases, a single
specifier may be insufficient to target a scripting message. The true power of specifiers lies in
their ability to be chained together in the specifier stack.

An example best illustrates the operation of the specifier stack. The following code snippet creates
a message that will target the frame of the second view of the window named "egg" in the target
application:

	message.AddSpecifier("Label");
	message.AddSpecifier("MenuBar");
	message.AddSpecifier("Window", 1);

Repeated calls to {cpp:func}`AddSpecifier()` build the specifier stack. The order of the calls is
very important; the specifies are evaluated in the opposite order from which they were added. When
this message is received by the target application, it will first peel off the third specifier and
direct the message to the second window of the application. The {cpp:class}`BWindow` will then peel
off the second specifier and direct the message to the window's key menu bar. The first specifier
("Label") is then processed by the {cpp:class}`BMenuBar`. This process is covered in more detail
below under {cpp:func}`ResolveSpecifier()`.

## Replies

A reply is generated for every scripting request. The reply message contains the following fields:

- The `what` data member defaults to {cpp:enum}`B_REPLY` unless some other constant is appropriate.
  For example; if the message was not understood, the object responds with a
  {cpp:enum}`B_MESSAGE_NOT_UNDERSTOOD` {cpp:class}`BMessage`.
- The {cpp:enum}`B_INT32_TYPE` field `error` contains the error code for the operation. This field
  is always present.
- Responses to a successful {cpp:enum}`B_GET_PROPERTY` request will additionally contain the value
  or values of the requested property in the `result` array. The data will be of a type appropriate
  for the property.

Any scriptable objects that you create should also obey the above protocol. Of course, individual
objects are free to define their own protocols for relaying additional information in the reply; in
those cases, consult the documentation for the class in question.

# Creating and Sending Scripting Messages

The scripting facilities of an application can be invoked in three easy steps:

1. Set the command constant for the scripting message.
2. Construct the specifier stack for the scripting message.
3. Send the scripting message to the target application.

## Example

Suppose we want to fetch the frame rectangle of the second view of the window titled "egg" in an
application with the signature "application/x-fish". The code:

	BMessage message, reply;
	BRect result;

	// set the command constant
	message.what = B_GET_PROPERTY;

	// construct the specifier stack
	message.AddSpecifier("Frame");			// B_DIRECT_SPECIFIER
	message.AddSpecifier("View", 1);		// B_INDEX_SPECIFIER
	message.AddSpecifier("WIndow", "egg");	// B_NAME_SPECIFIER

	// send the message and fetch the result
	BMessenger("application/x-fish").SendMessage(&message, &reply);
	reply.FindRect("result", &result);

Short and sweet.

---

## Suites

There is one missing element in the scripting system, namely the ability to query an object for its
scripting abilities. This is useful when the controlling application doesn't know the precise type
of the object it is scripting. Having a method of discovering the scripting abilities of an object
enables more dynamic uses of scripting.

An object's scripting abilities are organized into one or more scripting "suites," a set of
supported messages and associated specifiers. A suite is identified by a MIME-like string with the
"suite" supertype. For example, {cpp:class}`BControl` implements the "suite/vnd.Be-control"
scripting suite. Nothing prevents two objects from implementing the same suite; two sound editors,
for example, could have different implementations of a common scripting suite for filtering audio
data.

To ask an object for its supported scripting suites, send it a standard scripting message with a
{cpp:enum}`B_GET_PROPERTY` request for the "Suites" property:

	message.what = B_GET_PROPERTY;
	message.AddSpecifier("Suites");

	// ... add remaining specifiers here ...

	messenger.SendMessage(&message, &reply);

The target object responds with a {cpp:enum}`B_REPLY` {cpp:class}`BMessage` with the following
fields:

- The error code in `error`.
- An array named `suites` containing the names of the suites supported by the object.
- An array named `messages` containing flattened {cpp:class}`BPropertyInfo` objects describing the
  supported messages and specifiers for the various supported suites.

Less usefully, you can send a {cpp:enum}`B_GET_SUPPORTED_SUITES` {cpp:class}`BMessage` directly to
an object and obtain its supported suites in an identically-formed reply.

Every scriptable object supports the "suite/vn.Be-handler" suite by dint of its
{cpp:class}`BHandler` heritage. This suite is sometimes referred to as the "universal suite." It
performs the following functions:

- Implements the "Suites" property and responds to {cpp:enum}`B_GET_SUPPORTED_SUITES` messages, as
  described above.
- Implements the "Messenger" property, allowing the caller to obtain a {cpp:class}`BMessenger` to
  the object, simplifying further communication with the object.
- Implements the "InternalName" property, returning the name of the {cpp:class}`BHandler`.
- Responds to any other scripting requests with a {cpp:enum}`B_MESSAGE_NOT_UNDERSTOOD`
  {cpp:class}`BMessage`. This is a "catch-all" response after all the other objects in the hierarchy
  have rejected the scripting request.

---

# Making Objects Scriptable

Since scripting messages are passed via {cpp:class}`BMessenger`s, objects accepting scripting
messages must be derived from {cpp:class}`BHandler`. Typically, adding scripting support entails
little more than overriding the following methods:

- {cpp:func}`BHandler::ResolveSpecifier()` directs the scripting message to the appropriate
  {cpp:class}`BHandler`.
- {cpp:func}`BHandler::MessageReceived()` implements the scripting requests.
- {cpp:func}`BHandler::GetSupportedSuites()` publishes the supported scripting suites.

See the documentation of these functions in the {cpp:class}`BHandler` class for details.
