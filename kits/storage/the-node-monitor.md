# The Node Monitor

Declared in: storage/NodeMonitor.h

The Node Monitor is a service that lets you ask to be notified of certain
file system changes. You can ask to be told when a change is made to…

-   The contents of a specific directory.

-   The name of a specific entry.

-   Any stat field of a specific entry.

-   Any attribute of a specific entry.

You can also ask to be notified when…

-   Volumes are mounted and unmounted.

:::{admonition} Note
:class: note
Volume monitoring is also provided by the {cpp:class}`BVolumeRoster`
class: {cpp:class}`BVolumeRoster` can talk to the Node Monitor for you. The
{cpp:class}`BVolumeRoster` volume-watching API is more humane than that
which you'll find here.
:::

When something interesting happens, the Node Monitor lets you know by
sending a {cpp:class}`BMessage` to the target of your choice.

## Node Monitor Functions

There are two Node Monitor functions, watch_node() and stop_watching().
The names are a wee bit misleading, so before we go on to the full
technical descriptions, let's nip some buds:

-   {cpp:func}`watch_node() <watch::node>` tells the Node Monitor to start
__or stop__ watching a __specific__ node, or to watch for volumes being
mounted and unmounted. Memorize the emphasized words.

-   {cpp:func}`stop_watching() <stop::watching>` tells the Node Monitor to
stop sending notifications to a particular target.

::::{abi-group}
:::{cpp:function} status_t The Node Monitor::watch_node(const node_ref* nref, uint32 flags, BMessenger messenger)
:::

:::{cpp:function} status_t The Node Monitor::watch_node(const node_ref* nref, uint32 flags, const BHandler* handler, const BLooper* looper = NULL)
:::

watch_node() tells the Node Monitor to…

-   …start paying attention to the node specified by the {cpp:func}`node_ref
<node::ref>` argument. If you're watching for volumes (only),
{hparam}`nref` can be {cpp:expr}`NULL`. The easiest way to get a
{cpp:func}`node_ref <node::ref>` is to invoke
{cpp:func}`BStatable::GetNodeRef` on any {cpp:class}`BEntry` or
{cpp:class}`BNode` object.

-   The {hparam}`flags` argument lists the changes that you want the Monitor
to pay attention to. See below for details.

-   The target of the change notification messages is specified either as a
{cpp:class}`BMessenger`, or as a {cpp:class}`BHandler` /
{cpp:class}`BLooper` pair. (The target specification follows the
{cpp:func}`BInvoker::SetTarget` protocol; see the {cpp:class}`BInvoker`
class for details.) The notification shows up as a {cpp:class}`BMessage` in
the target's {cpp:func}`MessageReceived() <BHandler::MessageReceived>`
function.

:::{admonition} Note
:class: note
You can't tell the Node Monitor to send its notifications to another
application. Currently, the {cpp:class}`BMessenger` that you specify must
identify a target in the caller's team.
:::

Jumping ahead a bit, here's a sample function that tells the Node Monitor
to watch for name and attribute changes to a given entry. The Monitor's
notifications will be sent to the application's main loop:

:::{code} cpp
status_t WatchThis(BEntry *entry)
{
   node_ref nref;
   entry->GetNodeRef(&nref);
   return (watch_node(&nref,
            B_WATCH_NAME | B_WATCH_ATTR,
            be_app_messenger));
}
:::

#### Monitor Flags















watch_node()'s {hparam}`flags` argument is a combination of the following

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
	- {cpp:enumerator}`B_WATCH_NAME`
	- Watches for name changes. This includes moving the node to a different
		directory, or removing the node altogether.
-
	- {cpp:enumerator}`B_WATCH_STAT`
	- Watches for any change to the node's {htype}`stat` structure. This
		includes changes to the size, modification date, owner, and so on. See
		"The stat Structure" in the {cpp:class}`BStatable` class for a description
		of what's in the {htype}`stat` structure.
-
	- {cpp:enumerator}`B_WATCH_ATTR`
	- Watches for changes to any of the node's attributes. This includes adding
		and removing attributes.
-
	- {cpp:enumerator}`B_WATCH_DIRECTORY`
	- Only applies to nodes that are directories. The flag tells the Monitor to
		watch for changes (new entries, entry deletions, entries being renamed) to
		the directory. (You can apply the other flags to a directory, as well).
		It's not an error to set {cpp:enumerator}`B_WATCH_DIRECTORY` on a node that
		isn't a directory—but it doesn't do anything for you.
-
	- {cpp:enumerator}`B_WATCH_ALL`.
	- This is a convenience that combines all the above.
-
	- {cpp:enumerator}`B_WATCH_MOUNT`
	- Watches for volumes being mounted and unmounted. As mentioned above, the
		{hparam}`nref` argument isn't needed (it can be {cpp:expr}`NULL`) if all
		you're doing is watching volumes. {cpp:enumerator}`B_WATCH_MOUNT` isn't
		included in {cpp:enumerator}`B_WATCH_ALL`.

:::

There's one other constant, which lives in a class by itself:

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
	- {cpp:enumerator}`B_STOP_WATCHING`
	- Tells the Node Monitor to stop watching the {hparam}`nref` argument.

:::

You can't combine {cpp:enumerator}`B_STOP_WATCHING` with any of the others
in an attempt to stop watching a specific category of changes. For example,
if you call…

:::{code} cpp
watch_node(&nref, B_WATCH_STAT, be_app_messenger);
watch_node(&nref, B_WATCH_ATTR, be_app_messenger);
:::

…and then call…

:::{code} cpp
watch_node(&nref, B_STOP_WATCHING, be_app_messenger);
:::

…both of the previous Monitor calls are stopped.

:::{admonition} Warning
:class: warning
{cpp:enumerator}`B_STOP_WATCHING` does not apply to volume watching. The
only way to stop monitoring volume un/mounts is to call stop_watching().
:::

#### Combining Flags and the 4096 Limit

If you can, you should combine as many flags as you're going to need in
single calls to watch_node(). Recall the example used above:

:::{code} cpp
watch_node(&nref,
    B_WATCH_NAME | B_WATCH_ATTR,
    be_app_messenger);
:::

This is better than making separate watch_node() calls (one to pass
{cpp:enumerator}`B_WATCH_NAME` and another to pass
{cpp:enumerator}`B_WATCH_ATTR`)—not only because the single call is
naturally more efficient than two, but also because the Node Monitor can
only monitor 4096 nodes per team at a time. Every call to watch_node()
consumes a Node Monitor slot, even if you're already monitoring the
requested node.

If you want to watch all aspects of a node, just pass
{cpp:enumerator}`B_WATCH_ALL` to every watch_node() call. This will consume
only a single Node Monitor slot.

#### Notification Messages

A {cpp:class}`BMessage` notification sent by the Node Monitor looks like
this:

-   The {hparam}`what` value is {cpp:enumerator}`B_NODE_MONITOR`.

-   The field named {hparam}`opcode` is an {htype}`int32` constant that tells
you what happened.

-   Additional fields give you information (device, node, name, and so on)
about the node (or volume) that it happened to.

The {hparam}`opcode` constants and additional fields are described in
"{ref}`Opcode Constants`." In general, the opcodes correspond to the flags
that you passed to watch_node(); however, this correspondence isn't always
one-to-one.

There are seven opcode constants:

-   {cpp:enumerator}`B_ENTRY_CREATED`

-   {cpp:enumerator}`B_ENTRY_REMOVED`

-   {cpp:enumerator}`B_ENTRY_MOVED`

-   {cpp:enumerator}`B_STAT_CHANGED`

-   {cpp:enumerator}`B_ATTR_CHANGED`

-   {cpp:enumerator}`B_DEVICE_MOUNTED`

-   {cpp:enumerator}`B_DEVICE_UNMOUNTED`

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
	- The Node Monitor is off and running.
-
	- {cpp:enumerator}`B_BAD_VALUE`.
	- Bad {hparam}`nref` argument (not applicable to mount-only watches), or
		poorly formed target.
-
	- {cpp:enumerator}`B_NO_MEMORY`.
	- Couldn't allocate resources, or out of Node Monitor slots.
-
	- {cpp:enumerator}`B_ERROR`.
	- Some cases of bad {hparam}`nref` arguments erroneously return
		{cpp:enumerator}`B_ERROR`. This will be fixed.

:::
::::

::::{abi-group}
:::{cpp:function} status_t (BMessenger messenger)
:::

:::{cpp:function} status_t (const BHandler* handler, const BLooper* looper = NULL)
:::

Tells the Node Monitor to stop sending notifications to the target
described by the arguments. All the Node Monitor "slots" that were
allocated to the target are freed. Keep in mind that are only 4096 slots
for the entire system.

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
	- The target is now out of the Node Monitor loop.
-
	- {cpp:enumerator}`B_BAD_VALUE`.
	- Badly formed target description.

:::
::::

## Opcode Constants

The following sections describe the "opcode" constants; these are the
values that appear in the {hparam}`opcode` field of the
{cpp:class}`BMessage`s that are generated by the Node Monitor. Note that in
these descriptions, the use of the terms "entry" and "node" is sometimes
blurred.

Declared in: storage/NodeMonitor.h

::::{abi-group}
:::{cpp:enumerator} B_ENTRY_CREATED
:::

A completely new entry was created in a monitored directory. (This doesn't
include entries that are moved into this directory from some other
directory—see {cpp:enumerator}`B_ENTRY_MOVED`.)

You get this notification if you applied
{cpp:enumerator}`B_WATCH_DIRECTORY` to the directory in which the entry was
created. The message's fields are:

:::{list-table}
---
header-rows: 1
align: left
widths: auto
---
-
	- Field

	- Type code

	- Description

-
	- {hparam}`opcode`

	- {cpp:enumerator}`B_INT32_TYPE`

	- {cpp:enumerator}`B_ENTRY_CREATED`

-
	- {hparam}`name`

	- {cpp:enumerator}`B_STRING_TYPE`

	- The name of the new entry.

-
	- {hparam}`directory`

	- {cpp:enumerator}`B_INT64_TYPE`

	- The {htype}`ino_t` (node) number for the directory in which the entry was
created.

-
	- {hparam}`device`

	- {cpp:enumerator}`B_INT32_TYPE`

	- The {htype}`dev_t` number of the device on which the new entry resides.

-
	- {hparam}`node`

	- {cpp:enumerator}`B_INT64_TYPE`

	- The {htype}`ino_t` number of the new entry itself. (More accurately, it
identifies the node that corresponds to the entry.)


:::

#### Parsing and Tricks

In your code, you would parse a {cpp:enumerator}`B_ENTRY_CREATED` message
like this:

:::{code} cpp
void MyTarget::MessageReceived(BMessage *msg)
{
   int32 opcode;
   dev_t device;
   ino_t directory;
   ino_t node;
   const char *name;

   if (msg->what == B_NODE_MONITOR) {
      if (msg->FindInt32("opcode", &opcode) == B_OK) {
         switch (opcode) {
            case B_ENTRY_CREATED:
               msg->FindInt32("device", &device);
               msg->FindInt64("directory", &directory);
               msg->FindInt64("node", &node);
               msg->FindString("name", &name);
               break;
            ...
:::

So, what do you do with these fields?

#### Create an entry_ref to the entry.

The {hparam}`device`, {hparam}`directory`, and {hparam}`name` fields can
be used to create an {htype}`entry_ref` to the new entry:

:::{code} cpp
entry_ref ref;
const char *name;
...
msg->FindInt32("device", &ref.device);
msg->FindInt64("directory", &ref.directory);
msg->FindString("name", &name);
ref.set_name(name);
:::

#### Create a node_ref to the entry.

If you want to start Node Monitoring the new entry (or, more accurately,
the node of the new entry), you stuff {hparam}`device` and
{hparam}`directory` into a {htype}`node_ref`:

:::{code} cpp
node_ref nref;
status_t err;

...
msg->FindInt32("device", &nref.device);
msg->FindInt64("node", &nref.node);

err = watch_node(&nref, B_WATCH_ALL, be_app_messenger);
:::

#### Create a node_ref to the entry's parent.

Note that the {hparam}`directory` field is a node number. By combining
this number with the {hparam}`device` field, you can create a
{htype}`node_ref` that points to the entry's parent. From there, you're a
{cpp:func}`SetTo() <BDirectory::SetTo>` away from a {cpp:class}`BDirectory`
object:

:::{code} cpp
node_ref nref;
BDirectory dir;
status_t err;

...
msg->FindInt32("device", &nref.device);
msg->FindInt64("directory", &nref.node);
err = dir.SetTo(&nref);
:::
::::

::::{abi-group}
:::{cpp:enumerator} B_ENTRY_REMOVED
:::

A node was removed (deleted) from a directory.

You get this if you applied {cpp:enumerator}`B_WATCH_NAME` on the node
itself, or {cpp:enumerator}`B_WATCH_DIRECTORY` on the directory that the
node lived in. The message's fields are:

:::{list-table}
---
header-rows: 1
align: left
widths: auto
---
-
	- Field

	- Type code

	- Description

-
	- {hparam}`opcode`

	- {cpp:enumerator}`B_INT32_TYPE`

	- {cpp:enumerator}`B_ENTRY_REMOVED indicates that an entry was removed.`

-
	- {hparam}`directory`

	- {cpp:enumerator}`B_INT64_TYPE`

	- The {htype}`ino_t` (node) number of the directory from which the entry was
removed.

-
	- {hparam}`device`

	- {cpp:enumerator}`B_INT32_TYPE`

	- The {htype}`dev_t` number of the device that the removed node used to live
on.

-
	- {hparam}`node`

	- {cpp:enumerator}`B_INT64_TYPE`

	- The {htype}`ino_t` number of the node that was removed.


:::

:::{admonition} Note
:class: note
Since this message is telling you that the node was removed, the "node"
value will be invalid. The node number can be useful (and sometimes
necessary) for comparison with cached node numbers (as demonstrated below).
:::

Parsing the message is the same as for {cpp:enumerator}`B_ENTRY_CREATED`,
but without the {hparam}`name` field. See "{cpp:func}`Parsing and Tricks
<TheNodeMonitor::ParsingAndTricks>`," above.

Note that the {cpp:enumerator}`B_ENTRY_REMOVED` message is sent as soon as
the node's entry is "unlinked" from its directory. The node itself may
linger for while after that. Follow this logic:

-   When a file (regardless of flavor) is removed, the entry for that file is
immediately removed ("unlinked") from the file hierarchy, and the Node
Monitor message is immediately sent—even if you have an object that has
opened the file's node.

-   The node isn't actually destroyed until the last open object (to that
node) is destroyed. (In POSIX speak, the node is destroyed when the last
file descriptor to the node is closed.)

-   Until the node is destroyed, the open objects (file descriptors) can still
access the node's data.

You can take advantage of this to warn a user that a file is going to go
away, or to make a backup, or whatever. For example, let's say you have an
application that lets the user open files; each time a file is opened, your
OpenFile() function creates a {cpp:class}`BFile` object and starts the Node
Monitor running:

:::{code} cpp
status_t YourApp::OpenFile(const char *pathname)
{
   BFile *file;
   node_ref nref;
   status_t err;

   file = new BFile(pathname, B_READ_WRITE);
   if ((err=file->InitCheck()) != B_OK)
      return err;

   file->GetNodeRef(&nref);
   err = watch_node(&nref, B_WATCH_NAME, be_app_messenger);

   if (err != B_OK) {
      delete file;
      return err;
   }

   /* We've got the file and we're monitoring it; now we cache
   * the BFile by adding it to a BList (data member).
   * function. There's a race condition between the
   * watch_node() call above and the following AddItem().
   */
   return ((FileList->AddItem((void *)file)) ? B_OK : B_ERROR);

}
:::

Now we receive a Node Monitor message telling us the node has been
removed. We stuff the {hparam}`device` and {hparam}`node` fields into a
{htype}`node_ref` and pass them to a (fictitious) {hmethod}`AlertUser()`
function:

:::{code} cpp
void YourApp::MessageReceived(BMessage *msg)
{
   int32 opcode;
   node_ref nref;

   if (msg->what == B_NODE_MONITOR) {
      if (msg->FindInt32("opcode", &opcode) == B_OK) {
         switch (opcode) {
            case B_ENTRY_REMOVED:
               msg->FindInt32("device", &nref.device);
               msg->FindInt64("node", &nref.node);
               GoodbyeFile(nref);
   ...
}
:::

The implementation of {hmethod}`GoodbyeFile()` (which we won't show here)
would walk down the {cpp:class}`BFile` list looking for a {htype}`node_ref`
that matches the argument:

:::{code} cpp
void YourApp::GoodbyeFile(node_ref nref)
{
   BFile *filePtr;
   int32 ktr = 0;
   node_ref cref;

   while ((*filePtr = (BFile *)FileList->ItemAt(ktr++))) {
      filePtr->GetNodeRef(&cref);
      if (nref == cref) {
         /* We found it. Now we do whatever
         * we need to do.
         */
      }
   }
}
:::

If a match is found, your app could then do whatever it needs to do.
Remember—the node's data is still valid until your {cpp:class}`BFile` is
destroyed or re-initialized.
::::

::::{abi-group}
:::{cpp:enumerator} B_ENTRY_MOVED
:::

A node was moved from one directory to a different directory.

You get this if you applied {cpp:enumerator}`B_WATCH_NAME` on the node
itself, or {cpp:enumerator}`B_WATCH_DIRECTORY` on either of the
directories. The message's fields are:

:::{list-table}
---
header-rows: 1
align: left
widths: auto
---
-
	- Field

	- Type code

	- Description

-
	- {hparam}`opcode`

	- {cpp:enumerator}`B_INT32_TYPE`

	- {cpp:enumerator}`B_ENTRY_MOVED indicates that an existing entry moved from
one directory to another.`

-
	- {hparam}`name`

	- {cpp:enumerator}`B_STRING_TYPE`

	- The name of the entry that moved.

-
	- {hparam}`from directory`

	- {cpp:enumerator}`B_INT64_TYPE`

	- The {htype}`ino_t` (node) number of the directory from that the node was
removed from.

-
	- {hparam}`to directory`

	- {cpp:enumerator}`B_INT64_TYPE`

	- The {htype}`ino_t` (node) number of the directory that the node was added
to.

-
	- {hparam}`device`

	- {cpp:enumerator}`B_INT32_TYPE`

	- The {htype}`dev_t` number of the device that the moved node entry lives
on. (You can't move a file between devices, so this value will be apply to
the file's old and new locations.)

-
	- {hparam}`node`

	- {cpp:enumerator}`B_INT64_TYPE`

	- The {htype}`ino_t` number of the node that moved.


:::

:::{admonition} Note
:class: note
Moving a node __does not__ change its {htype}`ino_t` number.
:::

Parsing the message is much the same as for
{cpp:enumerator}`B_ENTRY_CREATED`, modulo the {hparam}`directory` field
changes. See "{cpp:func}`Parsing and Tricks
<TheNodeMonitor::ParsingAndTricks>`"

Moving a node doesn't affect the objects that hold the node open. They
(the objects) can continue to read and write data from the node.
::::

::::{abi-group}
:::{cpp:enumerator} B_STAT_CHANGED
:::

A field in the node's {htype}`stat` structure changed (this doesn't
include the {htype}`stat` structure disappearing because the node was
deleted).

You get this if you applied {cpp:enumerator}`B_WATCH_STAT` on the node
itself. The message's fields are:

:::{list-table}
---
header-rows: 1
align: left
widths: auto
---
-
	- Field

	- Type code

	- Description

-
	- {hparam}`opcode`

	- {cpp:enumerator}`B_INT32_TYPE`

	- {cpp:enumerator}`B_STAT_CHANGED indicates that some statistic of a node
(as recorded in its stat structure) changed.`

-
	- {hparam}`node`

	- {cpp:enumerator}`B_INT64_TYPE`

	- The {htype}`ino_t` number of the node.

-
	- {hparam}`device`

	- {cpp:enumerator}`B_INT32_TYPE`

	- The {htype}`dev_t` number of the node's device.


:::

The stat structure is described in "The stat Structure" in the
{cpp:class}`BStatable` class. The fields that you can change are:

-   Owner ({hparam}`st_uid`), group ({hparam}`st_gid`), and permissions (low
four bytes of {hparam}`st_mode`).

-   Creation ({hparam}`st_ctime`), modification ({hparam}`st_mtime`), and
access times ({hparam}`st_atime`; currently unused).

-   The size of the node's data ({hparam}`st_size`). The measurement doesn't
include attributes.

A couple of important points:

-   The {cpp:enumerator}`B_STAT_CHANGED` message doesn't give you enough
information to construct an object from which you can get a {htype}`stat`
structure. In other words, you can't play the same games that were
described in "{cpp:func}`Parsing and Tricks
<TheNodeMonitor::ParsingAndTricks>`."

-   The message also doesn't tell you which stat field changed.

In most uses of the {cpp:enumerator}`B_STAT_CHANGED` message, you have to
cache the objects that you're monitoring so you can compare their
{htype}`node_ref`s to the message fields (an example of this is given in
{cpp:enumerator}`B_ENTRY_REMOVED`). Furthermore, you may want to cache the
objects' {htype}`stat` structures so you can figure out which field
changed.
::::

::::{abi-group}
:::{cpp:enumerator} B_ATTR_CHANGED
:::

An attribute of the node changed.

You get this if you applied {cpp:enumerator}`B_WATCH_ATTR` on the node
itself. The message's fields are:

:::{list-table}
---
header-rows: 1
align: left
widths: auto
---
-
	- Field

	- Type code

	- Description

-
	- "opcode"

	- {cpp:enumerator}`B_INT32_TYPE`

	- {cpp:enumerator}`B_ATTR_CHANGED indicates that some attribute of a node
changed.`

-
	- "node"

	- {cpp:enumerator}`B_INT64_TYPE`

	- The ino_t number of the node.

-
	- "device"

	- {cpp:enumerator}`B_INT32_TYPE`

	- The dev_t number of the node's device.


:::

Attributes are key/value pairs that can be "attached" to any file
(regardless of flavor). They're described in the {cpp:class}`BNode` class.

As with {cpp:enumerator}`B_STAT_CHANGED` messages, you may not be able to
use the {cpp:enumerator}`B_ATTR_CHANGED` information directly. Instead, you
have to cache references to the ({cpp:class}`BNode`) objects that you're
monitoring so you can compare their {htype}`node_ref`s to the message
fields (an example of this is given in {cpp:enumerator}`B_ENTRY_REMOVED`).
::::

::::{abi-group}
:::{cpp:enumerator} B_DEVICE_MOUNTED
:::

A file system device (in other words, a volume) was mounted.

You get this if you passed {cpp:enumerator}`B_WATCH_MOUNT` to
{cpp:func}`watch_node() <watch::node>`. The message's fields are:

:::{list-table}
---
header-rows: 1
align: left
widths: auto
---
-
	- Field

	- Type code

	- Description

-
	- "opcode"

	- {cpp:enumerator}`B_INT32_TYPE`

	- {cpp:enumerator}`B_DEVICE_MOUNTED indicates that a new device (or file
system volume) has been mounted.`

-
	- "new device"

	- {cpp:enumerator}`B_INT32_TYPE`

	- The {htype}`dev_t` number of the newly-mounted device.

-
	- "device"

	- {cpp:enumerator}`B_INT32_TYPE`

	- The {htype}`dev_t` number of the device that holds the directory of the
new device's mount point.

-
	- "directory"

	- {cpp:enumerator}`B_INT64_TYPE`

	- The {htype}`ino_t` (node) number of the directory that acts as the new
device's mount point.


:::

Obviously, there's no node involved, here, so the first argument to the
{cpp:func}`watch_node() <watch::node>` call can be {cpp:expr}`NULL`:

:::{code} cpp
watch_node(NULL, B_WATCH_MOUNT, be_app_messenger);
:::

Unlike with the other "watch flags," the only way to stop the
mount-watching is to call {cpp:func}`stop_watching() <stop::watching>`.
::::

::::{abi-group}
:::{cpp:enumerator} B_DEVICE_UNMOUNTED
:::

A file system device (in other words, a volume) was unmounted.

You get this if you passed {cpp:enumerator}`B_WATCH_MOUNT` to
{cpp:func}`watch_node() <watch::node>`. The message's fields are:

:::{list-table}
---
header-rows: 1
align: left
widths: auto
---
-
	- Field

	- Type code

	- Description

-
	- "opcode"

	- {cpp:enumerator}`B_INT32_TYPE`

	- {cpp:enumerator}`B_DEVICE_UNMOUNTED indicates that a device has been
unmounted.`

-
	- "device"

	- {cpp:enumerator}`B_INT32_TYPE`

	- The {htype}`dev_t` number of the unmounted device.


:::

Be careful with the device number: {htype}`dev_t`s are quickly recycled.
You should only need this number if you're keeping a list of the
{htype}`dev_t`s of all mounted disks and you want to remove the
{htype}`dev_t` for this recently-unmounted volume (keeping in mind that a
device mounted message bearing this {htype}`dev_t` may arrive in the
meantime).
::::
