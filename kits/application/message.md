:::{cpp:class} BMessage
:::

# BMessage

## Data Members

::::{abi-group}
:::{cpp:member} public uint32 what
:::

A coded constant that captures what the message is about.
::::

## Constructor and Destructor

::::{abi-group}
:::{cpp:function} BMessage::BMessage(uint32 command)
:::

:::{cpp:function} BMessage::BMessage(const BMessage& message)
:::

:::{cpp:function} BMessage::BMessage()
:::

Creates a new {hclass}`BMessage` object that has the given
{hparam}`command` constant, or that's a copy of another {hclass}`BMessage`.
If it's a copy, the new object contains the same command constant and data
fields as {hparam}`message`.

See also: {cpp:func}`BLooper::DetachCurrentMessage`
::::

::::{abi-group}
:::{cpp:function} virtual BMessage::~BMessage()
:::

Frees all memory allocated to hold message data. If the message sender is
expecting a reply but hasn't received one, a default reply (with
{cpp:enumerator}`B_NO_REPLY` as the {hparam}`what` data member) is sent
before the message is destroyed.

The system retains ownership of the messages it delivers to you. Each
message loop routinely deletes delivered {hclass}`BMessage`s after the
application is finished responding to them.
::::

## Member Functions

::::{abi-group}
:::{cpp:function} status_t BMessage::AddData(const char* name, type_code type, const void* data, ssize_t numBytes, bool fixedSize = true, int32 numItems = 1)
:::

:::{cpp:function} status_t BMessage::AddBool(const char* name, bool aBool)
:::

:::{cpp:function} status_t BMessage::AddInt8(const char* name, int8 anInt8)
:::

:::{cpp:function} status_t BMessage::AddInt16(const char* name, int16 anInt16)
:::

:::{cpp:function} status_t BMessage::AddInt32(const char* name, int32 anInt32)
:::

:::{cpp:function} status_t BMessage::AddInt64(const char* name, int64 anInt64)
:::

:::{cpp:function} status_t BMessage::AddFloat(const char* name, float aFloat)
:::

:::{cpp:function} status_t BMessage::AddDouble(const char* name, double aDouble)
:::

:::{cpp:function} status_t BMessage::AddString(const char* name, const char* string)
:::

:::{cpp:function} status_t BMessage::AddString(const char* name, const BString string)
:::

:::{cpp:function} status_t BMessage::AddPoint(const char* name, BPoint point)
:::

:::{cpp:function} status_t BMessage::AddRect(const char* name, BRect rect)
:::

:::{cpp:function} status_t BMessage::AddRef(const char* name, const entry_ref* ref)
:::

:::{cpp:function} status_t BMessage::AddMessage(const char* name, const BMessage* message)
:::

:::{cpp:function} status_t BMessage::AddMessenger(const char* name, BMessenger messenger)
:::

:::{cpp:function} status_t BMessage::AddPointer(const char* name, const void* pointer)
:::

:::{cpp:function} status_t BMessage::AddFlat(const char* name, BFlattenable* object, int32 numItems = 1)
:::

These functions add data to the field named {hparam}`name` and assign a
data type to the field. Field names can be no longer than 255 characters.
If more than one item of data is added under the same name, the
{hclass}`BMessage` creates an array of data for that name. Each time you
add another value (to the same name), the value is added to the end of the
array—you can't add a value at a specific index. A given field can only
store one type of data.

{hmethod}`AddData()` copies {hparam}`numBytes` of {hparam}`data` into the
field, and assigns the data a {hparam}`type` code. It copies whatever the
{hparam}`data` pointer points to. For example, if you want to add a string
of characters to the message, {hparam}`data` should be the string pointer
({htype}`char *`). If you want to add only the string pointer, not the
characters themselves, {hparam}`data` should be a pointer to the pointer
({htype}`char **`). The assigned {hparam}`type` must be a specific data
type; it should not be {cpp:enumerator}`B_ANY_TYPE`.

When you call {hmethod}`AddData()` to place the first item in an array
under a new name, you can provide it with two arguments,
{hparam}`fixedSize` and {hparam}`numItems`, that will improve the object's
efficiency. If the {hparam}`fixedSize` flag is {cpp:expr}`true`, each item
in the array must have the same number of bytes; if the flag is
{cpp:expr}`false`, items can vary in size. {hparam}`numItems` tells the
object to pre-allocate storage for some number of items. This isn't a
limit, you can add more than {hparam}`numItems` to the field.

Most of the other functions are variants of {hmethod}`AddData()` that
hard-code the field's type. For example, {hmethod}`AddFloat()` assigns the
type {cpp:enumerator}`B_FLOAT_TYPE`; {hmethod}`AddBool()` assigns
{cpp:enumerator}`B_BOOL_TYPE`, and so on.

{hmethod}`AddString()`, like {hmethod}`AddData()`, takes a pointer to the
data it adds, or you can use a {cpp:class}`BString` object. The
{hparam}`string` must be null-terminated; the null character is counted and
copied into the message. Similarly, {hmethod}`AddRef()` adds the pointed to
{htype}`entry_ref` structure to the message (and the variable-length name
that's one of the elements of the structure); {hmethod}`AddMessage()` adds
one {hclass}`BMessage` to another.

The other functions are simply passed the data directly. For example,
{hmethod}`AddInt32()` takes an {htype}`int32` or {htype}`uint32` and
{hmethod}`AddMessenger()` takes a {cpp:class}`BMessenger` object, whereas
{hmethod}`AddData()` would be passed a pointer to an {htype}`int32` and a
pointer to a {cpp:class}`BMessenger`. {hmethod}`AddPointer()` adds only the
pointer it's passed, not the data it points to. To accomplish the same
thing, {hmethod}`AddData()` would take a pointer to the pointer. (The
pointer will be valid only locally; it won't be useful to a remote
destination.)

{hmethod}`AddFlat()` flattens an {hparam}`object` (by calling its
{hmethod}`Flatten()` function) and adds the flat data to the message. It
calls the object's {cpp:func}`TypeCode() <BFlattenable::TypeCode>` function
to learn the type code it should associate with the data. Objects that are
added through {hmethod}`AddFlat()` must inherit from
{cpp:class}`BFlattenable` (defined in the {ref}`Support Kit`).

You can also provide a {hparam}`numItems` hint to {hmethod}`AddFlat()`
when you call it to set up a new array. {hmethod}`AddFlat()` calls the
object's {cpp:func}`IsFixedSize() <BFlattenable::IsFixedSize>` function to
discover whether all items in the array will be the same size.

These functions return {cpp:enumerator}`B_ERROR` if the data is too
massive to be added to the message, {cpp:enumerator}`B_BAD_TYPE` if the
data can't be added to an existing array because it's the wrong type,
{cpp:enumerator}`B_NO_MEMORY` if the {hclass}`BMessage` can't get enough
memory to hold the data, and {cpp:enumerator}`B_BAD_VALUE` if the proposed
{hparam}`name` for the data is longer than 255 bytes. If all goes well,
they return {cpp:enumerator}`B_OK`.

There's no limit on the number of named fields a message can contain or on
the size of a field's data. However, since the search is linear, combing
through a very long list of names to find a particular piece of data may be
inefficient. Also, because of the amount of data that must be moved, an
extremely large message can slow the delivery mechanism. It's sometimes
better to put some of the information in a common location (a file, a
private clipboard, a shared area of memory) and just refer to it in the
message.

See also: {cpp:func}`FindData() <BMessage::FindData>`,
{cpp:func}`GetInfo() <BMessage::GetInfo>`
::::

::::{abi-group}
:::{cpp:function} status_t BMessage::AddSpecifier(const BMessage* message)
:::

:::{cpp:function} status_t BMessage::AddSpecifier(const char* property)
:::

:::{cpp:function} status_t BMessage::AddSpecifier(const char* property, int32 index)
:::

:::{cpp:function} status_t BMessage::AddSpecifier(const char* property, int32 index, int32 range)
:::

:::{cpp:function} status_t BMessage::AddSpecifier(const char* property, const char* name)
:::

Adds a specifier to the specifier stack. There are several variations of
this method. The first adds the specifier {hparam}`message` to the
specifier stack. The other methods add a specifier targeting the property
{hparam}`property`, with specifier constants
{cpp:enumerator}`B_DIRECT_SPECIFIER`, {cpp:enumerator}`B_INDEX_SPECIFIER`,
{cpp:enumerator}`B_RANGE_SPECIFIER`, and
{cpp:enumerator}`B_NAME_SPECIFIER`, respectively. For all other specifiers,
you must construct the specifier separately and then call
{hmethod}`AddSpecifier()` on the message. For more information about
specifiers, see the "Scripting" section near the beginning of this chapter.

Specifiers are stored in a data array named "specifiers". However, since
{hmethod}`AddSpecifier()` also sets the notion of the current specifier,
specifiers should always be added to a scripting message with this method
rather than with {cpp:func}`AddMessage() <BMessage::AddData>`.

{hmethod}`AddSpecifier()` returns {cpp:enumerator}`B_OK` if it's able to
add the specifier to the {hclass}`BMessage` and an error code, generally
only {cpp:enumerator}`B_NO_MEMORY` to indicate that it has run out of
memory, if not.

See also: {cpp:func}`GetCurrentSpecifier()
<BMessage::GetCurrentSpecifier>`, {cpp:func}`HasSpecifiers()
<BMessage::HasSpecifiers>`, {cpp:func}`PopSpecifier()
<BMessage::PopSpecifier>`
::::

::::{abi-group}
:::{cpp:function} int32 BMessage::CountNames(type_code type) const
:::

Returns the number of named data fields in the {hclass}`BMessage` that
store data of the specified {hparam}`type`. An array of information held
under a single name counts as one field; each name is counted only once, no
matter how many data items are stored under that name.

If {hparam}`type` is {cpp:enumerator}`B_ANY_TYPE`, this function counts
all named fields. If {hparam}`type` is a specific type, it counts only
fields that store data registered as that type.

See also: {cpp:func}`GetInfo() <BMessage::GetInfo>`
::::

::::{abi-group}
:::{cpp:function} status_t BMessage::FindData(const char* name, type_code type, int32 index, const void** data, ssize_t* numBytes) const
:::

:::{cpp:function} status_t BMessage::FindData(const char* name, type_code type, const void** data, ssize_t* numBytes) const
:::

:::{cpp:function} status_t BMessage::FindBool(const char* name, int32 index, bool* aBool) const
:::

:::{cpp:function} status_t BMessage::FindBool(const char* name, bool* aBool) const
:::

:::{cpp:function} status_t BMessage::FindInt8(const char* name, int32 index, int8* anInt8) const
:::

:::{cpp:function} status_t BMessage::FindInt8(const char* name, int8* anInt8) const
:::

:::{cpp:function} status_t BMessage::FindInt16(const char* name, int32 index, int16* anInt16) const
:::

:::{cpp:function} status_t BMessage::FindInt16(const char* name, int16* anInt16) const
:::

:::{cpp:function} status_t BMessage::FindInt32(const char* name, int32 index, int32* anInt32) const
:::

:::{cpp:function} status_t BMessage::FindInt32(const char* name, int32* anInt32) const
:::

:::{cpp:function} status_t BMessage::FindInt64(const char* name, int32 index, int64* anInt64) const
:::

:::{cpp:function} status_t BMessage::FindInt64(const char* name, int64* anInt64) const
:::

:::{cpp:function} status_t BMessage::FindFloat(const char* name, int32 index, float* aFloat) const
:::

:::{cpp:function} status_t BMessage::FindFloat(const char* name, float* aFloat) const
:::

:::{cpp:function} status_t BMessage::FindDouble(const char* name, int32 index, double* aDouble) const
:::

:::{cpp:function} status_t BMessage::FindDouble(const char* name, double* aDouble) const
:::

:::{cpp:function} status_t BMessage::FindString(const char* name, int32 index, const char** string) const
:::

:::{cpp:function} status_t BMessage::FindString(const char* name, const char** string) const
:::

:::{cpp:function} status_t BMessage::FindString(const char* name, int32 index, BString* string) const
:::

:::{cpp:function} status_t BMessage::FindString(const char* name, BString* string) const
:::

:::{cpp:function} status_t BMessage::FindPoint(const char* name, int32 index, BPoint* point) const
:::

:::{cpp:function} status_t BMessage::FindPoint(const char* name, BPoint* point) const
:::

:::{cpp:function} status_t BMessage::FindRect(const char* name, int32 index, BRect* rect) const
:::

:::{cpp:function} status_t BMessage::FindRect(const char* name, BRect* rect) const
:::

:::{cpp:function} status_t BMessage::FindRef(const char* name, int32 index, entry_ref* ref) const
:::

:::{cpp:function} status_t BMessage::FindRef(const char* name, entry_ref* ref) const
:::

:::{cpp:function} status_t BMessage::FindMessage(const char* name, int32 index, BMessage* message) const
:::

:::{cpp:function} status_t BMessage::FindMessage(const char* name, BMessage* message) const
:::

:::{cpp:function} status_t BMessage::FindMessenger(const char* name, int32 index, BMessenger* messenger) const
:::

:::{cpp:function} status_t BMessage::FindMessenger(const char* name, BMessenger* messenger) const
:::

:::{cpp:function} status_t BMessage::FindPointer(const char* name, int32 index, void** pointer) const
:::

:::{cpp:function} status_t BMessage::FindPointer(const char* name, void** pointer) const
:::

:::{cpp:function} status_t BMessage::FindFlat(const char* name, int32 index, BFlattenable* object) const
:::

:::{cpp:function} status_t BMessage::FindFlat(const char* name, BFlattenable* object) const
:::

These functions retrieve data from the {hclass}`BMessage`. Each looks for
data stored under the specified {hparam}`name`. If more than one data item
has the same name, an {hparam}`index` can be provided to tell the function
which item in the {hparam}`name` array it should find. Indices begin at 0.
If an {hparam}`index` isn't provided, the function will find the first, or
only, item in the array.

:::{admonition} Important
:class: important
In all cases except {hmethod}`FindData()` and {hmethod}`FindString()`, the
data that's retrieved from the {hclass}`BMessage` is copied into the
reference argument; the caller is responsible for freeing the copied data.
For {hmethod}`FindData()` and the non-{cpp:class}`BString` version of
{hmethod}`FindString()`, a pointer to the data is returned; the
{hclass}`BMessage` retains ownership of the actual data and will delete the
data when the object itself is deleted.
:::

{hmethod}`FindData()` places, in {hparam}`*data`, a pointer to the
requested data item. The size of the item in bytes is written to
{hparam}`numBytes`. If {hparam}`type` is {cpp:enumerator}`B_ANY_TYPE`, it
provides a pointer to the data no matter what type it actually is. But if
{hparam}`type` is a specific data type, it provides the pointer only if the
{hparam}`name` field holds data of that particular type.

The other functions are specialized versions of {hmethod}`FindData()`.
They match the corresponding {cpp:func}`Add…() <BMessage::AddData>` methods
and search for named data of a particular type, as described below:

:::{list-table}
---
header-rows: 1
align: left
widths: auto
---
-
	- Function

	- Finds data

	- Registered as type

-
	- {hmethod}`FindBool()`

	- a {htype}`bool`

	- {cpp:enumerator}`B_BOOL_TYPE`

-
	- {hmethod}`FindInt8()`

	- an {htype}`int8` or {htype}`uint8`

	- {cpp:enumerator}`B_INT8_TYPE`

-
	- {hmethod}`FindInt16()`

	- an {htype}`int16` or {htype}`uint16`

	- {cpp:enumerator}`B_INT16_TYPE`

-
	- {hmethod}`FindInt32()`

	- an {htype}`int32` or {htype}`uint32`

	- {cpp:enumerator}`B_INT32_TYPE`

-
	- {hmethod}`FindInt64()`

	- an {htype}`int64` or {htype}`uint64`

	- {cpp:enumerator}`B_INT64_TYPE`

-
	- {hmethod}`FindFloat()`

	- a {htype}`float`

	- {cpp:enumerator}`B_FLOAT_TYPE`

-
	- {hmethod}`FindDouble()`

	- a {htype}`double`

	- {cpp:enumerator}`B_DOUBLE_TYPE`

-
	- {hmethod}`FindString()`

	- a character string

	- {cpp:enumerator}`B_STRING_TYPE`

-
	- {hmethod}`FindPoint()`

	- a {cpp:class}`BPoint` object

	- {cpp:enumerator}`B_POINT_TYPE`

-
	- {hmethod}`FindRect()`

	- a {cpp:class}`BRect` object

	- {cpp:enumerator}`B_RECT_TYPE`

-
	- {hmethod}`FindRef()`

	- an {htype}`entry_ref`

	- {cpp:enumerator}`B_REF_TYPE`

-
	- {hmethod}`FindMessage()`

	- a {hclass}`BMessage` object

	- {cpp:enumerator}`B_MESSAGE_TYPE`

-
	- {hmethod}`FindMessenger()`

	- a {cpp:class}`BMessenger` object

	- {cpp:enumerator}`B_MESSENGER_TYPE`

-
	- {hmethod}`FindPointer()`

	- a pointer to anything

	- {cpp:enumerator}`B_POINTER_TYPE`


:::

The other type-specific functions retrieve the requested data item from
the message by copying it to the variable referred to by the last argument;
you get the data, not just a pointer to it. For example,
{hmethod}`FindMessenger()` assigns the {cpp:class}`BMessenger` it finds in
the message to the {hparam}`messenger` object, whereas
{hmethod}`FindData()` would provide only a pointer to a
{cpp:class}`BMessenger`. {hmethod}`FindPointer()` puts the found pointer in
the {htype}`void*` variable that {hparam}`pointer` refers to;
{hmethod}`FindData()`, as illustrated above, would provide a pointer to the
pointer. (If the message was delivered from a remote source, pointers
retrieved from the message won't be valid.)

{hmethod}`FindRef()` retrieves an {htype}`entry_ref` structure; the data
that's used to reconstitute the structure may have been added as an
{htype}`entry_ref` (through {hmethod}`AddRef()`), or as a flattened
{cpp:class}`BPath` object ({hmethod}`AddFlat()`).

{hmethod}`FindFlat()` assigns the object stored in the {hclass}`BMessage`
to the {hparam}`object` passed as an argument, it calls the
{hparam}`object`'s {cpp:func}`Unflatten() <BMessage::Unflatten>` function
and passes it the flat data from the message, provided that the two objects
have compatible types. The argument object's {hmethod}`AllowsTypeCode()`
function must return {cpp:expr}`true` when tested with the type code stored
in the message; if not, {hmethod}`FindFlat()` fails and returns
{cpp:enumerator}`B_BAD_VALUE`.

If these functions can't find any data associated with {hparam}`name`,
they return a {cpp:enumerator}`B_NAME_NOT_FOUND` error. If they can't find
{hparam}`name` data of the requested {hparam}`type` (or the type the
function returns), they return {cpp:enumerator}`B_BAD_TYPE`. If the
{hparam}`index` is out of range, they return {cpp:enumerator}`B_BAD_INDEX`.
You can rely on the values they retrieve only if they return
{cpp:enumerator}`B_OK` and the data was correctly recorded when it was
added to the message.

When they fail, {hmethod}`FindData()` and {hmethod}`FindString()` provide
{cpp:expr}`NULL` pointers. {hmethod}`FindRect()` hands you an invalid
rectangle and {hmethod}`FindMessenger()` an invalid
{cpp:class}`BMessenger`. Most of the other functions set the data values to
0, which may be indistinguishable from valid values.

Finding a data item doesn't remove it from the {hclass}`BMessage`.

(Several functions, such as {hmethod}`FindRect()` and
{hmethod}`FindInt32()`, have versions that return the found value directly.
These versions don't report errors and may not be supported in the future.)

See also: {cpp:func}`GetInfo() <BMessage::GetInfo>`, {cpp:func}`AddData()
<BMessage::AddData>`
::::

::::{abi-group}
:::{cpp:function} status_t BMessage::Flatten(BDataIO* object, ssize_t* numBytes = NULL) const
:::

:::{cpp:function} status_t BMessage::Flatten(char* address, ssize_t numBytes = NULL) const
:::

:::{cpp:function} status_t BMessage::Unflatten(BDataIO* object)
:::

:::{cpp:function} status_t BMessage::Unflatten(const char* address)
:::

:::{cpp:function} ssize_t BMessage::FlattenedSize() const
:::

These functions write the {hclass}`BMessage` and the data it contains to a
"flat" (untyped) buffer of bytes, and reconstruct a {hclass}`BMessage`
object from such a buffer.

If passed a {cpp:class}`BDataIO` {hparam}`object` (including a
{cpp:class}`BFile`), {hmethod}`Flatten()` calls the object's
{hmethod}`Write()` function to write the message data. If passed the
{hparam}`address` of a buffer, it begins writing at the start of the
buffer. {hmethod}`FlattenedSize()` returns the number of bytes you must
provide in the buffer to hold the flattened object. {hmethod}`Flatten()`
places the number of bytes actually written in the variable that its
{hparam}`numBytes` argument refers to.

{hmethod}`Unflatten()` empties the {hclass}`BMessage` of any information
it may happen to contain, then initializes the object from data read from
the buffer. If passed a {cpp:class}`BDataIO` {hparam}`object`, it calls the
object's {hmethod}`Read()` function to read the message data. If passed a
buffer {hparam}`address`, it begins reading at the start of the buffer.
It's up to the caller to make sure that {hmethod}`Unflatten()` reads data
that {hmethod}`Flatten()` wrote and that pointers are positioned correctly.

{hmethod}`Flatten()` returns any errors encountered when writing the data,
or {cpp:enumerator}`B_OK` if there is no error.

If it doesn't recognize the data in the buffer as being a flattened object
or there's a failure in reading the data, {hmethod}`Unflatten()` returns
{cpp:enumerator}`B_BAD_VALUE`. If it doesn't have adequate memory to
recreate the whole message, it returns {cpp:enumerator}`B_NO_MEMORY`.
Otherwise, it returns {cpp:enumerator}`B_OK`.

See also: the {cpp:class}`BDataIO` class in the {ref}`Support Kit`
::::

::::{abi-group}
:::{cpp:function} status_t BMessage::GetCurrentSpecifier(int32* index, BMessage* specifier = NULL, int32* what = NULL, const char** property = NULL) const
:::

:::{cpp:function} status_t BMessage::PopSpecifier()
:::

{hmethod}`GetCurrentSpecifier()` unpacks the current specifier in the
{hclass}`BMessage`, the one at the top of the specifier stack;
{hmethod}`PopSpecifier()` changes the notion of which specifier is current,
by popping the current one from the stack.

These functions aid in implementing a class-specific version of
{cpp:class}`BHandler`'s {cpp:func}`ResolveSpecifier()
<BHandler::ResolveSpecifier>` function—the first gets the specifier that
needs to be resolved, and the second pops it from the stack after it is
resolved. You can also call them to examine relevant specifiers when
handling a message that targets an object property (such as
{cpp:enumerator}`B_GET_PROPERTY`).

A scripting {hclass}`BMessage` keeps specifiers in a data array named
"specifiers"; each specifier is itself a {hclass}`BMessage`, but one with a
special structure and purpose in the scripting system. See the "Scripting"
section near the beginning of this chapter for an overview of the system
and the place of specifiers in it.

The specifiers in a message are ordered and, until
{hmethod}`PopSpecifier()` is called, the one that was added last, the one
with the greatest index, is the current specifier.
{hmethod}`PopSpecifier()` merely decrements the index that picks the
current specifier; it doesn't delete anything from the {hclass}`BMessage`.

{hmethod}`GetCurrentSpecifier()` puts the index of the current specifier
in the variable that its first argument, {hparam}`index`, refers to. If
other arguments are provided, it makes the {hparam}`specifier`
{hclass}`BMessage` a copy of the current specifier. It also extracts two
pieces of information from the {hparam}`specifier`: It places the
{hparam}`what` data member of the specifier in the {hparam}`what` variable
and a pointer to the property name in the {hparam}`property` variable.
These last two output arguments won't be valid if the {hparam}`specifier`
argument is {cpp:expr}`NULL`.

Both functions fail if the {hclass}`BMessage` doesn't contain specifiers.
In addition, {hmethod}`GetCurrentSpecifier()` fails if it can't find data
in the {hclass}`BMessage` for its {hparam}`specifier` and
{hparam}`property` arguments, and {hmethod}`PopSpecifier()` fails if the
{hclass}`BMessage` isn't one that has been delivered to you after being
processed through a message loop. When it fails,
{hmethod}`GetCurrentSpecifier()` returns
{cpp:enumerator}`B_BAD_SCRIPT_SYNTAX`, but {hmethod}`PopSpecifier()`
returns {cpp:enumerator}`B_BAD_VALUE`. On success, both functions return
{cpp:enumerator}`B_OK`.

See also: {cpp:func}`AddSpecifier() <BMessage::AddSpecifier>`,
{cpp:func}`HasSpecifiers() <BMessage::HasSpecifiers>`,
{cpp:func}`BHandler::ResolveSpecifier`
::::

::::{abi-group}
:::{cpp:function} status_t BMessage::GetInfo(const char* name, type_code* typeFound, int32* countFound = NULL) const
:::

:::{cpp:function} status_t BMessage::GetInfo(const char* name, type_code* typeFound, bool* fixedSize) const
:::

:::{cpp:function} status_t BMessage::GetInfo(type_code type, int32 index, char** nameFound, type_code* typeFound, int32* countFound = NULL) const
:::

Provides information about the data fields stored in the
{hclass}`BMessage`.

When passed a {hparam}`name` that matches a name within the
{hclass}`BMessage`, {hmethod}`GetInfo()` places the type code for data
stored under that name in the variable referred to by {hparam}`typeFound`
and writes the number of data items with that name into the variable
referred to by {hparam}`countFound`. It then returns
{cpp:enumerator}`B_OK`. If it can't find a {hparam}`name` field within the
{hclass}`BMessage`, it sets the {hparam}`countFound` variable to 0, and
returns {cpp:enumerator}`B_NAME_NOT_FOUND` (without modifying the
{hparam}`typeFound` variable).

When the {hparam}`fixedSize` argument is specified, the bool referenced by
{hparam}`fixedSize` is set to {cpp:expr}`true` if all items in the array
specified by {hparam}`name` must be the same size, and {cpp:expr}`false` if
the items can be of different sizes (see {cpp:func}`AddData()
<BMessage::AddData>`).

When passed a {hparam}`type` and an {hparam}`index`, {hmethod}`GetInfo()`
looks only at fields that store data of the requested {hparam}`type` and
provides information about the field at the requested {hparam}`index`.
Indices begin at 0 and are type specific. For example, if the requested
{hparam}`type` is {cpp:enumerator}`B_DOUBLE_TYPE` and the
{hclass}`BMessage` contains a total of three named fields that store double
data, the first field would be at index 0, the second at 1, and the third
at 2, no matter what other types of data actually separate them in the
{hclass}`BMessage`, and no matter how many data items each field contains.
(Note that the {hparam}`index` in this case ranges over fields, each with a
different name, not over the data items within a particular named field.)
If the requested type is {cpp:enumerator}`B_ANY_TYPE`, this function looks
at all fields and gets information about the one at {hparam}`index`
whatever its type.

If successful in finding data of the {hparam}`type` requested at
{hparam}`index`, {hmethod}`GetInfo()` returns {cpp:enumerator}`B_OK` and
provides information about the data through the last three arguments:

-   It places a pointer to the name of the data field in the variable referred
to by {hparam}`nameFound`.

-   It puts the code for the type of data the field contains in the variable
referred to by {hparam}`typeFound`. This will be the same as the
{hparam}`type` requested, unless the requested type is
{cpp:enumerator}`B_ANY_TYPE`, in which case {hparam}`typeFound` will be the
actual type stored under the name.

-   It records the number of data items stored within the field in the
variable referred to by {hparam}`countFound`.

If {hmethod}`GetInfo()` can't find data of the requested {hparam}`type` at
{hparam}`index`, it sets the {hparam}`countFound` variable to 0, and
returns {cpp:enumerator}`B_BAD_TYPE`. If the index is out of range, it
returns {cpp:enumerator}`B_BAD_INDEX`.

This version of {hmethod}`GetInfo()` can be used to iterate through all
the {hclass}`BMessage`'s data. For example:

:::{code} cpp
char *name;
uint32 type;
int32 count;

for ( int32 i = 0;
      msg->GetInfo(B_ANY_TYPE, i, &name, &type, &count) == B_OK;
      i++ ) {
   . . .
}
:::

If the index is incremented from 0 in this way, all data of the requested
type will have been read when {hmethod}`GetInfo()` returns
{cpp:enumerator}`B_NAME_NOT_FOUND`. If the requested type is
{cpp:enumerator}`B_ANY_TYPE`, as shown above, it will reveal the name and
type of every field in the {hclass}`BMessage`.

See also: {cpp:func}`AddData() <BMessage::AddData>`, {cpp:func}`FindData()
<BMessage::FindData>`
::::

::::{abi-group}
:::{cpp:function} bool BMessage::HasSpecifiers() const
:::

Returns {cpp:expr}`true` if the {hclass}`BMessage` has specifiers added by
an {cpp:func}`AddSpecifier() <BMessage::AddSpecifier>` function, and
{cpp:expr}`false` if not.

See also: {cpp:func}`AddSpecifier() <BMessage::AddSpecifier>`,
{cpp:func}`GetCurrentSpecifier() <BMessage::GetCurrentSpecifier>`
::::

::::{abi-group}
:::{cpp:function} bool BMessage::IsSystem() const
:::

Returns {cpp:expr}`true` if the {hparam}`what` data member of the
{hclass}`BMessage` object identifies it as a system-defined message, and
{cpp:expr}`false` if not.
::::

::::{abi-group}
:::{cpp:function} status_t BMessage::MakeEmpty()
:::

:::{cpp:function} bool BMessage::IsEmpty() const
:::

{hmethod}`MakeEmpty()` removes and frees all data that has been added to
the {hclass}`BMessage`, without altering the {hparam}`what` constant. It
returns {cpp:enumerator}`B_OK`, unless the message can't be altered (as it
can't if it's being dragged), in which case it returns
{cpp:enumerator}`B_ERROR`.

{hmethod}`IsEmpty` returns {cpp:expr}`true` if the {hclass}`BMessage` has
no data (whether or not it was emptied by {hmethod}`MakeEmpty()`), and
{cpp:expr}`false` if it has some.

See also: {cpp:func}`RemoveName() <BMessage::RemoveName>`
::::

::::{abi-group}
:::{cpp:function} void BMessage::PrintToStream() const
:::

Prints information about the {hclass}`BMessage` to the standard output
stream (stdout). Each field of named data is reported in the following
format,

:::{code} sh
#entry name, type = type, count = count
:::

where _name_ is the name that the data is registered under, _type_ is the
constant that indicates what type of data it is, and _count_ is the number
of data items in the named array.
::::

::::{abi-group}
:::{cpp:function} status_t BMessage::RemoveName(const char* name)
:::

:::{cpp:function} status_t BMessage::RemoveData(const char* name, int32 index = 0)
:::

{hmethod}`RemoveName()` removes all data entered in the {hclass}`BMessage`
under {hparam}`name` and the name itself. {hmethod}`RemoveData()` removes
the single item of data at {hparam}`index` in the {hparam}`name` array. If
the array has just one data item, it removes the array and {hparam}`name`
just as {hmethod}`RemoveName()` would.

Both functions free the memory that was allocated to hold the data, and
return {cpp:enumerator}`B_OK` when successful. However, if there's no data
in the {hclass}`BMessage` under {hparam}`name`, they return a
{cpp:enumerator}`B_NAME_NOT_FOUND` error. If message data can be read but
can't be changed (as it can't for a message that's being dragged), they
both return {cpp:enumerator}`B_ERROR`. If the {hparam}`index` is out of
range, {hmethod}`RemoveData()` returns {cpp:enumerator}`B_BAD_INDEX` (the
index is too high) or {cpp:enumerator}`B_BAD_VALUE` (the value passed is a
negative number).

See also: {cpp:func}`MakeEmpty() <BMessage::MakeEmpty>`
::::

::::{abi-group}
:::{cpp:function} status_t BMessage::ReplaceData(const char* name, type_code type, const void* data, ssize_t numBytes)
:::

:::{cpp:function} status_t BMessage::ReplaceData(const char* name, type_code type, int32 index, const void* data, ssize_t numBytes)
:::

:::{cpp:function} status_t BMessage::ReplaceBool(const char* name, bool aBool)
:::

:::{cpp:function} status_t BMessage::ReplaceBool(const char* name, int32 index, bool aBool)
:::

:::{cpp:function} status_t BMessage::ReplaceInt8(const char* name, int8 anInt8)
:::

:::{cpp:function} status_t BMessage::ReplaceInt8(const char* name, int32 index, int8 anInt8)
:::

:::{cpp:function} status_t BMessage::ReplaceInt16(const char* name, int16 anInt16)
:::

:::{cpp:function} status_t BMessage::ReplaceInt16(const char* name, int32 index, int16 anInt16)
:::

:::{cpp:function} status_t BMessage::ReplaceInt32(const char* name, int32 anInt32)
:::

:::{cpp:function} status_t BMessage::ReplaceInt32(const char* name, int32 index, int32 anInt32)
:::

:::{cpp:function} status_t BMessage::ReplaceInt64(const char* name, int64 anInt64)
:::

:::{cpp:function} status_t BMessage::ReplaceInt64(const char* name, int32 index, int64 anInt64)
:::

:::{cpp:function} status_t BMessage::ReplaceFloat(const char* name, float aFloat)
:::

:::{cpp:function} status_t BMessage::ReplaceFloat(const char* name, int32 index, float aFloat)
:::

:::{cpp:function} status_t BMessage::ReplaceDouble(const char* name, double aDouble)
:::

:::{cpp:function} status_t BMessage::ReplaceDouble(const char* name, int32 index, double aDouble)
:::

:::{cpp:function} status_t BMessage::ReplaceString(const char* name, const char* aString)
:::

:::{cpp:function} status_t BMessage::ReplaceString(const char* name, int32 index, const char* aString)
:::

:::{cpp:function} status_t BMessage::ReplaceString(const char* name, BString& aString)
:::

:::{cpp:function} status_t BMessage::ReplaceString(const char* name, int32 index, BString& aString)
:::

:::{cpp:function} status_t BMessage::ReplacePoint(const char* name, BPoint point)
:::

:::{cpp:function} status_t BMessage::ReplacePoint(const char* name, int32 index, BPoint point)
:::

:::{cpp:function} status_t BMessage::ReplaceRect(const char* name, BRect rect)
:::

:::{cpp:function} status_t BMessage::ReplaceRect(const char* name, int32 index, BRect rect)
:::

:::{cpp:function} status_t BMessage::ReplaceRef(const char* name, entry_ref* ref)
:::

:::{cpp:function} status_t BMessage::ReplaceRef(const char* name, int32 index, entry_ref* ref)
:::

:::{cpp:function} status_t BMessage::ReplaceMessage(const char* name, BMessage* message)
:::

:::{cpp:function} status_t BMessage::ReplaceMessage(const char* name, int32 index, BMessage* message)
:::

:::{cpp:function} status_t BMessage::ReplaceMessenger(const char* name, BMessenger messenger)
:::

:::{cpp:function} status_t BMessage::ReplaceMessenger(const char* name, int32 index, BMessenger messenger)
:::

:::{cpp:function} status_t BMessage::ReplacePointer(const char* name, const void* pointer)
:::

:::{cpp:function} status_t BMessage::ReplacePointer(const char* name, int32 index, const void* pointer)
:::

:::{cpp:function} status_t BMessage::ReplaceFlat(const char* name, BFlattenable* object)
:::

:::{cpp:function} status_t BMessage::ReplaceFlat(const char* name, int32 index, BFlattenable* object)
:::

These functions replace a data item in the {hparam}`name` field with
another item passed as an argument. If an {hparam}`index` is provided, they
replace the item in the {hparam}`name` array at that index; if an
{hparam}`index` isn't mentioned, they replace the first (or only) item
stored under {hparam}`name`. If an {hparam}`index` is provided but it's out
of range, the replacement fails.

{hmethod}`ReplaceData()` replaces an item in the {hparam}`name` field with
{hparam}`numBytes` of data, but only if the {hparam}`type` code that's
specified for the data matches the type of data that's already stored in
the field. The {hparam}`type` must be specific; it can't be
{cpp:enumerator}`B_ANY_TYPE`.

{hmethod}`FindFlat()` replaces a flattened object with another
{hparam}`object`, provided that the type reported by the argument
{hparam}`object` (by its {cpp:func}`TypeCode() <BFlattenable::TypeCode>`
function) matches the type recorded for the item in the message. If not, it
returns {cpp:enumerator}`B_BAD_VALUE`.

The other functions are simplified versions of {hmethod}`ReplaceData()`.
They each handle the specific type of data declared for their last
arguments. They succeed if this {hparam}`type` matches the type of data
already in the {hparam}`name` field, and fail if it does not. The new data
is added precisely as the counterpart {cpp:func}`Add…()
<BMessage::AddData>` function would add it.

If successful, all these functions return {cpp:enumerator}`B_OK`. If
unsuccessful, they return an error code{cpp:enumerator}`B_ERROR` if the
message is read-only (as it is while the message is being dragged),
{cpp:enumerator}`B_BAD_INDEX` if the {hparam}`index` is out of range,
{cpp:enumerator}`B_NAME_NOT_FOUND` if the {hparam}`name` field doesn't
exist, or {cpp:enumerator}`B_BAD_TYPE` if the field doesn't contain data of
the specified type.

See also: {cpp:func}`AddData() <BMessage::AddData>`
::::

::::{abi-group}
:::{cpp:function} BMessenger BMessage::ReturnAddress()
:::

Returns a {cpp:class}`BMessenger` object that can be used to reply to the
{hclass}`BMessage`. Calling the {cpp:class}`BMessenger`'s
{cpp:func}`SendMessage() <BMessenger::SendMessage>` function is equivalent
to calling {cpp:func}`SendReply() <BMessage::SendReply>`, except that the
return message won't be marked as a reply. If a reply isn't allowed (if the
{hclass}`BMessage` wasn't delivered), the returned {cpp:class}`BMessenger`
will be invalid.

If you want to use the {hmethod}`ReturnAddress()` {cpp:class}`BMessenger`
to send a synchronous reply, you must do so before the {hclass}`BMessage`
is deleted and a default reply is sent.

See also: {cpp:func}`SendReply() <BMessage::SendReply>`,
{cpp:func}`WasDelivered() <BMessage::WasDelivered>`
::::

::::{abi-group}
:::{cpp:function} status_t BMessage::SendReply(BMessage* message, BMessage* reply, bigtime_t sendTimeout = B_INFINITE_TIMEOUT, bigtime_t replyTimeout = B_INFINITE_TIMEOUT)
:::

:::{cpp:function} status_t BMessage::SendReply(BMessage* message, BHandler* replyHandler = NULL, bigtime_t sendTimeout = B_INFINITE_TIMEOUT)
:::

:::{cpp:function} status_t BMessage::SendReply(uint32 command, BMessage* reply)
:::

:::{cpp:function} status_t BMessage::SendReply(uint32 command, BHandler* replyHandler = NULL)
:::

Sends a reply {hparam}`message` back to the sender of the
{hclass}`BMessage` (in the case of a synchronous reply) or to a target
{cpp:class}`BHandler` (in the case of an asynchronous reply). Whether the
reply is synchronous or asynchronous depends on how the {hclass}`BMessage`
that's sending the reply was itself sent:

-   The reply is delivered synchronously if the message sender is waiting for
one to arrive. The function that sent the {hclass}`BMessage` doesn't return
until it receives the reply (or a timeout expires). If an expected reply
has not been sent by the time the {hclass}`BMessage` object is deleted, a
default {cpp:enumerator}`B_NO_REPLY` message is returned to the sender. If
a reply is sent after the sender gave up waiting for it to arrive, the
reply {hparam}`message` disappears into the bowels of the system.

-   The reply is delivered asynchronously if the message sender isn't waiting
for a reply. In this case, the sending function designates a target
{cpp:class}`BHandler` and {cpp:class}`BLooper` for any replies that might
be sent, then returns immediately after putting the {hclass}`BMessage` in
the pipeline. Posted messages and messages that are dragged and dropped are
also eligible for asynchronous replies.

{hmethod}`SendReply()` works only for {hclass}`BMessage` objects that have
been processed through a message loop and delivered to you. The caller
retains ownership of the reply {hparam}`message` passed to
{hmethod}`SendReply()`; it can be deleted (or left to die on the stack)
after the function returns.

{hmethod}`SendReply()` sends a message—a reply message, to be sure, but a
message nonetheless. It behaves exactly like the other message-sending
function, {cpp:class}`BMessenger`'s {cpp:func}`SendMessage()
<BMessenger::SendMessage>`:

-   By passing it a {hparam}`reply` argument, you can ask for a synchronous
reply to the reply message it sends. It won't return until it receives the
reply.

-   By supplying a {hparam}`replyHandler` argument, you can arrange for an
expected asynchronous reply. If a specific target isn't specified, the
{cpp:class}`BApplication` object will handle the reply if one is sent.

By default, {hmethod}`SendReply()` doesn't return until the reply message
is delivered (placed in the {cpp:class}`BLooper`'s port queue). It's
possible, in some circumstances, for the receiving port queue to be full,
in which case {hmethod}`SendReply()` will block until a slot becomes free.
However, you can limit how long {hmethod}`SendReply()` will wait to deliver
the message before it gives up and returns. The {hparam}`sendTimeout`
argument is the number of microseconds you give the function to do its
work. If the time limit is exceeded, the function fails and returns an
error ({cpp:enumerator}`B_TIMED_OUT`).

When asking for a synchronous reply, separate {hparam}`sendTimeout` and
{hparam}`replyTimeout` limits can be set for sending the message and
receiving the reply. There is no time limit if a timeout value is set to
{cpp:enumerator}`B_INFINITE_TIMEOUT`—as it is by default. The function
won't block at all if the timeout is set to 0.

If a {hparam}`command` is passed rather than a {hparam}`message`,
{hmethod}`SendReply()` constructs the reply {hclass}`BMessage`, initializes
its {hparam}`what` data member with the {hparam}`command` constant, and
sends it just like any other reply. The {hparam}`command` versions of this
function have infinite timeouts; they block until the message is delivered
and, if requested, a synchronous reply is received.

This function returns {cpp:enumerator}`B_OK` if the reply is successfully
sent. If there's a problem in sending the message, it returns the same sort
of error code as {cpp:class}`BMessenger`'s {cpp:func}`SendMessage()
<BMessenger::SendMessage>`. It may also report a reply-specific problem.
The more informative return values are as follows:

:::{list-table}
---
header-rows: 1
align: left
widths: auto
---
-
	- Constant

	- Description

-
	- {cpp:enumerator}`B_BAD_REPLY`
	- Attempting to reply to a message that hasn't been delivered yet
-
	- {cpp:enumerator}`B_DUPLICATE_REPLY`
	- Sending a reply after one has already been sent and delivered.
-
	- {cpp:enumerator}`B_BAD_THREAD_ID`
	- Sending a reply to a destination thread that no longer exists.
-
	- {cpp:enumerator}`B_BAD_PORT_ID`
	- Sending a reply to a {cpp:class}`BLooper` and port that no longer exist.
-
	- {cpp:enumerator}`B_TIMED_OUT`
	- Taking longer than the specified time limit to deliver a reply message or
		to receive a synchronous reply to the reply.

:::

If you want to delay sending a reply and keep the {hclass}`BMessage`
object beyond the time it's scheduled to be deleted, you may be able to
detach it from the message loop. See {cpp:func}`DetachCurrentMessage()
<BLooper::DetachCurrentMessage>` in the {cpp:class}`BLooper` class.

See also: {cpp:func}`BMessenger::SendMessage`,
{cpp:func}`BLooper::DetachCurrentMessage`, {cpp:func}`ReturnAddress()
<BMessage::ReturnAddress>`
::::

::::{abi-group}
:::{cpp:function} bool BMessage::WasDelivered() const
:::

:::{cpp:function} bool BMessage::IsSourceRemote() const
:::

:::{cpp:function} bool BMessage::IsSourceWaiting() const
:::

:::{cpp:function} bool BMessage::IsReply() const
:::

:::{cpp:function} const BMessage* BMessage::Previous() const
:::

These functions can help if you're engaged in an exchange of messages or
managing an ongoing communication.

{hmethod}`WasDelivered()` indicates whether it's possible to send a reply
to a message. It returns {cpp:expr}`true` for a {hclass}`BMessage` that was
posted, sent, or dropped – that is, one that has been processed through a
message loop—and {cpp:expr}`false` for a message that has not yet been
delivered by any means.

{hmethod}`IsSourceRemote()` returns {cpp:expr}`true` if the message had
its source in another application, and {cpp:expr}`false` if the source is
local or the message hasn't been delivered yet.

{hmethod}`IsSourceWaiting()` returns {cpp:expr}`true` if the message
source is waiting for a synchronous reply, and {cpp:expr}`false` if not.
The source thread can request and wait for a reply when calling either
{cpp:class}`BMessenger`'s {cpp:func}`SendMessage()
<BMessenger::SendMessage>` or {hclass}`BMessage`'s {cpp:func}`SendReply()
<BMessage::SendReply>` function.

{hmethod}`IsReply()` returns {cpp:expr}`true` if the {hclass}`BMessage` is
a reply to a previous message (if it was sent by the {cpp:func}`SendReply()
<BMessage::SendReply>` function), and {cpp:expr}`false` if not.

{hmethod}`Previous()` returns the previous message – the message to which
the current {hclass}`BMessage` is a reply. It works only for a
{hclass}`BMessage` that's received as an asynchronous reply to a previous
message. A synchronous reply is received in the context of the previous
message, so it's not necessary to call a function to get it. But when an
asynchronous reply is received, the context of the original message is
lost; this function can provide it. {hmethod}`Previous()` returns
{cpp:expr}`NULL` if the {hclass}`BMessage` isn't an asynchronous reply to
another message.

See also: {cpp:func}`BMessenger::SendMessage`, {cpp:func}`SendReply()
<BMessage::SendReply>`, {cpp:func}`ReturnAddress()
<BMessage::ReturnAddress>`
::::

::::{abi-group}
:::{cpp:function} bool BMessage::WasDropped() const
:::

:::{cpp:function} BPoint BMessage::DropPoint(BPoint* offset = NULL) const
:::

{hmethod}`WasDropped()` returns {cpp:expr}`true` if the user delivered the
{hclass}`BMessage` by dragging and dropping it, and {cpp:expr}`false` if
the message was posted or sent in application code or if it hasn't yet been
delivered at all.

{hmethod}`DropPoint()` reports the point where the cursor was located when
the message was dropped (when the user released the mouse button). It
directly returns the point in the screen coordinate system and, if an
{hparam}`offset` argument is provided, returns it by reference in
coordinates based on the image or rectangle the user dragged. The
{hparam}`offset` assumes a coordinate system with (0.0, 0.0) at the left
top corner of the dragged rectangle or image.

Since any value can be a valid coordinate, {hmethod}`DropPoint()` produces
reliable results only if {hmethod}`WasDropped()` returns {cpp:expr}`true`.

See also: {cpp:func}`BView::DragMessage`
::::

## Operators

::::{abi-group}
:::{cpp:function} BMessage BMessage::operator=(const BMessage&)
:::

Assigns one {hclass}`BMessage` object to another. After the assignment,
the two objects are duplicates of each other without shared data.
::::

::::{abi-group}
:::{cpp:function} void* BMessage::operator new(size_t numBytes)
:::

Allocates memory for a {hclass}`BMessage` object, or takes the memory from
a previously allocated cache. The caching mechanism is an efficient way of
managing memory for objects that are created frequently and used for short
periods of time, as {hclass}`BMessage`s typically are.
::::

::::{abi-group}
:::{cpp:function} void BMessage::operator delete(void* memory, size_t numBytes)
:::

Frees memory allocated by the {hclass}`BMessage` version of
{hmethod}`new`, which may mean restoring the memory to the cache.
::::

## Constants

### Message Specifiers

:::{code} c
B_NO_SPECIFIER
B_DIRECT_SPECIFIER
B_INDEX_SPECIFIER
B_REVERSE_INDEX_SPECIFIER
B_RANGE_SPECIFIER
B_REVERSE_RANGE_SPECIFIER
B_NAME_SPECIFIER
B_ID_SPECIFIER
B_SPECIFIERS_END = 128
:::

These constants fill the {hparam}`what` slot of specifier
{hclass}`BMessage`s. Each constant indicates what other information the
specifer contains and how it should be interpreted. For example, a
{cpp:enumerator}`B_REVERSE_INDEX_SPECIFIER` message has an {hparam}`index`
field with an index that counts backwards from the end of a list. A
{cpp:enumerator}`B_NAME_SPECIFIER` message includes a {hparam}`name` field
that names the requested item.

See Also: {cpp:func}`AddSpecifier() <BMessage::AddSpecifier>`, the
{ref}`Scripting` chapter.
