:::{cpp:class} BResources
:::

# BResources

## Constructor and Destructor

::::{abi-group}
:::{cpp:function} BResources::BResources()
:::

:::{cpp:function} BResources::BResources(BFile* file, bool clobber = false)
:::

Creates a new {hclass}`BResources` object. You can initialize the object
by passing a pointer to a valid {cpp:class}`BFile`; without the argument,
the object won't refer to a file until {cpp:func}`SetTo()
<BResources::SetTo>` is called.

If {hparam}`clobber` is {cpp:expr}`true`, the file that's referred to by
{cpp:class}`BFile` is truncated (it's data is erased), and a new resource
file header is written to the file. If {hparam}`clobber` is
{cpp:expr}`false` and the file doesn't otherwise doesn't have a resource
header, the initialization fails.

{hclass}`BResources` copies the {cpp:class}`BFile` argument; after the
constructor returns, you can, for example, delete the {cpp:class}`BFile`
that you passed in.
::::

::::{abi-group}
:::{cpp:function} virtual BResources::~BResources()
:::

Destroys the BResources object.
::::

## Member Functions

::::{abi-group}
:::{cpp:function} status_t BResources::AddResource(type_code type, int32 id, const void* data, size_t length, const char* name = NULL)
:::

Adds a new resource to the file. For this function to have an effect, the
file must be open for writing. The arguments are:

-   {hparam}`type` is one of the {htype}`type_code` constants defined in
support/TypeConstants.h.

-   {hparam}`id` is the ID number that you want to assign to the resource. The
value of the ID has no meaning other than that which your application gives
it; the only restriction on the ID is that the combination of it and the
data type constant must be unique across all resources in this resource
file.

-   {hparam}`data` is a pointer to the data that you want the resource to
hold.

-   {hparam}`length` is the length of the data buffer, in bytes.

-   {hparam}`name` is optional, and needn't be unique. Or even interesting.

Ownership of the data pointer isn't assigned to the {hclass}`BResources`
object by this function; after {hmethod}`AddResource()` returns, your
application can free or otherwise manipulate the buffer that data points to
without affecting the data that was written to the file.

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
	- The resource was successfully added.
-
	- {cpp:enumerator}`B_NOT_ALLOWED`.
	- The is open read-only.
-
	- {cpp:enumerator}`B_FILE_ERROR`.
	- The file's resource map doesn't exist or is invalid.
-
	- {cpp:enumerator}`B_BAD_VALUE`.
	- The {hparam}`data` pointer is {cpp:expr}`NULL`.
-
	- {cpp:enumerator}`B_NO_MEMORY`.
	- Not enough memory to add the resource to the file.

:::
::::

::::{abi-group}
:::{cpp:function} const BFile& BResources::File() const
:::

Returns the {cpp:class}`BFile` the {hclass}`BResource` object references.
::::

::::{abi-group}
:::{cpp:function} bool BResources::GetResourceInfo(int32 byIndex, type_code* typeFound, int32* idFound, const char** nameFound, size_t* lengthFound)
:::

:::{cpp:function} bool BResources::GetResourceInfo(type_code byType, int32 andIndex, int32* idFound, const char** nameFound, size_t* lengthFound)
:::

:::{cpp:function} bool BResources::GetResourceInfo(type_code byType, int32 andId, const char** nameFound, size_t* lengthFound)
:::

:::{cpp:function} bool BResources::GetResourceInfo(type_code byType, const char* andName, int32* idFound, size_t* lengthFound)
:::

:::{cpp:function} bool BResources::GetResourceInfo(const void* byPointer, type_code* typeFound, int32* idFound, size_t* lengthFound, const char** nameFound)
:::

These functions return information about a specific resource, as
identified by the first one or two arguments:

-   The first version ({hparam}`byIndex`) searches for the
{hparam}`byIndex`'th resource in the file.

-   The second ({hparam}`byType`/{hparam}`andIndex`) searches for the
{hparam}`byIndex`'th resource that has the given type.

-   The third ({hparam}`byType`/{hparam}`andId`) looks for the resource with
the unique combination of type and ID.

-   The fourth ({hparam}`byType`/{hparam}`andName`) looks for the first
resource that has the given type and name.

-   The last ({hparam}`byPointer`) returns information about the resource
whose data is pointed to by {hparam}`byPointer`. This can be used to trace
a resource that's already been loaded with {cpp:func}`LoadResource()
<BResources::LoadResource>` back to its information.

The other arguments return the other statistics about the resource (if
found).

The pointer that's returned in {hparam}`*foundName` belongs to the
{hclass}`BResources`. Don't free it.

The functions return {cpp:expr}`true` if a resource was found and
{cpp:expr}`false` otherwise.
::::

::::{abi-group}
:::{cpp:function} bool BResources::HasResource(type_code type, int32 id)
:::

:::{cpp:function} bool BResources::HasResource(type_code type, const char* name)
:::

Returns {cpp:expr}`true` if the resource file contains a resource as
identified by the arguments, otherwise it returns {cpp:expr}`false`.

Keep in mind that there may be more than one resource in the file with the
same name and type combination. The type and id combo, on the other hand,
is unique. See "{ref}`Identifying a Resource within a Resource File`."
::::

::::{abi-group}
:::{cpp:function} const void* BResources::LoadResource(type_code type, int32 id, size_t* outSize)
:::

:::{cpp:function} const void* BResources::LoadResource(type_code type, const char* name, size_t* outSize)
:::

Loads the specified resource into memory. The resource can be identified
by either type code and ID or by type code and name. See "{ref}`Identifying
a Resource within a Resource File`."

The returned pointer belongs to the resource file; it's valid until the
resource gets changed. If an error occurs while trying to load the
resource, {cpp:expr}`NULL` is returned.
::::

::::{abi-group}
:::{cpp:function} status_t BResources::MergeFrom(BFile* fromFile)
:::

Copies all the resource from the file specified by {hparam}`fromFile` into
the file targeted by the {hclass}`BResources` object. The original file
isn't changed. You can do this to a file that's opened read-only, but the
changes won't have any effect.

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
	- The resources were copied without error.
-
	- {cpp:enumerator}`B_BAD_FILE`.
	- The resource map is empty.
-
	- {cpp:enumerator}`B_FILE_ERROR`.
	- A file error occurred, or the resource map is nonexistent.
-
	- {cpp:enumerator}`B_IO_ERROR`.
	- An error occurred while writing the data.
-
	- {cpp:enumerator}`B_ERROR`.
	- Something else went wrong.

:::
::::

::::{abi-group}
:::{cpp:function} status_t BResources::PreloadResourceType(type_code type = 0)
:::

If you know you're going to need to access all resources of a particular
type, you can preload them all into memory in one shot using this function.
If you specify a type of 0, all resources of all types are preloaded.

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
	- The resources were preloaded without error.
-
	- {cpp:enumerator}`B_BAD_FILE`.
	- The resource map is empty.
-
	- Other values.
	- The returned value is the negative of the number of errors that occurred
		while preloading resources; for example, if five errors occurred, the
		result is -5.

:::
::::

::::{abi-group}
:::{cpp:function} status_t BResources::RemoveResource(type_code type, int32 id)
:::

:::{cpp:function} status_t BResources::RemoveResource(const void* resource)
:::

Removes the resource identified by the arguments. See "{ref}`Identifying a
Resource within a Resource File`."

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
	- The resource was removed.
-
	- {cpp:enumerator}`B_FILE_ERROR`.
	- The file's resource map doesn't exist.
-
	- {cpp:enumerator}`B_NOT_ALLOWED`.
	- The file is opened read-only.
-
	- {cpp:enumerator}`B_NOT_ALLOWED`.
	- Couldn't find the specified resource, or an error occurred trying to
		remove it (first form of {cpp:func}`RemoveResource()
		<BResources::RemoveResource>`).
-
	- {cpp:enumerator}`B_ERROR`.
	- Couldn't find the specified resource, the pointer doesn't indicate a valid
		resource, or an error occurred while removing the resource (second form).

:::
::::

::::{abi-group}
:::{cpp:function} status_t BResources::SetTo(BFile* file, bool clobber = false)
:::

Unlocks and closes the object's previous {cpp:class}`BFile`, and
re-initializes it to refer to a copy of the argument. If the new BFile is
open for writing, the {hclass}`BResources`' copy of the {cpp:class}`BFile`
is locked.

If {hparam}`clobber` is {cpp:expr}`true`, the file that's referred to by
{cpp:class}`BFile` is truncated (it's data is erased), and a new resource
file header is written to the file. If {hparam}`clobber` is
{cpp:expr}`false` and the file doesn't otherwise doesn't have a resource
header, the initialization fails.

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
	- The resource was removed.
-
	- {cpp:enumerator}`B_BAD_VALUE`.
	- The argument {cpp:class}`BFile` is invalid (uninitialized).
-
	- {cpp:enumerator}`B_ERROR`.
	- The {hclass}`BResources` couldn't be initialized (for whatever reason).

:::
::::

::::{abi-group}
:::{cpp:function} status_t BResources::Sync()
:::

Updates all changed resources on disk. This actually rewrites the entire
resource file, so be aware of this when designing your code. This is a very
good reason not to use {hclass}`BResources` for anything other than
permanent, nonchanging application data, and only developer tools should
write to resource files.

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
	- The resources were updated without error.
-
	- {cpp:enumerator}`B_BAD_FILE`.
	- The resource map is empty.
-
	- {cpp:enumerator}`B_NOT_ALLOWED`.
	- The file is opened read-only.
-
	- {cpp:enumerator}`B_FILE_ERROR`.
	- A file error occurred.
-
	- {cpp:enumerator}`B_IO_ERROR`.
	- An error occurred while writing the data.

:::
::::

::::{abi-group}
:::{cpp:function} status_t BResources::WriteTo(BFile* newFile)
:::

Writes all the file's resources into a new file. After this function
returns, the {hclass}`BResources` object is targeted on the new
{cpp:class}`BFile`; all future operations will be done in the new file.

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
	- The resources were written without error.
-
	- Other errors.
	- File errors indicating problems copying the data.

:::
::::
