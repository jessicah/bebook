# BMediaBufferDecoder
## Constructor and Destructor
::::{abi-group}

:::{cpp:function} BMediaBufferDecoder::BMediaBufferDecoder()
:::
:::{cpp:function} BMediaBufferDecoder::BMediaBufferDecoder(const media_format* inFormat, const void* info = NULL, size_t infoSize = 0)
:::
:::{cpp:function} BMediaBufferDecoder::BMediaBufferDecoder(const media_codec_info* mci)
:::
The constructor sets up the {hclass}`BMediaBufferDecoder`. If you use the empty
form of the constructor, you'll have to call
{cpp:func}`~BMediaDecoder::SetTo`
to establish the format to be decoded before calling
{cpp:func}`~BMediaDecoder::Decode`.
The second form accepts a
{cpp:func}`~media::format`
structure, {hparam}`inFormat`, that
indicates the type of media data that will be input into the decoder.
{hparam}`info`, if specified, will be filled out with text information about the
node; you must specify a buffer {hparam}`infoSize` bytes long.
The third form of the constructor accepts a
{cpp:func}`~media::codec`
structure, {hparam}`mci`, that determines which codec should be used.
:::{admonition} Note
:class: note
If you use either the
{cpp:func}`~media::format`
or {cpp:func}`~media::codec`
form of the constructor, you must call
{cpp:func}`~BMediaBufferDecoder::InitCheck`
to ensure that construction was
successful before using any other functions in this class.
:::
::::

::::{abi-group}

:::{cpp:function} virtual BMediaBufferDecoder::~BMediaBufferDecoder()
:::
Releases the decoder add-on being used by the
{hclass}`BMediaBufferDecoder`.
::::

## Member Functions
::::{abi-group}

:::{cpp:function} status_t BMediaBufferDecoder::DecodeBuffer(const void* inputBuffer, size_t inputSize, void* outBuffer, int64* outFrameCount, media_header* outMH, media_decode_info* info)
:::
Decodes a chunk of media data from the input buffer
{hparam}`inputBuffer` into the output buffer specified by
{hparam}`outBuffer`. The input buffer contains
{hparam}`inputSize` bytes of media data. On return,
{hparam}`outFrameCount` is set to indicate how many frames
of data were decoded, and outMH is the header for the decoded
buffer.
The
{cpp:func}`~media::decode`
structure info is used on input to specify decoding parameters.
:::{list-table}
---
header-rows: 1
---
-
	- Return Code
	- Description
-
	- {cpp:enum}`B_OK`
	- No error.
-
	- Other errors.
	- The decoder's {cpp:func}`~BMediaDecoder::Decode` function can return errors.
:::
::::

::::{abi-group}

:::{cpp:function} status_t BMediaBufferDecoder::GetNextChunk(const void** chunkData, size_t* chunkLen, media_header* mh) = 0
:::
Implementation detail. This function is implemented to fetch memory from
the input buffer specified by the call to
{cpp:func}`~BMediaBufferDecoder::DecodeBuffer`.
::::

::::{abi-group}

:::{cpp:function} status_t BMediaBufferDecoder::InitCheck() const
:::
Returns a status_t value indicating whether or not construction was
successful. You must call this function after construction before calling
any other {hclass}`BMediaBufferDecoder` functions.
:::{list-table}
---
header-rows: 1
---
-
	- Return Code
	- Description
-
	- {cpp:enum}`B_OK`
	- The constructor was successful.
-
	- Other errors.
	- See {cpp:class}`BMediaDecoder`'s {cpp:func}`~BMediaDecoder::SetTo` function.
:::
::::
