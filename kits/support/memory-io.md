# BMemoryIO

## Constructor and Destructor

::::{abi-group} BMemory()

:::{cpp:function} BMemoryIO::BMemoryIO(void* buffer, size_t numBytes)
:::
:::{cpp:function} BMemoryIO::BMemoryIO(const void* buffer, size_t numBytes)
:::

The {hclass}`BMemoryIO` constructor assigns the object a buffer with at least {hparam}`numBytes` of
available memory. If the buffer is declared {cpp:expr}`const`, the object is read-only; calls to
{cpp:func}`~BMemoryIO::Write()` (inherited from {cpp:class}`BPositionIO`) and
{cpp:func}`~BMemoryIO::WriteAt()` will fail. Otherwise, the buffer can be both read and written. In
either case, the caller retains responsibility for the buffer; the {hclass}`BMemoryIO` object won't
free it.
::::

::::{abi-group} ~BMemoryIO()

:::{cpp:function} virtual BMemoryIO::~BMemoryIO()
:::

The {hclass}`BMemoryIO` destructor does nothing.
::::

## Member Functions

::::{abi-group} ReadAt()

:::{cpp:function} virtual ssize_t BMemoryIO::ReadAt(off_t position, void* buffer, size_t numBytes)
:::

Copies up to {hparam}`numBytes` of data from the object into the {hparam}`buffer` and returns the
actual number of bytes placed in the buffer. The data is read beginning at the {hparam}`position`
offset.

This function doesn't read beyond the end of the data. If there are fewer than {hparam}`numBytes` of
data available at the {hparam}`position` offset, it reads only through the last data byte and
returns a smaller number than {hparam}`numBytes`. If {hparam}`position` is out of range, it returns
0.
::::

::::{abi-group} "Seek(), Position()"

:::{cpp:function} virtual off_t BMemoryIO::Seek(off_t position, int32 mode)
:::
:::{cpp:function} virtual off_t BMemoryIO::Position() const
:::

{hmethod}`Seek()` sets the position in the data buffer where the {cpp:func}`~BMemoryIO::Read()` and
{cpp:func}`~BMemoryIO::Write()` functions (inherited from {cpp:class}`BPositionIO()`) begin reading
and writing. How the {hparam}`position` argument is understood depends on the {hparam}`mode` flag.
There are three possible modes:

:::{list-table}
---
header-rows: 1
---

-
	- Constant
	- Description
-
	- {cpp:enum}`SEEK_SET`
	- The {hparam}`position` passed is an offset from the beginning of allocated memory; in other
	words, the current position is set to {hparam}`position`. For this mode, {hparam}`position`
	shoould be a positive value.
-
	- {cpp:enum}`SEEK_CUR`
	- The {hparam}`position` argument is an offset from the current position; the value of the
	argument is added to the current position.
-
	- {cpp:enum}`SEEK_END`
	- The {hparam}`position` argument is an offset from the end of the object's data buffer. In this
	mode the {hparam}`position` argument must be negative.
:::

{cpp:func}`~BMemoryIO::Write()` fails if the current position is beyond the end of assigned memory.

Both {hmethod}`Seek()` and {hmethod}`Position()` return the current position as an offset in bytes
from the beginning of allocated memory.
::::

::::{abi-group} WriteAt()

:::{cpp:function} virtual ssize_t BMemoryIO::WriteAt(off_t position, const void* buffer, size_t numBytes)
:::

Copies {hparam}`numBytes` of data from {hparam}`buffer` into allocated memory beginning at
{hparam}`position`, and returns the number of bytes written.

{hmethod}`WriteAt()` won't write outside the memory buffer. If {hparam}`position` is beyond the end
of the buffer, it returns 0. If the object is read-only, it returns {cpp:enum}`B_NOT_ALLOWED`.
::::
