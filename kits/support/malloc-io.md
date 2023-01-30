# BMallocIO

## Constructor and Destructor

::::{abi-group}

:::{cpp:function} BMallocIO::BMallocIO()
:::

The {hclass}`BMallocIO` constructor creates an empty object and sets the default block size to 256 bytes. The constructor doesn't allocate any memory; memory is allocated when you first write to the object or when you call {cpp:func}`~BMallocIO::SetSize()` to set the amount of memory.
::::

::::{abi-group}

:::{cpp:function} BMallocIO::~BMallocIO()
:::

The {hclass}`BMallocIO` destructor frees all memory that was allocated by the object.
::::

## Member Functions

::::{abi-group}

:::{cpp:function} const void* BMallocIO::Buffer() const
:::
:::{cpp:function} size_t BMallocIO::BufferLength() const
:::

{hmethod}`Buffer()` returns a pointer to the memory that the {hclass}`BMallocIO` object has allocated, or {cpp:expr}`NULL` if it hasn't yet had occasion to allocate any memory.

{hmethod}`BufferLenth()` returns the number of data bytes in the buffer (not necessarily the full number of bytes that were allocated).
::::

::::{abi-group}

:::{cpp:function} virtual ssize_t BMallocIO::ReadAt(off_t position, void* buffer, size_t numBytes)
:::

Reads up to {hparam}`numBytes` of data from the object and copies it into the {hparam}`buffer`. Returns the actual number of bytes placed in the buffer. The data is read beginning at {hparam}`position` offset.

This function doesn't read beyond the end of the data. If there are fewer than {hparam}`numBytes` of data available at the {hparam}`position` offset, it reads only through to the last data byte and returns a smaller number than {hparam}`numBytes`. If {hparam}`position` is out of range, it returns 0.
::::

::::{abi-group}

:::{cpp:function} virtual off_t BMallocIO::Seek(off_t position, int32 mode)
:::
:::{cpp:function} virtual off_t BMallocIO::Position() const
:::

{hparam}`Seek()` sets the position in the data buffer where the {cpp:func}`~BMallocIO::Read()` and {cpp:func}`~BMallocIO::Write()` functions (inherited from {cpp:class}`BPositionIO`) begin reading and writing. How the {hparam}`position` argument is understood depends on the {hparam}`mode` flag. There are three possible modes:

:::{list-table}
:header-rows: 1

-
    - Constant
    - Description
-
    - {cpp:enum}`SEEK_SET`
    - The {hparam}`position` passed is an offset from the beginning of allocated memory; in other words, the current position is set to {hparam}`position`. For this mode, {hparam}`position` should be a positive value.
-
    - {cpp:enum}`SEEK_CUR`
    - The {hparam}`position` argument is an offset from the current position; the value of the argument is added to the current position.
-
    - {cpp:enum}`SEEK_END`
    - The {hparam}`position` argument is an offset from the end of the object's data (not necessarily from the end of allocated memory). Positive values seek beyond the end of the data; negative values seek backwards into the data.
:::

Attempts to seek beyond the end of allocated memory are legal. What {cpp:func}`~BMallocIO::Write()` is subsequently called, the object updaates its conception of where the data ends to bring the current position within range. If necessary, enough memory will be allocated to accommodate any data added at the current position.

Both {hmethod}`Seek()` and {hmethod}`Position()` return the current position as an offset in bytes from the beginning of allocatedd memory.
::::

::::{abii-group}

:::{cpp:function} void BMallocIO::SetBlockSize(size_t blockSize)
:::
:::{cpp:function} virtual status_t BMallocIO::SetSize(off_t numBytes)
:::

{hmethod}`SetBlockSize()` sets the size of the memory blocks that the {hclass}`BMallocIO` object deals with. The object allocates memory in multiples of the block size. The default is 256 bytes.

{hmethod}`SetSize()` sets the size of allocated memory to {hparam}`numBytes` (modulo the block size). Shrinking the buffer should always be successful ({cpp:enum}`B_OK`); if the buffer can't be grown, {cpp:enum}`B_NO_MEMORY` is returned.
::::

::::{abi-group}

:::{cpp:function} virtual ssize_t BMallocIO::WriteAt(off_t position, const void* buffer, size_t numBytes)
:::

Copies {hparam}`numBytes` of data from {hparam}`buffer` into the object's data beginning at {hparam}`position`.

A successful {hmethod}`WriteAt()` always returns {hparam}`numBytes`. {hmethod}`WriteAt()` reallocates the buffer (in multiples of the block size) if it needs more room. If the reallocation fails, this function returns {cpp:enum}`B_NO_MEMORY`.
::::
