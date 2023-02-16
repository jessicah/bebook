:::{cpp:class} BStatable
:::

# BStatable

## Member Functions

::::{abi-group}
:::{cpp:function} status_t BStatable::GetCreationTime(time_t* ctime) const
:::

:::{cpp:function} status_t BStatable::SetCreationTime(time_t ctime)
:::

:::{cpp:function} status_t BStatable::GetModificationTime(time_t* mtime) const
:::

:::{cpp:function} status_t BStatable::SetModificationTime(time_t mtime)
:::

:::{cpp:function} status_t BStatable::GetAccessTime(time_t* atime) const
:::

:::{cpp:function} status_t BStatable::SetAccessTime(time_t atime)
:::

:::{admonition} Warning
:class: warning
Access time is currently unused.
:::

These function let you get and set the time at which the item was created,
last modified, and last accessed (opened). The measure of time is given as
seconds since (the beginning of ) January 1, 1970.

:::{admonition} Note
:class: note
The time quanta that stat uses is seconds; the rest of the BeOS measures
time in microseconds ({htype}`bigtime_t`).
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
	- Success.
-
	- {cpp:enumerator}`B_NOT_ALLOWED`.
	- You tried to set a time field for a file on a read-only volume.
-
	- {cpp:enumerator}`B_NO_MEMORY`.
	- Couldn't get the necessary resources to complete the transaction.
-
	- {cpp:enumerator}`B_BAD_VALUE`.
	- The node doesn't exist (abstract entry).

:::
::::

::::{abi-group}
:::{cpp:function} status_t BStatable::GetNodeRef(node_ref* nref) const
:::

Copies the item's {htype}`node_ref` structure into the {hparam}`nref`
argument, which must be allocated.

Typically, you use an node's {htype}`node_ref` as a key to the Node
Monitor by passing the {htype}`node_ref` structure to the
{cpp:func}`watch_node() <watch::node>` function. The Node Monitor watches
the node for specific changes; see "{ref}`The Node Monitor`" section of
this chapter for details.

As a convenience, you can use a {htype}`node_ref` structure to initialize
a {cpp:class}`BDirectory` object (through the constructor or
{cpp:func}`BDirectory::SetTo` function).

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
	- Success.
-
	- {cpp:enumerator}`B_NO_MEMORY`.
	- Couldn't get the necessary resources to complete the transaction.
-
	- {cpp:enumerator}`B_BAD_VALUE`.
	- The node doesn't exist (abstract entry).

:::
::::

::::{abi-group}
:::{cpp:function} status_t BStatable::GetOwner(uid_t* owner) const
:::

:::{cpp:function} status_t BStatable::SetOwner(uid_t owner)
:::

:::{cpp:function} status_t BStatable::GetGroup(gid_t* group) const
:::

:::{cpp:function} status_t BStatable::SetGroup(gid_t group)
:::

:::{cpp:function} status_t BStatable::GetPermissions(mode_t* perms) const
:::

:::{cpp:function} status_t BStatable::SetPermissions(mode_t perms)
:::

These functions set and get the owner, group, and read/write/execute
permissions for the node:

-   The {hparam}`owner` identifier encodes the identity of the user that
"owns" the file.

-   The {hparam}`group` identifier encodes the "group" that is permitted group
access to the file (as declared by the permissions).

-   The {hparam}`permissions` value records nine "permission facts": Whether
the file can be read, written, and executed by the node's owner, by users
in the node's group, and by everybody else (read/write/execute *
owner/group/others = 9 items).

The {htype}`uid_t`, {htype}`gid_t`, and {htype}`mode_t` types used here
are standard POSIX types. All three are 32-bit unsigned integers and are
defined in posix/sys/types.h.

The owner and group encodings must match values found in the system's user
and group files (which are as currently unimplemented).

The permissions value is a combination of the following bitfield constants
(defined in posix/sys/stat.h):

-   {cpp:enumerator}`S_IRUSR` owner's read bit.

-   {cpp:enumerator}`S_IWUSR` owner's write bit.

-   {cpp:enumerator}`S_IXUSR` owner's execute bit.

-   {cpp:enumerator}`S_IRGRP` group's read bit.

-   {cpp:enumerator}`S_IWGRP` group's write bit.

-   {cpp:enumerator}`S_IXGRP` group's execute bit.

-   {cpp:enumerator}`S_IROTH` others' read bit.

-   {cpp:enumerator}`S_IWOTH` others' write bit.

-   {cpp:enumerator}`S_IXOTH` others' execute bit.

For example:

:::{code} cpp
/* Is a file readable by everybody? */
mode_t perms;
if (node.GetPermissions(&perms) < B_OK)
   /* handle the error... */

if (perms & S_ISROTH)
   // Yes it is
else
   // No it isn't
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
	- Success.
-
	- {cpp:enumerator}`B_NOT_ALLOWED`.
	- You tried to set permissions on a read-only volume.
-
	- {cpp:enumerator}`B_BAD_VALUE`.
	- The node doesn't exist (abstract entry).

:::
::::

::::{abi-group}
:::{cpp:function} status_t BStatable::GetSize(off_t* size) const
:::

Gets the size of the node's data portion (in bytes). Only the "used"
portions of the node's file blocks are counted; the amount of storage the
node actually requires (i.e. the number of blocks the node consumes) may be
larger than the size given here.

The size measurement doesn't include the node's attributes.

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
	- Success.
-
	- {cpp:enumerator}`B_NO_MEMORY`.
	- Couldn't get the necessary resources to complete the transaction.
-
	- {cpp:enumerator}`B_BAD_VALUE`.
	- The node doesn't exist (abstract entry).

:::
::::

::::{abi-group}
:::{cpp:function} virtual status_t BStatable::GetStat(struct stat* st) const
:::

{hmethod}`GetStat()` returns the {ref}`stat` structure for the node. The
structure is copied into the {hparam}`st` argument, which must be
allocated. The {hclass}`BStatable` object does not cache the {htype}`stat`
structure; every time you call {hmethod}`GetStat()`, fresh stat information
is retrieved.

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
	- Success.
-
	- {cpp:enumerator}`B_NO_MEMORY`.
	- Couldn't get the necessary resources to complete the transaction.
-
	- {cpp:enumerator}`B_BAD_VALUE`.
	- The node doesn't exist (abstract entry).

:::
::::

::::{abi-group}
:::{cpp:function} bool BStatable::IsFile() const
:::

:::{cpp:function} bool BStatable::IsDirectory() const
:::

:::{cpp:function} bool BStatable::IsSymLink() const
:::

These functions return true if the node is a plain file, a directory, or a
symbolic link, respectively.
::::
