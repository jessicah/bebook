# BNodeInfo

{hclass}`BNodeInfo` provides file type information about a particular
node; specifically:

-   The (MIME) file type.

-   The node's icons, including the node-specific icon that the Tracker
displays.

-   The "preferred app"; this is the application that's used to access the
node's contents.

Except for the Tracker icon, all this information can also be set through
the {hclass}`BNodeInfo` class. None of the information is passed on to the
File Type database; if you want to record a node's file type information
with the database, you have to create a {cpp:class}`BMimeType` object
(based on the node's file type) and go from there.

## Initialization

You initialize a {hclass}`BNodeInfo` object by passing it a
{cpp:class}`BNode` object. Although you can pass any flavor of node, you
typically only care about files; passing a {cpp:class}`BFile` object (or
any subclass of {cpp:class}`BNode`) is, of course, acceptable. The
{hclass}`BNodeInfo` object maintains its own pointer to the BNode you pass
in. You don't have to avoid touching the {cpp:class}`BNode` while a
{hclass}`BNodeInfo` is looking at it (or changing it); the only thing you
shouldn't do is delete the {cpp:class}`BNode`.

{hclass}`BNodeInfo` doesn't care if the {cpp:class}`BNode` is
locked—there's no particular reason to lock the {cpp:class}`BNode` before
passing it in, but the {hclass}`BNodeInfo` won't balk if you do. If you
pass in a {cpp:class}`BFile` object, {hclass}`BNodeInfo` does not obey the
{cpp:class}`BFile`'s read/write flags. For example, you can set the node
info for a {cpp:class}`BFile` even if you've opened it in read-only mode.

## Node Info Equals Attributes

The {hclass}`BNodeInfo` class does nothing more than look in a node's
attributes for the information it sets or gets. The attribute names for the
various information particles are given in the function descriptions,
below. If you want, you can bypass {hclass}`BNodeInfo` and get the node
information directly by passing the attribute names to {cpp:class}`BNode`'s
{cpp:func}`ReadAttr() <BNode::ReadAttr>` and {cpp:func}`WriteAttr()
<BNode::WriteAttr>` functions.

The one exception to this is {cpp:func}`GetTrackerIcon()
<BNodeInfo::GetTrackerIcon>`: This function starts by looking in the node's
attributes, but then it goes out hunting if it has to (if the icon isn't
found in the attributes).

## BAppFileInfo

{hclass}`BNodeInfo` has a single subclass: {cpp:class}`BAppFileInfo`. You
use a {cpp:class}`BAppFileInfo` object to get more information about a
specific executable image (file).

## Errors

Unlike most of the other Storage Kit classes, when you ask a
{hclass}`BNodeInfo` to retrieve some information by reference, the object
doesn't clear the reference argument if it fails. Because of this, you
should always check the error code that's returned by the {hmethod}`Get…()`
functions.
