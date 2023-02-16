:::{cpp:class} BEntry
:::

# BEntry

## Constructor and Destructor

::::{abi-group}
:::{cpp:function} BEntry::BEntry()
:::

:::{cpp:function} BEntry::BEntry(const BDirectory* dir, const char* path, bool traverse = false)
:::

:::{cpp:function} BEntry::BEntry(const entry_ref* entry, bool traverse = false)
:::

:::{cpp:function} BEntry::BEntry(const char* path, bool traverse = false)
:::

:::{cpp:function} BEntry::BEntry(const BEntry& entry)
:::

Creates a new {hclass}`BEntry` object that represents the entry described
by the arguments. See the analogous {cpp:func}`SetTo() <BEntry::SetTo>`
functions for descriptions of the flavorful constructors.

The default constructor does nothing; it should be followed by a call to
{cpp:func}`SetTo() <BEntry::SetTo>`.

The copy constructor points the new object to the entry that's represented
by the argument. The two objects themselves maintain separate
representation of the entry; in other words, they each contain their own a)
file descriptor and b) string to identify the entry's a) directory and b)
name.

To see if the initialization was successful, call {cpp:func}`InitCheck()
<BEntry::InitCheck>`.
::::

::::{abi-group}
:::{cpp:function} virtual BEntry::BEntry()
:::

Closes the {hclass}`BEntry`'s file descriptor and destroys the
{hclass}`BEntry` object.
::::

## Member Functions

::::{abi-group}
:::{cpp:function} bool BEntry::Exists() const
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
	- {cpp:enumerator}`true`
	- The entry exists.
-
	- {cpp:enumerator}`false`
	- otherwise.

:::
::::

::::{abi-group}
:::{cpp:function} status_t BEntry::GetName(char* buffer) const
:::

:::{cpp:function} status_t BEntry::GetPath(BPath* path) const
:::

These functions return the leaf name and full pathname of the
{hclass}`BEntry`'s entry. The arguments must be allocated before they're
passed in.

{hmethod}`GetName()` copies the leaf name into {hparam}`buffer`. The
{hparam}`buffer` must be large enough to accommodate the name;
{cpp:enumerator}`B_FILE_NAME_LENGTH` is a 100% safe bet:

:::{code} cpp
char name[B_FILE_NAME_LENGTH];
entry.GetName(name);
:::

If {hmethod}`GetName()` fails, {hparam}`*buffer` is pointed at
{cpp:expr}`NULL`.

{hmethod}`GetPath()` takes the entry's full pathname and initializes the
{cpp:class}`BPath` argument with it. To retrieve the path from the
{cpp:class}`BPath` object, call {cpp:func}`BPath::Path`:

:::{code} cpp
BPath path;
entry.GetPath(&path);
printf(">Entry pathname: %sn", path.Path());
:::

If {hmethod}`GetPath()` fails, the argument is {cpp:func}`Unset()
<BEntry::Unset>`.

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
	- The information was successfully retrieved.
-
	- {cpp:enumerator}`B_NO_INIT`.
	- The {hclass}`BEntry` isn't initialized.
-
	- {cpp:enumerator}`B_BUSY`
	- ({hmethod}`GetPath()` only). A directory in the entry's path is locked.

:::
::::

::::{abi-group}
:::{cpp:function} status_t BEntry::GetParent(BEntry* entry) const
:::

:::{cpp:function} status_t BEntry::GetParent(BDirectory* dir) const
:::

Gets the directory, as a {hclass}`BEntry` or {cpp:class}`BDirectory`
object, in which the object's entry lives. The argument must be allocated
before it's passed in.

If the function is unsuccessful, the argument is {cpp:func}`Unset()
<BEntry::Unset>`. Because of this, you should be particularly careful if
you're using the {hclass}`BEntry`-argument version to destructively get a
{hclass}`BEntry`'s parent:

:::{code} cpp
if (entry.GetParent(&entry) != B_OK) {
   /* you just lost 'entry' */
}
:::

This example __is__ legal; for example, you can use destructive iteration
to loop your way up to the root directory. When you reach the root ("/"),
{hmethod}`GetParent()` returns {cpp:enumerator}`B_ENTRY_NOT_FOUND`:

:::{code} cpp
BEntry entry("/boot/home/fido");
status_t err;
char name[B_FILE_NAME_LENGTH];

/* Spit out the path components backwards, one at a time. */
do {
   entry.GetName(name);
   printf("> %sn", name);
} while ((err=entry.GetParent(&entry)) == B_OK);

/* Complain for reasons other than reaching the top. */
if (err != B_ENTRY_NOT_FOUND)
   printf(">> Error: %sn", strerror(err));
:::

This produces:

:::{code} sh
> fido
> home
> boot
> /
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
	- The information was successfully retrieved.
-
	- {cpp:enumerator}`B_NO_INIT`.
	- This {hclass}`BEntry` isn't initialized.
-
	- {cpp:enumerator}`B_ENTRY_NOT_FOUND`.
	- Attempt to get the parent of the root directory.
-
	- {cpp:enumerator}`B_NO_MORE_FDS`.
	- Couldn't get another file descriptor.

:::
::::

::::{abi-group}
:::{cpp:function} status_t BEntry::GetRef(entry_ref* ref) const
:::

Gets the {htype}`entry_ref` for the object's entry; {hparam}`ref` must be
allocated before it's passed in. As with {hclass}`BEntry` objects,
{htype}`entry_ref` structures can be abstract—getting a valid
{htype}`entry_ref` does __not__ guarantee that the entry actually exists.

If the function isn't successful, {hparam}`ref` is unset.

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
	- The {htype}`entry_ref` was successfully retrieved.
-
	- {cpp:enumerator}`B_NO_INIT`.
	- This object isn't initialized.
-
	- {cpp:enumerator}`B_NO_MEMORY`.
	- Storage for the {htype}`entry_ref`'s name couldn't be allocated.

:::
::::

::::{abi-group}
:::{cpp:function} virtual status_t BEntry::GetStat(struct stat* st) const
:::

{hmethod}`GetStat()` returns the {htype}`stat` structure for the entry.
The structure is copied into the {hparam}`st` argument, which must be
allocated. The {cpp:class}`BStatable` object does not cache the
{htype}`stat` structure; every time you call {hmethod}`GetStat()`, fresh
stat information is retrieved.

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
	- The entry doesn't exist (abstract entry).

:::
::::

::::{abi-group}
:::{cpp:function} status_t BEntry::InitCheck() const
:::

Returns the status of the previous construction, assignment operation, or
{cpp:func}`SetTo() <BEntry::SetTo>` call.

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
	- The initialization was successful.
-
	- {cpp:enumerator}`B_NO_INIT`.
	- The object is uninitialized (this includes {cpp:func}`Unset()
		<BEntry::Unset>`).
-
	- Other errors.
	- See {cpp:func}`SetTo() <BEntry::SetTo>`

:::
::::

::::{abi-group}
:::{cpp:function} status_t BEntry::Remove()
:::

{hmethod}`Remove()` "unlinks" the entry from its directory. The entry's
node isn't destroyed until all file descriptors that are open on the node
are closed. This means that if you create {cpp:class}`BFile` based on a
{hclass}`BEntry`, and then {hmethod}`Remove()` the {hclass}`BEntry`, the
{cpp:class}`BFile` will still be able to read and write the file's data—the
{cpp:class}`BFile` has no way of knowing that the entry is gone. When the
{cpp:class}`BFile` is deleted, the node will be destroyed as well.

:::{admonition} Note
:class: note
{hmethod}`Remove()` does __not__ invalidate the {hclass}`BEntry`. It
simply makes it abstract (see "{ref}`Abstract Entries`").
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
	- {cpp:enumerator}`B_NO_INIT`.
	- The {hclass}`BEntry` is not initialized.
-
	- {cpp:enumerator}`B_BUSY`.
	- The entry's directory is locked.

:::
::::

::::{abi-group}
:::{cpp:function} status_t BEntry::Rename(const char* path, bool clobber = false)
:::

:::{cpp:function} status_t BEntry::MoveTo(BDirectory* dir, const char* path = NULL, bool clobber = false)
:::

These functions move the {hclass}`BEntry`'s entry and node to a new
location. In both cases, the {hclass}`BEntry` must not be abstract—you
can't rename or move an abstract entry.

{hmethod}`Rename()` moves the entry to a new name, as given by
{hparam}`path`. {hparam}`path` is usually a simple leaf name, but it can be
a relative path. In the former case (simple leaf) the entry is renamed
within its current directory. In the latter, the entry is moved into a
subdirectory of its current directory, as given by the argument.

{hmethod}`MoveTo()` moves the entry to a different directory and
optionally renames the leaf. Again, {hparam}`path` can be a simple leaf or
a relative path; in both cases, {hparam}`path` is reckoned off of
{hparam}`dir`. If path is {cpp:expr}`NULL`, the entry is moved to
{hparam}`dir`, but retains its old leaf name.

If the entry's new location is already taken, the clobber argument decides
whether the existing entry is removed to make way for yours. If it's
{cpp:expr}`true`, the existing entry is removed; if it's {cpp:expr}`false`,
the {hmethod}`Rename()` or {hmethod}`MoveTo()` function fails.

Upon success, this is updated to reflect the change to its entry. For
example, when you invoke {hmethod}`Rename()` on a {hclass}`BEntry`, the
name of __that specific__ {hclass}`BEntry` object also changes. If the
rename or move-to isn't successful, this isn't altered.

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
	- {cpp:enumerator}`B_NO_INIT`.
	- The {hclass}`BEntry` is not initialized.
-
	- {cpp:enumerator}`B_ENTRY_NOT_FOUND`.
	- A directory to the new location doesn't exist, or this is an abstract
		entry.
-
	- {cpp:enumerator}`B_FILE_EXISTS`.
	- The new location is already taken (and you're not clobbering).
-
	- {cpp:enumerator}`B_BUSY`.
	- The directory that you're moving the entry into is locked.

:::
::::

::::{abi-group}
:::{cpp:function} status_t BEntry::SetTo(const entry_ref* ref, bool traverse = false)
:::

:::{cpp:function} status_t BEntry::SetTo(const char* path, bool traverse = false)
:::

:::{cpp:function} status_t BEntry::SetTo(const BDirectory* dir, const char* path, bool traverse = false)
:::

:::{cpp:function} void BEntry::Unset()
:::

Frees the {hclass}`BEntry`'s current entry reference, and initializes it
to refer to the entry identified by the argument(s):

-   In the {hparam}`ref` version, the {hclass}`BEntry` is initialized to refer
to the given {htype}`entry_ref`.

-   In the {hparam}`path` version, {hparam}`path` can be absolute or relative,
and can contain "." and ".." elements. If {hparam}`path` is relative, it's
reckoned off of the current working directory.

-   In the {hparam}`dir`/{hparam}`path` version, {hparam}`path` must be
relative. It's reckoned off of the directory given by {hparam}`dir`.

The {hparam}`traverse` argument is used to resolve (or not) entries that
are symlinks:

-   If {hparam}`traverse` is {cpp:expr}`true`, the link is resolved.

-   If {hparam}`traverse` is {cpp:expr}`false`, the {hclass}`BEntry` refers to
the link itself.

See "{ref}`Initializing and Traversing`" for more information.

When you initialize a {hclass}`BEntry`, you're describing a leaf name
within a directory. The directory __must__ exist, but the leaf doesn't have
to. This allows you to create a {hclass}`BEntry` to a file that doesn't
exist (yet). See "{ref}`Abstract Entries`" for more information.

:::{admonition} Note
:class: note
Remember—successfully initializing a {hclass}`BEntry` consumes a file
descriptor. When you re-initialize, the old file descriptor is closed.
:::

{hmethod}`Unset()` removes the object's association with its current
entry, and sets {cpp:func}`InitCheck() <BEntry::InitCheck>` to
{cpp:enumerator}`B_NO_INIT`.

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
	- The {hclass}`BEntry` was successfully initialized.
-
	- {cpp:enumerator}`B_BAD_VALUE`.
	- Bad argument value; uninitialized {hparam}`ref` or {hparam}`dir`.
-
	- {cpp:enumerator}`B_ENTRY_NOT_FOUND`.
	- A directory in the path to the entry doesn't exist.
-
	- {cpp:enumerator}`B_ENTRY_NOT_FOUND`.
	- The entry's directory is locked.

:::
::::

## Operators

::::{abi-group}
:::{cpp:function} BEntry& BEntry::operator=(const BEntry& entry)
:::

In the expression

:::{code} cpp
BEntry a = b;
:::

{hclass}`BEntry` {hparam}`a` is initialized to refer to the same entry as
{hparam}`b`. To gauge the success of the assignment, you should call
{cpp:func}`InitCheck() <BEntry::InitCheck>` immediately afterwards.
Assigning a {hclass}`BEntry` to itself is safe.

Assigning from an uninitialized {hclass}`BEntry` is "successful": The
assigned-to {hclass}`BEntry` will also be uninitialized
({cpp:enumerator}`B_NO_INIT`).
::::

::::{abi-group}
:::{cpp:function} bool BEntry::operator==(const BEntry& entry) const
:::

:::{cpp:function} bool BEntry::operator!=(const BEntry& entry) const
:::

Two {hclass}`BEntry` objects are said to be equal if they refer to the
same entry (even if the entry is abstract), or if they're both
uninitialized.
::::

## Global C Function

::::{abi-group}
:::{cpp:function} status_t BEntry::get_ref_for_path(const char* path, entry_ref* ref)
:::

Returns in {hparam}`ref` an {htype}`entry_ref` for the file specified by
the {hparam}`path` argument.

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
	- The ref was returned successfully.
-
	- {cpp:enumerator}`B_ENTRY_NOT_FOUND`.
	- The file wasn't found, or the pathname string is empty.
-
	- {cpp:enumerator}`B_NO_MEMORY`.
	- Not enough memory.
-
	- Other file errors.
	- 


:::
::::

## Defined Types

::::{abi-group}
Declared in: storage/Entry.h

:::{code} cpp
struct entry_ref {
               entry_ref();
               entry_ref(dev_t device, ino_t dir, const char* name);
               entry_ref(const entry_ref& ref);
               ~entry_ref();

    status_t   set_name(const char* name);
    bool       operator==(const entry_ref& ref) const;
    bool       operator!=(const entry_ref& ref) const;
    entry_ref& operator=(const entry_ref& ref);

    dev_t      device;
    ino_t      directory;
    char*      name;
}
:::

The {htype}`entry_ref` structure describes a single entry in a directory.

-   {hparam}`device` contains the device number on which the entry's target is
located.

-   {hparam}`directory` contains the inode of the directory that contains the
entry's target.

-   {hparam}`name` contains the name of the entry.

:::{cpp:function} BEntry::entry_ref()
:::

:::{cpp:function} BEntry::entry_ref(const entry_ref& ref)
:::

:::{cpp:function} BEntry::entry_ref(dev_t device, ino_t dir, const char* name)
:::

The constructor for the {htype}`entry_ref` structure. The first of these
creates an empty {htype}`entry_ref`, the second duplicates an existing
{htype}`entry_ref`, and the last version of the constructor accepts a
device number, directory inode number, and a file name and constructs an
{htype}`entry_ref` referring to that entry.

:::{cpp:function} BEntry::~entry_ref()
:::

The destructor for {htype}`entry_ref`.

:::{cpp:function} status_t BEntry::set_name(const char* name)
:::

Lets you change the name of the file referred to by the {htype}`entry_ref`
structure.

{hmethod}`operator ==`

Lets you perform comparisons of {htype}`entry_ref` structures to see if
they refer to the same entry.

{hmethod}`operator !=`

Lets you test to see if two {htype}`entry_ref` structures refer to
different entries.
::::
