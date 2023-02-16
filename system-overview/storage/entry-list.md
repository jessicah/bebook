# BEntryList

{hclass}`BEntryList` is a pure abstract class that defines the protocol
for iterating over a set of file system entries. Each derived class must
figure out how to create (or "discover") the entry list in the first place:
{hclass}`BEntryList` only supplies functions for getting entries out of the
list, it doesn't let you put them in. The {hclass}`BEntryList` class has
two derived classes: {cpp:class}`BDirectory` and {cpp:class}`BQuery`.

At the heart of the {hclass}`BEntryList` class are the three
{hmethod}`GetNext…()` functions, which let you retrieve the entries as…

-   {cpp:class}`BEntry` objects ({cpp:func}`GetNextEntry()
<BEntryList::GetNextEntry>`),

-   {htype}`entry_ref` structures ({cpp:func}`GetNextRef()
<BEntryList::GetNextRef>`),

-   or {htype}`dirent` ("directory entry") structures
({cpp:func}`GetNextDirents() <BEntryList::GetNextDirents>`).

You call these functions iteratively; each call gets the "next" entry (or
set of entries in the case of {cpp:func}`GetNextDirents()
<BEntryList::GetNextDirents>`). You check the {hmethod}`GetNext…()` return
value to detect the end of the list:

-   For {cpp:func}`GetNextEntry() <BEntryList::GetNextEntry>` and
{cpp:func}`GetNextRef() <BEntryList::GetNextRef>`,
{cpp:enumerator}`B_ENTRY_NOT_FOUND` indicates that there are no more
entries to get.

-   {cpp:func}`GetNextDirents() <BEntryList::GetNextDirents>` returns 0 when
it's at the end of the list.

To get back to the top of an entry list, you call {cpp:func}`Rewind()
<BEntryList::Rewind>`, but note…

:::{admonition} Warning
:class: warning
{cpp:func}`Rewind() <BEntryList::Rewind>` applies to
{cpp:class}`BDirectory`s only. You can't rewind a {cpp:class}`BQuery`'s
entry list.
:::

Here's an example of an iteration over all the entries in a
{cpp:class}`BDirectory`, retrieved as {cpp:class}`BEntry` objects:

:::{code} cpp
BDirectory dir("/boot/home/fido");
BEntry entry;

dir.Rewind();
while (dir.GetNextEntry(&entry) == B_OK)
   /* do something with entry here. */
:::

The final {hclass}`BEntryList` function, {cpp:func}`CountEntries()
<BEntryList::CountEntries>`, also only applies to {cpp:class}`BDirectory`s;
but even there you shouldn't depend on it. The count is stale as soon as
{cpp:func}`CountEntries() <BEntryList::CountEntries>` returns. The user
could create a new file or delete a file in the directory while you're
iterating over the entries. Also, {cpp:func}`CountEntries()
<BEntryList::CountEntries>` shares the entry list pointer with the
{hmethod}`GetNext…()` functions. You mustn't intermingle a
{cpp:func}`CountEntries() <BEntryList::CountEntries>` call within your
{hmethod}`GetNext…()` loop.

One more {cpp:class}`BDirectory` wrinkle:

-   Entries are retrieved in "directory order". (This is a POSIX term that
means, roughly, ASCII order.) If the user renames a file while you're
iterating over the directory, it's possible that the file won't be seen, or
will show up under its old name and its new name.

## The Entry List Pointer

Each {hclass}`BEntryList` object has a single iterator pointer that's
shared by all three {hmethod}`GetNext…()` formats (and
{cpp:func}`CountEntries() <BEntryList::CountEntries>`). Thus, each
successive call to a {hmethod}`GetNext…()` function gets the next entry,
regardless of the format. For example:

:::{code} cpp
BEntry entry;
entry_ref ref;

dir.GetNextEntry(&entry);
dir.GetNextRef(&ref);
:::

Here, {hparam}`entry` represents the first entry in the directory, and
{hparam}`ref` represents the second entry.

## Multiple Retrieval

{cpp:func}`GetNextDirents() <BEntryList::GetNextDirents>` is different
from the other two flavors in that it can retrieve more than one entry at a
time. Or it will, someday; currently {cpp:func}`GetNextDirents()
<BEntryList::GetNextDirents>` retrieves only one entry at a time, no matter
how many you ask for.

## Choosing an Iterator

So, which flavor of {hmethod}`GetNext…()` should you use? Here's how they
compare:

-   {cpp:func}`GetNextDirents() <BEntryList::GetNextDirents>` is by far the
fastest (even in the current one-struct-at-a-time version), but it's also
the least wieldy—the protocol isn't nearly as nice as the other two
functions. The {htype}`dirent` structure, while jam-packed with fun facts,
usually has to be turned into other structures ({htype}`node_ref`s or
{htype}`entry_ref`s) in order to be useful.

-   {cpp:func}`GetNextRef() <BEntryList::GetNextRef>` is slower, but the
{htype}`entry_ref` structure can be immediately usable (or, at least,
cachable). Nonetheless, you're still a step away from a "real" object.

-   {cpp:func}`GetNextEntry() <BEntryList::GetNextEntry>` is the slowest, but
at least it hands you an object that you can sink your teeth into.

The actual timing numbers depend on your machine, the class that you're
invoking the functions through, and some other factors. But the difference
is (ahem) significant: {cpp:func}`GetNextDirents()
<BEntryList::GetNextDirents>` is about an order of magnitude faster than
{cpp:func}`GetNextEntry() <BEntryList::GetNextEntry>`, with
{cpp:func}`GetNextRef() <BEntryList::GetNextRef>` right about in the
middle.

If, for example, you're simply compiling a list of leaf names, you should
certainly use {cpp:func}`GetNextDirents() <BEntryList::GetNextDirents>`
(painful though it may be). But if you plan on actually doing something
with each and every entry that you retrieve, then bite the bullet: Use
{cpp:func}`GetNextEntry() <BEntryList::GetNextEntry>`.

## The dirent Structure and GetNextDirents()

Of the three iterator functions, {cpp:func}`GetNextDirents()
<BEntryList::GetNextDirents>` needs some explanation. The dirent structure,
which is what the function returns, describes aspects of the retrieved
entry:

:::{code} c
typedef struct dirent {
   dev_t d_dev;
   ino_t d_ino;
   dev_t d_pdev;
   ino_t d_pino;
   unsigned short d_reclen;
   char d_name[1];
} dirent;
:::

The fields are:

-   {hparam}`d_dev` is a device id that identifies the device (file system) on
which this entry lies.

-   {hparam}`d_ino` is the node number for this entry's node.

-   {hparam}`d_pdev` and {hparam}`d_pino` are the device and inode numbers for
the parent directory.

-   {hparam}`d_reclen` is the length of this {htype}`dirent` structure. The
length is variable because…

-   {hparam}`d_name` is a buffer that's allocated to hold the
({cpp:expr}`NULL`-terminated) name of this entry.

So—let's pretend we've retrieved a {htype}`dirent` and we want to do
something with it. In addition to looking at individual fields, we can
combine some of them to make other structures:

-   {hparam}`d_dev` + {hparam}`d_ino` = {htype}`node_ref` of the entry's node

-   {hparam}`d_pdev` + {hparam}`d_pino` = {htype}`node_ref` of the parent
directory

-   {hparam}`d_pdev` + {hparam}`d_pino` + {hparam}`d_name` =
{htype}`entry_ref` for the entry

In code:

:::{code} c
dirent* dent;
entry_ref ref;
node_ref nref;
node_ref pnref;

/* Allocate and fill the dirent here... */
...

/* Make a node_ref to this entry's node. */
nref.device = dirent->d_dev;
nref.node = dirent->d_ino;

/* Make a node_ref to this entry's parent. */
pnref.device = dirent->d_pdev;
pnref.node = dirent->d_pino;

/* Make an entry_ref to this entry. */
ref.device = dirent->d_pdev;
ref.directory = dirent->d_pino;
ref.set_name(dirent->d_name);
:::

Where you go from here is a simple matter of programming. Me? I'm going to
lunch.

::::{abi-group}
Now that we know what to do with a dirent, let's see how to get one. The
{cpp:func}`GetNextDirents() <BEntryList::GetNextDirents>` protocol looks
like this:

:::{cpp:function} int32 BEntryList::GetNextDirents(dirent* buf, size_t bufsize, int32 count = INT_MAX)
:::

By default, the function stuffs as many {htype}`dirent` structs as it can
into the first {hparam}`bufsize` bytes of {hparam}`buf`. These structures
represent the next N entries in the entry list. The {hparam}`count`
argument lets you set a limit to the number of structures that you want to
be retrieved at a time. The function returns the number of structures that
it actually got.

:::{admonition} Warning
:class: warning
Keep in mind that currently {cpp:func}`GetNextDirents()
<BEntryList::GetNextDirents>` can only read one dirent at a time,
regardless of the size of {hparam}`buf`, or the value of {hparam}`count`.
:::

Let's try it. For the purposes of this example, we'll convert each
{htype}`dirent` into an {htype}`entry_ref`, as described in the previous
section.

:::{code} c
/* This is the buffer that we'll stuff structures into. */
char buf[4096];
dirent* dent;
entry_ref ref;

/* We'll assume dir is a valid BDirectory object. */
while ((count = dir.GetNextDirents((dirent*)buf, 4096)) > 0) {
   dent = (dirent*)buf;

   /* Now we step through the dirents. */
   while (count-- > 0) {
      ref.device = dent->d_pdev;
      ref.directory = dent->d_pino;
      ref.set_name(dent->d_name);

      /* Do something with the ref. */
      ...

      /* Bump the pointer. */
      dent = (dirent*)((char*)dent + dent->d_reclen);
   }
}
:::

Remember, the structure is variable length—you have to increment the
pointer by hand, as shown here.
::::
