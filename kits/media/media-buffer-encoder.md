:::{cpp:class} BMediaBufferEncoder
:::

# BMediaBufferEncoder

## Constructor and Destructor

::::{abi-group}
:::{cpp:function} BMediaBufferEncoder::BMediaBufferEncoder()
:::

:::{cpp:function} BMediaBufferEncoder::BMediaBufferEncoder(const media_format* outputFormat)
:::

:::{cpp:function} BMediaBufferEncoder::BMediaBufferEncoder(const media_codec_info* mci)
:::

The constructor sets up the {hclass}`BMediaBufferEncoder`. If you use the
empty form of the constructor, you'll have to call {cpp:func}`SetTo()
<BMediaEncoder::SetTo>` to establish the format to be encoded before
calling {cpp:func}`Encode() <BMediaEncoder::Encode>`.

The second form accepts a {cpp:func}`media_format <media::format>`
structure, {hparam}`inFormat`, that indicates the type of media data that
will be input into the encoder.

The third form of the constructor accepts a {ref}`media_codec_info`
structure, {hparam}`mci`, that determines which codec should be used.

:::{admonition} Note
:class: note
If you use either the {cpp:func}`media_format <media::format>` or
{ref}`media_codec_info` form of the constructor, you must call
{cpp:func}`InitCheck() <BMediaBufferEncoder::InitCheck>` to ensure that
construction was successful before using any other functions in this class.
:::
::::

::::{abi-group}
:::{cpp:function} virtual BMediaBufferEncoder::~BMediaBufferEncoder()
:::

Releases the encoder add-on being used by the
{hclass}`BMediaBufferEncoder`.
::::

## Member Functions

::::{abi-group}
:::{cpp:function} status_t BMediaBufferEncoder::EncodeToBuffer(void* outputBuffer, size_t* outputSize, const void* inputBuffer, int64 frameCount, media_encode_info* info)
:::

Encodes a chunk of media data from the input buffer by
{hparam}`inputBuffer`, which contains {hparam}`frameCount` frames of data.
The encoded data is written into the buffer indicated by
{hparam}`outputBuffer`. On return, {hparam}`outputSize` indicates how many
bytes of data were written into the buffer.

The {ref}`media_encode_info` structure info is used on input to specify
encoding parameters.

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
	- {cpp:enumerator}`B_OK`
	- No error.
-
	- Other errors.
	- The encoder's {cpp:func}`Encode() <BMediaEncoder::Encode>` function can
		return errors.

:::
::::

::::{abi-group}
:::{cpp:function} status_t BMediaBufferEncoder::InitCheck() const
:::

Returns a {htype}`status_t` value indicating whether or not construction
was successful. You must call this function after construction before
calling any other {hclass}`BMediaBufferEncoder` functions.

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
	- {cpp:enumerator}`B_OK`
	- The constructor was successful.
-
	- Other errors.
	- See {cpp:class}`BMediaEncoder`'s {cpp:func}`SetTo()
		<BMediaEncoder::SetTo>` function.

:::
::::

::::{abi-group}
:::{cpp:function} status_t BMediaBufferEncoder::WriteChunk(const void* chunkData, size_t chunkLength, media_encode_info* info) = 0
:::

Implemented to write the encoded media data into the buffer specified when
{cpp:func}`EncodeToBuffer() <BMediaBufferEncoder::EncodeToBuffer>` was
called.
::::
