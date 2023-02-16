# BEntry

The {hclass}`BEntry` class defines objects that represent "locations" in
the file system hierarchy. Each location (or entry) is given as a name
within a directory. For example, when you create a {hclass}`BEntry` thus…

:::{code} cpp
BEntry entry("/boot/home/fido");
:::

…you're telling the {hclass}`BEntry` object to represent the location of
the file called fido within the directory /boot/home.

A {hclass}`BEntry` doesn't care whether the entry you tell it to represent
is a plain file, a directory, or a symbolic link—it doesn't even care if
the entry even exists (but we'll get to that later in "{ref}`Abstract
Entries`"):

-   All the {hclass}`BEntry` cares about is a name in a directory.

The most important implication of this is the object's attitude towards
data. {hclass}`BEntry`s don't know how to operate on data. You can't use a
{hclass}`BEntry` to read or write a file's data or attributes. For data
operations, you have to turn your {hclass}`BEntry` into a
{cpp:class}`BNode`.

Nonetheless, it's often convenient to speak of a {hclass}`BEntry` as
having data; for example, the phrase "the entry's data" really means "the
data that lies in the file that's located by the entry."

## Talents and Abilities

A properly initialized {hclass}`BEntry` object (we'll get to the rules of
initialization later) knows the following:

-   Location info. A {hclass}`BEntry` knows its own (leaf) name
({cpp:func}`GetName() <BEntry::GetName>`), its full pathname
({cpp:func}`GetPath() <BEntry::GetPath>`), and the identity of its parent
directory ({cpp:func}`GetParent() <BEntry::GetParent>`).

-   {cpp:class}`BStatable` info. As a descendant of {cpp:class}`BStatable`, a
{hclass}`BEntry` can return statistical information about the entry's
data—its size, creation date, owner, and so on.

-   {htype}`entry_ref` identifier. A {hclass}`BEntry` can return the
{htype}`entry_ref` that globally identifies the entry ({cpp:func}`GetRef()
<BEntry::GetRef>`).

A {hclass}`BEntry` can do these things:

-   Perform hierarchical operations. A {hclass}`BEntry` can change the name of
its entry ({cpp:func}`Rename() <BEntry::Rename>`), move it to another
directory ({cpp:func}`MoveTo() <BEntry::MoveTo>`), and remove it from the
file hierarchy ({cpp:func}`Remove() <BEntry::Remove>`).

-   Initialize {cpp:class}`BNode` objects. The constructors and
{cpp:func}`SetTo() <BEntry::SetTo>` initializers for {cpp:class}`BNode` and
its children ({cpp:class}`BFile`, {cpp:class}`BDirectory`, and
{cpp:class}`BSymLink`) accept {hclass}`BEntry` arguments.

As mentioned above, the most important thing that a {hclass}`BEntry` can't
do is access its own data: A {hclass}`BEntry` can't read or write data or
attributes. To do these things you need a {cpp:class}`BNode` object.

(Actually, this isn't entirely true: A BEntry can set the size of its data
through the BStatable::SetSize() function. The function only works on plain
files.)

## Initializing and Traversing

To initialize a {hclass}`BEntry`, you have to tell it which entry to
represent; in other words, you have to identify a directory and a name. You
can initialize a {hclass}`BEntry` object directly…

-   during construction,

-   through the {cpp:func}`SetTo() <BEntry::SetTo>` function,

-   or through the assignment operator.

Or you can have some other object initialize your {hclass}`BEntry` for
you, by passing the {hclass}`BEntry` as an argument to…

-   {cpp:class}`BDirectory`'s {cpp:func}`FindEntry() <BDirectory::FindEntry>`
or {cpp:func}`GetEntry() <BDirectory::GetEntry>` function,

-   {cpp:class}`BEntryList`'s {cpp:func}`GetNextEntry()
<BEntryList::GetNextEntry>` function (implemented by
{cpp:class}`BDirectory` and {cpp:class}`BQuery`).

-   {hclass}`BEntry`'s {cpp:func}`GetParent() <BEntry::GetParent>` function.

In all cases (except the assignment operator) you're asked if you want to
"traverse" the entry during initialization. Traversal is used to "resolve"
symbolic links:

-   If you traverse: The {hclass}`BEntry` will point to the entry that the
symbolic link is linked to.

-   If you don't traverse: The {hclass}`BEntry` will point to the symbolic
link itself.

For example, let's say /boot/home/fidoLink is linked to /fido, to wit:

:::{code} sh
$ cd /boot/home
$ ln -s ./fido fidoLink
:::

Now let's make a traversed {hclass}`BEntry` for fidoLink:

:::{code} cpp
/* The second argument is the traversal bool. */
BEntry entry("/boot/home/fidoLink", true);
:::

If we ask for the entry's pathname…

:::{code} cpp
BPath path;
entry.GetPath(&path);
printf("Pathname: %sn", path.Path());
:::

…we see

:::{code} sh
Pathname: /boot/home/fido
:::

In other words, the {hclass}`BEntry` refers to fido, not fidoLink.

Traversal resolves nested links—it really wants to find a "real" file (or
directory). If the entry that you're initializing to isn't a link, then the
traversal flag is ignored.

### When to Traverse

When should you traverse, and when not? Here are a few rules of thumbs:

-   If somebody hands you a file reference—if your app gets a
{cpp:func}`RefsReceived() <BApplication::RefsReceived>` message—then you
probably want to traverse the entry.

-   If you're pawing over the contents of a directory (through
{cpp:class}`BDirectory`'s {cpp:func}`GetNextEntry()
<BDirectory::GetNextEntry>`), then you probably don't want to traverse.

-   If you're looking at the result of a query (through {cpp:class}`BQuery`'s
{cpp:func}`GetNextEntry() <BQuery::GetNextEntry>`), then you almost
certainly don't want to traverse. The query finds entries that satisfy
certain criteria; if a symbolic link is in the list, it's because the link
itself was a winner. If the linked-to file is also a winner, it will show
up on its own.

### Traverso Post Facto

Let's say you create a {hclass}`BEntry` (to a symlink) without traversing,
but then you decide that you do want to resolve the link. Unfortunately,
you can't resolve in-place; instead, you have to initialize another
{hclass}`BEntry` using info ({htype}`entry_ref` or pathname) that you get
from the link entry:

:::{code} cpp
BEntry entry1("/boot/home/fidoLink", false);
BEntry entry2;
entry_ref ref;

/* First we check to see if it's a link. */
if (entry1.IsSymLink()) {
   /* Get the link's entry_ref... */
   entry1.GetRef(&ref);

   /* ...and use it to initialize the other BEntry. */
   entry2.SetTo(&ref, true);
}
:::

## Abstract Entries

As we all should know by now, a {hclass}`BEntry` identifies a name within
a specific directory. The directory that a {hclass}`BEntry` identifies must
exist, but the entry that corresponds to the name doesn't have to. In other
words…

-   A {hclass}`BEntry` can represent a file that doesn't exist. The entry is
said to be "abstract."

For example, the following construction creates a {hclass}`BEntry` object
based on a {cpp:class}`BDirectory` and a name:

:::{code} cpp
BEntry entry(someDir, "myFile.h");
:::

Let's assume that myFile.h doesn't exist. As long as the directory that's
referred to by someDir does exist, then the construction is legal. Some of
the {hclass}`BEntry` functions (those inherited from
{cpp:class}`BStatable`, for instance) won't work, but the object itself is
valid.

But validity doesn't equal existence:

-   {cpp:func}`SetTo() <BEntry::SetTo>` and {cpp:func}`InitCheck()
<BEntry::InitCheck>` __do not__ tell you if a {hclass}`BEntry`'s entry
actually exists. Don't be confused; a return value of
{cpp:enumerator}`B_OK` simply means the object is valid.

If you want to know if a {hclass}`BEntry`'s entry actually exists, use the
{cpp:func}`Exists() <BEntry::Exists>` function.

### Creating a File From an Abstract Entry

To turn an abstract {hclass}`BEntry` into a real entry (or, more
accurately, a real node), you have to specify the flavor of node that you
want. There are two methods for creating a node; the first is general, the
second applies to plain files only.

#### The General Approach.

{cpp:class}`BDirectory`'s {cpp:func}`CreateFile()
<BDirectory::CreateFile>`, {cpp:func}`CreateDirectory()
<BDirectory::CreateDirectory>`, {cpp:func}`CreateSymLink()
<BDirectory::CreateSymLink>` functions create nodes of the designated
flavor. The functions don't take {hclass}`BEntry` arguments directly;
instead, you invoke the functions on the {hclass}`BEntry`'s directory,
passing the entry's leaf name as an argument. Here we turn an abstract
entry ({hparam}`entry`) into a directory:

:::{code} cpp
BPath path;
char name[B_FILE_NAME_LENGTH]; /* A buffer for the name. */
BDirectory parent; /* The parent of our entry. */
BDirectory target_dir; /* The product of the transformation. */

if (!entry.Exists()) {
   entry.GetParent(&path);
   entry.GetName(name);
   parent.SetTo(&path);
   parent.CreateDirectory(name, &dir);
}
:::

#### The Plain-File-Only Approach.

You can create a plain file by passing the {hclass}`BEntry` to the
{cpp:class}`BFile` constructor or {cpp:func}`SetTo() <BFile::SetTo>`
function. To do this, you also have to add {cpp:enumerator}`B_CREATE_FILE`
to the "open mode" flags:

:::{code} cpp
BFile file;

if (!entry.Exists())
   file.SetTo(&entry, B_CREATE_FILE|B_READ_WRITE);
:::

## Subtleties and Details

The following details understand you should, particularly if you want to
participate in bedevtalk.

### File Descriptors

Although it's not intuitively obvious, a {hclass}`BEntry` object does
consume a file descriptor. The file descriptor is opened on the entry's
directory.

Your app has a limited number of file descriptors (currently 128, max), so
you may not want to cache {hclass}`BEntry` objects as your primary means
for identifying an entry. If you're going to be dealing with a lot of
entries and you want to keep track of them all, it's better to cache
{htype}`entry_ref` structures or {cpp:class}`BPath` objects.

### Directories are Persistent, Names Are Not

One more time: A {hclass}`BEntry` identifies an entry as a name in a
directory. As described above, the directory is maintained internally as a
file descriptor; the name is simply a string. This means that…

-   The directory for a given BEntry is persistent. If you move the directory,
the file descriptor, and so the BEntry, moves with it.

-   The name isn't persistent. If the user renames the leaf that a BEntry is
pointing to, the BEntry will become abstract.

For example, take the following {hclass}`BEntry`…

:::{code} cpp
BEntry entry("/boot/home/lbj/footFetish.jpeg");
:::

If the user moves the directory…

:::{code} sh
$ cd /boot/home
$ mv lbj jfk
:::

The {hclass}`BEntry` ({hparam}`entry`) "moves" with the directory. If you
print the pathname and ask if the {hclass}`BEntry`'s entry exists…

:::{code} cpp
BPath path;
entry.GetPath(&path);
printf("> Foot movie: %sn", path.Path());
printf("> Exists? %sn", entry.Exists()?"Oui":"Non");
:::

…you'll see this:

:::{code} sh
> Foot movie: /boot/home/jfk/footFetish.jpeg
> Exists? Oui
:::

The same isn't so for the name portion of a {hclass}`BEntry`. If the user
now moves footFetish.jpeg…

:::{code} sh
$ cd /boot/home/jfk
$ mv footFetish.jpeg hammerToe.jpeg
:::

…your {hclass}`BEntry` will not follow the file (it doesn't "follow the
data"). The object will still represent the entry called footFetish.jpeg.
The {hclass}`BEntry` will, in this case, become abstract.

Don't be confused: The {hclass}`BEntry` only "loses track" of a renamed
entry if the name change is made behind the object's back. Manipulating the
entry name through the {hclass}`BEntry` object's {cpp:func}`Rename()
<BEntry::Rename>` function (for example), doesn't baffle the object. For
example:

:::{code} cpp
BPath path;
BEntry entry("/boot/home/lbj/footFetish.jpeg");

entry.Rename("hammerToe.jpeg");
entry.GetPath(&path);
printf("> Foot movie: %sn", path.Path());
printf("> Exists? %sn", entry.Exists()?"Oui":"Non");
:::

…and we see…

:::{code} sh
> Foot movie: /boot/home/lbj/hammerToe.jpeg
> Exists? Oui
:::

### BEntries and Locked Nodes

You can't lock an entry, but you can lock the entry's node (through
{cpp:class}`BNode`'s {cpp:func}`Lock() <BNode::Lock>` function).
Initializing a {hclass}`BEntry` to point to a locked node is permitted, but
the entry's directory must not be locked. If the directory is locked, the
{hclass}`BEntry` constructor and {cpp:func}`SetTo() <BEntry::SetTo>`
function fail and set {cpp:func}`InitCheck() <BEntry::InitCheck>` to
{cpp:enumerator}`B_BUSY`.

Furthermore, the destination directories in {hclass}`BEntry`'s
{cpp:func}`Rename() <BEntry::Rename>` and {cpp:func}`MoveTo()
<BEntry::MoveTo>` must be unlocked for the functions to succeed. And all
directories in the path to the entry must be unlocked for
{cpp:func}`GetPath() <BEntry::GetPath>` to succeed.

If you get a {cpp:enumerator}`B_BUSY` error, you may want to try
again—it's strongly advised that locks be held as briefly as possible.
