# BStatable

{hclass}`BStatable` is a pure abstract class that provides functionality
for its two derived class, {cpp:class}`BEntry` and {cpp:class}`BNode`. The
{hclass}`BStatable` functions let you get and set "statistical" information
about a node in the file system. You can…

-   Determine whether the node is a file, directory, or symbolic link.

-   Get and set an node's owner, group, and permissions.

-   Get and set the node's creation, modification, and access times.

-   Get the size of the node's data (not counting attributes).

-   Get a {cpp:class}`BVolume` object for the node's volume.

-   Get the {htype}`node_ref` of the node (and pass it to
{cpp:func}`watch_node() <watch::node>`, most likely).

## Nodes and Entries

Technically, {hclass}`BStatable` information pertains to nodes, not
entries. The fact that {cpp:class}`BEntry` implements the
{hclass}`BStatable` functions is a (slightly confusing) convenience: When
you invoke a {hclass}`BStatable` function on a {cpp:class}`BEntry` object,
what you're really doing is asking for information about the node that
corresponds to the object.

## Abstract Entries

As explained in {cpp:class}`BEntry`, it's possible to create "abstract"
{cpp:class}`BEntry` objects; in other words, objects that don't correspond
to actual files (nodes) on the disk. You can't get (or set)
{hclass}`BStatable` information for abstract entries. The
{hclass}`BStatable` functions return {cpp:enumerator}`B_BAD_VALUE` if the
invoked-upon entry is abstract.

## Relationship to stat()

The {hclass}`BStatable` functions are covers for the POSIX {ref}`stat()`
call. stat() retrieves a file-specific {htype}`stat` structure, which
records the statistics listed above (and then some). Although
{hclass}`BStatable` was designed to hide stat details, you can get the
{ref}`stat()` structure through the {cpp:func}`GetStat()
<BStatable::GetStat>` function.

stat() is notorious for being expensive. Furthermore, the {htype}`stat`
structure is stale as soon as it gets back from the stat() call. If you're
concerned with efficiency, be aware that every {hclass}`BStatable` function
(the "setters" as well as the "getters") performs a stat(). For example,
calling {cpp:func}`GetOwner() <BStatable::GetOwner>` and then
{cpp:func}`GetGroup() <BStatable::GetGroup>` results in two stat() calls.
If you want to look at lot of fields (within the same {htype}`stat`
structure) all at once, you might consider using {hclass}`BStatable`'s
{cpp:func}`GetStat() <BStatable::GetStat>` function.

As for integrity, {hclass}`BStatable` info-getting functions are obviously
in the same boat as the stat() call itself: The retrieved data isn't
guaranteed to be in sync with the actual state of the stat()'d item.

The {cpp:class}`BDirectory` class also defines a stat-retrieving function
that, in some cases, can be more efficient than the {cpp:func}`GetStat()
<BStatable::GetStat>` function defined here:

-   The {cpp:func}`BDirectory::GetStatFor` function retrieves the
{htype}`stat` structure for the node of a named entry within a directory.
If you're interested in getting stat information for a series of nodes
within the same directory, you should use this function. You have to call
it iteratively (once for each named entry), but the accumulation of the
iterated calls will be faster than the {cpp:func}`GetStat()
<BStatable::GetStat>` calls made on the analogous {cpp:class}`BEntry`
objects.

## Accessing Unreadable and Unwritable Entries

{hclass}`BStatable` isn't thwarted by file permissions: If you can
construct a valid {cpp:class}`BEntry` or {cpp:class}`BNode` to an item,
then you can invoke any of the info-getting {hclass}`BStatable` functions
on that object:

-   The {hclass}`BStatable` functions aren't denied even if the node that
you're looking at is read-protected. However, you can only invoke the
info-setting functions if the node allows writing.

-   Similarly, you can get stat info for a locked node, but you won't be able
to write the info (through functions such as {cpp:func}`SetOwner()
<BStatable::SetOwner>`) unless your object holds the lock. See
{cpp:class}`BNode` for more on locking.

## Other Details

You rarely set stat information. In practice, you rarely use
{hclass}`BStatable`'s info-setting functions. Setting information such as
when a file was created, who owns it, or how big it is, is the
responsibility of the system and the privilege of the user. For example,
when you {cpp:func}`Write() <BFile::Write>` to a {cpp:class}`BFile` object,
the system automatically updates the size and modification date for the
file.
