:::{cpp:class} BBuffer
:::

# BBuffer

## Constructor and Destructor

The {hclass}`BBuffer` constructor and destructor are private; use the
appropriate functions in the {cpp:class}`BBufferGroup` class to create and
destroy {hclass}`BBuffers`.

## Member Functions

::::{abi-group}
:::{cpp:function} media_audio_header* BBuffer::AudioHeader()
:::

Returns a pointer to an audio buffer's header; this is just an alias for:

:::{code} cpp
&BBuffer::Header()->u.raw_audio;
:::
::::

::::{abi-group}
:::{cpp:function} buffer_clone_info BBuffer::CloneInfo() const
:::

Returns a {ref}`buffer_clone_info` structure describing a buffer. This
information is primarily for debugging purposes; don't use this
{ref}`buffer_clone_info` structure to add a buffer to a buffer group,
because it'll just alias an existing buffer.
::::

::::{abi-group}
:::{cpp:function} void BBuffer::Data()
:::

The {hmethod}`Data()` function returns a pointer to the first byte of the
buffer, or {cpp:expr}`NULL` if the buffer somehow couldn't be properly
initialized (in which case the buffer can't be used).
::::

::::{abi-group}
:::{cpp:function} int32 BBuffer::Flags()
:::

Returns the buffer's flags. The flags let you specify options for the
buffer. For example, you might create a {cpp:class}`BBufferGroup` in which
some buffers are intended for odd video fields
({cpp:enumerator}`B_F1_BUFFER`), and other buffers are intended for even
video fields ({cpp:enumerator}`B_F2_BUFFER`), thereby letting you handle
interlaced video much more easily by having each buffer know where the
video should be displayed.
::::

::::{abi-group}
:::{cpp:function} media_header* BBuffer::Header()
:::

Returns a pointer to the buffer's header. This header describes the media
data contained therein. The result is only valid for a buffer received from
either {cpp:func}`BBufferGroup::RequestBuffer` or
{cpp:func}`BBufferConsumer::BufferReceived`.

If you put data into a buffer, you should call {hmethod}`Header()` to
obtain a pointer to the buffer's header, then fill out the
{cpp:func}`media_header <media::header>` structure with information
describing the buffer's contents.
::::

::::{abi-group}
:::{cpp:function} media_buffer_id BBuffer::ID()
:::

If the buffer has been successfully registered with the Media Server, and
is available for use by other clients, {hmethod}`ID()` returns a positive
buffer ID. Otherwise, a negative number is returned.
::::

::::{abi-group}
:::{cpp:function} void BBuffer::Recycle()
:::

Sends the buffer back to the BBufferGroup that owns it so the buffer can
be reused. You can only call Recycle() on a buffer that you received from
either the {cpp:func}`BBufferGroup::RequestBuffer` call or the
{cpp:func}`BBufferConsumer::BufferReceived` call.

:::{admonition} Warning
:class: warning
Don't call both BroadcastBuffer() and {hmethod}`Recycle()` on the same
buffer.
:::
::::

::::{abi-group}
:::{cpp:function} size_t BBuffer::SizeAvailable()
:::

Returns the size, in bytes, of the buffer. The actual number of bytes used
might be less than this value, and is stored in the buffer's header, which
can be obtained by calling the {cpp:func}`Header() <BBuffer::Header>`
function.
::::

::::{abi-group}
:::{cpp:function} size_t BBuffer::SizeUsed()
:::

:::{cpp:function} void BBuffer::SetSizeUsed(ssize_t sizeUsed)
:::

{hmethod}`SizeUsed()` returns the number of bytes in the buffer that are
currently in use.

{hmethod}`SetSizeUsed()` sets this value. This should be called after
writing data into the buffer in order to indicate the size of the written
data.
::::

::::{abi-group}
:::{cpp:function} media_type BBuffer::Type()
:::

Returns the media type of the data contained within the buffer, as
specified by the {cpp:class}`BBufferProducer` from which the buffer
originated. This value is only valid if you received the buffer from either
the {cpp:func}`BBufferGroup::RequestBuffer` call or the
{cpp:func}`BBufferConsumer::BufferReceived` call.
::::

::::{abi-group}
:::{cpp:function} media_video_header* BBuffer::VideoHeader()
:::

Returns a pointer to a video buffer's header; this is just an alias for:

:::{code} cpp
&BBuffer::Header()->u.raw_video;
:::
::::

## Constants

### Flags

Declared in: media/Buffer.h

:::{list-table}
---
header-rows: 1
align: left
widths: auto
---
-
	- Constant

	- Description

-
	- {cpp:enumerator}`B_F1_BUFFER`.
	- Buffer is for odd fields.
-
	- {cpp:enumerator}`B_F2_BUFFER`.
	- Buffer is for even fields.
-
	- {cpp:enumerator}`B_SMALL_BUFFER`.
	- The buffer is a small buffer.

:::

These flags can be assigned to a buffer; the current possible values let
you specify whether the buffer should be used for even video fields or odd
video fields; if {cpp:enumerator}`B_SMALL_BUFFER` is set, the buffer is a
{cpp:class}`BSmallBuffer`.

## DefinedTypes

### buffer_clone_info

Declared in: media/Buffer.h

:::{code} cpp
struct buffer_clone_info {
   buffer_clone_info();
   ~buffer_clone_info();
   media_buffer_id buffer;
   area_id area;
   size_t offset;
   size_t size;
   int32 flags;
private:
   _reserved_[4];
};
:::

Describes where in memory a {hclass}`BBuffer` resides (in terms of the
memory area and offset into the area at which the buffer is located, and
the size of the buffer), as well as the buffer's flags.
