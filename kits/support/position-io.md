# BPositionIO

## Constructor and Destructor

::::{abi-group} BPositionIO()

:::{cpp:function} BPositionIO::BPositionIO()
:::

Does nothing. Constructors in derived classes should initialize the object to default values—for
example, set the current position to the beginning of the data.
::::

::::{abi-group} ~BPositionIO()

:::{cpp:funcion} virtual BPositionIO::~BPositionIO()
:::

Does nothing.
::::

## Member Functions

::::{abi-group} "Read(), ReadAt()"

:::{cpp:function} virtual ssize_t BPositionIO::Read(void* buffer, size_t numBytes)
:::
:::{cpp:function} virtual ssize_t BPositionIO::ReadAt(off_t position, void* buffer, size_t numBytes) = 0
:::

{hmethod}`Read()` copies {hparam}`numBytes` bytes of data from the object to the {hparam}`buffer`.
It returns the number of bytes actually read (which may be 0) or an error code if something goes
wrong. {hmethod}`Read()` is implemented using {cpp:func}`~BPositionIO::Seek()`, {hmethod}`ReadAt()`,
and {cpp:func}`BPositionIO::Position()`, all of which are pure virtual functions.

{hmethod}`ReadAt()` is a pure virtual that must be implemented by derived classes to read
{hparam}`numBytes` bytes of data beginning at {hparam}`position` in the data source, and to place
them in the {hparam}`buffer`. It should return the number of bytes actually read, or an error code
if something goes wrong.
::::

::::{abi-group} "Seek(), Position()"

:::{cpp:function} virtual off_t BPositionIO::Seek(off_t position, int32 mode) = 0
:::
:::{cpp:function} virtual off_t BPositionIO::Position() const = 0
:::

{hmethod}`Seek()` is implemented by derived classes to modify the current position maintained by the
object. The current position is an offset in bytes from the beginning of the object's data. How the
{hparam{`position` argument is interpreted will depend on the {hparam}`mode` flag. Three possible
modes should be supported:

:::{list-table}
---
header-rows: 1
----
-
	- Constant
	- Description
-
	- {cpp:enum}`SEEK_SET`
	
	- The {hparam}`position` passed is an offset from the beginning of allocated memory; in other
	words, the current position should be set to {hparam}`position`.
-
	- {cpp:enum}`SEEK_CUR`

	- The {hparam}`position` argument is an offset from the current position; the current position
should be incremented by {hparam}`position`.

-
	- {cpp:enum}`SEEK_END`

	- The {hparam}`position` argument is an offset from the end of the data; the current position should be
the sum of {hparam}`position` plus the number of bytes in the data.
:::

For the {cpp:enum}`SEEK_SET` mode, {hparam}`position` should be a positive value. The other modes permit negative offsets.

{hmethod}`Seek()` should return the new position.

{hmethod}`Position()` should return the current position.
::::

::::{abi-group} SetSize()

:::{cpp:function} virtual status_t BPositionIO::SetSize(off_t numBytes)
:::

Returns {cpp:enum}`B_ERROR` to indicate that, in general, {hclass}`BPositionIO` objects can't set
the amount of memory in the repositories they represent. However, the {cpp:class}`BMallocIO` class
in this kit and {cpp:class}`BFile` in the "Storage Kit" implement {hmethod}`SetSize()` functions
that override this default.
::::

::::{abi-group}

:::{cpp:function} virtual ssize_t BPositionIO::Write(const void* buffer, size_t numBytes)
:::
:::{cpp:function} virtual ssize_t BPositionIO::WriteAt(off_t position, const void* buffer, size_t numBytes) = 0
:::

{hmethod}`Write()` copies {hparam}`numBytes` bytes of data from the object into the
{hparam}`buffer`. It returns the number of bytes actually written (which may be 0) or an error code
if something goes wrong. {hmethod}`Write()` is implemented using {cpp:func}`~BPositionIO::Seek()`,
{cpp:func}`~BPositionIO::Position()`, and {hmethod}WriteAt()`, all of which are pure virtual
functions.

{hmethod}`WriteAt()` is a pure virtual that must be implemented by derived classes to copy
{hparam}`numBytes` bytes of data from {hparam}`buffer` and write them into the object, starting at
byte {hparam}`position` within the object. It should return the number of bytes actually read, or an
error code if something goes wrong.
::::
