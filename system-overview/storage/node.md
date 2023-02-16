# BNode

The {hclass}`BNode` class gives you access to the data that a file system
entry (a file, directory, or symbolic link) contains. There are two parts
to this data:

1.    There's the "data portion" itself…

2.    …and then there are the node's attributes.

The content of the data portion depends on the node's flavor:

-   If it's a regular file, the data is whatever it is that the file is meant
to contain: ASCII text, binary image or sound data, executable code, and so
on. Note that resources (as created by the {cpp:class}`BResources` class)
are kept in the data portion.

-   If it's a directory, the data is the list of entries that the directory
contains.

-   If it's a symbolic link, the data is the path of the "linked-to" file. The
path can be absolute or relative.

The content of the attributes, on the other hand, isn't qualified by the
node's flavor: Any node can contain any set of attributes.

## Nodes are Dumb

Keep in mind that the concept of a "node" designates the data parts (data
and attributes) of a file (a file, directory, or link). Contrast this with
an "entry," which designates the entity's location within the file system:
For example, you can write to a "node" (but not an entry), and you can
rename an "entry" (but not a node).

This isn't just a conceptual crutch, it's the law: Nodes really don't know
where they're located. For example, you can't ask a node for its name, or
for the identity of its parent. This has some serious implications, the
most important of which is…

-   If you need to store a reference to a file (or directory, or symbolic
link), don't store the node—in other words, don't cache the BNode object.
Instead, store the information that you used to create the {hclass}`BNode`
(typically, a pathname or {htype}`entry_ref` structure).

Now that we've got that straight, we'll relax the rules a bit:

-   {cpp:class}`BDirectory` objects are node/entry hybrids. A
{cpp:class}`BDirectory` does know its own name (and parent, and so on).

This doesn't really change the "store the info" rule. Even if you're
dealing exclusively with {cpp:class}`BDirectory` objects, you should keep
the generative information around. The primary reason for this is…

### The "Node Pool" is Limited (File Descriptors)

Every {hclass}`BNode` object consumes a "file descriptor." Your
application can only maintain 256 file descriptors at a time. Because of
this limit, you shouldn't keep {hclass}`BNode`s around that you don't need.
Keep in mind that {cpp:class}`BEntry` objects also consumes file
descriptors (one per object).

:::{admonition} Note
:class: note
The file descriptor limit will probably be lifted, or at least settable,
in a subsequent release. But even then you should be frugal.
:::

## Derived Classes and their Uses

{hclass}`BNode` has three derived classes: {cpp:class}`BFile`,
{cpp:class}`BDirectory`, and {cpp:class}`BSymLink`. The derived classes
define functions that let you access the node's data portion in the
appropriate style; for example…

-   {cpp:class}`BFile` implements {cpp:func}`Read() <BFile::Read>` and
{cpp:func}`Write() <BFile::Write>` functions that let you retrieve
arbitrary amounts of data from arbitrary positions in the file.

-   {cpp:class}`BDirectory` implements functions, such as
{cpp:func}`GetNextEntry() <BDirectory::GetNextEntry>` and
{cpp:func}`FindEntry() <BDirectory::FindEntry>`, that read entries from the
directory.

-   {cpp:class}`BSymLink`'s {cpp:func}`ReadLink() <BSymLink::ReadLink>`
returns the pathname that it contains.

If you want to (sensibly) look at a node's data portion, you must create
an instance of the appropriate derived class. In other words, if you want
to browse a directory, you have to create a {cpp:class}`BDirectory`
instance; if you want to write to a file, you create a {cpp:class}`BFile`.

Be aware that it's not (always) an error to create an instance of the
"wrong" derived class; setting a {cpp:class}`BFile` to a symbolic link, for
example, will traverse the link such that the {cpp:class}`BFile` opens the
file that the symbolic link is linked to. See the individual derived class
specifications for more information.

## BNode Instances

In practice, you almost always want to create an instance of one of the
{hclass}`BNode`-derived classes; but if, for whatever reason, you find
yourself holding a {hclass}`BNode` instance, here's what you'll be able to
do with it:

-   Read and write attributes. The attribute-accessing functions
({cpp:func}`ReadAttr() <BNode::ReadAttr>`, {cpp:func}`WriteAttr()
<BNode::WriteAttr>`, and so on) are general—they work without regard for
the node's flavor. Thus, you don't need an instance of a specific derived
class to read and write attributes.

-   Get stat information. The {cpp:class}`BStatable` functions can be invoked
on any flavor of node.

-   Lock the node. This prevents other "agents" (other objects, other apps,
the user) from accessing reading or writing the node's data and attributes.
See "{ref}`Node Locking`".

## Converting a BNode to an Instance of a Derived Class

:::{admonition} Note
:class: note
This section describes situations and presents solutions to problems that
are a bit esoteric. If you never create direct instances of BNode (and you
never have to), then you should skip this and go to "{ref}`Node Locking`".
:::

There may be times when you find yourself holding on to a {hclass}`BNode`
(instance) that you want to convert into a {cpp:class}`BFile`,
{cpp:class}`BDirectory`, or {cpp:class}`BSymLink`. However, you can't go
directly from a {hclass}`BNode` instance to an instance of
{cpp:class}`BFile`, {cpp:class}`BDirectory`, or {cpp:class}`BSymLink`—you
can't tell your {hclass}`BNode` to "cast itself" as one of its children.

There are solutions, however…

### Converting to BDirectory

Converting from a {hclass}`BNode` to a {cpp:class}`BDirectory`, while not
transparent, is pretty simple: Grab the {htype}`node_ref` out of the
{hclass}`BNode` and pass it to the {cpp:class}`BDirectory` constructor or
{cpp:func}`SetTo() <BDirectory::SetTo>` function. Regard this example
function:

:::{code} cpp
void Node2Directory(BNode *node, BDirectory *dir)
{
   node_ref nref;

   if (!node || !dir) {
      dir.Unset();
      return;
   }

   node.GetNodeRef(&nref);

   /* Set the BDirectory. If nref isn't a directory node,
   * the SetTo() will fail.
   */
   dir.SetTo(&nref);
}
:::

### Converting to BFile or BSymLink

Converting a {hclass}`BNode` instance to a {cpp:class}`BFile` or
{cpp:class}`BSymLink` isn't as neat as the foregoing. Instead, you have to
cache the information that you used to initialize the {hclass}`BNode` in
the first place, and then reuse it to create the {cpp:class}`BFile` or
{cpp:class}`BSymLink`.

For example, let's say you receive an {htype}`entry_ref`. You turn it into
a {hclass}`BNode`, but then decide you need the data-writing power of a
{cpp:class}`BFile`. If, in the meantime, you lost the original
{htype}`entry_ref`, you're sunk—there's nothing you can do.

## Node Locking

Another feature provided by the {hclass}`BNode` class is "node locking":
Through {hclass}`BNode`'s {cpp:func}`Lock() <BNode::Lock>` function you can
restrict access to the node. The lock is removed when {cpp:func}`Unlock()
<BNode::Unlock>` is called, or when the {hclass}`BNode` object is deleted.

-   When you lock a node, you prevent other objects (or agents) from reading
or writing the node's data and attributes. No other agent can even open the
node—other {hclass}`BNode` constructions and POSIX open() calls (on that
node) will fail while you hold the lock.

-   You can only acquire a node lock if there are no file descriptors open on
the node (with one exception). This means that no other {hclass}`BNode` may
be open on the node (locked or not), nor may the node be held open because
of a POSIX open() (or opendir()) call.

The one exception to the no-file descriptors rule has to do with
{cpp:class}`BEntry`s: Let's say you lock a directory, and then you
initialize a {cpp:class}`BEntry` to point to an entry within that
directory. Even though the {cpp:class}`BEntry` creates a file descriptor to
the directory (as explained in the {cpp:class}`BEntry` class), the
initialization will succeed.

### Implications

For files (and, less importantly, symlinks), the implications of locking
are pretty clear: No one else can read or write the file. For directories,
it's worth a closer look:

-   Locking a directory means that the contents of the directory can't change:
You can't create new nodes in the directory, or rename or remove existing
ones. (You can, however, create abstract entries within the directory; see
{cpp:class}`BEntry` for more on abstract entries.)

Locking a node does not lock the node's entry: You can't "lock out" entry
operations, such as rename, move, and remove. Even if you have a node
locked, the entry that acts as the "container" for that node could
disappear. If you want to prevent such operations on a node's entry, lock
the entry's parent directory.

In general, you should try to avoid locking your nodes. If you must lock,
try to make it brief. The primary reason (and, pretty much, the only
reason) to lock is if separate elements in the data and/or attributes must
be kept in a consistent state. In such a case, you should hold the lock
just long enough to ensure consistency.

:::{admonition} Warning
:class: warning
You shouldn't use locks to "privatize" data. Locking isn't meant to be
used as a heightened permissions bit.
:::
