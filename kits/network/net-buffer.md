# BNetBuffer
## Constructor and Destructor
::::{abi-group}

:::{cpp:function} BNetBuffer::BNetBuffer(size_t size = 0)
:::
:::{cpp:function} BNetBuffer::BNetBuffer(const BNetBuffer& from)
:::
:::{cpp:function} BNetBuffer::BNetBuffer(BMessage* archive)
:::
Creates a {hclass}`BNetBuffer`. The first form creates a new buffer capable of
holding up to {hparam}`size` bytes of data. In this case, the buffer begins life
empty.
The second form creates a new buffer which is an exact duplicate of the
{hclass}`BNetBuffer` specified by the {hparam}`from` argument, including any data that might
already be in the buffer. The third form reconstructs an archived
{hclass}`BNetBuffer`.
::::

::::{abi-group}

:::{cpp:function} virtual BNetBuffer::~BNetBuffer()
:::
A typical destructor.
::::

## Member Functions
::::{abi-group}

:::{cpp:function} status_t BNetBuffer::AppendInt8(int8 value)
:::
:::{cpp:function} status_t BNetBuffer::AppendUint8(uint8 value)
:::
:::{cpp:function} status_t BNetBuffer::AppendInt16(int16 value)
:::
:::{cpp:function} status_t BNetBuffer::AppendUint16(uint16 value)
:::
:::{cpp:function} status_t BNetBuffer::AppendInt32(int32 value)
:::
:::{cpp:function} status_t BNetBuffer::AppendUint32(uint32 value)
:::
:::{cpp:function} status_t BNetBuffer::AppendInt64(int64 value)
:::
:::{cpp:function} status_t BNetBuffer::Appenduint64(uint64 value)
:::
:::{cpp:function} status_t BNetBuffer::AppendFloat(float value)
:::
:::{cpp:function} status_t BNetBuffer::AppendDouble(double value)
:::
:::{cpp:function} status_t BNetBuffer::AppendString(const char* string)
:::
:::{cpp:function} status_t BNetBuffer::AppendData(const void* data, size_t size)
:::
:::{cpp:function} status_t BNetBuffer::AppendMessage(BMessage& message)
:::
Appends the specified data type to the end of the buffer. Integer values
are automatically converted to network byte ordering (but floats and
doubles are not, nor are values inside structures added using
{hmethod}`AppendData()`).
Strings are appended as null-terminated strings.
{hmethod}`AppendData()` copies
{hparam}`size` bytes from the buffer pointed at by
{hparam}`data`.
:::{list-table}
---
header-rows: 1
---
-
	- Return Code
	- Description
-
	- {cpp:enum}`B_OK`
	- The data was appended without error.
-
	- {cpp:enum}`B_ERROR`
	- The data couldn't be appended.
:::
::::

::::{abi-group}

:::{cpp:function} unsigned char* BNetBuffer::Data() const
:::
:::{cpp:function} size_t BNetBuffer::Size() const
:::
:::{cpp:function} size_t BNetBuffer::BytesRemaining() const
:::
{hmethod}`Data()` returns a pointer to the
{hclass}`BNetBuffer`'s internal data buffer.
{hmethod}`Size()` returns the number of
bytes currently in the buffer.
{hmethod}`BytesRemaining()` returns the
number of unused bytes in the buffer.
::::

::::{abi-group}

:::{cpp:function} status_t BNetBuffer::RemoveInt8(int8& value)
:::
:::{cpp:function} status_t BNetBuffer::RemoveUint8(uint8& value)
:::
:::{cpp:function} status_t BNetBuffer::RemoveInt16(int16& value)
:::
:::{cpp:function} status_t BNetBuffer::RemoveUint16(uint16& value)
:::
:::{cpp:function} status_t BNetBuffer::RemoveInt32(int32& value)
:::
:::{cpp:function} status_t BNetBuffer::RemoveUint32(uint32& value)
:::
:::{cpp:function} status_t BNetBuffer::RemoveInt64(int64& value)
:::
:::{cpp:function} status_t BNetBuffer::Removeuint64(uint64& value)
:::
:::{cpp:function} status_t BNetBuffer::RemoveFloat(float& value)
:::
:::{cpp:function} status_t BNetBuffer::RemoveDouble(double& value)
:::
:::{cpp:function} status_t BNetBuffer::RemoveString(const char* string, size_t size)
:::
:::{cpp:function} status_t BNetBuffer::RemoveData(const void* data, size_t size)
:::
:::{cpp:function} status_t BNetBuffer::RemoveMessage(BMessage& message)
:::
Removes the specified data type from the buffer. Integer values are
automatically converted from network byte ordering (but floats and
doubles are not, nor are values inside structures removed using
{hmethod}`RemoveData()`).
Strings are removed as null-terminated strings, up
to {hparam}`size` bytes. Be sure
the string buffer is at least {hparam}`size` bytes long.
{hmethod}`RemoveData()` removes
{hparam}`size` bytes and copies them into the buffer
pointed at by {hparam}`data`. Be sure the
{hparam}`data` buffer is at least
{hparam}`size` bytes long.
These functions start at the beginning of the buffer. After each item is
removed, the next {hmethod}`Remove…()` call will start at the next byte in the
buffer.
:::{list-table}
---
header-rows: 1
---
-
	- Return Code
	- Description
-
	- {cpp:enum}`B_OK`
	- The data was removed without error.
-
	- {cpp:enum}`B_ERROR`
	- The data couldn't be removed.
:::
::::

## Operators
::::{abi-group}

:::{cpp:function} BNetBuffer& operator =(const BNetBuffer& from)
:::
Copies the {hclass}`BNetBuffer` specified by
{hparam}`from` into the left-side object, thereby
duplicating that object. If {hparam}`from` is connected,
the left-side object will duplicate and open the same connection. Even the
data in the buffer is copied, if there is any.
::::
