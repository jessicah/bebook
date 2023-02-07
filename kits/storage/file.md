# BFile
## Constructor and Destructor
::::{abi-group}

:::{cpp:function} BFile::BFile()
:::
:::{cpp:function} BFile::BFile(const entry_ref* ref, uint32 openMode)
:::
:::{cpp:function} BFile::BFile(const BEntry* entry, uint32 openMode)
:::
:::{cpp:function} BFile::BFile(const char* path, uint32 openMode)
:::
:::{cpp:function} BFile::BFile(BDirectory* dir, const char* path, uint32 openMode)
:::
Creates a new {hclass}`BFile` object, initializes it according to the arguments,
and sets {cpp:func}`~BFile::InitCheck`
to return the status of the initialization.
The default constructor does nothing and sets
and sets {cpp:func}`~BFile::InitCheck`
to {cpp:enum}`B_NO_INIT`.
To initialize the object, call
{cpp:func}`~BFile::SetTo`.
The copy constructor creates a new {hclass}`BFile` that's open on the same file as
that of the argument. Note that the two objects maintain separate data
pointers into the same file:
- Separate pointers: Reading and writing through one object does not affect the position of the data pointer in the other object.
- Same file: If one object writes to the file, the other object will see the written data.

For information on the other constructors, see the analogous
{cpp:func}`~BFile::SetTo`
functions.
::::

::::{abi-group}

:::{cpp:function} virtual BFile::~BFile()
:::
Closes the object's file, frees its file descriptor, and destroys the
object.
::::

## Member Functions
::::{abi-group}

:::{cpp:function} virtual status_t BFile::GetSize(off_t* size) const
:::
:::{cpp:function} virtual status_t BFile::SetSize(off_t size)
:::
These functions get and set the size, in bytes, of the object's file.
{hmethod}`GetSize()` returns the size of the file's data
portion in the {hparam}`size`
argument; the measurement doesn't include attributes.
{hmethod}`SetSize()` sets the size of the data portion to the size given by the
argument:
- Enlarging a file adds (uninitialized) bytes to its end.
- Shrinking a file removes bytes from the end.

:::{list-table}
---
header-rows: 1
---
-
	- Return Code
	- Description
-
	- {cpp:enum}`B_OK`.
	- The file's size was successfully gotten or set.
-
	- {cpp:enum}`B_NOT_ALLOWED`.
	- ({hmethod}`SetSize()`) The file lives on a read-only volume.
-
	- {cpp:enum}`B_DEVICE_FULL`.
	- ({hmethod}`SetSize()`) No more room on the file's device.
:::
::::

::::{abi-group}

:::{cpp:function} status_t BFile::InitCheck() const
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
	- The object is initialized.
-
	- {cpp:enum}`B_NO_INIT`.
	- The object is uninitialized.
-
	- For other errors.
	- See {cpp:func}`~BFile::SetTo`
:::
::::

::::{abi-group}

:::{cpp:function} bool BFile::IsReadable() const
:::
:::{cpp:function} bool BFile::IsWritable() const
:::
These functions tell you whether the {hclass}`BFile` was initialized to read or
write its file. If the object isn't (properly) initialized, they both
return {cpp:enum}`false`.
Note that these functions don't query the actual file to check
permissions, they only tell you what the access request was when the
{hclass}`BFile` object was initialized.
::::

::::{abi-group}

:::{cpp:function} virtual ssize_t BFile::Read(void* buffer, size_t size)
:::
:::{cpp:function} virtual ssize_t BFile::ReadAt(off_t location, void* buffer, size_t size)
:::
:::{cpp:function} virtual ssize_t BFile::Write(const void* buffer, size_t size)
:::
:::{cpp:function} virtual ssize_t BFile::WriteAt(off_t location, const void* buffer, size_t size)
:::
These functions, which are inherited from
{cpp:class}`BPositionIO`, read and write the
file's data; note that they don't touch the file's attributes.
The {hmethod}`Read()` and {hmethod}`ReadAt()`
functions read {hparam}`size` bytes of data from the file
and place this data in {hparam}`buffer`. The buffer that {hparam}`buffer` points to must
already be allocated, and must be large enough to accommodate the read
data. Note that the read-into buffer is not null-terminated by the
reading functions.
The two functions differ in that…
- {hmethod}`Read()` reads the data starting at the current location of the file's data pointer, and increments the file pointer as it reads.
- {hmethod}`ReadAt()` reads the data from the location specified by the {hparam}`location` argument, which is taken as a measure in bytes from the beginning of the file. {hmethod}`ReadAt()` does not bump the file's data pointer.

{hmethod}`Write()` and {hmethod}`WriteAt()` write
{hparam}`size` bytes of data into the file; the data is
taken from the {hparam}`buffer` argument. The two functions differ in their use (or
non-use) of the file's data pointer in the same manner as {hmethod}`Read()` and
{hmethod}`ReadAt()`.
All four functions return the number of bytes that were actually read or
written; negative return values indicate an error.
Reading fewer-than-{hparam}`size` bytes isn't uncommon—consider the case
where the file is smaller than the size of your buffer. If you want your
buffer to be {cpp:enum}`NULL`-terminated, you can use the return value to set the
{cpp:enum}`NULL`:
:::{code}
char buf[1024];
ssize_t amt_read;
if ((amt_read = file.Read((void *)buf, 1024)) < 0)
   /* handle errors first */
else
   /* otherwise set null */
   buf[amt_read] = '0';
:::
A successful {hmethod}`Write()` or {hmethod}`WriteAt()`,
on the other hand, will always write
exactly the number of bytes you requested. In other words, {hmethod}`Write()`
returns either the {hparam}`size` value that you passed to it, or else it returns a
negative (error) value.
:::{admonition} Note
:class: note
Error codes returned by these functions can vary depending on the file
system handling the operation. For this reason, specific error codes
aren't listed here.
:::
::::

::::{abi-group}

:::{cpp:function} virtual off_t BFile::Seek(off_t offset, int32 seekMode)
:::
:::{cpp:function} virtual off_t BFile::Position() const
:::
{hmethod}`Seek()` sets the location of the file's data pointer. The new location is
reckoned as {hparam}`offset` bytes from the position given by the
{hparam}`seekMode` constant:
:::{list-table}
---
header-rows: 1
---
-
	- Constant
	- Description
-
	- {cpp:enum}`SEEK_SET`
	- Seek from the beginning of the file.
-
	- {cpp:enum}`SEEK_CUR`
	- Seek from the pointer's current position.
-
	- {cpp:enum}`SEEK_END`
	- Seek from the end of the file.
:::
If you {hmethod}`Seek()` to a position that's past the end of the file and then do a
{cpp:func}`~BFile::Write`, the file
will be extended (padded with garbage) from the old end
of file to the {hmethod}`Seek()`'d position. If you don't
follow the {hmethod}`Seek()` with a
{hmethod}`Write()`, the file isn't extended.
{hmethod}`Seek()` returns the new position as measured (in bytes) from the beginning
of the file.
{hmethod}`Position()` returns the current position as measured (in bytes) from the
beginning of the file. It doesn't move the pointer.
:::{list-table}
---
header-rows: 1
---
-
	- Return Code
	- Description
-
	- {cpp:enum}`B_ERROR`.
	- Attempted to {hmethod}`Seek()` "before" the beginning of the file, or you called {hmethod}`Position()` after such a {hmethod}`Seek()`. You also get {cpp:enum}`B_ERROR` if you call {hmethod}`Seek()` on an uninitialized file.
-
	- {cpp:enum}`B_BAD_FILE`.
	- {hmethod}`Position()` called on an uninitialized file.
:::
:::{admonition} Warning
:class: warning
If you do a "before the beginning" seek, subsequent
{cpp:func}`~BFile::Read` and
{cpp:func}`~BFile::Write`
calls do not fail. But they almost certainly aren't doing what you want
(you shouldn't be "before the file," anyway). The moral: Always check
your {hmethod}`Seek()` return.
:::
::::

::::{abi-group}

:::{cpp:function} status_t BFile::SetTo(const entry_ref* ref, uint32 openMode)
:::
:::{cpp:function} status_t BFile::SetTo(const BEntry* entry, uint32 openMode)
:::
:::{cpp:function} status_t BFile::SetTo(const char* path, uint32 openMode)
:::
:::{cpp:function} status_t BFile::SetTo(const BDirectory* dir, const char* path, uint32 openMode)
:::
:::{cpp:function} void BFile::Unset()
:::
Closes the {hclass}`BFile`'s current file (if any), and opens the file specified by
the arguments. If the specified file is a symbolic link, the link is
automatically traversed (recursively, if necessary). Note that you're not
prevented from opening a directory as a {hclass}`BFile`, but you are prevented from
writing to it.
- In the {hparam}`path` function, {hparam}`path` can be absolute or relative, and can contain "." and ".." elements. If {hparam}`path` is relative, it's reckoned off of the current working directory.
- In the {hparam}`dir`/{hparam}`path` function, {hparam}`path` must be relative and is reckoned off of {hparam}`dir`.

{hparam}`openMode` is a combination of flags that determines how the file is opened
and what this object can do with it once it is open. There are two sets
of flags; you must pass one (and only one) of the following "read/write"
constants:
:::{list-table}
---
header-rows: 1
---
-
	- Constant
	- Description
-
	- {cpp:enum}`B_READ_ONLY`
	- This object can read, but not write, the file.
-
	- {cpp:enum}`B_WRITE_ONLY`
	- This object can write, but not read, the file.
-
	- {cpp:enum}`B_READ_WRITE`
	- This object can read and write the file.
:::
You can also pass any number of the following (these are optional):
:::{list-table}
---
header-rows: 1
---
-
	- Constant
	- Description
-
	- {cpp:enum}`B_CREATE_FILE`
	- Create the file if it doesn't already exist.
-
	- {cpp:enum}`B_FAIL_IF_EXISTS`
	- If the file already exists, the initialization (of the {hclass}`BFile` object) fails.
-
	- {cpp:enum}`B_ERASE_FILE`
	- If the file already exists, erase all its data and attributes.
-
	- {cpp:enum}`B_OPEN_AT_END`
	- Sets the data pointer to point to the end of the file.
:::
To open a file for reading and writing, for example, you simply pass:
:::{code}
file.SetTo(entry, B_READ_WRITE);
:::
Here we create a new file or erase its data if it already exists:
:::{code}
file.SetTo(entry, B_READ_WRITE | B_CREATE_FILE | B_ERASE_FILE);
:::
And here we create a new file, but only if it doesn't already exist:
:::{code}
file.SetTo(entry, B_READ_WRITE | B_CREATE_FILE | B_FAIL_IF_EXISTS);
:::
{hmethod}`Unset()` closes the object's file and sets its
{cpp:func}`~BFile::InitCheck` value to
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
	- The file was successfully opened.
-
	- {cpp:enum}`B_BAD_VALUE`.
	- {cpp:enum}`NULL` {hparam}`path` in {hparam}`dir`/{hparam}`path`, or some other argument is uninitialized.
-
	- {cpp:enum}`B_ENTRY_NOT_FOUND`.
	- File not found, or couldn't create the file.
-
	- {cpp:enum}`B_FILE_EXISTS`.
	- File exists (and you set {cpp:enum}`B_FAIL_IF_EXISTS`).
-
	- {cpp:enum}`B_PERMISSION_DENIED`.
	- Read or write permission request denied.
-
	- {cpp:enum}`B_NO_MEMORY`.
	- Couldn't allocate necessary memory to complete the operation.
:::
::::

## Operators
::::{abi-group}

:::{cpp:function} BFile& BFile::operator=(const BFile& file)
:::
In the expression
:::{code}
BFile a = b;
:::
{hclass}`BFile` a is initialized to refer
to the same file as b. To gauge the
success of the assignment, you should call
{cpp:func}`~BFile::InitCheck` immediately
afterwards. You can't assign a {hclass}`BFile` to itself
({cpp:enum}`B_BAD_VALUE`).
Assigning to an uninitialized {hclass}`BFile` is "successful": The assigned-to
{hclass}`BFile` will also be uninitialized ({cpp:enum}`B_NO_INIT`).
::::
