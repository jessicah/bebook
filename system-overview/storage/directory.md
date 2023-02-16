# BDirectory

A {cpp:class}`BDirectory` object gives you access to the contents of a
directory. A {cpp:class}`BDirectory`'s primary features are:

-   It can iteratively retrieve the entries in the directory. The entries are
returned as {cpp:class}`BEntry` objects, {htype}`entry_ref`s, or
{htype}`dirent` structures ({cpp:func}`GetNextEntry()
<BDirectory::GetNextEntry>`, {cpp:func}`GetNextRef()
<BDirectory::GetNextRef>`, {cpp:func}`GetNextDirents()
<BDirectory::GetNextDirents>`).

-   It can find a specific entry. You can ask if the entry exists
({cpp:func}`Contains() <BDirectory::Contains>`), and you can retrieve the
entry as a {cpp:class}`BEntry` ({cpp:func}`FindEntry()
<BDirectory::FindEntry>`).

-   It can create new entries. Through the aptly named {cpp:func}`CreateFile()
<BDirectory::CreateFile>`, {cpp:func}`CreateDirectory()
<BDirectory::CreateDirectory>` and {cpp:func}`CreateSymLink()
<BDirectory::CreateSymLink>` functions.

Unlike the other {cpp:class}`BNode` classes, a {cpp:class}`BDirectory`
knows its own entry ({cpp:func}`GetEntry() <BDirectory::GetEntry>`), and
can be initialized with a {htype}`node_ref` structure.

## Retrieving Entries

The {cpp:class}`BDirectory` functions that let you iterate over a
directory's entries are inherited from {cpp:class}`BEntryList`:

:::{code} cpp
status_t GetNextEntry(BEntry *entry, bool traverse = true);
status_t GetNextRef(entry_ref *ref);
int32 GetNextDirents(dirent *buf, size_t length,
                     int32 count = INT_MAX)
:::

For the basic story on these functions, see the {cpp:class}`BEntryList`
class and the function descriptions below. In addition to the info you'll
find there, you should be aware of the following:

-   Entries are returned in "directory order". This is, roughly, the ASCII
order of their names.

-   Try not to alter the directory while you're getting its entries. Entries
are delivered on demand. If you do something to change the contents of the
directory while you're iterating through those contents (such as change the
name of the file "aaa" to "zzz") you could end up seeing an entry more than
once (technically, you'll see the same node under the guise of different
entries), or you could miss an entry.

-   Counting entries uses the same iterator that retrieves entries. You
mustn't call {cpp:func}`CountEntries() <BDirectory::CountEntries>` while
you're looping over a {hmethod}`GetNext…()` function.

## Creating New Directories

To create a new directory, you can use {cpp:class}`BDirectory`'s
{cpp:func}`CreateDirectory() <BDirectory::CreateDirectory>` function. The
function creates a single new directory as identified by its argument. The
new directory will be a subdirectory of the invoked-upon
{cpp:class}`BDirectory`'s directory.

You can also create an entire path full of new directories through the
global {cpp:func}`create_directory() <create::directory>` function. This
convenient function attempts to create all "missing" directories along the
path that you pass in.

## Finding a Directory

The {cpp:func}`find_directory() <find::directory>` function gives you the
pathnames for pre-defined directories. These directories, such as those
that store Be-supplied applications and user-defined preferences settings,
are represented by directory_which constants. These constants are not
strings; you can't use them directly. You have to pass them through
{cpp:func}`find_directory() <find::directory>`.

Note that the {cpp:class}`BDirectory` class itself doesn't let you find
directories on the basis of the {ref}`directory_which` constants—you have
to use the {cpp:func}`find_directory() <find::directory>` function (which
is documented at the end of this class description).

## Node Monitoring a Directory

:::{admonition} Note
:class: note
The following description is a brief, directory-specific view into the
Node Monitor. For the full story, see "{ref}`The Node Monitor`" section of
this chapter.
:::

You can monitor changes to the contents of a directory by passing a
{cpp:class}`BDirectory`'s {htype}`node_ref` and the
{cpp:enumerator}`B_WATCH_DIRECTORY` flag to the Node Monitor's
{cpp:func}`watch_node() <watch::node>` function. As with all invocations of
{cpp:func}`watch_node() <watch::node>`, you also have to pass a
{cpp:class}`BMessenger` (the "target") that will receive the Node Monitor
notifications; here, we use {cpp:var}`be_app_messenger`:

:::{code} cpp
BDirectory dir("/boot/home");
node_ref nref;
status_t err;

if (dir.InitCheck() == B_OK) {
   dir.GetNodeRef(&nref);
   err = watch_node(&nref, B_WATCH_DIRECTORY, be_app_messenger);
   if (err != B_OK)
      /* handle the error */
}
:::

The following changes to the monitored directory cause
{cpp:class}`BMessage`s to be sent to the target. The {hparam}`what` field
for all Node Monitor messages is {cpp:enumerator}`B_NODE_MONITOR`; the
{hparam}`opcode` field (an integer code) describes the activity:

-   An entry was created ({hparam}`opcode` =
{cpp:enumerator}`B_ENTRY_CREATED`).

-   An entry was moved to a different name in the same directory
({cpp:enumerator}`B_ENTRY_RENAMED`).

-   An entry was from moved from this directory to a different directory, or
vice versa ({cpp:enumerator}`B_ENTRY_MOVED`).

-   An entry (and the node it represents) was deleted from the file system
({cpp:enumerator}`B_ENTRY_REMOVED`).

The {cpp:enumerator}`B_WATCH_DIRECTORY` flag (by itself) doesn't monitor
changes to the directory's own entry. For example, if you change the name
of the directory that you're monitoring, the target isn't sent a message.
If you want a {cpp:class}`BDirectory` to watch changes to itself, you have
to throw in one of the other Node Monitor flags
({cpp:enumerator}`B_WATCH_NAME`, {cpp:enumerator}`B_WATCH_STAT`, or
{cpp:enumerator}`B_WATCH_ATTR`).

The other fields in the Node Monitor message describe the entry that
changed. The set of fields depends on the opcode (the following is a
summary of the list given in "{cpp:func}`Notification Messages
<TheNodeMonitor::NotificationMessages>`" in the Node Monitor
documentation):

### B_ENTRY_CREATED

:::{list-table}
---
header-rows: 1
align: left
widths: auto
---
-
	- Field

	- Type

	- Description

-
	- {hparam}`device`

	- {cpp:enumerator}`B_INT32_TYPE`

	- {htype}`dev_t` of the directory's device.

-
	- {hparam}`directory`

	- {cpp:enumerator}`B_INT64_TYPE`

	- {htype}`ino_t` (node number) of the directory.

-
	- {hparam}`node`

	- {cpp:enumerator}`B_INT64_TYPE`

	- {htype}`ino_t` of the new entry's node.

-
	- {hparam}`name`

	- {cpp:enumerator}`B_STRING_TYPE`

	- The name of the new entry.


:::

### B_ENTRY_MOVED

The {hparam}`device`, {hparam}`node`, and {hparam}`name` fields are the
same as for {cpp:enumerator}`B_ENTRY_CREATED`, plus…

:::{list-table}
---
header-rows: 1
align: left
widths: auto
---
-
	- Field

	- Type

	- Description

-
	- {hparam}`from_directory`

	- {cpp:enumerator}`B_INT64_TYPE`

	- The {htype}`ino_t` number of the old directory.

-
	- {hparam}`to_directory`

	- {cpp:enumerator}`B_INT64_TYPE`

	- The {htype}`ino_t` number of the new directory.


:::

### B_ENTRY_REMOVED

The {cpp:enumerator}`B_ENTRY_REMOVED` message takes the same form as
{cpp:enumerator}`B_ENTRY_CREATED`, but without the {hparam}`name` field.
This, obviously, can be a problem—what good is it if you're told that a
file has been removed, but you're not told the file's name? In some cases,
simply being told that a file has been removed actually is good enough: You
can simply re-read the contents of the directory.
