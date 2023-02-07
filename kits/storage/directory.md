# BDirectory
## Constructor and Destructor
::::{abi-group}

:::{cpp:function} BDirectory::BDirectory()
:::
:::{cpp:function} BDirectory::BDirectory(const entry_ref* ref)
:::
:::{cpp:function} BDirectory::BDirectory(const BEntry* entry)
:::
:::{cpp:function} BDirectory::BDirectory(const node_ref* nref)
:::
:::{cpp:function} BDirectory::BDirectory(const char* path)
:::
:::{cpp:function} BDirectory::BDirectory(const BDirectory* dir, const char* path)
:::
:::{cpp:function} BDirectory::BDirectory(const BDirectory& directory)
:::
Creates a new {hclass}`BDirectory` object that represents the directory as given by
the arguments. See the analogous
{cpp:func}`~BDirectory::SetTo` functions for descriptions of
the flavorful constructors.
- The default constructor does nothing; it should be followed by a call to {cpp:func}`~BDirectory::SetTo`.
- The copy constructor points the {hclass}`BDirectory` to the same directory as is represented by the argument. The two objects have their own entry iterators.

To check to see if an initialization was successful, call
{cpp:func}`~BNode::InitCheck`.
::::

::::{abi-group}

:::{cpp:function} virtual BDirectory::~BDirectory()()
:::
Deletes the object.
::::

## Member Functions
::::{abi-group}

:::{cpp:function} bool BDirectory::Contains(const char* path, int32 nodeFlags = B_ANY_NODE) const
:::
:::{cpp:function} bool BDirectory::Contains(const BEntry* entry, int32 nodeFlags = B_ANY_NODE) const
:::
Returns {cpp:enum}`true` if {hparam}`path` or
{hparam}`entry` is contained within this directory, or in any
of its subdirectories (no matter how deep). You can use the
{hparam}`nodeFlags` argument to limit the search to a
particular flavor of node:
:::{list-table}
---
header-rows: 1
---
-
	- Constant
	- Description
-
	- {cpp:enum}`B_FILE_NODE`
	- Looks for a "plain" file.
-
	- {cpp:enum}`B_DIRECTORY_NODE`
	- Looks for a directory.
-
	- {cpp:enum}`B_SYMLINK_NODE`
	- Looks for a symbolic link.
-
	- {cpp:enum}`B_ANY_NODE`
	- (The default) Doesn't discriminate between flavors.
:::
::::

::::{abi-group}

:::{cpp:function} status_t BDirectory::CreateFile(const char* path, BFile* file, bool failIfExists = false)
:::
:::{cpp:function} status_t BDirectory::CreateDirectory(const char* path, BDirectory* dir)
:::
:::{cpp:function} status_t BDirectory::CreateSymLink(const char* path, const char* linkToPath, BSymLink* link)
:::

These functions create a new file, directory, or symbolic link. The new
node is located at {hparam}`path`. If {hparam}`path` is relative, it's reckoned off of the
directory represented by this {hclass}`BDirectory`; if it's absolute, the path of
this {hclass}`BDirectory` is ignored.

- {hmethod}`CreateFile()` fails if the file already exists and {hparam}`failIfExists` is {cpp:enum}`true`. If the flag is {cpp:enum}`false` (and the file exists), the old file is clobbered and a new one is created. If successful, the {cpp:class}`BFile` argument that you pass in is opened on the new file in {cpp:enum}`B_READ_WRITE` mode.
- {hmethod}`CreateDirectory()` and {hmethod}`CreateSymLink()` fail if {hparam}`path` already exists—you can't clobber an existing directory or link.
- The {hparam}`linkToPath` argument ({hmethod}`CreateSymLink()`) is the path that the new symbolic link will be linked to.

The object argument (the
{hclass}`BDirectory`,
{cpp:class}`BFile`, or
{cpp:class}`BSymLink`)
may be {cpp:enum}`NULL`. If
the function fails, the object argument, if non-{cpp:enum}`NULL`, is
{cpp:func}`~BDirectory::Unset`.

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
	- {cpp:enum}`B_BAD_VALUE`.
	- Illegal {hparam}`path`, {hparam}`file`, {hparam}`dir`, or {hparam}`link` specified; may be {cpp:enum}`NULL`. path may be empty.
-
	- {cpp:enum}`B_BUSY`.
	- A busy node could not be accessed.
-
	- {cpp:enum}`B_ENTRY_NOT_FOUND`.
	- The specified {hparam}`path` does not exist or is an empty string.
-
	- {cpp:enum}`B_FILE_ERROR`.
	- A file system error prevented the operation.
-
	- {cpp:enum}`B_FILE_EXISTS`.
	- The file specified by {hparam}`path` already exists.
-
	- {cpp:enum}`B_LINK_LIMIT`.
	- A cyclic loop has been detected in the file system.
-
	- {cpp:enum}`B_NAME_TOO_LONG`.
	- The {hparam}`path` specified is too long.
-
	- {cpp:enum}`B_NO_MEMORY`.
	- Insufficient memory to perform the operation.
-
	- {cpp:enum}`B_NO_MORE_FDS`.
	- All file descriptors are in use (too many open files).
-
	- {cpp:enum}`B_IS_A_DIRECTORY`.
	- Can't replace a directory with a file.
-
	- {cpp:enum}`B_NOT_A_DIRECTORY`.
	- A component of the {hparam}`path` is not a directory.
-
	- {cpp:enum}`B_NOT_ALLOWED`.
	- The volume is read-only.
-
	- {cpp:enum}`B_PERMISSION_DENIED`.
	- Create access is denied in the specified {hparam}`path`.
-
	- {cpp:enum}`E2BIG`.
	- {hparam}`linkToPath` is too long ({hmethod}`CreateSymLink()` only).
:::
::::

::::{abi-group}

:::{cpp:function} status_t BDirectory::FindEntry(const char* path, BEntry* entry, bool traverse = false) const
:::

Finds the entry with the given name, and sets the second argument to
refer to that entry.

- {hparam}`path` must be a relative pathname. It's reckoned off of the {hclass}`BDirectory`'s directory.
- You are allowed to look for "." and "..". The former represents this directory's entry. The latter refers to this directory's parent.
- The {hparam}`entry` argument must be allocated before it's passed in (it needn't be initialized).
- The {hparam}`traverse` applies to symbolic links: If the flag is {cpp:enum}`true`, the link is traversed. If it's {cpp:enum}`false`, you get the {cpp:class}`BEntry` that points to the link itself.

If {hparam}`path` isn't found, the second argument is
automatically {cpp:func}`~BDirectory::Unset`. To
find out why the lookup failed, invoke
{cpp:func}`~BNode::InitCheck`
on the {hparam}`entry` argument:

:::{code}
BEntry entry;
status_t err;
if (dir.FindEntry("aFile", &entry) != B_OK) {
   err = entry.InitCheck();
}
:::

The direct return value is also informative, but it may not be as precise
as the {cpp:func}`~BNode::InitCheck`
value.

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
	- {cpp:enum}`B_BAD_VALUE`.
	- Invalid {hparam}`path` specified; it may be {cpp:enum}`NULL` or empty.
-
	- {cpp:enum}`B_ENTRY_NOT_FOUND`.
	- The specified {hparam}`path` does not exist.
-
	- {cpp:enum}`B_NAME_TOO_LONG`.
	- The {hparam}`path` specified is too long.
-
	- {cpp:enum}`B_LINK_LIMIT`.
	- A cyclic loop has been detected in the file system.
-
	- {cpp:enum}`B_NO_MEMORY`.
	- Insufficient memory to perform the operation.
-
	- {cpp:enum}`B_FILE_ERROR`.
	- An invalid file prevented the operation.
:::
::::

::::{abi-group}

:::{cpp:function} status_t BDirectory::GetEntry(BEntry* entry) const
:::

Initializes {hparam}`entry` to represent this
{hclass}`BDirectory`. If the initialization
fails, {hparam}`entry` is
{cpp:func}`~BDirectory::Unset`.

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
	- {cpp:enum}`B_NAME_TOO_LONG`.
	- The path specified by {hparam}`entry` is too long.
-
	- {cpp:enum}`B_ENTRY_NOT_FOUND`.
	- The specified path does not exist.
-
	- {cpp:enum}`B_LINK_LIMIT`.
	- A cyclic loop has been detected in the file system.
-
	- {cpp:enum}`B_BAD_VALUE`.
	- {hparam}`entry` is uninitialized.
-
	- {cpp:enum}`B_NO_MEMORY`.
	- Insufficient memory to perform the operation.
-
	- {cpp:enum}`B_BUSY`.
	- A busy node could not be accessed.
-
	- {cpp:enum}`B_FILE_ERROR`.
	- An invalid file prevented the operation.
-
	- {cpp:enum}`B_NO_MORE_FDS`.
	- All file descriptors are in use (too many open files).
-
	- {cpp:enum}`B_NOT_A_DIRECTORY`.
	- The path includes non-directory entries.
:::
::::

::::{abi-group}

:::{cpp:function} virtual status_t BDirectory::GetNextEntry(BEntry* entry, bool traverse = false)
:::
:::{cpp:function} virtual status_t BDirectory::GetNextRef(entry_ref* ref)
:::
:::{cpp:function} virtual int32 BDirectory::GetNextDirents(dirent* buf, size_t bufsize, int32 count = INT_MAX)
:::
:::{cpp:function} virtual int32 BDirectory::CountEntries()
:::
:::{cpp:function} virtual status_t BDirectory::Rewind()
:::

The three {hmethod}`GetNext…()` functions retrieve the "next" entry that lives in
the {hclass}`BDirectory` and returns it as a
{cpp:class}`BEntry`,
entry_ref, or dirent structure.

- {hmethod}`GetNextEntry()` returns the entry as a {cpp:class}`BEntry` object. If {hparam}`traverse` is {cpp:enum}`true` and the entry is a symbolic link, the link is traversed. In other words, {hparam}`entry` could end up being in a different directory than the one referred to by this. When all entries have been visited, the function returns {cpp:enum}`B_ENTRY_NOT_FOUND`. The {hparam}`entry` argument must be allocated before it's passed in.
- {hmethod}`GetNextRef()` return the next entry in {hparam}`ref`. Since an entry_ref doesn't supply enough information to determine if the entry is a link, there's no question of traversal: The entry_ref points to exactly the next entry. When all entries have been visited, the function returns {cpp:enum}`B_ENTRY_NOT_FOUND`. The {hparam}`ref` argument must be allocated before it's passed in.
- {hmethod}`GetNextDirents()` returns some number of dirent structures, either as many as can be stuffed into {hparam}`buf` (where {hparam}`bufsize` gives the size of {hparam}`buf`), or {hparam}`count` structures, whichever is smaller. The function returns the number of structures that were stuffed into {hparam}`buf`; when all entries have been visited, it returns 0.

:::{admonition} Warning
:class: warning
Currently, {hmethod}`GetNextDirents()` only reads
one dirent at a time, no matter
how many you ask for.
:::

{hmethod}`GetNextEntry()` and {hmethod}`GetNextRef()`
are reasonably clear; the dirent version
deserves more explanation. You'll find this explanation (and an example)
in the {cpp:class}`BEntryList`
class. Also, keep in mind that the set of candidate
entries is different for the dirent version:
{hmethod}`GetNextDirents()` finds all
entries, including the entries for "." and "..". The other two versions
skip these entries.

When you're done reading the {hclass}`BDirectory`'s entries, you can rewind the
object's entry iterator by calling
{cpp:func}`~BDirectory::Rewind`.

{hmethod}`CountEntries()` returns the number of entries
(not counting "." and "..")
in the directory.

:::{admonition} Warning
:class: warning
Never call {hmethod}`CountEntries()` while you're iterating through the directory.
{hmethod}`CountEntries()` does a rewind, iterates through the entries, and then
rewinds again.
:::
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
	- {cpp:enum}`B_FILE_ERROR`.
	- {hclass}`BDirectory` object has not been properly initialized.
-
	- {cpp:enum}`B_NOT_A_DIRECTORY`.
	- The directory is invalid.
-
	- {cpp:enum}`B_NAME_TOO_LONG`.
	- The dirent's name is too long.
-
	- {cpp:enum}`B_ENTRY_NOT_FOUND`.
	- End of directory reached.
-
	- {cpp:enum}`B_LINK_LIMIT`.
	- A cyclic loop has been detected in the file system.
-
	- {cpp:enum}`B_BAD_VALUE`.
	- Invalid input specified, or {hclass}`BDirectory` object has not been properly initialized.
-
	- {cpp:enum}`B_NO_MEMORY`.
	- Insufficient memory to perform the operation.
:::
::::

::::{abi-group}

:::{cpp:function} status_t BDirectory::GetStatFor(const char* path, stat* st) const
:::

Gets the stat structure for the entry designated by {hparam}`path`. {hparam}`path` may be
either absolute or relative; if it's relative, it's reckoned off of the
{hclass}`BDirectory`'s directory. This is, primarily, a convenience function; but
it's also provided for efficiency.

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
	- {cpp:enum}`B_FILE_ERROR`.
	- An invalid file prevented the operation.
-
	- {cpp:enum}`B_NAME_TOO_LONG`.
	- The {hparam}`path` specified is too long.
-
	- {cpp:enum}`B_ENTRY_NOT_FOUND`.
	- The specified {hparam}`path` does not exist.
-
	- {cpp:enum}`B_LINK_LIMIT`.
	- A cyclic loop has been detected in the file system.
-
	- {cpp:enum}`B_BAD_VALUE`.
	- Invalid input specified; the {hparam}`path` may be {cpp:enum}`NULL` or empty.
-
	- {cpp:enum}`B_NO_MEMORY`.
	- Insufficient memory to perform the operation.
:::
::::

::::{abi-group}

:::{cpp:function} bool BDirectory::IsRootDirectory() const
:::

Returns {hparam}`true` if this {hclass}`BDirectory` represents a root directory. A root
directory is the directory that's at the root of a volume's file
hierarchy. Every volume has exactly one root directory; all other files
in the volume's hierarchy descend from the root directory.

::::

::::{abi-group}

:::{cpp:function} status_t BDirectory::SetTo(const entry_ref* ref)
:::
:::{cpp:function} status_t BDirectory::SetTo(const node_ref* nref)
:::
:::{cpp:function} status_t BDirectory::SetTo(const BEntry* entry)
:::
:::{cpp:function} status_t BDirectory::SetTo(const char* path)
:::
:::{cpp:function} status_t BDirectory::SetTo(const BDirectory* directory, const char* path)
:::
:::{cpp:function} void BDirectory::Unset()
:::

Closes the {hclass}`BDirectory`'s current directory (if any), and initializes the
object to open the directory as given by the arguments.

- In the {hparam}`path` version, path can be absolute or relative, and can contain "." and ".." elements. If {hparam}`path` is relative, it's reckoned off of the current working directory.
- In the {hparam}`dir`/{hparam}`path` version, {hparam}`path` must be relative. It's reckoned off of the directory given by {hparam}`dir`.

If the specification results in a symbolic link that resolves to a
directory, then the linked-to directory is opened. If the specification
is (or resolves to) a regular file, the initialization fails.

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
	- {cpp:enum}`B_NAME_TOO_LONG`.
	- The {hparam}`path` specified is too long.
-
	- {cpp:enum}`B_ENTRY_NOT_FOUND`.
	- The directory does not exist.
-
	- {cpp:enum}`B_LINK_LIMIT`.
	- A cyclic loop has been detected in the file system.
-
	- {cpp:enum}`B_BAD_VALUE`.
	- Invalid input specified.
-
	- {cpp:enum}`B_NO_MEMORY`.
	- Insufficient memory to perform the operation.
-
	- {cpp:enum}`B_BUSY`.
	- A busy node could not be accessed.
-
	- {cpp:enum}`B_FILE_ERROR`.
	- An invalid file prevented the operation.
-
	- {cpp:enum}`B_NO_MORE_FDS`.
	- All file descriptors are in use (too many open files).
:::
::::

## Operators
::::{abi-group}

:::{cpp:function} BDirectory& BDirectory::operator=(const BDirectory& directory)
:::

In the expression

:::{code}
BDirectory a = b;
:::

{hclass}`BDirectory` a is initialized to
refer to the same directory as b. To gauge
the success of the assignment, you should call
{cpp:func}`~BNode::InitCheck` immediately
afterwards. Assigning a {hclass}`BDirectory` to itself is safe.

Assigning from an uninitialized {hclass}`BDirectory` is "successful": The
assigned-to {hclass}`BDirectory` will also be
uninitialized ({cpp:enum}`B_NO_INIT`).

::::

## C Functions
::::{abi-group}


:::{cpp:function} status_t BDirectory::create_directory(const char* path, mode_t mode)
:::

Creates all missing directories along the path specified by {hparam}`path`.

- The pathname can be absolute or relative. If it's relative, the path is reckoned of the current working directory. If any symlinks are found in the existing portion of the path, they're traversed.
- {hparam}`path` can contain ".", but it may not contain "..".
- {hparam}`mode` is the permissions setting (typically expressed as an octal number) that's assigned to all directories that are created. To set the directories to be readable, writable, and "enterable" by all (for example), you would set the mode to 0777.

:::{list-table}
---
header-rows: 1
---
-
	- Return Code
	- Description
-
	- {cpp:enum}`B_OK`.
	- {hparam}`path` now fully exists (or did in the first place).
-
	- {cpp:enum}`B_BAD_VALUE`.
	- {hparam}`path` is {cpp:enum}`NULL`, is empty, or contains "..".
-
	- {cpp:enum}`B_NOT_ALLOWED`.
	- Read-only volume.
-
	- {cpp:enum}`B_NO_MEMORY`.
	- Insufficient memory to perform the operation.
:::
::::

::::{abi-group}


Declared in: storage/FindDirectory.h

:::{cpp:function} status_t BDirectory::find_directory(directory_which which, dev_t volume, bool create_it, char* path_string, int32 length)
:::
:::{cpp:function} status_t BDirectory::find_directory(directory_which which, BPath* path_obj, bool create_it = false, BVolume volume = NULL)
:::
:::{admonition} Note
:class: note
The first version of this function can be used in either C or C++ code.
The second version is for C++ code only.
:::

Finds the path to the directory symbolized by {hparam}`which` and copies it into
{hparam}`path_string`, or uses it to initialize {hparam}`path_obj`.

- The {hparam}`create_it` argument tells the function to create the directory if it doesn't already exist.
- {hparam}`volume` identifies the volume (as a dev_t identifier or {cpp:class}`BVolume` object) on which you want to look. The C++ default ({cpp:enum}`NULL`) means to look in the boot volume.
- The {hparam}`length` argument (first version only) gives the length of {hparam}`path`.

The {cpp:func}`~Constants::directory`
constants are described below.
:::{list-table}
---
header-rows: 1
---
-
	- Return Code
	- Description
-
	- {cpp:enum}`B_OK`.
	- The directory was found.
-
	- Other codes.
	- The directory wasn't found or couldn't be created.
:::
::::

## Constants
::::{abi-group}









































Declared in: storage/FindDirectory.h
:::{list-table}
---
header-rows: 1
---
-
	- Constant
	- Description
-
	- {cpp:enum}`B_DESKTOP_DIRECTORY`
	- Desktop directory.
-
	- {cpp:enum}`B_TRASH_DIRECTORY`
	- Trash directory.
-
	- {cpp:enum}`B_APPS_DIRECTORY`
	- Applications directory.
-
	- {cpp:enum}`B_PREFERENCES_DIRECTORY`
	- Preferences directory.
-
	- {cpp:enum}`B_BEOS_DIRECTORY`
	- BeOS directory.
-
	- {cpp:enum}`B_BEOS_SYSTEM_DIRECTORY`
	- System directory.
-
	- {cpp:enum}`B_BEOS_ADDONS_DIRECTORY`
	- BeOS add-ons directory.
-
	- {cpp:enum}`B_BEOS_BOOT_DIRECTORY`
	- Boot volume's root directory.
-
	- {cpp:enum}`B_BEOS_FONTS_DIRECTORY`
	- BeOS fonts directory.
-
	- {cpp:enum}`B_BEOS_LIB_DIRECTORY`
	- BeOS libraries directory.
-
	- {cpp:enum}`B_BEOS_SERVERS_DIRECTORY`
	- BeOS servers directory.
-
	- {cpp:enum}`B_BEOS_APPS_DIRECTORY`
	- BeOS applications directory.
-
	- {cpp:enum}`B_BEOS_BIN_DIRECTORY`
	- /bin directory.
-
	- {cpp:enum}`B_BEOS_ETC_DIRECTORY`
	- /etc directory.
-
	- {cpp:enum}`B_BEOS_DOCUMENTATION_DIRECTORY`
	- BeOS documentation directory.
-
	- {cpp:enum}`B_BEOS_PREFERENCES_DIRECTORY`
	- BeOS preferences directory.
-
	- {cpp:enum}`B_COMMON_DIRECTORY`
	- The common directory, shared by all users.
-
	- {cpp:enum}`B_COMMON_SYSTEM_DIRECTORY`
	- The shared system directory.
-
	- {cpp:enum}`B_COMMON_ADDONS_DIRECTORY`
	- The shared addons directory.
-
	- {cpp:enum}`B_COMMON_BOOT_DIRECTORY`
	- The shared boot directory.
-
	- {cpp:enum}`B_COMMON_FONTS_DIRECTORY`
	- The shared fonts directory.
-
	- {cpp:enum}`B_COMMON_LIB_DIRECTORY`
	- The shared libraries directory.
-
	- {cpp:enum}`B_COMMON_SERVERS_DIRECTORY`
	- The shared servers directory.
-
	- {cpp:enum}`B_COMMON_BIN_DIRECTORY`
	- The shared /bin directory.
-
	- {cpp:enum}`B_COMMON_ETC_DIRECTORY`
	- The shared /etc directory.
-
	- {cpp:enum}`B_COMMON_DOCUMENTATION_DIRECTORY`
	- The shared documentation directory.
-
	- {cpp:enum}`B_COMMON_SETTINGS_DIRECTORY`
	- The shared settings directory.
-
	- {cpp:enum}`B_COMMON_DEVELOP_DIRECTORY`
	- The shared develop directory.
-
	- {cpp:enum}`B_COMMON_LOG_DIRECTORY`
	- The shared log directory.
-
	- {cpp:enum}`B_COMMON_SPOOL_DIRECTORY`
	- The shared spool directory.
-
	- {cpp:enum}`B_COMMON_TEMP_DIRECTORY`
	- The shared temporary items directory.
-
	- {cpp:enum}`B_COMMON_VAR_DIRECTORY`
	- The shared /var directory.
-
	- {cpp:enum}`B_USER_DIRECTORY`
	- The user's home directory.
-
	- {cpp:enum}`B_USER_CONFIG_DIRECTORY`
	- The user's config directory.
-
	- {cpp:enum}`B_USER_ADDONS_DIRECTORY`
	- The user's add-ons directory.
-
	- {cpp:enum}`B_USER_BOOT_DIRECTORY`
	- The user's /boot directory.
-
	- {cpp:enum}`B_USER_FONTS_DIRECTORY`
	- The user's fonts directory.
-
	- {cpp:enum}`B_USER_LIB_DIRECTORY`
	- The user's libraries directory.
-
	- {cpp:enum}`B_USER_SETTINGS_DIRECTORY`
	- The user's settings directory.
-
	- {cpp:enum}`B_USER_DESKBAR_DIRECTORY`
	- The user's Deskbar directory.
:::

These constants are used when calling the
{cpp:func}`~find::directory` function to
determine the pathname of a particular directory of interest.

{cpp:enum}`B_DESKTOP_DIRECTORY` and {cpp:enum}`B_TRASH_DIRECTORY` are per-volume directories; if
you don't specify the volume you wish to locate these directories on,
{cpp:func}`~find::directory`
will assume you mean the boot disk.

{cpp:enum}`B_APPS_DIRECTORY` and {cpp:enum}`B_PREFERENCES_DIRECTORY` are global directories, and
always refer to the standard apps and preferences directories.

The {cpp:enum}`B_BEOS_*` constants refer to BeOS-owned directories, the {cpp:enum}`B_COMMON_*`
constants refer to directories that are common to all users of the
system, and the {cpp:enum}`B_USER_*` constants refer to the current user's
directories (currently these are all in a subtree rooted at
/boot/home,
but when multiuser support is implemented in a future version of BeOS,
these won't necessarily all be the same anymore).

In general, global application and system settings should be kept in
{cpp:enum}`B_COMMON_*`; while settings that each user should be able to configure
individually should be kept in {cpp:enum}`B_USER_*`.

By using these constants properly, your code will be compatible with
future generations of the BeOS.

::::
