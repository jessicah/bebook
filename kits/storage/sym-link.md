:::{cpp:class} BSymLink
:::

# BSymLink

## Constructor and Destructor

::::{abi-group}
:::{cpp:function} BSymLink::BSymLink()
:::

:::{cpp:function} BSymLink::BSymLink(const entry_ref* ref)
:::

:::{cpp:function} BSymLink::BSymLink(const BEntry* entry)
:::

:::{cpp:function} BSymLink::BSymLink(const char* path)
:::

:::{cpp:function} BSymLink::BSymLink(const BDirectory* dir, const char* path)
:::

:::{cpp:function} BSymLink::BSymLink(const BSymLink& link)
:::

Creates a new {hclass}`BSymLink` object, initializes it according to the
arguments, and sets {cpp:func}`InitCheck() <BNode::InitCheck>` to return
the status of the initialization.

-   The default constructor does nothing and sets {cpp:func}`InitCheck()
<BNode::InitCheck>` to {cpp:enumerator}`B_NO_INIT`. To initialize the
object, call {cpp:func}`SetTo() <BNode::SetTo>`.

-   The copy constructor creates a new {hclass}`BSymLink` that's open on the
same node as that of the argument.

-   For information on the other constructors, see the analogous
{cpp:func}`SetTo() <BNode::SetTo>` functions in the {cpp:class}`BNode`
class; {hclass}`BSymLink` inherits them without change.
::::

::::{abi-group}
:::{cpp:function} virtual BSymLink::~BSymLink()
:::

Closes the object's file descriptor and destroys the object.
::::

## Member Functions

::::{abi-group}
:::{cpp:function} bool BSymLink::IsAbsolute()
:::

Returns {cpp:expr}`true` if the symlink contains an absolute pathname.
::::

::::{abi-group}
:::{cpp:function} ssize_t BSymLink::MakeLinkedPath(const BDirectory* dir, BPath* path) const
:::

:::{cpp:function} ssize_t BSymLink::MakeLinkedPath(const char* dirPath, BPath* path) const
:::

This function creates an absolute pathname to the linked-to entry and
returns it as a {cpp:class}`BPath` object. For this to work you have to
tell the object which directory you want to reckon off of (in case the
symlink specifies a relative path). This should be the directory in which
the symlink itself lives.

:::{admonition} Note
:class: note
Remember—a {hclass}`BSymLink` is a node, and nodes don't know what
directory they live in. That's why you have to tell it here.
:::

If the symlink contains an absolute path, then the {hparam}`dir` or
{hparam}`dirPath` arguments are ignored. Nonetheless, they must be
supplied.

The function returns the length of the pathname that's set in
{cpp:class}`BPath` (or an error).

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
	- {cpp:enumerator}`B_FILE_ERROR`.
	- The object is uninitialized.
-
	- {cpp:enumerator}`B_BAD_VALUE`.
	- The object doesn't refer to a symlink, or {hparam}`dir`/{hparam}`dirPath`
		is {cpp:expr}`NULL`.
-
	- {cpp:enumerator}`B_NAME_TOO_LONG`.
	- They concatenated pathname is too long.

:::
::::

::::{abi-group}
:::{cpp:function} ssize_t BSymLink::ReadLink(char* buf, size_t length)
:::

Copies the contents of the symlink into {hparam}`buf`. {hparam}`length` is
the size of the buffer; to be perfectly safe, the buffer should be
{cpp:enumerator}`B_PATH_NAME_LENGTH` characters long. The function returns
the number of bytes that were copied (or it returns an error).

The symlink's contents is the pathname (relative or absolute) to the
linked-to entry. Note that since the pathname might be relative,
{hmethod}`ReadLink()` can't give you a {cpp:class}`BPath` object. If you
want a {cpp:class}`BPath` to the linked-to entry, see
{cpp:func}`MakeLinkedPath() <BSymLink::MakeLinkedPath>`.

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
	- {cpp:enumerator}`B_FILE_ERROR`.
	- The object is uninitialized.
-
	- {cpp:enumerator}`B_BAD_VALUE`.
	- The object doesn't refer to a symlink.

:::
::::
