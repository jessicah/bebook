# BAppFileInfo
## Constructor and Destructor
::::{abi-group}

:::{cpp:function} BAppFileInfo::BAppFileInfo()
:::
:::{cpp:function} BAppFileInfo::BAppFileInfo(BFile* file)
:::

The default constructor creates a new, uninitialized {hclass}`BAppFileInfo` object.
To initialize you have to follow this construction with a call to
{cpp:func}`~BAppFileInfo::SetTo`.

The {cpp:class}`BFile`
version intializes the {hclass}`BAppFileInfo` by passing the argument to
{cpp:func}`~BAppFileInfo::SetTo`.

::::

::::{abi-group}

:::{cpp:function} BAppFileInfo::~BAppFileInfo()
:::

Destroys the object. The {cpp:class}`BFile`
that was used to initialize this object isn't touched.

::::

## Member Functions
::::{abi-group}

:::{cpp:function} status_t BAppFileInfo::GetAppFlags(uint32* flags) const
:::
:::{cpp:function} status_t BAppFileInfo::SetAppFlags(uint32 flags)
:::

These functions get and set the executable's "app flags." These are the
constants that determine whether an executable can only be launched once,
whether it runs in the background, and so on. The app flag constants are
defined in
app/Roster.h;
the flags must include one of the following…

- {cpp:enum}`B_SINGLE_LAUNCH`
- {cpp:enum}`B_MULTIPLE_LAUNCH`
- {cpp:enum}`B_EXCLUSIVE_LAUNCH`

…plus either of these two:

- {cpp:enum}`B_BACKGROUND_APP`
- {cpp:enum}`B_ARGV_ONLY`

See the {cpp:class}`BApplication`
class for details on the meanings of these constants.

:::{list-table}
---
header-rows: 1
---
-
	- Return Code
	- Description
-
	- {cpp:enum}`B_OK`
	- Everything went fine.
-
	- {cpp:enum}`B_NO_INIT`
	- The object is not properly initialized.
-
	- {cpp:enum}`B_BAD_VALUE`
	- {cpp:enum}`NULL` flags.
-
	- {cpp:enum}`B_BAD_TYPE`
	- The attribute/resources the flags are stored in have the wrong type.
-
	- {cpp:enum}`B_ENTRY_NOT_FOUND`
	- No application flags are set on the file.
:::
::::

::::{abi-group}

:::{cpp:function} status_t BAppFileInfo::GetIcon(BBitmap* icon, icon_size which) const
:::
:::{cpp:function} status_t BAppFileInfo::SetIcon(BBitmap* icon, icon_size which)
:::
:::{cpp:function} status_t BAppFileInfo::GetIconForType(const char* file_type, BBitmap* icon, icon_size which) const
:::
:::{cpp:function} status_t BAppFileInfo::SetIconForType(const char* file_type, BBitmap* icon, icon_size which)
:::

{hmethod}`GetIcon()` and {hmethod}`SetIcon()`
get and set the icons that are represent the
executable. {hmethod}`GetIconForType()` and {hmethod}`SetIconForType()` get and set the icons
that the executable uses when it writes (or otherwise "takes possession
of") a file of the given type, identified by {hparam}`file_type`. You specify which
icon you want (large or small) by passing {cpp:enum}`B_LARGE_ICON` or {cpp:enum}`B_MINI_ICON` as
the {hparam}`which` argument.

The icon is passed in or returned through the icon argument. The bitmap
must be the proper size: 32x32 for the large icon, 16x16 for the small
one. In {cpp:class}`BRect` lingo, that's
`BRect(0, 0, 31, 31)` and
`BRect(0, 0, 15, 15)`.
The bitmap's color space must be {cpp:enum}`B_CMAP8`. For example:

:::{code}
BBitmap* bitmap = new BBitmap(BRect(0,0,31,31), B_CMAP8);
appFileInfo.GetIcon(bitmap, B_LARGE_ICON);
:::

You can remove an icon by passing {cpp:enum}`NULL` as the {hparam}`icon`
argument to {hmethod}`SetIcon()`.

:::{admonition} Note
:class: note
To create a {cpp:class}`BBitmap`
you must have a {cpp:func}`~BApplication::be`
object ; the object needn't be running.
:::
:::{list-table}
---
header-rows: 1
---
-
	- Return Code
	- Description
-
	- {cpp:enum}`B_OK`.
	- Success
-
	- {cpp:enum}`B_BAD_VALUE`.
	- ({hmethod}`Get…()`) {cpp:enum}`NULL` {hclass}`BBitmap`, or invalid {hparam}`file_type`.
-
	- {cpp:enum}`B_BAD_VALUE`.
	- ({hmethod}`Set…()`) The bitmap data isn't the proper size.
-
	- {cpp:enum}`B_NO_INIT`.
	- The object is not properly initialized.
:::
::::

::::{abi-group}

An application's preferred app must be itself; an add-on is more flexible. For syntax, see
{cpp:func}`BNodeInfo::SetPreferredApp`.

::::

::::{abi-group}

:::{cpp:function} status_t BAppFileInfo::GetSignature(char* signature) const
:::
:::{cpp:function} status_t BAppFileInfo::SetSignature(const char* signature)
:::

These functions get and set the executable's MIME type signature. The
{hparam}`signature` buffer you pass to {hmethod}`GetSignature()` should be at least
{cpp:enum}`B_MIME_TYPE_LENGTH` characters long; the
{hmethod}`SetSignature()` buffer must be no
longer than that.

When you set an executable's signature, the signature is installed in the
File Type database if it's not there already. The old signature isn't
removed from the database.

:::{list-table}
---
header-rows: 1
---
-
	- Return Code
	- Description
-
	- {cpp:enum}`B_OK`.
	- Success.
-
	- {cpp:enum}`B_ENTRY_NOT_FOUND`.
	- ({hmethod}`Get…()`) The executable doesn't have a signature.
-
	- {cpp:enum}`B_BAD_VALUE`.
	- ({hmethod}`Set…()`) {hparam}`signature` is too long.
:::
::::

::::{abi-group}

:::{cpp:function} status_t BAppFileInfo::GetSupportedTypes(BMessage* types) const
:::
:::{cpp:function} status_t BAppFileInfo::SetSupportedTypes(const BMessage* types)
:::
:::{cpp:function} status_t BAppFileInfo::SetSupportedTypes(const BMessage* types, bool sync_all)
:::

These functions get and set the MIME file types that this executable can
read and/or write. The {hparam}`types`
{cpp:class}`BMessage` that you pass in looks like this:

FieldTypeDescriptiontypes (array)B_STRING_TYPEAn array of MIME strings.

{hmethod}`GetSupportedTypes()` copies the types
into the types field;
{hmethod}`SetSupportedTypes()` reads them from the field. The message's command
constants (its what value) is ignored.

Here we print an executable's supported types:

:::{code}
BMessage msg;
uint32 i=0;
char* ptr;
if (appFileInfo.GetSupportedTypes(&msg) != B_OK)
   /* Handle the error. */
while (msg.FindString("types", i++, &ptr) == B_OK)
   printf("> Supported Type: %sn", ptr);
:::

If {hmethod}`SetSupportedTypes()` names a type that doesn't already appear in the
File Type database, the new type is added to the database and its
preferred handler is set to the executable that this {hclass}`BAppFileInfo` object
represents.

:::{admonition} Warning
:class: warning
{hmethod}`SetSupportedTypes()` clobbers an executable's existing set of supported
types. If you want to augment an executable's supported types, you should
retrieve the existing set, add the new ones, and then call
{hmethod}`SetSupportedTypes()`.
:::
:::{list-table}
---
header-rows: 1
---
-
	- Return Code
	- Description
-
	- {cpp:enum}`B_OK`.
	- Success.
-
	- {cpp:enum}`B_NO_MEMORY`.
	- Insufficient memory to copy the types.
:::

See Also:
{cpp:func}`~BAppFileInfo::Supports`

::::

::::{abi-group}

Implementation detail; see "{cpp:func}`~BAppFileInfo::Functions`". An
executable's default file type (for both applications and add-ons) is
{cpp:enum}`B_APP_MIME_TYPE`. This value mustn't be changed. For syntax, see
{cpp:func}`BNodeInfo::SetType`.

::::

::::{abi-group}

:::{cpp:function} status_t BAppFileInfo::GetVersionInfo(version_info* info, version_kind kind) const
:::
:::{cpp:function} status_t BAppFileInfo::SetVersionInfo(const version_info* info, version_kind kind)
:::

The functions get and set the application's "version info." The
information is recorded in the version_info structure:

:::{code}
struct version_info {
   uint32 major;
   uint32 middle;
   uint32 minor;
   uint32 variety;
   uint32 internal;
   char short_info[64];
   char long_info[256];
}
:::

The field names (and types) provide suggestions for the type of info they
want to store.

There are two kinds of version info, as specified by the {hparam}`kind` argument:

:::{list-table}
---
header-rows: 1
---
-
	- Constant
	- Description
-
	- {cpp:enum}`B_APP_VERSION_KIND`
	- Provides information about this specific app.
-
	- {cpp:enum}`B_SYSTEM_VERSION_KIND`
	- Provides information about the "suite," or other grouping of apps, that this app belongs to.
:::

Again, the uses of the two kinds is up to the app
developer—currently, nothing in the BeOS depends on any information
being stored in either version_info structure.

:::{list-table}
---
header-rows: 1
---
-
	- Return Code
	- Description
-
	- {cpp:enum}`B_OK`.
	- The version_info was found or set.
-
	- {cpp:enum}`B_ENTRY_NOT_FOUND`.
	- ({hmethod}`Get…()`) the app doesn't have the requested version info.
:::
::::

::::{abi-group}

:::{cpp:function} status_t BAppFileInfo::InitCheck() const
:::

Returns the status of the most recent initialization.

:::{list-table}
---
header-rows: 1
---
-
	- Return Code
	- Description
-
	- {cpp:enum}`B_OK`.
	- The object was successfully initialized.
-
	- {cpp:enum}`B_BAD_VALUE`.
	- The object is uninitialized.
:::
::::

::::{abi-group}

:::{cpp:function} bool BAppFileInfo::IsSupportedType(const char* type) const
:::
:::{cpp:function} bool BAppFileInfo::Supports(BMimeType* type) const
:::

Returns {cpp:enum}`true` if the app supports the given MIME type and {cpp:enum}`false` if it
doesn't. {hmethod}`IsSupportedType()` always returns {cpp:enum}`true` if the application
supports "application/octet-stream", while {hmethod}`Supports()` returns {cpp:enum}`true` only
if {hparam}`type` is explicitly supported.

See Also:
{cpp:func}`~BAppFileInfo::GetSupportedTypes`,
{cpp:func}`~BAppFileInfo::SetSupportedTypes`

::::

::::{abi-group}

:::{cpp:function} void BAppFileInfo::SetInfoLocation(info_location loc)
:::
:::{cpp:function} bool BAppFileInfo::IsUsingAttributes() const
:::
:::{cpp:function} bool BAppFileInfo::IsUsingResources() const
:::

{hmethod}`SetInfoLocation()` sets the location where
the {hclass}`BAppFileInfo` object stores
its information. It can store them as either attributes, resources, or
both. {hparam}`loc` takes the following values:

- {cpp:enum}`B_USE_ATTRIBUTES`
- {cpp:enum}`B_USE_RESOURCES`
- {cpp:enum}`B_USE_BOTH`

{hmethod}`IsUsingAttributes()` and {hmethod}`IsUsingResources()`
return {cpp:enum}`true` if the
{hclass}`BAppFileInfo` object is storing information in the designated location and
{cpp:enum}`false` otherwise.

::::

::::{abi-group}

:::{cpp:function} status_t BAppFileInfo::SetTo(BFile* file)
:::

Initializes the {hclass}`BAppFileInfo` object by pointing it
to {hparam}`file`, which must be a valid (initialized)
{cpp:class}`BFile` object, and
must not be locked. The {hclass}`BFile` is
not copied, or re-opened by {hclass}`BAppFileInfo`. In particular, the {hclass}`BAppFileInfo`
uses {hparam}`file`'s file descriptor, and doesn't destroy the {hclass}`BFile` object when it
(the {hclass}`BAppFileInfo`) is destroyed or reinitialized.

:::{admonition} Warning
:class: warning
The {hclass}`BAppFileInfo` object doesn't check to make sure that the file that
you pass in really is an executable. Passing in a non-executable (a plain
file, a directory, etc.) could corrupt the file.
:::
:::{list-table}
---
header-rows: 1
---
-
	- Return Code
	- Description
-
	- {cpp:enum}`B_OK`.
	- The object was successfully initialized.
-
	- {cpp:enum}`B_BAD_VALUE`.
	- {hparam}`file` is invalid (uninitialized).
:::
::::

## Constants
::::{abi-group}



Declared in: storage/AppFileInfo.h

:::{list-table}
---
header-rows: 1
---
-
	- Constant
	- Description
-
	- {cpp:enum}`B_APP_VERSION_KIND`
	- Records information about a specific application.
-
	- {cpp:enum}`B_SYSTEM_VERSION_KIND`
	- Records information about a "suite," or other grouping of applications, that the application belongs to.
:::

These constants are used when setting or retrieving the version
information attached to an application. There are two version information
records for each application, and these two constants select which one
you wish to reference. Although there is no prescribed use for these
structures or their constants, it is suggested that {cpp:enum}`B_APP_VERSION_KIND` be
used for application-specific version information, and
{cpp:enum}`B_SYSTEM_VERSION_KIND` be used for information about the suite of
applications to which the application belongs.

::::

## Defined Types
::::{abi-group}


Declared in: storage/AppFileInfo.h

:::{code}
struct version_info {
    uint32    major;
    uint32    middle;
    uint32    minor;
    uint32    variety;
    uint32    internal;
    char      short_info[64];
    char      long_info[256];
}
:::

The version_info structure is used to contain version information about
an application. Although none of these fields have prescribed uses, and
you can use them for anything you want, their names do hint at their
suggested uses.

::::
