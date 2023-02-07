# BNode
## Constructor and Destructor
::::{abi-group}

:::{cpp:function} BNode::BNode()
:::
:::{cpp:function} BNode::BNode(const entry_ref* ref)
:::
:::{cpp:function} BNode::BNode(const BEntry* entry)
:::
:::{cpp:function} BNode::BNode(const char* path)
:::
:::{cpp:function} BNode::BNode(const BDirectory* dir, const char* path)
:::
:::{cpp:function} BNode::BNode(const BNode& node)
:::

Creates a new {hclass}`BNode` object that's initialized to represent a specific
file system node. To retrieve the status of the initialization, call
{cpp:func}`~BNode::InitCheck`
immediately after constructing the object:

:::{code}
BNode node("/boot/lbj/FidoOnFire.gif");
if (node.InitCheck() != B_OK)
   /* The object wasn't initialized. */
:::

A successfully initialized {hclass}`BNode` object creates a "file descriptor"
through which the object reads and writes the node's data and attributes.
You can only have 256 file descriptors at a time (per application). The
object's file descriptor is closed when the object is deleted, reset
(through
{cpp:func}`~BNode::SetTo`), or unset
({cpp:func}`~BNode::Unset`).

- Default constructor. The object's status will be {cpp:enum}`B_NO_INIT`, and the file descriptor isn't allocated until you actually initialize the object with a call to {cpp:func}`~BNode::SetTo`.
- Copy constructor. The new {hclass}`BNode` is set to the same node as the argument. Each of the two {hclass}`BNode` objects has its own file descriptor.
- Other constructors. See the {cpp:func}`~BNode::SetTo` functions.

::::

::::{abi-group}

:::{cpp:function} virtual BNode::~BNode()
:::

Frees the object's file descriptor, unlocks the node (if it was locked),
and destroys the object.

::::

## Member Functions
::::{abi-group}

:::{cpp:function} status_t BNode::GetAttrInfo(const char* attr, attr_info* info) const
:::

Gets information about the attribute named by {hparam}`attr`. The information is
copied into the {cpp:func}`~attr::info`
parameter {hparam}`info`, which must be allocated before it's passed in.

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
	- The node doesn't have an attribute named {hparam}`attr`.
-
	- {cpp:enum}`B_FILE_ERROR`.
	- The object is uninitialized.
:::
::::

::::{abi-group}

:::{cpp:function} status_t BNode::GetNextAttrName(char* buffer)
:::
:::{cpp:function} status_t BNode::RewindAttrs()
:::

Every {hclass}`BNode` maintains a pointer into its list of attributes.
{hmethod}`GetNextAttrName()` retrieves the name of the attribute that the pointer is
currently pointing to, and then bumps the pointer to the next attribute.
The name is copied into the buffer, which should be at least
{cpp:enum}`B_ATTR_NAME_LENGTH` characters long. The copied name is {cpp:enum}`NULL`-terminated.
When you've asked for every name in the list, {hmethod}`GetNextAttrName()` returns
an error.

:::{admonition} Warning
:class: warning
{hmethod}`GetNextAttrName()` does not
clear its argument if it returns an error.
This will be corrected in a subsequent release.
:::

{hmethod}`RewindAttrs()` resets the {hclass}`BNode`'s
attribute pointer to the first elementin the list.

To visit every attribute name, you would do something like this:

:::{code}
/* Print every attribute name. */
char buf[B_ATTR_NAME_LENGTH];
while (node.GetNextAttrName(buf) == B_OK) {
   printf("> Attr name: %sn", buf);
}
:::

The attribute list is not static; when you ask for the next attribute
name, you're asking for the next name in the list
as it exists right now.

Furthermore, the ordinal position of an attribute within the list is
indeterminate. "Newer" attributes are not necessarily added to the end of
the list: If you alter the list while you're walking through it, you may
get curious results—you may not see the attribute that you just now
added (for example).

In general, it's best to avoid altering the list while you're iterating
over it.

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
	- You've hit the end of the list.
-
	- {cpp:enum}`B_FILE_ERROR`
	- The object is uninitialized.
:::
::::

::::{abi-group}

:::{cpp:function} status_t BNode::InitCheck() const
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
	- {cpp:enum}`B_NO_INIT`.
	- The object is uninitialized.
-
	- Other return values
	- See the {cpp:func}`~BNode::SetTo` function.
:::
::::

::::{abi-group}

:::{cpp:function} status_t BNode::Lock()
:::
:::{cpp:function} status_t BNode::Unlock()
:::

Locks and unlocks the {hclass}`BNode`'s node. While the node is locked, no other
object can access the node's data or attributes. More precisely, no other
agent can create a file descriptor to the node. If a file descriptor
already exists to this node, the {hmethod}`Lock()` function fails.

See "{cpp:func}`~BNode::Node`" for details.

:::{list-table}
---
header-rows: 1
---
-
	- Return Code
	- Description
-
	- {cpp:enum}`B_OK`.
	- The node was successfully locked or unlocked.
-
	- {cpp:enum}`B_BUSY`.
	- ({hmethod}`Lock()`) The node can't be locked.
-
	- {cpp:enum}`B_BAD_VALUE`.
	- ({hmethod}`Unlock()`) The node isn't locked.
-
	- {cpp:enum}`B_FILE_ERROR`.
	- The object is uninitialized.
:::
::::

::::{abi-group}

:::{cpp:function} ssize_t BNode::ReadAttr(const char* name, type_code type, off_t offset, void* buffer, size_t length)
:::
:::{cpp:function} ssize_t BNode::WriteAttr(const char* name, type_code type, off_t offset, const void* buffer, size_t length)
:::
:::{cpp:function} status_t BNode::RemoveAttr(const char* attr)
:::

These functions read, write, and remove the node's attributes. Attributes
are name/data pairs, where names must be unique (within a given node) and
the data can be of arbitrary length.

{hmethod}`ReadAttr()` reads the data in the attribute named {hparam}`name`, and copies it in
{hparam}`buffer`. The length of the buffer (the maximum number of bytes to copy) is
given by {hparam}`length`. Currently, the {hparam}`type`
and {hparam}`offset` arguments are unused (or
unreliable). The function returns the number of bytes that were actually
read.

{hmethod}`WriteAttr()` erases the data currently held by
{hparam}`name` (if such an attribute exists) and replaces it
with a copy of the first {hparam}`length` bytes of data in
{hparam}`buffer`. The {hparam}`type` argument
is remembered—you can retrieve an attribute's
type through {cpp:func}`~BNode::GetAttrInfo`, for
example—and you need to specify the correct type when you're forming
a query (see {cpp:class}`BQuery`
and the note below). But, as mentioned above, you don't need to match types
when you're reading the attribute. The {hparam}`offset`
argument is currently unreliable and shouldn't be used. The functions
returns the number of bytes that were written.

:::{admonition} Note
:class: note
If you want to use the attribute in a query, its type must be either
string, int32, uint32, int64,
uint64, double, or float. (In other words,
{hparam}`type` must be {cpp:enum}`B_STRING_TYPE`, or {cpp:enum}`B_INT32_TYPE`, or
{cpp:enum}`B_UINT32_TYPE`, and so on.)
:::
:::{admonition} Warning
:class: warning
The value of an indexed attribute must be no more than 255 bytes long.
:::

{hmethod}`RemoveAttr()` deletes the attribute given by {hparam}`name`.

{hmethod}`ReadAttr()` and {hmethod}`WriteAttr()`,
if successful, return the number of bytes read or written.

:::{list-table}
---
header-rows: 1
---
-
	- Return Code
	- Description
-
	- {cpp:enum}`B_OK`.
	- ({hmethod}`RemoveAttr()`) The attribute was successfully removed.
-
	- {cpp:enum}`B_ENTRY_NOT_FOUND`.
	- ({hmethod}`ReadAttr()` and {hmethod}`RemoveAttr()`) The attribute doesn't exist.
-
	- {cpp:enum}`B_FILE_ERROR`.
	- The object is uninitialized.
-
	- {cpp:enum}`B_FILE_ERROR`.
	- ({hmethod}`WriteAttr()` and {hmethod}`RemoveAttr()`) This object is a read-only {cpp:class}`BFile`.
-
	- {cpp:enum}`B_NOT_ALLOWED`.
	- ({hmethod}`WriteAttr()` and {hmethod}`RemoveAttr()`) The node is on a read-only volume.
-
	- {cpp:enum}`B_DEVICE_FULL`.
	- ({hmethod}`WriteAttr()`) Out of disk space.
-
	- {cpp:enum}`B_NO_MEMORY`.
	- ({hmethod}`WriteAttr()`) Not enough memory to complete the operation.
:::
::::

::::{abi-group}

:::{cpp:function} status_t BNode::RenameAttr(const char* name, const char* new_name)
:::

Moves the attribute given by {hparam}`name` to {hparam}`new_name`.
If {hparam}`new_name` exists, it's
clobbered.

:::{list-table}
---
header-rows: 1
---
-
	- Return Code
	- Description
-
	- {cpp:enum}`B_OK`.
	- The attribute was successfully renamed.
-
	- {cpp:enum}`B_ENTRY_NOT_FOUND`.
	- The {hparam}`name` attribute doesn't exist.
-
	- {cpp:enum}`B_FILE_ERROR`.
	- The object is uninitialized.
-
	- {cpp:enum}`B_FILE_ERROR`.
	- This object is a read-only {cpp:class}`BFile`.
-
	- {cpp:enum}`B_NOT_ALLOWED`.
	- The node is on a read-only volume.
:::
::::

::::{abi-group}

:::{cpp:function} status_t BNode::SetTo(const entry_ref* ref)
:::
:::{cpp:function} status_t BNode::SetTo(const BEntry* entry)
:::
:::{cpp:function} status_t BNode::SetTo(const char* path)
:::
:::{cpp:function} status_t BNode::SetTo(const BDirectory* dir, const char* path)
:::
:::{cpp:function} void BNode::Unset()
:::

Closes the {hclass}`BNode`'s current file descriptor and opens it on the node (of
the entry) that's designated by the arguments.

- In the {hparam}`path` version, {hparam}`path` can be absolute or relative, and can contain "." and ".." elements. If {hparam}`path` is relative, it's reckoned off of the current working directory.
- In the {hparam}`dir`/{hparam}`path` version, {hparam}`path` must be relative. It's reckoned off of the directory given by {hparam}`dir`.

{hclass}`BNode` instances never traverse symbolic links. If the designated entry is
a symbolic link, the BNode will open the link's node. (Conversely,
{cpp:class}`BFile`
instances always traverse symbolic links.)

{hmethod}`Unset()` closes the {hclass}`BNode`'s
file descriptor and sets
{cpp:func}`~BNode::InitCheck` to
{cpp:enum}`B_NO_INIT`.

:::{list-table}
---
header-rows: 1
---
-
	- Return Code
	- Description
-
	- {cpp:enum}`B_OK`.
	- All is well.
-
	- {cpp:enum}`B_BAD_VALUE`.
	- The designated entry doesn't exist.
-
	- {cpp:enum}`B_BAD_VALUE`.
	- Uninitialized or malformed argument.
-
	- {cpp:enum}`B_BUSY`.
	- The node is locked.
:::
::::

::::{abi-group}

:::{cpp:function} status_t BNode::Sync()
:::

Immediately performs any pending disk transactions for the file,
returning {cpp:enum}`B_OK` on success and an appropriate error message otherwise.

::::

## Operators
::::{abi-group}

:::{cpp:function} BNode& BNode::operator=(const BNode& node)
:::

In the expression

:::{code}
BNode a = b;
:::

{hclass}`BNode` a is initialized to refer
to the same node as b. To gauge the
success of the assignment, you should call
{cpp:func}`~BNode::InitCheck` immediately
afterwards. It's safe to assign a {hclass}`BNode` to itself.

::::

::::{abi-group}

:::{cpp:function} bool BNode::operator==(const BNode& node) const
:::
:::{cpp:function} bool BNode::operator!=(const BNode& node) const
:::

Two {hclass}`BNode` objects are said to be equal if they're set to the same node,
or if they're both {cpp:enum}`B_NO_INIT`.

::::

## Defined Types
::::{abi-group}


Declared in: storage/Node.h

:::{code}
struct node_ref {
              node_ref();
              node_ref(const node_ref& ref);
              ~node_ref();
    bool      operator==(const node_ref& ref) const;
    bool      operator!=(const node_ref& ref) const;
    node_ref& operator=(const node_ref& ref);
    dev_t     device;
    ino_t     node;
}
:::

The node_ref structure describes a node in a file system.

- device contains the device number on which the node is located.
- node contains the inode of the node.

:::{cpp:function} BNode::node_ref()
:::
:::{cpp:function} BNode::node_ref(const node_ref& ref)
:::

The constructor for the node_ref structure. The first of these
creates an empty node_ref, and the second duplicates an existing
node_ref.

:::{cpp:function} BNode::~node_ref()
:::

The destructor for node_ref.

{hmethod}`operator ==`

Lets you perform comparisons of node_ref structures to see if they
refer to the same node.

{hmethod}`operator !=`

Lets you test to see if two node_ref structures refer to different
nodes.

::::
