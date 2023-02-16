# BMessage

A {cpp:class}`BMessage` is a bundle of structured information. Every
{cpp:class}`BMessage` contains a command constant and some number of data
fields.

-   The command constant is an {htype}`int32` value that describes, roughly,
the purpose of the {cpp:class}`BMessage`. It's stored as the public
{hparam}`what` data member. You always set and examine the {hparam}`what`
value directly, you don't need to call a function. (As a convenience, you
can set the command constant when you create your {cpp:class}`BMessage`
object.)

-   The data fields are name-type-value triplets. A field is be primarily
identified by name, but you can look for fields by name, type, or a
combination of the two. The type is encoded as a constant
({cpp:enumerator}`B_INT32_TYPE`, {cpp:enumerator}`B_STRING_TYPE` etc), and
is meant to describe the type of value that the field holds. A single field
can have only one name and one type, but can contain an array of values.
Individual values in a field are accessible by index.

Neither the command constant nor the data fields are mandatory. You can
create a {cpp:class}`BMessage` that has data but no command, or that _only_
has a command. However, creating a {cpp:class}`BMessage` that has neither
is pointless.

## Preparatory Reading

{cpp:class}`BMessage`s are used throughout the kits to send data (or
notifications) to another threadpossibly in another application. To
understand how {cpp:class}`BMessage`s fit into the messaging system, see
"{ref}`Messaging`".

The {cpp:class}`BMessage` class also contributes a number of functions
that help define the scripting system. See "{ref}`Scripting`" for an
introduction to this system.

{cpp:class}`BMessage`s are also used by a number of classes
({cpp:class}`BClipboard`, {cpp:class}`BArchivable`, and others) for their
ability to store data.

## Types of Functions

The {cpp:class}`BMessage` class defines five types of functions:

Data field functions.

: These functions either set or retrieve the value of a data field. See
{cpp:func}`AddData() <BMessage::AddData>`, {cpp:func}`FindData()
<BMessage::FindData>`, {cpp:func}`ReplaceData() <BMessage::ReplaceData>`,
and {cpp:func}`RemoveName() <BMessage::RemoveName>`.

Info functions.

: These functions retrieve information about the state and contents of the
{cpp:class}`BMessage`. See {cpp:func}`IsSystem() <BMessage::IsSystem>` and
{cpp:func}`GetInfo() <BMessage::GetInfo>`.

Messaging functions.

: These functions are part of the messaging system. A smaller set of
functions reports on the status of a received message. For example,
{cpp:func}`IsSourceWaiting() <BMessage::IsSourceWaiting>` tells whether the
message sender is waiting for a reply, {cpp:func}`WasDropped()
<BMessage::WasDropped>` says whether it was dragged and dropped, and
{cpp:func}`DropPoint() <BMessage::DropPoint>` says where it was dropped.

Scripting functions.

: Functions such as {cpp:func}`AddSpecifier() <BMessage::AddSpecifier>` and
{cpp:func}`PopSpecifier() <BMessage::PopSpecifier>`.

Flattening functions.

: The data in a {cpp:class}`BMessage` can be flattened into an untyped
stream of bytes. See {cpp:func}`Flatten() <BMessage::Flatten>`.

## BMessage Ownership

The documentation for the functions that accept or pass back a
{cpp:class}`BMessage` object should tell you who's responsible for deleting
the object. Most functions that accept a {cpp:class}`BMessage` argument
copy the object, leaving the caller with the responsibility for deleting
the argument. The exceptions i.e. {cpp:class}`BMessage`-accepting functions
that take over ownership of the object are listed below:

Functions that return a {cpp:class}`BMessage` to you usually don't give up
ownership; in general, you don't delete the {cpp:class}`BMessage`s that are
passed to you. The exceptions, functions that expect the caller to take
over ownership of a passed-back {cpp:class}`BMessage`,are listed below:
