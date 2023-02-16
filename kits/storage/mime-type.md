:::{cpp:class} BMimeType
:::

# BMimeType

## Constructor and Destructor

::::{abi-group}
:::{cpp:function} BMimeType::BMimeType()
:::

:::{cpp:function} BMimeType::BMimeType(const char* MIME_string)
:::

Constructs a new {hclass}`BMimeType` object and initializes its MIME type
to a copy of {hparam}`MIME_string` (if the argument is given). The rules of
validity apply (see "{ref}`Valid MIME Strings`"). To see if the
initialization was successful, call {cpp:func}`InitCheck()
<BMimeType::InitCheck>` after you construct a new {hclass}`BMimeType`
object.

You can also set the MIME type through the {cpp:func}`SetTo()
<BMimeType::SetTo>` function.
::::

::::{abi-group}
:::{cpp:function} virtual BMimeType::~BMimeType()
:::

Frees the object's MIME string and destroys the object.
::::

## Member Functions

::::{abi-group}
:::{cpp:function} bool BMimeType::Contains(const BMimeType* other) const
:::

Compares the MIME string with {hparam}`other`, returning {cpp:expr}`true`
if they are identical. If the object is a supertype and it's the supertype
of {hparam}`other`, then the method returns {cpp:expr}`true`. Otherwise, it
returns {cpp:expr}`false`.
::::

::::{abi-group}
:::{cpp:function} status_t BMimeType::GetAppHint(entry_ref* app_ref) const
:::

:::{cpp:function} status_t BMimeType::SetAppHint(const entry_ref* app_ref)
:::

These functions get and set the "app hint" for the object's application
signature. The app hint is a path that identifies the executable that
should be used when launching an application that has this signature. For
example, when the Tracker needs to launch an app of type
"application/YourAppHere", it asks the database for the application hint.
This hint is converted to an {htype}`entry_ref` before it is passed to the
caller. Of course, the path may not point to an application, or it might
point to an application with the wrong signature (and so on)—that's why
this is merely a hint.

{hmethod}`GetAppHint()` function initializes the {htype}`entry_ref` to the
hint recorded in the database; the argument must be allocated before it's
passed in.

{hmethod}`SetAppHint()` copies the path corresponding to the
{htype}`entry_ref` into the database. {hparam}`app_ref` should point to an
executable file that has the same signature as this object's MIME type.

:::{list-table}
---
header-rows: 1
align: left
widths: auto
---
-
	- Return Code

	- Description

-
	- {cpp:enumerator}`B_OK`.
	- The ref was successfully retrieved or set.
-
	- {cpp:enumerator}`B_NO_INIT`.
	- The {hclass}`BMimeType` is uninitialized.
-
	- {cpp:enumerator}`B_BAD_VALUE`.
	- (Set) The ref is uninitialized.

:::

See Also: {cpp:func}`BNodeInfo::GetAppHint`
::::

::::{abi-group}
:::{cpp:function} status_t BMimeType::GetAttrInfo(BMessage* info) const
:::

:::{cpp:function} status_t BMimeType::SetAttrInfo(BMessage* info)
:::

These functions use a {cpp:class}`BMessage` to get and set the list of
attributes that are typically associated with files of the MIME type. The
{cpp:class}`BMessage` must have the following fields:

:::{list-table}
---
header-rows: 1
align: left
widths: auto
---
-
	- Field Name

	- Type

	- element[0..n]

-
	- {hparam}`attr:name`

	- {cpp:enumerator}`B_STRING_TYPE`

	- Each element is the name of one attribute.

-
	- {hparam}`attr:public_name`

	- {cpp:enumerator}`B_STRING_TYPE`

	- Each element is the human-readable name of one attribute.

-
	- {hparam}`attr:type`

	- {cpp:enumerator}`B_INT32_TYPE`

	- Each element is the type code for the corresponding attribute.

-
	- {hparam}`attr:public`

	- {cpp:enumerator}`B_BOOL_TYPE`

	- {cpp:expr}`true` if the attribute is public, {cpp:expr}`false` if it's
private.

-
	- {hparam}`attr:editable`

	- {cpp:enumerator}`B_BOOL_TYPE`

	- {cpp:expr}`true` if the attribute should be user-editable,
{cpp:expr}`false` if not.


:::

You can actually have any fields you want; it's up to applications to
determine which attributes they recognize and which they don't.

Each element in each field describes the next attribute. If a file has
three attributes, there should be three elements in each field, one per
attribute.

:::{list-table}
---
header-rows: 1
align: left
widths: auto
---
-
	- Return Code

	- Description

-
	- {cpp:enumerator}`B_OK`.
	- No error.
-
	- {cpp:enumerator}`B_BAD_VALUE`.
	- Invalid file.

:::
::::

::::{abi-group}
:::{cpp:function} status_t BMimeType::GetFileExtensions(BMessage* msg) const
:::

:::{cpp:function} status_t BMimeType::SetFileExtensions(const BMessage* msg)
:::

The database associates a list of file extensions (.xxx filename
appendages) with each file type. If a file is otherwise untyped, clients of
the database can figure out its type by matching the file's extension to
the lists in the database.

These functions get and set the file extensions that are associated with
the object's MIME type.

-   If you're getting the extensions, you'll find them copied into your
{cpp:class}`BMessage`'s {hparam}`extensions` field (the
{cpp:class}`BMessage` must be allocated). They're given as an indexed array
of strings ({cpp:enumerator}`B_STRING_TYPE`).

-   Similarly, you pass in the extensions by adding strings to the message's
{hparam}`extensions` field.

-   The {cpp:class}`BMessage`'s {hparam}`what` field is unimportant.

For example, to retrieve all the extensions that correspond to this
object's MIME type, you would do the following:

:::{code} cpp
BMessage msg();
uint32 i=0;
char *ptr;

if (mime.GetFileExtensions(&msg) != B_OK)
   /* Handle the error. */

while (true) {
   if (msg.FindString("extensions", i++, &ptr) != B_OK)
      break;
   printf("> Extension: %sn", ptr);
}
:::

A given extension can be associated with more than one MIME type.

A {cpp:expr}`NULL` msg to {hmethod}`SetFileExtensions()` clears the type's
extension list.

:::{admonition} Warning
:class: warning
{hmethod}`SetFileExtensions()` clobbers the existing set of extensions. If
you want to augment a type's extensions, you should retrieve the existing
set, add the new ones, and then call {hmethod}`SetFileExtensions()`.

Also, there's no way to ask the database to give you a set of file types
that map to a given extension. To find a type for an extension, you have to
get all the installed types with {cpp:func}`GetInstalledTypes()
<BMimeType::GetInstalledTypes>` and ask each one for its set of extensions.
:::

:::{list-table}
---
header-rows: 1
align: left
widths: auto
---
-
	- Return Code

	- Description

-
	- {cpp:enumerator}`B_OK`.
	- The extensions were found or set.
-
	- {cpp:enumerator}`B_NO_INIT`.
	- The {hclass}`BMimeType` is uninitialized.
-
	- {cpp:enumerator}`B_NO_MEMORY`.
	- Insufficient memory to copy the extensions.

:::
::::

::::{abi-group}
:::{cpp:function} status_t BMimeType::GetIcon(BBitmap* icon, icon_size which) const
:::

:::{cpp:function} status_t BMimeType::SetIcon(BBitmap* icon, icon_size which)
:::

{hmethod}`GetIcon()` and {hmethod}`SetIcon()` get and set the icons that
are associated (in the database) with this object's MIME type. You specify
which icon you want (large or small) by passing
{cpp:enumerator}`B_LARGE_ICON` or {cpp:enumerator}`B_MINI_ICON` as the
{hparam}`which` argument. The icon is passed in or returned through the
{hparam}`icon` argument. The icon data is copied out of or into the
{cpp:class}`BBitmap` object.

The bitmap (if you're calling {hmethod}`SetIcon()`) or icon (if you're
calling {hmethod}`GetIcon()`) must be the proper size: 32x32 for the large
icon, 16x16 for the small one. Additionally, the bitmap must be in the
{cpp:enumerator}`B_CMAP8` color space (8-bit color), or the application
will crash.

If you want to erase the node's icon, pass {cpp:expr}`NULL` as the
{hparam}`icon` argument to {hmethod}`SetIcon()`.

:::{list-table}
---
header-rows: 1
align: left
widths: auto
---
-
	- Return Code

	- Description

-
	- {cpp:enumerator}`B_OK`.
	- The icon was found or set.
-
	- {cpp:enumerator}`B_NO_INIT`.
	- The {hclass}`BMimeType` is uninitialized.
-
	- {cpp:enumerator}`B_BAD_VALUE`.
	- The bitmap or icon wasn't the proper size.

:::
::::

::::{abi-group}
:::{cpp:function} status_t BMimeType::GetIconForType(const char* file_type, BBitmap* icon, icon_size which) const
:::

:::{cpp:function} status_t BMimeType::SetIconForType(const char* file_type, BBitmap* icon, icon_size which)
:::

These functions get and set the icons that an application that has this
object's MIME type as a signature uses to display the given file type.
{hparam}`file_type` must be a valid MIME string.

The icon is passed in or returned through the {hparam}`icon` argument:

-   If you're getting the icon, the {cpp:class}`BBitmap` must be allocated;
the icon data is copied into your {cpp:class}`BBitmap` object.

-   If you're setting the icon, the bitmap must be the proper size: 32x32 for
the large icon, 16x16 for the small one. In {cpp:class}`BRect` lingo,
that's `BRect(0, 0, 31, 31)` and `BRect(0, 0, 15, 15)`.

-   If you're setting the icon, the bitmap must be in the
{cpp:enumerator}`B_CMAP8` color space (8-bit color), or the application
will crash.

-   You can remove an icon by passing {cpp:expr}`NULL` as the icon argument to
{hmethod}`SetIconForType()`.

:::{list-table}
---
header-rows: 1
align: left
widths: auto
---
-
	- Return Code

	- Description

-
	- {cpp:enumerator}`B_OK`
	- The icon was found or set.
-
	- {cpp:enumerator}`B_NO_INIT`.
	- The {hclass}`BMimeType` is uninitialized.
-
	- {cpp:enumerator}`B_BAD_VALUE`.
	- ({hmethod}`Get`) {cpp:expr}`NULL` {cpp:class}`BBitmap` pointer, or
		{hparam}`file_type` is invalid.
-
	- {cpp:enumerator}`B_BAD_VALUE`.
	- ({hmethod}`Set`) The bitmap data isn't the proper size, or
		{hparam}`file_type` is invalid.

:::
::::

::::{abi-group}
:::{cpp:function} static status_t BMimeType::GetInstalledTypes(BMessage* types)
:::

:::{cpp:function} static status_t BMimeType::GetInstalledTypes(const char* supertype, BMessage* subtypes)
:::

:::{cpp:function} static status_t BMimeType::GetInstalledSupertypes(BMessage* supertypes)
:::

These `static` functions retrieve all the file types that are currently
installed in the database, all the installed subtypes for a given
supertype, and all the installed supertypes. The types are copied into the
{hparam}`types` field of the passed-in {cpp:class}`BMessage` (which must be
allocated).

:::{list-table}
---
header-rows: 1
align: left
widths: auto
---
-
	- Return Code

	- Description

-
	- {cpp:enumerator}`B_OK`.
	- The types were found.
-
	- {cpp:enumerator}`B_BAD_VALUE`.
	- The {hparam}`supertype` string isn't valid.
-
	- {cpp:enumerator}`B_NO_MEMORY`.
	- Insufficient memory to copy the types.

:::
::::

::::{abi-group}
:::{cpp:function} status_t BMimeType::GetLongDescription(char* description) const
:::

:::{cpp:function} status_t BMimeType::SetLongDescription(const char* description)
:::

:::{cpp:function} status_t BMimeType::GetShortDescription(char* description) const
:::

:::{cpp:function} status_t BMimeType::SetShortDescription(const char* description)
:::

Each file type has a couple of human-readable description strings
associated with it. Neither description string may be longer than
{cpp:enumerator}`B_MIME_TYPE_LENGTH` characters.

These functions get and set the long and short description strings. The
{hmethod}`Get` functions copy the string into the argument (which must be
allocated). The {hmethod}`Set` functions copy the string that the argument
points to.

:::{list-table}
---
header-rows: 1
align: left
widths: auto
---
-
	- Return Code

	- Description

-
	- {cpp:enumerator}`B_OK`.
	- The description was found or set.
-
	- {cpp:enumerator}`B_NO_INIT`.
	- The {hclass}`BMimeType` is uninitialized.
-
	- {cpp:enumerator}`B_BAD_VALUE`.
	- ({hmethod}`Set`) {hparam}`description` is too long.
-
	- {cpp:enumerator}`B_NO_MEMORY`.
	- Insufficient memory to copy the description.

:::
::::

::::{abi-group}
:::{cpp:function} status_t BMimeType::GetPreferredApp(char* signature, app_verb verb = B_OPEN) const
:::

:::{cpp:function} status_t BMimeType::SetPreferredApp(const char* signature, app_verb verb = B_OPEN)
:::

These functions get and set the "preferred app" for this object's MIME
type. The preferred app is the application that's used to access a file
when, for example, the user double-clicks the file in a Tracker window:
Unless the file identifies (in its attributes) a "custom" preferred app,
the Tracker will ask the File Type database for the preferred app that's
associated with the file's type.

-   The preferred app is identified by {hparam}`signature`, a MIME string. A
value of {cpp:expr}`NULL` indicates that there is no preferred app for the
MIME type.

-   The {htype}`app_verb` argument specifies the type of access; currently,
the only {htype}`app_verb` is {cpp:enumerator}`B_OPEN`.

:::{list-table}
---
header-rows: 1
align: left
widths: auto
---
-
	- Return Code

	- Description

-
	- {cpp:enumerator}`B_OK`.
	- The preferred app was found or set.
-
	- {cpp:enumerator}`B_NO_INIT`.
	- The {hclass}`BMimeType` is uninitialized.
-
	- {cpp:enumerator}`B_BAD_VALUE`
	- ({hmethod}`Set…()` only). The {hparam}`signature` argument is too long
		(greater than {cpp:enumerator}`B_MIME_TYPE_LENGTH`).

:::
::::

::::{abi-group}
:::{cpp:function} status_t BMimeType::GetSupportingApps(BMessage* msg) const
:::

:::{cpp:function} static status_t BMimeType::GetWildcardApps(BMessage* msg)
:::

These functions retrieve a list of applications (identified by signature)
that know how to handle the object's MIME type (for
{hmethod}`GetSupportingApps()`) or all MIME types
({hmethod}`GetWildCardApps()`). The information is returned in
{hparam}`msg`, which must be allocated by the caller. The {hparam}`msg`
format is:

:::{list-table}
---
header-rows: 1
align: left
widths: auto
---
-
	- Field name

	- Type

	- Description

-
	- {hparam}`applications`

	- {cpp:enumerator}`B_STRING_TYPE` (array)

	- The signatures of the application that know how to handle the MIME type.
The first __n__ applications (where __n__ is defined by {hparam}`be:sub`,
below) can handle the full type (supertype __and__ subtype). The rest of
the applications in the array handle the supertype only.

-
	- {hparam}`be:sub`

	- {cpp:enumerator}`B_INT32_TYPE`

	- The number of applications in the "applications" array that can handle the
object's full MIME type. These applications are listed first in the array.
This field is omitted if the object represents a supertype only.

-
	- {hparam}`be:super`

	- {cpp:enumerator}`B_INT32_TYPE`

	- The number of applications in the {hparam}`applications` array that can
handle the object's supertype (not counting those that can handle the full
type). These applications are listed after the full-MIME type supporters.
By definition, the {hmethod}`GetWildcardApps()` function never returns
supertype-only apps.


:::

For example, here we print the signatures of the apps that can handle
"text/plain" and "text" (without checking for errors):

:::{code} cpp
BMessage msg();
BMimeType mime("text/plain");
int32 subs=0, supers=0, n, hold;
char *ptr;

mime.GetSupportingApps(&msg);
msg.FindInt32("be:subs", &subs);
msg.FindInt32("be:supers", &supers);

for (n = 0; n < subs; n++) {
   msg.FindString("applications", n, &ptr);
   printf("Full support: %sn", ptr);
}
hold = n;
for (n = 0; n < supers; n++) {
   msg.FindString("applications", n+hold, &ptr);
   printf("Supertype support: %sn", ptr);
}
:::

If an application supports both the full type and the supertype, it will
be listed only once in the "applications" array (as a full supporter).

To set the types that an application supports, use
{cpp:func}`BAppFileInfo::SetSupportedTypes`. To tell an app to support all
types, add "application/octet-stream" to its supported-types list.

:::{list-table}
---
header-rows: 1
align: left
widths: auto
---
-
	- Return Code

	- Description

-
	- {cpp:enumerator}`B_OK`.
	- The signatures were found.
-
	- {cpp:enumerator}`B_BAD_PORT`.
	- No {cpp:var}`be_app` found.
-
	- {cpp:enumerator}`B_NO_INIT`.
	- The {hclass}`BMimeType` is uninitialized.
-
	- {cpp:enumerator}`B_NO_MEMORY`.
	- Insufficient memory to copy the signatures.

:::
::::

::::{abi-group}
:::{cpp:function} status_t BMimeType::InitCheck() const
:::

Returns the status of the most recent construction or {cpp:func}`SetTo()
<BMimeType::SetTo>` call.

See {cpp:func}`SetTo() <BMimeType::SetTo>`.
::::

::::{abi-group}
:::{cpp:function} status_t BMimeType::Install()
:::

:::{cpp:function} status_t BMimeType::Delete()
:::

:::{cpp:function} bool BMimeType::IsInstalled() const
:::

{hmethod}`Install()` adds the object's MIME type to the File Type
database. {hmethod}`Delete()` removes the type from the database.
{hmethod}`IsInstalled()` tells you if the type is currently installed.

None of these functions affect the object's copy of the MIME type; for
instance, deleting a MIME type from the database doesn't uninitialize the
object.

:::{admonition} Warning
:class: warning
Currently, {hmethod}`Install()` may return a random value if the object is
already installed. To avoid confusion, you should call
{hmethod}`IsInstalled()` first:
:::

:::{list-table}
---
header-rows: 1
align: left
widths: auto
---
-
	- Return Code

	- Description

-
	- {cpp:enumerator}`B_OK`.
	- The type was successfully added or deleted.
-
	- {cpp:enumerator}`B_BAD_VALUE`.
	- The object is uninitialized.

:::
::::

::::{abi-group}
:::{cpp:function} static bool BMimeType::IsValid(const char* MIME_string)
:::

:::{cpp:function} bool BMimeType::IsValid() const
:::

:::{cpp:function} bool BMimeType::IsSupertypeOnly() const
:::

The `static` {hmethod}`IsValid()` tests its argument for MIME validity.
See "{ref}`Valid MIME Strings`" for the rules. The non-static version
checks the validity of the object's MIME string.

{hmethod}`IsSupertypeOnly()` returns {cpp:expr}`true` if the object's MIME
string doesn't include a subtype.
::::

::::{abi-group}
:::{cpp:function} status_t BMimeType::SetTo(const char* MIME_string)
:::

:::{cpp:function} void BMimeType::Unset()
:::

{hmethod}`SetTo()` initializes this {hclass}`BMimeType` object to
represent {hparam}`MIME_string`. The object's previous MIME string is
freed; the argument is then copied. The argument can be a full
supertype/subtype string, or simply a supertype. In any case, it must pass
the validity test described in "{ref}`Valid MIME Strings`".

{hmethod}`Unset()` frees the object's current MIME string, and sets the
object's status to {cpp:enumerator}`B_NO_INIT`.

These return codes are also returned by the {cpp:func}`InitCheck()
<BMimeType::InitCheck>` function.

:::{list-table}
---
header-rows: 1
align: left
widths: auto
---
-
	- Return Code

	- Description

-
	- {cpp:enumerator}`B_OK`.
	- The initialization was successful.
-
	- {cpp:enumerator}`B_NO_INIT`.
	- {hparam}`MIME_string` is {cpp:expr}`NULL` or invalid.
-
	- {cpp:enumerator}`B_NO_MEMORY`.
	- Not enough memory to allocate a copy of the argument.

:::
::::

::::{abi-group}
:::{cpp:function} static status_t BMimeType::StartWatching(BMessenger target)
:::

:::{cpp:function} static status_t BMimeType::StopWatching(BMessenger target)
:::

{hmethod}`StartWatching()` initiates the MIME monitor, which is used for
keeping track of changes to the File Types database. Change notifications
will be sent via the {cpp:class}`BMessenger` {hparam}`target` in a
{cpp:class}`BMessage` with the {hparam}`what` field set to
{cpp:enumerator}`B_META_MIME_CHANGED`.

Notification messages have the following fields:

:::{list-table}
---
header-rows: 1
align: left
widths: auto
---
-
	- Field name

	- Type

	- Description

-
	- {hparam}`be:which`

	- {htype}`int32`

	- Change bitmap (see below for a list)

-
	- {hparam}`be:type`

	- string

	- MIME type whose database information was changed

-
	- {hparam}`be:extra_type`

	- string

	- Extra MIME field used for some notifications

-
	- {hparam}`be:large_icon`

	- {htype}`bool`

	- For notifications involving icon changes, {cpp:expr}`true` if the large
icon was changed; {cpp:expr}`false` otherwise


:::

{hparam}`be:which` is a bitmask describing the changes made to the
database for MIME type {hparam}`be:type`. The following masks are defined
along with the {hclass}`BMimeType` methods used to effect the changes they
signal:

:::{list-table}
---
header-rows: 1
align: left
widths: auto
---
-
	- Constant

	- Method

-
	- {cpp:enumerator}`B_ICON_CHANGED`

	- {cpp:func}`SetIcon() <BMimeType::SetIcon>`

-
	- {cpp:enumerator}`B_PREFERRED_APP_CHANGED`

	- {cpp:func}`SetPreferredApp() <BMimeType::SetPreferredApp>`

-
	- {cpp:enumerator}`B_ATTR_INFO_CHANGED`

	- {cpp:func}`SetAttrInfo() <BMimeType::SetAttrInfo>`

-
	- {cpp:enumerator}`B_FILE_EXTENSIONS_CHANGED`

	- {cpp:func}`SetFileExtensions() <BMimeType::SetFileExtensions>`

-
	- {cpp:enumerator}`B_SHORT_DESCRIPTION_CHANGED`

	- {cpp:func}`SetShortDescription() <BMimeType::SetShortDescription>`

-
	- {cpp:enumerator}`B_LONG_DESCRIPTION_CHANGED`

	- {cpp:func}`SetLongDescription() <BMimeType::SetLongDescription>`

-
	- {cpp:enumerator}`B_ICON_FOR_TYPE_CHANGED`

	- {cpp:func}`SetIconForType() <BMimeType::SetIconForType>`

-
	- {cpp:enumerator}`B_APP_HINT_CHANGED`

	- {cpp:func}`SetAppHint() <BMimeType::SetAppHint>`


:::

The {hclass}`BMimeType` methods are given for illustrative purposes only
—anything that alters the database for a MIME type will also trigger a
notification message. The {hparam}`be:extra_type` field is used only in the
{cpp:enumerator}`B_ICON_FOR_TYPE_CHANGED` message and indicates the
application signature for which the change is valid.

{hmethod}`StopWatching()` terminates the MIME monitor previously initiated
for the given {cpp:class}`BMessenger`.
::::

::::{abi-group}
:::{cpp:function} const char* BMimeType::Type() const
:::

:::{cpp:function} status_t BMimeType::GetSupertype(BMimeType* super) const
:::

{hmethod}`Type()` returns a pointer to the object's MIME string. If the
object isn't initialized, this returns a pointer to {cpp:expr}`NULL`.

{hmethod}`GetSupertype()` initializes the argument with this object's
supertype. (You can then call {hmethod}`Type()` on the argument to see the
supertype.) {hparam}`super` must be allocated before it's passed in. If
this object isn't initialized, {hparam}`super` is uninitialized.

The errors apply to {hmethod}`GetSupertype()` only.

:::{list-table}
---
header-rows: 1
align: left
widths: auto
---
-
	- Return Code

	- Description

-
	- {cpp:enumerator}`B_OK`.
	- Everything's fine.
-
	- {cpp:enumerator}`B_BAD_VALUE`.
	- This object isn't initialized.

:::
::::

## Operators

::::{abi-group}
:::{cpp:function} bool BMimeType::operator==(const BMimeType& type) const
:::

:::{cpp:function} bool BMimeType::operator==(const char* type) const
:::

Two MIME types are equal if they are both initialized to the same string
(without regard to case).
::::
