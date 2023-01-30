# BMessage

## Data Members

::::{abi-group}
:::{cpp:member} uint32 BMessage::what
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

Creates a new `BMessage` object that has the given `command` constant, or that's a copy of another
`BMessage`. If it's a copy, the new object contains the same command constant and data fields as
`message`.

See also: {cpp:func}`BLooper::DetachCurrentMessage()`.
::::

::::{abi-group}
:::{cpp:function} virtual BMessage::~BMessage()
:::

Frees all memory allocated to hold message data. If the message sender is expecting a reply but
hasn't received one, a default reply (with {cpp:enum}`B_NO_REPLY` as the `what` data member) is sent
before the message is destroyed.

The system retains ownership of the messages it delivers to you. Each message loop routinely deletes
delivered `BMessage`s after the application is finished responding to them.
::::

## Member Functions

::::{abi-group}

:::{cpp:function} status_t BMessage::AddData(const char* name, type_code type, const void* data, ssize_t numBytes, bool fixedSize = true, int32 numItems = 1)
:::
:::{cpp:function} status_t BMessage::BMessage::AddBool(const char* name, bool data)
:::
:::{cpp:function} status_t BMessage::AddInt8(const char* name, int8 data)
:::
:::{cpp:function} status_t BMessage::AddInt16(const char* name, int16 data)
:::
:::{cpp:function} status_t BMessage::AddInt32(const char* name, int32 data)
:::
:::{cpp:function} status_t BMessage::AddInt64(const char* name, int64 data)
:::
:::{cpp:function} status_t BMessage::AddFloat(const char* name, float data)
:::
:::{cpp:function} status_t BMessage::AddDouble(const char* name, double data)
:::
:::{cpp:function} status_t BMessage::AddString(const char* name, const char *string)
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

These functions add data to the field named `name` and assign a data type to the field. Field names
can be no longer than 255 characters. If more than one item of data is added under the same name,
the `BMessage` creates an array of data for that name. Each time you add another value (to the same
name), the value is added to the end of the array---you can't add a value at a specific index. A
given field can only store one type of data.

`AddData()` copies `numBytes` of `data` into the field, and assigns the data a `type` code. It
copies whatever the `data` pointer points to. For example, if you want to add a string of characters
to the message, `data` should be the string pointer (`char*`). If you want to add only the string
pointer, not the characters themselves, `data` should be a pointer to the pointer (`char**`). The
assigned `type` must be a specific data type; it should not be {cpp:enum}`B_ANY_TYPE`.

When you call `AddData()` to place the first item in an array under a new name, you can provide it
with two arguments, `fixedSize` and `numItems`, that will improve the object's efficiency. If the
`fixedSize` flag is {cpp:expr}`true`, each item in the array must have the same number of bytes; if
the flag is {cpp:expr}`false`, items can vary in size. `numItems` tells the object to pre-allocate
storage for some number of items. This isn't a limit, you can add more than `numItems` to the field.

Most of the other functions are variants of `AddData()` that hard-code the field's type. For
example, `AddFloat()` assigns the type {cpp:enum}`B_FLOAT_TYPE`; `AddBool()` assigns
{cpp:enum}`B_BOOL_TYPE`, and so on.

`AddString()`, like `AddData()`, takes a pointer to the data it adds, or you can use a
{cpp:class}`BString` object. The `string` must be null-terminated; the null character is counted and
copied into the message. Similarly, `AddRef()` adds the pointed to `entry_ref` structure to the
message (and the variable-length name that's one of the elements of the structure); `AddMessage()`
adds one `BMessage` to another.

The other functions are simply passed the data directly. For example, `AddInt32()` takes an int32 or
uint32 and `AddMessenger()` takes a {cpp:class}`BMessenger` object, whereas `AddData()` would be
passed a pointer to an int32 and a pointer to a {cpp:class}`BMessenger`. `AddPointer()` adds only
the pointer it's passed, not the data it points to. To accomplish the same thing, `AddData()` would
take a pointer to the pointer. (The pointer will be valid only locally; it won't be useful to a
remote destination.)

`AddFlat()` flattens an `object` (by calling its `Flatten()` function) and adds the flat data to the
message. It calls the object's {cpp:func}`~BFlattenable::TypeCode()` function to learn the type code
it should associated with the data. Objects that are added through `AddFlat()` must inherit from
{cpp:class}`BFlattenable` (defined in the "Support Kit").

You can also provide a `numItems` hint to `AddFlat()` when you call it to set up a new array.
`AddFlat()` calls the object's {cpp:func}`~BFlattenable::IsFixedSize()` function to discover whether
all items in the array will be the same size.

The functions return a {cpp:enum}`B_ERROR` if the data is too massive to be added to the message,
{cpp:enum}`B_BAD_TYPE` if the data can't be added to an existing array because it's the wrong type,
{cpp:enum}`B_NO_MEMORY` if the `BMessage` can't get enough memory to hold the data, and
{cpp:enum}`B_BAD_VALUE` if the proposed `name` for the data is longer than 255 bytes. If all goes
well, they return {cpp:enum}`B_OK`.

There's no limit on the number of named fields a message can contain, or on the size a field's data.
However, since the serach is linear, combing through a very long list of names to find a particular
piece of data my be inefficient. Also, because of the amount of data that must be moved, an
extremely large message can slow the delivery mechanism. It's sometimes better to put some of the
information in a common location (a file, a private clipboard, a shared area of memory) and just
refer to it in the message.

See also: {cpp:func}`~BMessage::FindData()`, {cpp:func}`~BMessage::GetInfo()`
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

Adds a specifier to the specifier stack. There are several variations of this method. The first adds
the specifier `message` to the specifier stack. The other methods add a specifier targeting the
property `property`, which specifier constants {cpp:enum}`B_DIRECT_SPECIFIER`,
{cpp:enum}`B_INDEX_SPECIFIER`, {cpp:enum}`B_RANGE_SPECIFIER`, and {cpp:enum}`B_NAME_SPECIFIER`. For
all other specifiers, you must construct the specifier separately and then call `AddSpecifier()` on
the message. For more information about specifiers, see the "Scripting" section near the beginning
of this chapter.

Specifiers are stored in a data array named "specifiers". However, since `AddSpecifier()` also sets
the notion of the current specifier, specifiers should always be added to a scripting message with
this method rather than with {cpp:func}`~BMessage::AddMessage()`.

`AddSpecifier()` returns {cpp:enum}`B_OK` if it's able to add the specifier to the `BMessage` and an
error code, generally only {cpp:enum}`B_NO_MEMORY` to indicate that it has run out of memory, if
not.

See also: {cpp:func}`~BMessage::GetCurrentSpecifier()`, {cpp:func}`~BMessage::HasSpecifiers()`,
{cpp:func}`~BMessage::PopSpecifier()`.
::::

::::{abi-group}
:::{cpp:function} int32 BMessage::CountNames(type_code type) const
:::

Returns the number of named data fields in the `BMessage` that store data of the specified `type`.
An array of information held under a single name counts as one field; each name is counted only
once, no matter how many data items are stored under that name.

If `type` is {cpp:enum}`B_ANY_TYPE`, this function counts all named fields. If `type` is a specific
type, it counts only fields that store data registered as that type.

See also: {cpp:func}`~BMessage::GetInfo()`.
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

These functions retrieve data from the `BMessage`. Each looks for data stored under the specified
`name`. If more than one data item has the same name, an `index` can be provided to tell the
function which item in the `name` array it should find. Indices begin at 0. If an `index` isn't
provided, the function will find the first, or only, item in the array.

:::{admonition} Important
:class: warning
In all cases except `FindData()` and `FindString()`, the data that's retrieved from the `BMessage`
is copied into the reference argument; the caller is responsible for freeing the copied data. For
`FindData()` and the non-{cpp:class}`BString` version of `FindString()`, a pointer to the data is
returned; the `BMessage` retains ownership of the actual data and will delete the data when the
object itself is deleted.
:::

`FindData()` places, in `*data`, a pointer to the requested data item. The size of the item in bytes
is written to `numBytes`. If `type` is {cpp:enum}`B_ANY_TYPE`, it provides a pointer to the data no
matter what type it actually is. But if `type` is a specific data type, it provides the pointer only
if the `name` field holds data of that particular type.

The other functions are specialized versions of `FindData()`. They match the corresponding Add...()
methods and search for named data of a particular type, as described below:

:::{list-table}
---
header-rows: 1
align: left
---
-
    - Function
    - Finds data
    - Registered as type
-
    - `FindBool()`
    - a bool
    - {cpp:enum}`B_BOOL_TYPE`
-
    - `FindInt8()`
    - an int8 or uint8
    - {cpp:enum}`B_INT8_TYPE`
-
    - `FindInt16()`
    - an int16 or uint16
    - {cpp:enum}`B_INT16_TYPE`
-
    - `FindInt32()`
    - an int32 or uint32
    - {cpp:enum}`B_INT32_TYPE`
-
    - `FindInt64()`
    - an int64 or uint64
    - {cpp:enum}`B_INT64_TYPE`
-
    - `FindFloat()`
    - a float
    - {cpp:enum}`B_FLOAT_TYPE`
-
    - `FindDouble()`
    - a double
    - {cpp:enum}`B_DOUBLE_TYPE`
-
    - `FindString()`
    - a character string
    - {cpp:enum}`B_STRING_TYPE`
-
    - `FindPoint()`
    - a {cpp:class}`BPoint` object
    - {cpp:enum}`B_POINT_TYPE`
-
    - `FindRect()`
    - a {cpp:class}`BRect` object
    - {cpp:enum}`B_RECT_TYPE`
-
    - `FindRef()`
    - an `entry_ref`
    - {cpp:enum}`B_REF_TYPE`
-
    - `FindMessage()`
    - a {cpp:class}`BMessage` object
    - {cpp:enum}`B_MESSGE_TYPE`
-
    - `FindMessenger()`
    - a {cpp:class}`BMessenger` object
    - {cpp:enum}`B_MESSENGER_TYPE`
-
    - `FindPointer()`
    - a pointer to anything
    - {cpp:enum}`B_POINTER_TYPE`
:::

The other type-specific functions retrieve the requested data item from the message by copying it to
the variable referred to by the last argument; you get the data, not just a pointer to it. For
example, `FindMessenger()` assigns the {cpp:class}`BMessenger` it finds in the message to the
`messenger` object, whereas `FindData()` would provide only a pointer to a {cpp:class}`BMessenger`.
`FindPointer()` puts the found pointer in the `void*` variable that `pointer` refers to;
`FindData()`, as ilustrated above, would provide a pointer to the pointer. (If the message was
delivered from a remote source, pointers retrieved from the message won't be valid.)

`FindRef()` retrieves an `entry_ref` structure; the data that's used to reconstitute the structure
may have been added as an `entry_ref` (through `AddRef()`), or as a flattened {cpp:class}`BPath`
object (`AddFlat()`).

`FindFlat()` assigns the object stored in the `BMessage` to the `object` passed as an argument, it
calls the `object`'s {cpp:func}`~BMessage::Unflatten()` function and passes it the flat data from
the message, provided that the two objects have compatible types. The argument object's
`AllowTypeCode()` function must return {cpp:enum}`true` when tested with the type code stored in the
message; if not, `FindFlat()` fails and returns {cpp:enum}`B_BAD_VALUE`.

If these functions can't find any data associated with `name`, they return a
{cpp:enum}`B_NAME_NOT_FOUND` error. If they can't find `name` data of the requested `type` (or the
type the function returns), they return {cpp:enum}`B_BAD_TYPE`. If the `index` is out of range, they
return {cpp:enum}`B_BAD_INDEX`. You can rely on the values they retrieve only if they return
{cpp:enum}`B_OK` and the data was correctly recorded when it was added to the message.

When they fail, `FindData()` and `FindString()` provide {cpp:enum}`NULL` pointers. `FindRect()`
hands you an invalid rectangle and `FindMessenger()` and invalid {cpp:class}`BMessenger`. Most of
the other functions set the data values to 0, which may be indistinguishable from valid values.

Find a data item doesn't remove it from the `BMessage`.

(Several functions, such as `FindRect()` and `FindInt32`, have versions that return the found value
directly. These versions don't report errors and may not be supported in the future.)

See also: {cpp:func}`~BMessage::GetInfo()`, {cpp:func}`~BMessage::AddData()`.
::::

::::{abi-group}
:::{cpp:function} status_t BMessage::Flatten(BDataIO* object, ssize_t* numBytes = NULL) const
:::
:::{cpp:function} status_t BMessage::Flatten(char* address, ssize_t* numBytes = NULL) const
:::
:::{cpp:function} status_t BMessage::Unflatten(BDataIO* object)
:::
:::{cpp:function} status_t BMessage::Unflatten(const char* address)
:::
:::{cpp:function} ssize_t BMessage::FlattenedSize() const
:::

These functions write the `BMessage` and the data in contains to a "flat" (untyped) buffer of bytes,
and reconstruct a `BMessage` object from such a buffer.

If a passed {cpp:class}`BDataIO` `object` (including a {cpp:class}`BFile`), `Flatten()` calls the
object's `Write()` function to write the message data. If passed the `address` of a buffer, it
begins writing at the start of the buffer. `FlattenedSize()` returns the number of bytes you must
provide in the buffer to hold the flattened object. `Flatten()` places the number of bytes actually
written in the variable that its `numBytes` argument refers to.

`Unflatten()` empties the `BMessage` of any information it may happen to contain, then initializes
the object from data read from the buffer. If passed a {cpp:class}`BDataIO` object, it calls the
object's `Read()` function to read the message data. If passed a buffer `address`, it begins reading
at the start of the buffer. It's up to the caller to make sure than `Unflatten()` reads data that
`Flatten()` wrote and that pointers are positioned correctly.

`Flatten()` returns any errors encountered when writing the data, of {cpp:enum}`B_OK` if there is no
error.

If it doesn't recognize the data in the buffer as being a flattened object or there's a failure in
reading the data, `Unflatten()` returns {cpp:enum}`B_BAD_VALUE`. If it doesn't have adequate memory
to recreate the whole message, it returns {cpp:enum}`B_NO_MEMORY`. Otherwise, it returns
{cpp:enum}`B_OK`.

See also: the {cpp:class}`BDataIO` class in the "Support Kit".
::::

::::{abi-group}
:::{cpp:function} status_t BMessage::GetCurrentSpecifier(int32* index, BMessage* specifier = NULL, int32* what = NULL, const char** property = NULL) const
:::
:::{cpp:function} status_t BMessage::PopSpecifier()
:::

`GetCurrentSpecifier()` unpacks the current specifier in the `BMessage`, the one at the top of the
specifier stack; `PopSpecifer()` changes the notion of which specifier is current, by popping the
current one from the stack.

These functions aid in implementing a class-specific version of {cpp:class}`BHandler`'s
{cpp:func}`~BHandler::ResolveSpecifier()` function---the first gets the specifier that needs to be
resolved, and the second pops it from the stack after it is resolved. You can also call them to
examine relevent specifiers when handling a message that targets an object property (such as
{cpp:enum}`B_GET_PROPERTY`).

A scripting `BMessage` keeps specifiers in a data array named "specifiers"; each specifier is itself
a `BMessage`, but one with a special structure and purpose in the scripting system. See the
"Scripting" section near the beginning of this chapter for an overview of the system and the place
of specifiers in it.

The specifiers in a message are ordered and, until `PopSpecifier()` is called, the one that was
added last, the one with the greatest index, is the current specifier. `PopSpecifier()` merely
decrements the index that picks the current specifier; it doesn't delete anything from the
`BMessage`.

`GetCurrentSpecifier()` puts the index of the current specifier in the variable that its first
argument, `index`, refers to. If other arguments are provided, it makes the `specifier` `BMessage` a
copy of the current specifier. It also extracts two pieces of information from the `specifier`. If
places the `what` data member of the specifier in the `what` variable and a pointer to the property
name in the `property` variable. These last two output arguments won't be valid if the `specifier`
argument is {cpp:enum}`NULL`.

Both functions fail if the {hclass}`BMessage` doesn't contain specifiers. In addition,
{hmethod}`GetCurrentSpecifier()` fails if it can't find data in the {hclass}`BMessage` for its
{hparameter}`specifier` and {hparameter}`property` arguments, and {hmethod}`PopSpecifier()` fails if
the {hclass}`BMessage` isn't one that has been delivered to you after being processed through a
message loop. When it fails, {hmethod}`GetCurrentSpecifier()` returns
{cpp:enum}`B_BAD_SCRIPT_SYNTAX`, but {hmethod}`PopSpecifier()` returns {cpp:enum}`B_BAD_VALUE`. On
success, both functions return {cpp:enum}`B_OK`.

See also: {cpp:func}`~BMessage::AddSpecifier()`, {cpp:func}`~BMessage:HasSpecifier()`,
{cpp:func}`BHandler::ResolveSpecifier()`.
::::

::::{abi-group}
:::{cpp:function} status_t BMessage::GetInfo(const char* name, type_code* typeFound, int32* countFound = NULL) const
:::
:::{cpp:function} status_t BMessage::GetInfo(const char* name, type_code* typeFound, bool* fixedSize) const
:::
:::{cpp:function} status_t BMessage::GetInfo(type_code type, int32 index, char** nameFound, type_code* typeFound, int32* countFound = NULL) const
:::

Provides information about the data fields stored in the {hclass}`BMessage`.

When passed a {hparameter}`name` that matches a name withing the {hclass}`BMessage`,
{hmethod}`GetInfo()` places the type code for data stored under that name in the variable referred
to by {hparameter}`typeFound` and writes the number of data items with that name into the variable
referred to by {hparameter}`countFound`. It then returns {cpp:enum}`B_OK`. If it can't find a
{hparameter}`name` field within the {hclass}`BMessage`, it sets the {hparameter}`countFound` variable to
0, and returns {cpp:enum}`B_NAME_NOT_FOUND` (without modifying the {hparameter}`typeFound` variable).

When the {hparameter}`fixedSize` argument is specified, the bool referenced by {hparameter}`fixedSize`
is set to {cpp:enum}`true` if all items in the array specified by {hparameter}`name` must be the same
size, and {cpp:enum}`false` if the items can be of different sizes (see
{cpp:func}`~BMessage::AddData()`).

When passed a {hparameter}`type` and an {hparameter}`index`, {hmethod}`GetInfo()` looks only at fields
that store data of the requested {hparameter}`type` and provides information about the field at the
requested {hparameter}`index`. Indices begin at 0 and are type specific. For example, if the requested
{hparameter}`type` is {cpp:enum}`B_DOUBLE_TYPE` and the {hclass}`BMessage` contains a total of three
named fields that store double data, the first field would be at index 0, the second at 1, and the
third at 2, no matter what other types of data actually separate them in the {hclass}`BMessage`, and
no matter how many data items each field contains. (Note that the {hparameter}`index` in this cases
ranges over fields, each with a different name, not over the data items within a particular named
field.) If the requested type is {cpp:enum}`B_ANY_TYPE`, this function looks at all fields and gets
information about the one at {hparameter}`index` whatever its type.

If successful in finding data of the {hparameter}`type` requested at {hparameter}`index`,
{hmethod}`GetInfo()` returns {cpp:enum}`B_OK` and provides information about the data through the
last three arguments:

- It places a pointer to the name of the data field in the variable referred to by
  {hparameter}`nameFound`.

- It puts the code for the type of data the field contains in the variable referred to by
  {hparameter}`typeFound`. This will be the same as the {hparameter}`type` requested, unless the
  requested type is {cpp:enum}`B_ANY_TYPE`, in which case {hparameter}`typeFound` will be the actual
  type stored under the name.

- It records the number of data items stored within the field in the variable referred to by
  {hparameter}`countFound`.

If {hmethod}`GetInfo()` can't find data of the requested {hparameter}`type` at {hparameter}`index`, it
sets the {hparameter}`countFound` variable to 0, and returns {cpp:enum}`B_BAD_TYPE`. If the index is
out of range, it returns {cpp:enum}`B_BAD_INDEX`.

This version of {hmethod}`GetInfo()` can be used to iterate through all the {hclass}`BMessage`'s
data. For example:

:::{code} cpp
char *name;
uint32 type;
int32 count;

for (int32 i = 0; msg->GetInfo(B_ANY_TYPE, i, &name, &type, &count) == B_OK; ++i)
{
    // . . .
}
:::

If the index is incremented from 0 in this way, all data of the requested type will have been read
when {hmethod}`GetInfo()` returns {cpp:enum}`B_NAME_NOT_FOUND`. If the requested type is
{cpp:enum}`B_ANY_TYPE`, as shown above, it will reveal the name and type of every field in the
{hclass}`BMessage`.

See also: {cpp:func}`~BMessage::AddData()`, {cpp:func}`~BMessage::FindData()`.
::::

::::{abi-group}
:::{cpp:function} bool BMessage::HasSpecifiers() const
:::

Returns {cpp:enum}`true` if the {hclass}`BMessage` has specifiers added by
{cpp:func}`~BMessage::AddSpecifier()` function, and {cpp:enum}`false` if not.

See also: {cpp:func}`~BMessage::AddSpecifier()`, {cpp:func}`~BMessage::GetCurrentSpecifier()`.
::::

::::{abi-group}
:::{cpp:function} bool BMessage::IsSystem() const
:::

Returns {cpp:enum}`true` if the {hfield}`what` data member of the {hclass}`BMessage` object
identifies it as a system-defined message, and {cpp:enum}`false` if not.
::::

::::{abi-group}
:::{cpp:function} status_t BMessage::MakeEmpty()
:::
:::{cpp:function} bool BMessage::IsEmpty() const
:::

{hmethod}`MakeEmpty()` removes and frees all data that has been added to the {hclass}`BMessage`,
without altering the {hfield}`what` constant. It returns {cpp:enum}`B_OK`, unless the message can't
be altered (as it can't if it's being dragged), in which case it returns {cpp:enum}`B_ERROR`.

{hmethod}`IsEmpty()` returns {cpp:enum}`true` if the {hclass}`BMessage` has no data (whether or not
is was emptied by {hmethod}`MakeEmpty()`), and {cpp:enum}`false` if it has some.

See also: {cpp:func}`~BMessage::RemoveName()`
::::

::::{abi-group}
:::{cpp:function} void BMessage::PrintToStream() const
:::

Prints information about the {hclass}`BMessage` to the standard output stream (stdout). Each field
of named data is reported in the following format,

<div class='highlight'><pre>
#entry <em>name</em>, type = <em>type</em>, count = <em>count</em>
</pre></div>

where _name_ is the name that the data is registered under, _type_ is the constant that indicates
what type of data it is, and _count_ is the number of data items in the named array.
::::

::::{abi-group}
:::{cpp:function} status_t BMessage::RemoveName(const char* name)
:::
:::{cpp:function} status_t BMessage::RemoveData(const char* name, int32 index = 0)
:::

{hmethod}`RemoveName()` removes all data entered in the {hclass}`BMessage` under {hparameter}`name`
and the name itself. {hmethod}`RemoveData()` removes the single item of data at {hparameter}`index`
in the {hparameter}`name` array. If the array has just one data item, it removes the array and
{hparameter}`name` just as {hmethod}`RemoveName()` would.

Both functions free the memory that was allocated to hold the data, and return {cpp:enum}`B_OK` when
successful. However, if there's no data in the {hclass}`BMessage` under {hparameter}`name`, they
return a {cpp:enum}`B_NAME_NOT_FOUND` error. If message data can be read but can't be changed (as it
can't for a message that's being dragged), they both return {cpp:enum}`B_ERROR`. If the
{hparameter}`index` is out of range, {hmethod}`RemoveData()` returns {cpp:enum}`B_BAD_INDEX` (the
index is too high), or {cpp:enum}`B_BAD_VALUE` (the value passed is a negative number).

See also: {cpp:func}`~BMessage::MakeEmpty()`.
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

These functions replace a data item in the {hparameter}`name` field with another item passed as an
argument. If an {hparameter}`index` is provided, they replace the item in the {hparameter}`name`
array at that index; if an {hparameter}`index` isn't mentioned, they replace the first (or only)
item stored under {hparameter}`name`. If an {hparameter}`index` is provided but it's out of range,
the replacement fails.

{hmethod}`ReplaceData()` replaces an item in the {hparameter}`name` field with
{hparameter}`numBytes` of data, but only if the {hparameter}`type` code that's specified for the
data matches the type of data that's already stored in the field. The {hparameter}`type` must be
specific; it can't be {cpp:enum}`B_ANY_TYPE`.

{hmethod}`ReplaceFlat()` replaces a flattened object with another {hparameter}`object`, provided
that the type reported by the argument {hparameter}`object` (by its
{cpp:func}`~BFlattenable::TypeCode()` function) matches the type recorded for the item in the
message. If not, it returns {cpp:enum}`B_BAD_VALUE`.

The other functions are simplified versions of {hmethod}`ReplaceData()`. They each handle the
specific type of data declared for their last arguments. They succeed if this {hparameter}`type`
matches the type of data already in the {hparameter}`name` field, and fail if it does not. The new
data is added precisely as the counterpart "Add...()" function would add it.

If successful, all these functions return {cpp:enum}`B_OK`. If unsuccessful, they return
{cpp:enum}`B_ERROR` if the message is read-only (as it is while the message is being dragged),
{cpp:enum}`B_BAD_INDEX` if the {hparameter}`index` is out of range, {cpp:enum}`B_NAME_NOT_FOUND` if
the {hparameter}`name` field doesn't exist, or {cpp:enum}`B_BAD_TYPE` if the field doesn't contain
data of the specified type.

See also: {cpp:func}`~BMessage::AddData()`.
::::

::::{abi-group}
:::{cpp:function} BMessenger BMessage::ReturnAddress()
:::

Returns a {cpp:class}`BMessenger` object that can be used to reply to the {hclass}`BMessage`.
Calling the {cpp:class}`BMessenger`'s {cpp:func}`~BMessenger::SendMessage()` function is equivalent
to calling {cpp:func}`~BMessage::SendReply()`, except that the return message won't be marked as a
reply. If a reply isn't allowed (if the {hclass}`BMessage` wasn't delivered), the returned
{cpp:class}`BMessenger` will be invalid.

If you want to use the {hmethod}`ReturnAddress()` {cpp:class}`BMessenger` to send a synchronous
reply, you must do so before the {hclass}`BMessage` is deleted and a default reply is sent.

See also: {cpp:func}`~BMessage::SendReply()`, {cpp:func}`~BMessage::WasDelivered()`.
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

Sends a reply {hparameter}`message` back to the sender of the {hclass}`BMessage` (in the case of a
synchronous reply) or to a target {cpp:class}`BHandler` (in the case of an asynchronous reply).
Whether the reply is synchronous or asynchronous depends on how the {hclass}`BMessage` that's
sending the reply was itself sent:

- The reply is delivered synchronously if the message sender is waiting for one to arrive. The
  function that sent the {hclass}`BMessage` doesn't return until it receives the reply (or a timeout
  expires). If an expected reply has not been sent by the time the {hclass}`BMessage` object is
  deleted, a default {cpp:enum}`B_NO_REPLY` message is returned to the sender. If a reply is sent
  aftethe sender gave up waiting for it to arrive, the reply {hparameter}`message` disappears into
  the bowels of the system.

- The reply is delivered asynchronously if the message sender isn't waiting for a reply. In this
  case, the sending function designates a target {cpp:class}`BHandler` and {cpp:class}`BLooper` for
  any replies that might be sent, then returns immediately after putting the {hclass}`BMessage` in
  the pipeline. Posted messages and messages that are dragged and dropped are also eligible for
  asynchronous replies.

{hmethod}`SendReply()` works only for {hclass}`BMessage` objects that have been processed through a
message loop and delivered to you. The caller retains ownership of the reply {hparameter}`message`
passed to {hmethod}`SendReply()`; it can be deleted (or left to die on the stack) after the function
returns.

{hmethod}`SendReply()` sends a message---a reply message, to be sure, but a message nonetheless. It
behaves exactly like the other message-sending function, {cpp:class}`BMessenger`'s
{cpp:func}`~BMessenger::SendMessage()`:

- By passing it a {hparameter}`reply` argument, you can ask for a synchronous reply to the reply
  message it sends. It won't return until it receives the reply.

- By supplying a {hparameter}`replyHandler` argument, you can arrange for an expected asynchronous
  reply. If a specific target isn't specified, the {cpp:class}`BApplication` object will handle the
  reply if one is sent.

By default, {hmethod}`SendReply()` doesn't return until the reply message is delivered (placed in
the {cpp:class}`BLooper`'s port queue). It's possible, in some circumstances, for the receiving port
queue to be full, in which case {hmethod}`SendReply()` will block until a slot becomes free.
However, you can limit how long {hmethod}`SendReply()` will wait to deliver the message before it
gives up and returns. The {hparameter}`sendTimeout` argument is the number of microseconds you give
the function to do its work. If the time limit is exceeded, the function fails and returns an error
(cpp:enum}`B_TIMED_OUT`).

When asking for a synchronous reply, separate {hparameter}`sendTimeout` and
{hparameter}`replyTimeout` limits can be set for sending the message and receiving the reply. There
is no time limit if a timeout value is set to {cpp:enum}`B_INFINITE_TIMEOUT`---as it is by default.
The function won't block at all if the timeout is set to 0.

If a {hparameter}`command` is passed rather than a {hparameter}`message`, {hmethod}`SendReply()`
constructs the reply {hclass}`BMessage`, initializes its {hfield}`what` data member with the
{hparameter}`command` constant, and sends it just like any other reply. The {hparameter}`command`
versions of this function have infinite timeouts; they block until the message is delivered and, if
requested, a synchronous reply is received.

This function returns {cpp:enum}`B_OK` if the reply is successfully sent. If there's a problem in
sending the message, it returns the same sort of error code as {cpp:class}`BMessenger`'s
{cpp:func}`~BMessenger::SendMessage()`. It may also report a reply-specific problem. The more
informative return values are as follows:

:::{list-table}
---
header-rows: 0
align: left
---

-
    - {cpp:enum}`B_BAD_REPLY`
    - Attempting to reply to a message that hasn't been delivered yet.
-
    - {cpp:enum}`B_DUPLICATE_REPLY`
    - Sending a reply after one has already been sent and delivered.
-
    - {cpp:enum}`B_BAD_THREAD_ID`
    - Sending a reply to a destination thread that no longer exists.
-
    - {cpp:enum}`B_BAD_PORT_ID`
    - Sending a reply to a {cpp:class}`BLooper` and port that no longer exist.
-
    - {cpp:enum}`B_TIMED_OUT`
    - Taking longer than the specified time limit to deliver a reply message or to receive a
    synchronous reply to the reply.
:::

If you want to delay sending a reply and keep the {hclass}`BMessage` object beyond the time it's
scheduled to be deleted, you may be able to detach it from the message loop. See
{cpp:func}`~BLooper::DetachCurrentMessage()` in the {cpp:class}`BLooper` class.

See also: {cpp:func}`BMessenger::SendMessage()`, {cpp:func}`BMessenger::DetachCurrentMessage()`,
{cpp:func}`~BMessage::ReturnAddress()`.
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
:::{cpp:function} const BMessage::BMessage* Previous() const
:::

These functions can help if you're engaged in an exchange of messages or managing an ongoing
communication.

{hmethod}`WasDelivered()` indicates whether it's possible to send a reply to a message. It returns
{cpp:enum}`true` for a {hclass}`BMessage` that was posted, sent, or dropped -- that is, one that has
been processed through a message loop---and {cpp:enum}`false` for a message that has not yet been
delivered by any means.

{hmethod}`IsSourceRemote()` returns {cpp:enum}`true` if the message had its source in another
application, and {cpp:enum}`false` if the source is local or the message hasn't been delivered yet.

{hmethod}`IsSourceWaiting()` returns {cpp:enum}`true` if the message source is waiting for a
synchronous reply, and {cpp:enum}`false` if not. The source thread can request and wait for a reply
when calling either {cpp:class}`BMessenger`'s {cpp:func}`~BMessenger::SendMessage()` or
{hclass}`BMessage`'s {cpp:func}`~BMessage::SendReply()` function.

{hmethod}`IsReply()` returns {cpp:enum}`true` if the {hclass}`BMessage` is a reply to a previous
message (if it was sent by the {cpp:func}`~BMessage::SendReply()` function), and {cpp:enum}`false`
if not.

{hmethod}`Previous()` returns the previous message -- the message to which the current
{hclass}`BMessage` is a reply. It works only for a {hclass}`BMessage` that's received as an
asynchronous reply to a previous message. A synchronous reply is received in the context of the
previous message, so it's not necessary to call a function to get it. But when an asynchronous reply
is received, the context of the original message is lost; this function can provide it.
{hmethod}`Previous()` returns {cpp:enum}`NULL` if the {hclass}`BMessage` isn't an asynchronous reply
to another message.

See also: {cpp:func}`BMessenger::SendMessage()`, {cpp:func}`~BMessage::SendReply()`,
{cpp:func}`~BMessage::ReturnAddress()`.
::::

::::{abi-group}
:::{cpp:function} bool BMessage::WasDropped() const
:::
:::{cpp:function} BPoint BMessage::DropPoint(BPoint* offset = NULL) const
:::

{hmethod}`WasDropped()` returns {cpp:enum}`true` if the user delivered the {hclass}`BMessage` by
dragging and dropping it, and {cpp:enum}`false` if the message was posted or sent in application
code or if it hasn't yet been delivered at all.

{hmethod}`DropPoint()` reports the point where the cursor was located when the message was dropped
(when the user released the mouse button). It directly returns the point in the screen coordinate
system and, if an {hparameter}`offset` argument is provided, returns it by reference in coordinates
based on the image or rectangle the user dragged. The {hparameter}`offset` assumes a coordinate
system with (0.0, 0.0) at the left top corner of the dragged rectangle or image.

Since any value can be a valid coordinate, {hmethod}`DropPoint()` produces reliable results only if
{hmethod}`WasDropped()` returns {cpp:enum}`true`.

See also: {cpp:func}`BView::DragMessage()`.
::::

## Operators

### = (assignment)

:::{cpp:function} BMessage BMessage::operator=(const BMessage&)
:::

Assigns one {hclass}`BMessage` object to another. After the assignment, the two objects are
duplicates of each other without shared data.

### new

:::{cpp:function} void* BMessage::operator new(size_t numBytes)
:::

Allocates memory for a {hclass}`BMessage` object, or takes the memory from a previously allocated
cache. The caching mechanism is an efficient way of managing memory for objects that are created
frequently and used for short periods of time, as {hclass}`BMessage`s typically are.

### delete

:::{cpp:function} void BMessage::operator delete(void* memory, size_t numBytes)
:::

Frees memory allocated by the {hclass}`BMessage` version of {hmethod}`new`, which may mean restoring
the memory to the cache.

## Constants

### Message Specifiers

:::{code} cpp
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

These constants fill the {hfield}`what` slot of specifier {hclass}`BMessage`s. Each constant indicates
what other information the specifier contains, and how it should be interpreted. For example, a
{cpp:enum}`B_REVERSE_INDEX_SPECIFER` message has an {hfield}`index` field with an index that counts
backwards from the end of a list. A {cpp:enum}`B_NAME_SPECIFIER` message includes a {hfield}`name`
field that names the requested item.

See also: {cpp:func}`~BMessage::AddSpecifier()`, the "Scripting" chapter.
