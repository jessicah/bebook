# Functions and Macros

This section lists the Support Kit's general-purpose functions and macros.

::::{abi-group}

Declared in: `support/SupportDefs.h`

:::{cpp:function} int32 atomic_add(vint32* atomicVariable, int32 addValue)
:::
:::{cpp:function} int32 atomic_and(vint32* atomicVariable, int32 andValue)
:::
:::{cpp:function} int32 atomic_or(vint32* atomicVariable, int32 orValue)
:::

These functions perform the named operations (addition, bitwise AND, or bitwise OR) on the 32-bit
value found in {hparam}`atomicVariable`, thus:

:::{code} cpp
*atomicVariable += addValue;
*atomicVariable &= andValue;
*atomicVariable |= orValue;
:::

Each function returns the previous value of the {cpp:expr}`vint32` variable that {hparam}`atomicVariable`
points to (in other words, they each return the value that was in {hparam}`*atomicVariable` before
the operation was performed).

These functions are guaranteed to be atomic: if two threads attempt to access the same atomic
variable at the same time (through these functions), one of the threads will be made to wait until
the other thread has completed the operation and updated the {hparam}`atomicVariable` value.
::::

::::{abi-group}

Declared in: `support/Beep.h`

:::{cpp:function} status_t beep()
:::
:::{cpp:function} status_t system_beep(char* eventName, uint32 flags = 0)
:::

{hmethod}`beep()` produces the basic system beep. This function engages the Media Server, but
doesn't wait for the sound to play. If it can't contact the server to play the beep, it returns
{cpp:enum}`B_ERROR`. If it can make contact but can't get a satisfactory reply back from the server,
it returns {cpp:enum}`B_BAD_REPLY`. Otherwise, it returns {cpp:enum}`B_OK`.

{hmethod}`system_beep()` plays the system beep configured for the event specified by the given
{hparam}`eventName`.

Applications can add new system beep events by calling {cpp:func}`add_system_beep_event()`, passing
the name to assign to the event; the {hparam}`flags` argument is currently unused and should be
zero. Once this has been done, the user can use the Sounds preference application to configure a
sound for the event.

See also: {cpp:func}`play_sound()` in the Media Kit.
::::

::::{abi-group}

Declared in: `support/ClassInfo.h`

:::{c:macro} class_name(object)
:::
:::{c:macro} is_instance_of(object, class)
:::
:::{c:macro} is_kind_of(object, class)
:::
:::{c:macro} cast_as(object, class)
:::

These macros deliver information about an object's type, including the name of its class and its
standing in the class hierarchy. In each case, the object argument is a pointer to an object; it can
be an object of any type (it doesn't have to descend from any particular class). The class argument
is a class name---not a string such as "{hclass}`BApplication`", but the type name itself (literally
{hclass}`BApplication`).

{hmethod}`class_name()` returns a {cpp:expr}`char*` to the name of the {hparam}`object`'s class.

{hmethod}`is_instance_of()` returns {cpp:expr}`true` if {hparam}`object` is an instance of
{hparam}`class`, and {cpp:expr}`false` otherwise.

{hmethod}`is_kind_of()` returns {cpp:expr}`true` if {hparam}`object` is an instance of
{hparam}`class or an instance of any class that inherits from {hparam}`class`, and {cpp:expr}`false`
if not.

{hmethod}`cast_as()` returns a pointer to {hparam}`object` cast as a pointer to an object of
{hparam}`class`, but only if {hparam}`object` is a kind of {hparam}`class`. If not, {hparam}`object`
cannot be safely cast as a pointer to {hparam}`class`, so {hmethod}`cast_as()` returns
{cpp:expr}`NULL`.

For example, given this slice of the inheritance hierarchy from the Interface Kit, and code like
this that creates an instance of the {hclass}`BPictureButton` class,

:::{code} cpp
BButton* button = new BPictureButton(/* ... */);
:::

the first three macros would work as follows:

- The {hmethod}`class_name()` macro would return a pointer to the string "BPictureButton":

	:::{code} cpp
	const char *s = class_name(button);
	:::

- The {hmethod}`is_instance_of()` macro would return {cpp:expr}`true` only if the {hparam}`class`
  passed to it is {cpp:class}`BPictureButton`. In the following example, it would return
  {cpp:expr}`false`, and the message would not be printed. Even though {cpp:class}`BPictureButton`
  inherits from {cpp:class}`BView`, the object is an instance of the {cpp:class}`BPictureButton`
  class, not {cpp:class}`BView`:

	:::{code} cpp
	if (is_instance_of(button, BView))
		printf("The button is an instance of BView.\n");
	:::

- The {hmethod}`is_kind_of()` macro would return {cpp:expr}`true` if {hparam}`class` is
  {cpp:class}`BPictureButton` or any class that {cpp:class}`BPictureButton` inherits from. In the
  following example, it would return {cpp:expr}`true` and the message would be printed. A
  {cpp:class}`BPictureButton` is a kind of {cpp:class}`BView`:

	:::{code} cpp
	if (is_kind_of(button, BView))
		printf("The button is a kind of BView.\n");
	:::

Note that class names are not passed as strings, but {hmethod}`class_name()` returns the name as a
string.

The {hmethod}`cast_as()` macro is most useful when you want to treat a generic object as an instance
of a more specific class. Support, for example, that the {cpp:class}`BPictureButton` mentioned above
becomes the focus view for a window and you retrieve it by calling the {cpp:class}`BWindow`s
{cpp:func}`~BWindow::CurrentFocus()` function:

:::{code} cpp
BView* focus = window->CurrentFocus();
:::

Since the focus view might be any type of view, {cpp:func}`~BWindow::CurrentFocus()` returns a
pointer to an object of the base {cpp:class}`BView` class. Unless you know otherwise, you cannot
treat the object as anything more specific than a {cpp:class}`BView` instance. However, you can ask
the object if it's a kind of {cpp:class}`BPictureButton` and, if it is, cast it to the
{cpp:class}`BPictureButton` type:

:::{code} cpp
if (is_kind_of(focus, BPictureButton)) {
	BPictureButton* pictureButton = (BPictureButton*)focus);
	if (pictureButton->Behavior() == B_TWO_STATE_BUTTON)
		// . . .
}
:::

The {hmethod}`cast_as()` macro does the same thing, but more efficiently. It casts the object to the
target class if it is safe to do so---if the object is an instance of a class that inherits from the
target class or an instance of the target class itself---and returns {cpp:expr}`NULL` if not.

:::{code} cpp
BPictureButton* pictureButton = cast_as(focus, BPictureButton);
if (pictureButton != NULL) {
	if (pictureButton->Behavior() == B_TWO_STATE_BUTTON)
		// . . .
}
:::

{hmethod}`cast_as()` is often used in place of the cast operator to assure code safety even where an
expected result is anticipated and there's no need for an intermediate variable (like `focus`):

:::{code} cpp
BPictureButton* pictureButton = cast_as(window->CurrentFocus(), BPictureButton);
if (pictureButton != NULL) {
	// . . .
}
:::

The {hmethod}`cast_as()` and {hmethod}`is_kind_of()` macros work alike; they're both based on the
C++ {cpp:expr}`dynamic_cast` operator and they reflect its behavior. To describe that behavior more
precisely, let's adopt the following shorthand terms for an object's type:

- The real type of an object is its type on construction. For example, if you construct an instance
  of the {hclass}`BButton` class, as shown above, {cpp:class}`BButton` is its real type.
- The declared type of an object is the class label it currently bears. For example,
  {hmethod}`CurrentFocus()` returns an object whose declared class is {cpp:class}`BView`.

Either of these types can be compared to a target type, the type you want to cast the object to or
test it against. The target type is the class argument passed to the macros.

In the best of all possible worlds, you'd want to ignore the declared type of an object and compare
only the real type to the target type. However, the {cpp:expr}`dynamic_cast` operator---and by
extensions {hmethod}`cast_as()` and {hmethod}`is_kind_of()`---considers the real type only if it has
to. It first compares the object's declared type to the target type. It assumes that the declared
type is accurate (that the object is truly the kind of object it's represented to be) and it
summarily handles the obvious cases: If the target type is the same as the declared type or if it's
a class that the declared type inherits from, the operation will succeed. Consequently,
{hmethod}`cast_as()` will cast the object to the target type and {hmethod}`is_kind_of()` will return
{cpp:expr}`true`, regardless of the object's real type. In other words, if the target class is above
or at the same level as the declared class in the inheritance hierarchy, the real class is ignored.

However, if the declared type doesn't match or derive from the target type, {cpp:expr}`dynamic_cast`
and the macros look at the real type: If the target class is identical to the real type, or if it's
a class that the real type derives from, the operation succeeds. If not, it fails.

Therefore, the {hmethod}`is_kind_of()` and {hmethod}`cast_as()` macros will produce reliable results
as long as objects are not arbitrarily cast to types that may not be accurate. For example, you
should not cast an object to a target type and then attempt to use the {hmethod}`is_kind_of()` to
determine if the cast was correct. This code is unreliable:

:::{code} cpp
BPictureButton* pictureButton = (BPictureButton)window->CurrentFocus();
if (is_kind_of(pictureButton, BPictureButton)) {
	// . . .
}
:::

In this example, {hmethod}`is_kind_of()` will always return {cpp:expr}`true`, no matter what the
class of the current focus view. The general rule is that the declared type of an object must always
be accurate; an object should be typed only to its own class or to a class that it inherits from.
The amcros cannot rescue you from an inaccurate cast.
::::

::::{abi-group}

Declared in: `support/UTF8.h`

:::{cpp:function} status_t convert_to_utf8(uint32 sourceEncoding, const char* source, int32* sourceLength, char* destination, int32* destinationLength, int32* state, char substitute = B_SUBSTITUTE)
:::
:::{cpp:function} status_t convert_from_utf8(uint32 destinationEncoding, const char* source, int32* sourceLength, char* destination, int32* destinationLength, int32* state, char substitute = B_SUBSTITUTE)
:::

These functions convert text to and from the Unicode(TM) UTF-8 encoding that's standard for Haiku
and is assumed in most contexts. UTF-8 is described under "Character Encoding" section of The
Interface Kit chapter.

{hmethod}`convert_to_utf8()` permits you to take text that's encoded according to another standard
and convert it to UTF-8 for Haiku. {hmethod}`convert_from_utf8()` lets you convert text from UTF-8
to other encodings for other venues (for example, to the encodings commonly used fro displaying text
on the World Wide Web --- this needs changing!).

The first argument passed to these functions names the other encoding: the source encoding for
{hmethod}`convert_to_utf8()` and the destination encoding for {hmethod}`convert_from_utf8()`. it can
be any of the following constants:

:::{list-table}
---
header-rows: 0
---
-
	- {cpp:enum}`B_ISO1_CONVERSION`
	- {cpp:enum}`B_MAC_ROMAN_CONVERSION`
-
	- {cpp:enum}`B_ISO2_CONVERSION`
	- {cpp:enum}`B_SJIS_CONVERSION`
-
	- {cpp:enum}`B_ISO3_CONVERSION`
	- {cpp:enum}`B_EUC_CONVERSION`
-
	- {cpp:enum}`B_ISO4_CONVERSION`
	- {cpp:enum}`B_JIS_CONVERSION`
-
	- {cpp:enum}`B_ISO5_CONVERSION`
	- {cpp:enum}`B_MS_WINDOWS_CONVERSION`
-
	- {cpp:enum}`B_ISO6_CONVERSION`
	- {cpp:enum}`B_UNICODE_CONVERSION`
-
	- {cpp:enum}`B_ISO7_CONVERSION`
	- {cpp:enum}`B_KOI8R_CONVERSION`
-
	- {cpp:enum}`B_ISO8_CONVERSION`
	- {cpp:enum}`B_MS_WINDOWS_1251_CONVERSION`
-
	- {cpp:enum}`B_ISO9_CONVERSION`
	- {cpp:enum}`B_MS_DOS_866_CONVERSION`
-
	- {cpp:enum}`B_ISO10_CONVERSION`
	-
:::

Most of these constants designate encoding schemes that are supported by the {cpp:class}`BFont`
class in the Interface Kit and its {cpp:func}`~BFont::SetEncoding()` function. They parallel the
constants that are passed to that function. For example, {cpp:enum}`B_IOS1_CONVERSION` (for these
functions) and {cpp:enum}`B_ISO_8859_1` (for {cpp:func}`~BFont::SetEncoding()`) both designate the
extended ASCII encoding defined in part one of ISO 8859 (Latin 1). Similarly,
{cpp:enum}`B_ISO2_CONVERSION` matches {cpp:enum}`B_ISO_8859_2`, {cpp:enum}`B_ISO3_CONVERSION`
matches {cpp:enum}`B_ISO_8859_3`, and so on. {cpp:enum}`B_MAC_ROMAN_CONVERSION` matches
{cpp:enum}`B_MACINTOSH_ROMAN`. ({cpp:enum}`B_ISO10_CONVERSION` is not implemented in this release.)

{cpp:enum}`B_SJIS_CONVERSION` stands for the Shift-JIS (Japanese Industrial Standard) encoding of
Japanese and {cpp:enum}`B_EUC_CONVERSION` stands for the EUC (Extended UNIX Code) encoding of
Japanese in packed format.

Both functions convert up to {hparam}`sourceLength` bytes of text from the source buffer. They write
up to {hparam}`destinationLength` bytes of converted text into the destination buffer. The amount of
text that they actually convert is therefore constrained both by the amount of source text
({hparam}`sourceLength`) and the capacity of the output buffer ({hparam}`destinationLength`).
Neither function stops at a null terminator ('0') when reading the input buffer nor adds one to the
text in the output buffer; they depend only on {hparam}`sourceLength` and
{hparam}`destinationLength` for guidance.

When finished, these functions modify the variable that {hparam}`sourceLength` refers to so that it
reports the number of bytes of source text actually converted. They also modify the variable that
{hparam}`destinationLength` refers to so that it reports the number of bytes actually written to the
destination buffer. Neither function will stop in the middle of a multibyte source character;
they're guaranteed to convert only full characters.

The {hparam}`state` argument serves as a cookie that lets you use multiple calls to these functions
to convert a batch of text (if, for example, the text is stored in multiple buffers). Pass 0 for the
first buffer, and pass the value returned in state to the next call to continue processing the same
text; this will cause the conversion to continue where it left off. For example:

:::{code} cpp
/* buffer is a pointer to a small source buffer */
/* destBuffer is a pointer to a small destination buffer */
/* destBufferLen is the size of the destination buffer in bytes */
int32 state = 0;
int32 bufferLen;

while ((bufferLen = GetNextBuffer(file, buffer))) {
	convert_to_utf8(buffer, &bufferLen, destBuffer, &destBufferLen, &state);
	/* do stuff with the buffer in destBuffer, which has the converted text */
}
:::

In this example, text is fetched using a call to a function called {hmethod}`GetNextBuffer()`, whose
implementation depends on the application's needs. Each buffer is converted, and the converted text
is stored in destBuffer, which can then be used by the application.

If either function encounters a character in the source that the destination format doesn't allow,
it puts the character specified by the substitute argument (or a question mark ('?') if substitute
isn't specified) in its place in the output text. This is much more likely to occur when converting
from UTF-8 than when converting to it, since Unicode represents a very large number of characters.

If successful in converting at least one source character, both functions return {cpp:enum}`B_OK`.
If unsuccessful, for example, if they don't recognize the source or destination encoding, they
return {cpp:enum}`B_ERROR`. If there's an error, you should not trust any of the output arguments.

:::{admonition} Note
:class: note
These functions are found in the `libtextencoding.so` library. If you use them, be sure to include
this library file.
:::

See also: {cpp:func}`BFont::SetEncoding()`, "Character Encoding" section of The Interface Kit
chapter.
::::

::::{abi-group}
Declared in: `support/Archivable.h`

:::{cpp:function} instantiation_func find_instantiation_func(const char* className)
:::
:::{cpp:function} instantiation_func find_instantiation_func(BMessage* archive)
:::

Returns a pointer to the {cpp:func}`~BArchivable::Instantiate()` function that can create instances
of the {hparam}`className` class, or {cpp:expr}`NULL` if the function can't be found. If passed a
{cpp:class}`BMessage` archive, {hmethod}`find_instantiation_func()` gets the name of the class from
a {cpp:enum}`B_STRING_TYPE` field called "class" in the {cpp:class}`BMessage`.

The instantiation_func type is defined as follows:

:::{code} cpp
BArchivable* (*instantiation_func) (BMessage *)
:::

In other words, the function has the same syntax as the {cpp:func}`~BArchivable::Instantiate()`
function declared in the {cpp:class}`BArchivable` class and replicated in derived classes (with
class-specific return values).

The function that's returned can be called like any C function; you don't need the class name or
another object of the class. For example:

:::{code} cpp
instantiation_func func;
if (func = find_instantiation_func(archiveMessage)) {
	BArchivable* object = func(archiveMessage);
}
:::

{hmethod}`instantiate_object()` will do this work for you.

See also: {cpp:func}`BArchivable::Instantiate()`, {cpp:func}`instantiate_object()`
::::

::::{abi-group}
Declared in: `support/Archivable.h`

:::{cpp:function} BArchivable* instantiate_object(BMessage* archive)
:::

Creates and returns a new instance of an archived object, or returns {cpp:expr}`NULL` if the object
can't be constructed. The object is created by calling the {cpp:func}`BArchivable::Instantiate()`
function of...

1. ...the class that was last added to the "class" field (an array of class names) of the archive
   {cpp:class}`BMessage`. This will be the "most derived" class in the array.
2. If the named class isn't recognized by the app (or doesn't define
   {cpp:func}`BArchivable::Instantiate()`), the function tries to load the add-on that's identified
   (by signature) in archive's {hparam}`add_on` field. This add-on should contain the code for the
   class.
3. If the add-on method doesn't work, {hmethod}`instantiate_object()` tries the next class in the
   "class" array, and so works its way up the class hierarchy.
4. If the appropriate class is never found, the function returns {cpp:expr}`NULL`.

When successful, {hmethod}`instantiate_object()` returns the object that {hmethod}Instantiate()`
created, but typed to the base {cpp:class}`BArchivable` class. The {hmethod}`cast_as()` macro can
type it to the proper class:

:::{code} cpp
BArchivable* base = instantiate_object(archive);
if (base) {
	TheClass* object = cast_as(base, TheClass);
	if (object) {
		// . . .
	}
}
:::
::::

::::{abi-group}
Declared in: `support/ByteSwap.h`

:::{cpp:function} status_t swap_data(type_code type, void* data, size_t length, swap_action action)
:::
:::{cpp:function} bool is_type_swapped(type_code type)
:::

{hmethod}`swap_data` is a general byte swapping function, converting data of type {hparam}`type` and
converting its endianness according to action (defined in "Byte Swapping Constants"). The
{hparam}`length` field can be used to specify an array of items to be converted. For example, you
can convert an array of {cpp:class}`BMessenger`s from little endian to the host endianness:

:::{code} cpp
BMessenger messengers[10];
// . . .
swap_data(B_MESSENGER_TYPE, messengers, 10 * sizeof(BMessenger), B_SWAP_LENDIAN_TO_HOST):
:::

The function can swap most data types with type constants defined in `support/TypeConstants.h`. It
returns {cpp:enum}`B_OK` on success and {cpp:enum}`B_BAD_VALUE` on failure.

{hmethod}`is_type_swapped()` takes a type code and determines whether or not it has been swapped.
This only works for types defined in `support/TypeConstants.h`. It returns {cpp:expr}`true` if the
type code is in the host's native endainness and {cpp:expr}`false` otherwise.

See also: "Byte Swapping Constants".
::::

::::{abi-group}
Declared in: `support/SupportDefs.h`

:::{c:macro) min(a, b)
:::
:::{c:macro} min_c(a, b)
:::
:::{c:macro} max(a, b)
:::
:::{c:macro} max_c(a, b)
:::

These macros compare two integers or floating-point numbers. {c:expr}`min()` and {c:expr}`min_c()`
return the lesser of the two (or b if they're equal); {c:expr}`max()` and {c:expr}`max_c()` return
the greater of the two (or a if they're equal). {c:expr}`min()` and {c:expr}`max()` can only be used
in straight C programs. {c:expr}`min_c()` and {c:expr}`max_c()` are defined for C and C++.
::::

::::{abi-group}
Declared in: `support/Archivable.h`

:::{cpp:function} bool validate_instantiation(BMessage* archive, const char* className)
:::

Returns {cpp:expr}`true` if the {hparam}`archive` {cpp:class}`BMessage` contains data for an object
belonging to the {hparam}`className` class, and {cpp:expr}`false` if not. The determination is made
by looking for the class name in a "class" array in the archive. If the class name appears anywhere
in the array, this function returns {cpp:expr}`true`. If not, it returns {cpp:expr}`false`.
::::
