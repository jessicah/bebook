# The area_malloc Module

Declared in: drivers/area_malloc.h

The area_malloc module provides a means for your driver to allocate memory
in areas instead of on the heap. It provides {ref}`malloc()`,
{ref}`calloc()`, {ref}`realloc()`, and {ref}`free()` functions that work
just like their POSIX counterparts, except they require a pool argument as
their first input.

:::{admonition} Warning
:class: warning
These functions aren't safe to call from interrupt handlers; they may
block on semaphores.
:::

The area_malloc functions are thread-safe in relation to one another, but
not in relation to {cpp:func}`delete_pool() <delete::pool>`. Be sure you
don't call {cpp:func}`delete_pool() <delete::pool>` on the pool you're
using until you know none of the other functions might be called.
{cpp:func}`create_pool() <create::pool>` and {cpp:func}`delete_pool()
<delete::pool>` are safe in relation to each other.

When the last user of the module puts it away, any remaining pools are
automatically deleted.

## Module Functions

::::{abi-group}
:::{cpp:function} const void* create_pool(uint32 addressSpec, size_t size, uint32 lockSpec, uint32 protection)
:::

:::{cpp:function} status_t delete_pool(const void* poolID)
:::

create_pool() creates a new pool of memory from which to allocate. The
parameters are the same as those used by {cpp:func}`create_area()
<create::area>`, so you have complete control over the area's
characteristics (except for its name). Returns an opaque pool idenfityer,
or {cpp:expr}`NULL` if the creation failed. The ability to share resources
allocated from the pool is determined by the permissions and protections
used to create the area.

delete_pool() deletes the pool specified by the opaque {hparam}`poolID`
given. Any pointers returned by the other functions in the module are
immediately invalid. Returns {cpp:enumerator}`B_OK` if the pool was
deleted, otherwise {cpp:enumerator}`B_ERROR`.
::::

::::{abi-group}
:::{cpp:function} void* malloc(const void* poolID, size_t size)
:::

:::{cpp:function} void* calloc(const void* poolID, size_t numMembers, size_t size)
:::

:::{cpp:function} void* realloc(const void* poolID, void* ptr, size_t size)
:::

malloc() allocates a block of {hparam}`size` bytes and returns a pointer
to it.

calloc() allocates a block that can contain {hparam}`numMembers` items of
the specified {hparam}`size` and returns a poiner to it.

realloc() resizes the memory block pointed to by {hparam}`ptr` to the
indicated {hparam}`size`. Resizing a block can require that the memory be
relocated, so this function returns the new pointer.

Each of these operations functions in the pool specified by
{hparam}`poolID`.

If there's not enough memory to allocate the requested block, these
functions return {cpp:expr}`NULL`.
::::

::::{abi-group}
:::{cpp:function} void* free(const void* poolID, void* ptr)
:::

Releases the memory block pointed to by {hparam}`ptr` from the pool
specified by {hparam}`poolID`.
::::

## Constants

::::{abi-group}
:::{cpp:enumerator} B_AREA_MALLOC_MODULE_NAME
:::

:::{code} cpp
#define B_AREA_MALLOC_MODULE_NAME "generic/area_malloc/v1"
:::

The {cpp:enumerator}`B_AREA_MALLOC_MODULE_NAME` constant identifies the
area_malloc module; use this constant to open the module.
::::
