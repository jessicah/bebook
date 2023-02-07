# BMediaDecoder
## Constructor and Destructor
::::{abi-group}

:::{cpp:function} BMediaDecoder::BMediaDecoder()
:::
:::{cpp:function} BMediaDecoder::BMediaDecoder(const media_format* inFormat, const void* info = NULL, size_t infoSize = 0)
:::
:::{cpp:function} BMediaDecoder::BMediaDecoder(const media_codec_info* mci)
:::
The constructor sets up the {hclass}`BMediaDecoder`. If you use the empty form of
the constructor, you'll have to call
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
structure,
{hparam}`mci`, that determines which codec should be used.
:::{admonition} Note
:class: note
If you use either the
{cpp:func}`~media::format`
or {cpp:func}`~media::codec`
form of the constructor, you must call
{cpp:func}`~BMediaDecoder::InitCheck`
to ensure that construction was
successful before using any other functions in this class.
:::
::::

::::{abi-group}

:::{cpp:function} virtual BMediaDecoder::~BMediaDecoder()
:::
Releases the decoder add-on being used by the {hclass}`BMediaDecoder`.
::::

## Hook Functions
::::{abi-group}

:::{cpp:function} status_t BMediaDecoder::GetNextChunk(const void** chunkData, size_t* chunkLen, media_header* mh)
:::
In derived classes, you should implement this function to fetch the media
data from the source. Set {hparam}`chunkData` to be a pointer to the next chunk of
media data, and {hparam}`chunkLen` to the size of that buffer. The
{cpp:func}`~media::header`
structure {hparam}`mh` provides information you can use
while fetching the chunk.
This hook is called by the decoder add-on in order to fetch the data from
the source.
Return {cpp:enum}`B_OK` if the chunk is fetched safely, or
an appropriate error code otherwise.
::::

## Member Functions
::::{abi-group}

:::{cpp:function} status_t BMediaDecoder::Decode(void* outBuffer, int64* frameCount, media_header* outMH, media_decode_info* info)
:::
Decodes a chunk of media data into the output buffer specified by
{hparam}`outBuffer`. On return, {hparam}`outFrameCount`
is set to indicate how many frames of
data were decoded, and {hparam}`outMH` is the header for the decoded buffer.
The
{cpp:func}`~media::decode`
structure info is used on input to specify decoding parameters.
The amount of data decoded is part of the format determined by
{cpp:func}`~BMediaDecoder::SetTo` or
{cpp:func}`~BMediaDecoder::SetInputFormat`.
For audio, it's the buffer size. For video, it's one
frame, which is height*row_bytes. The data to be decoded will be fetched
from the source by the decoder add-on calling the derived class'
{cpp:func}`~BMediaDecoder::GetNextChunk`
function.
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
	- {cpp:enum}`B_NO_INIT`
	- The {hclass}`BMediaDecoder` hasn't been initialized.
-
	- Other errors.
	- The decoder's {hmethod}`Decode()` function can return errors.
:::
::::

::::{abi-group}

:::{cpp:function} status_t BMediaDecoder::GetDecoderInfo(media_codec_info* outInfo) const
:::
Fills out the
{cpp:func}`~media::codec`
structure {hparam}`outInfo` with information about
the decoder being used by the {hclass}`BMediaDecoder`.
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
	- {cpp:enum}`B_NO_INIT`
	- The {hclass}`BMediaDecoder` hasn't been initialized.
-
	- Other errors.
	- The decoder's {hmethod}`GetCodecInfo()` function can return errors.
:::
::::

::::{abi-group}

:::{cpp:function} status_t BMediaDecoder::InitCheck() const
:::
Returns a status_t value indicating whether or not construction was
successful. You must call this function after construction before calling
any other {hclass}`BMediaDecoder` functions.
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
	- See {cpp:func}`~BMediaDecoder::SetTo`.
:::
::::

::::{abi-group}

:::{cpp:function} status_t BMediaDecoder::SetInputFormat(const media_format* inFormat, const void* info = NULL, size_t infoSize = 0)
:::
:::{cpp:function} status_t BMediaDecoder::SetOutputFormat(media_format* outputFormat)
:::
{hmethod}`SetInputFormat()` sets the input
data format to {hparam}`inFormat`. On return, {hparam}`info`
(if you don't specify {cpp:enum}`NULL`) is filled out by the decoder to contain
whatever textual information the decoder wants to provide. {hparam}`infoSize` must
indicate the size of the buffer pointed to by {hparam}`info`.
Unlike
{cpp:func}`~BMediaDecoder::SetTo`,
{hmethod}`SetInputFormat()` function does not select a codec, so the
currently-selected codec will continue to be used. You should only use
{hmethod}`SetInputFormat()` to refine the format settings if it will not require the
use of a different decoder.
{hmethod}`SetOutputFormat()` sets the format the decoder should output. On return,
the {hparam}`outputFormat` is changed to match the actual format that will be
output; this can be different if you specified any wildcards.
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
	- {cpp:enum}`B_NO_INIT`
	- The {hclass}`BMediaDecoder` hasn't been initialized yet.
-
	- Other errors.
	- The decoder's {hmethod}`Sniff()`, {hmethod}`Format()`,and {hmethod}`Reset()` functions can return errors through {hmethod}`SetInputFormat()`.
:::
::::

::::{abi-group}

:::{cpp:function} status_t BMediaDecoder::SetTo(const media_format* inFormat, const void* info = NULL, size_t infoSize = 0)
:::
:::{cpp:function} status_t BMediaDecoder::SetTo(const media_codec_info* mci)
:::
{hmethod}`SetTo()` sets the format of media data that will be decoded by the
{hclass}`BMediaDecoder` object. This also causes the
{hclass}`BMediaDecoder` to locate an
appropriate codec to use.
The first form accepts a
{cpp:func}`~media::format`
structure, {hparam}`inFormat`, that indicates
the type of media data that will be input into the decoder. {hparam}`info`, if
specified, will be filled out with text information about the node; you
must specify a buffer {hparam}`infoSize` bytes long.
The second form of {hmethod}`SetTo()` accepts a
{cpp:func}`~media::codec`
structure, {hparam}`mci`,
that determines which codec should be used.
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
	- {cpp:enum}`B_MEDIA_BAD_FORMAT`
	- The specified {cpp:func}`~media::format` isn't valid.
-
	- {cpp:enum}`B_BAD_VALUE`
	- Something else went wrong.
-
	- {cpp:enum}`B_ERROR`
	- Unable to instantiate the decoder.
:::
::::
