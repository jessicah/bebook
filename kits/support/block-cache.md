# BBlockCache

## Constructor and Destructor

::::{abi-group}
:::{cpp:function} BBlockCache::BBlockCache(size_t count, size_t size, uint32 type)
:::

Creates a new memory block pool, allocating memory for {hparameter}`count` blocks, each controlling {hparam}`size` bytes of memory. {hparam}`type` is either:
:::{list-table}
-
    - Constant
    - Description
-
    - {cpp:enum}`B_OBJECT_CACHE`
    - Memory is managed through {cpp:expr}`new` and {cpp:expr}`delete.
-
    - {cpp:enum}`B_MALLOC_CACHE`
    - Memory is managed through {cpp:expr}`malloc()` and {cpp:expr}`free()`.
:::
::::

::::{abi-group}
:::{cpp:function} BBlockCache::~BBlockCache()
:::

Frees any unused memory in the object's block pool. Memory that was retrieved through {hmethod}`Get()` (and that hasn't been returned through {hmethod}`Save()`) is not deallocated.
::::

## Member Functions

::::{abi-group}
:::{cpp:function} void* BBlockCache::Get(size_t size)
:::

Retrieves a block of memory of the given {hparam}`size` and returns it directly. If {hparam}`size` is the same as the {hparam}`size` argument you passed to the constructor, the memory returned will be taken from the object's cache. Otherwise, it's allocated using either {cpp:expr}`new` or {cpp:expr}`malloc()` as requested in the constructor. When you're don{e with the memory, you can either deallocate it yourself, or return it to the {hclass}`BBlockCache` object by calling {hmethod}`Save()`.
::::

::::{abi-group}
:::{cpp:function} void BBlockCache::Save(void* pointer, size_t size);
:::

Returns, to the {hclass}`BBlockCache` object, {hparam}`size` bytes of memory pointed to by {hparam}`pointer`. If the memory was taken from the object's pool, the memory is returned to the pool. Otherwise, it's deallocated. In either case, the caller is freed of responsibility for deallocating the memory.
::::
