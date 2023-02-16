# BAppFileInfo

{cpp:class}`BAppFileInfo` lets you get and set the signature, supported
types, icons, app flags, and version info that's stored in an executable
file's attributes and/or resources. The object also knows how to write
certain particles of information into the File Type database and, if the
executable is the progenitor of a running application, into the app roster
({cpp:var}`be_roster`).

:::{admonition} Warning
:class: warning
Most apps won't ever need to create or use a {cpp:class}`BAppFileInfo`
object. Setting an executable's info is best left to the file's creator,
through the use of resource data that's compiled into the executable. Even
the act of looking at a file's info should be rare for a normal
application.
:::

:::{admonition} Warning
:class: warning
{cpp:class}`BAppFileInfo` objects should only be used to examine and set
the characteristics of applications and add-ons. Using the object on a
non-executable file could corrupt the file.
:::

## Initialization

You initialize a {cpp:class}`BAppFileInfo` object by passing it a
{cpp:class}`BFile` object that represents an application or add-on. The
{cpp:class}`BFile` needn't be open for reading, but it must be open for
writing if you want to set information. The {cpp:class}`BAppFileInfo`
object doesn't take over ownership of the {cpp:class}`BFile` that you pass
it; in particular, deleting a {cpp:class}`BAppFileInfo` doesn't cause the
underlying {cpp:class}`BFile` to be deleted.

To initialize a {cpp:class}`BAppFileInfo` to point to the executable of
{cpp:var}`be_app`, you do this:

:::{code} cpp
/* To get app file info for be_app. */
app_info appInfo;
BFile file;
BAppFileInfo appFileInfo;

be_app->GetAppInfo(&appInfo);
file.SetTo(&appInfo.ref, B_READ_WRITE);
appFileInfo.SetTo(&file);
:::

## Attributes, Resources, and the File Type Database

When you ask a {cpp:class}`BAppFileInfo` object to get some information,
it looks in its {cpp:class}`BFile`'s attributes; if the information isn't
there, it then looks in the file's resources. When you ask it to set some
information, the info is written as an attribute and also stored as a
resource. You can modify this behavior through {cpp:func}`SetInfoLocation()
<BAppFileInfo::SetInfoLocation>`: You can tell the object to only access
the file's attributes, or to only access the resources.

The signature, icons, and supported types that you set through the
functions provided here ( {cpp:func}`SetSignature()
<BAppFileInfo::SetSignature>`, {cpp:func}`SetIcon()
<BAppFileInfo::SetIcon>`, {cpp:func}`SetIconForType()
<BAppFileInfo::SetIconForType>`, {cpp:func}`SetSupportedTypes()
<BAppFileInfo::SetSupportedTypes>`) are also recorded in the File Types
database, as described in the various functions.

## Functions Inherited From BNodeInfo

You should take care when using the following functions (inherited from
{cpp:class}`BNodeInfo`):

SetPreferredApp()

: Never set an application's preferred app; an application is automatically
set to be its own preferred app&mdash;it won't work otherwise. An add-on's
preferred app is usually itself, but it doesn't have to be. For example,
you could set an add-on's preferred app to be the server or application
that loads the add-on.

SetType()

: Never set the type of an application or add-on. The type is automatically
set to be {cpp:enumerator}`B_APP_MIME_TYPE` (a platform-dependent value).
If you change the type, your application or add-on will still run
(probably), but other parts of the system (double-clicked documents, for
example) may have a hard time finding it.

## Errors

When you ask a {cpp:class}`BAppFileInfo` to retrieve information by
reference, the object doesn't clear the reference argument if it fails.
Because of this, you should always check the error code that's returned by
the {hmethod}`Get…()` functions.

The common errors that {hclass}`BAppFileInfo` functions return are these:

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
	- {cpp:enumerator}`B_OK`
	- Success.
-
	- {cpp:enumerator}`B_NO_INIT`
	- The {cpp:class}`BAppFileInfo` is uninitialized, or its {cpp:class}`BFile`
		isn't open for writing.
-
	- {cpp:enumerator}`B_ERROR`
	- The {cpp:class}`BFile` was locked when you initialized the
		{cpp:class}`BAppFileInfo`.

:::

The info-reading and -writing functions may also return the error codes
declared by {cpp:func}`BNode::ReadAttr` and {cpp:func}`BNode::WriteAttr` ,
and by {cpp:func}`BResources::WriteTo`.
