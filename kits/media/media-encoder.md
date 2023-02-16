:::{cpp:class} BMediaEncoder
:::

# BMediaEncoder

## Constructor and Destructor

::::{abi-group}
:::{cpp:function} BMediaEncoder::BMediaEncoder()
:::

:::{cpp:function} BMediaEncoder::BMediaEncoder(const media_format* outputFormat)
:::

:::{cpp:function} BMediaEncoder::BMediaEncoder(const media_codec_info* mci)
:::

The constructor sets up the {hclass}`BMediaEncoder`. If you use the empty
form of the constructor, you'll have to call {cpp:func}`SetTo()
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
{cpp:func}`InitCheck() <BMediaEncoder::InitCheck>` to ensure that
construction was successful before using any other functions in this class.
:::
::::

::::{abi-group}
:::{cpp:function} virtual BMediaEncoder::~BMediaEncoder()
:::

Releases the encoder add-on being used by the {hclass}`BMediaEncoder`.
::::

## Member Functions

::::{abi-group}
:::{cpp:function} status_t BMediaEncoder::AddTrackInfo(uint32 code, const char* data, size_t size)
:::

In derived classes, you should implement this function to write track
information into the output file. {hparam}`code` indicates the type of
information being added, and {hparam}`data` is the information data itself.
{hparam}`size` indicates the size of the data to be written.

By default, this function returns {cpp:enumerator}`B_ERROR`. Your
implementation should return {cpp:enumerator}`B_OK` if the information was
written successfully; otherwise it should return an appropriate error code.
::::

::::{abi-group}
:::{cpp:function} status_t BMediaEncoder::Encode(void* inBuffer, int64 frameCount, media_encode_info* info)
:::

Encodes a chunk of media data from the input buffer by {hparam}`inBuffer`,
which contains {hparam}`frameCount` frames of data.

The {ref}`media_encode_info` structure info is used on input to specify
encoding parameters.

After the data is encoded, the encoder will call the derived class'
{cpp:func}`WriteChunk() <BMediaEncoder::WriteChunk>` function to write the
data into the file.

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
	- {cpp:enumerator}`B_NO_INIT`
	- The {hclass}`BMediaEncoder` hasn't been initialized.
-
	- Other errors.
	- The encoder's Encode() function can return errors.

:::
::::

::::{abi-group}
:::{cpp:function} status_t BMediaEncoder::GetEncodeParameters(encode_parameters* inParameters) const
:::

:::{cpp:function} status_t BMediaEncoder::SetEncodeParameters(encode_parameters* outParameters)
:::

{hmethod}`GetEncodeParameters()` returns in {hparam}`inParameters` the
{cpp:func}`encode_parameters <encode::parameters>` describing how the
encoder add-on is configured.

{hmethod}`SetEncodeParameters()` let you specify the
{cpp:func}`encode_parameters <encode::parameters>` for the add-on.

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

:::
::::

::::{abi-group}
:::{cpp:function} status_t BMediaEncoder::InitCheck() const
:::

Returns a {htype}`status_t` value indicating whether or not construction
was successful. You must call this function after construction before
calling any other {hclass}`BMediaEncoder` functions.

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

-
	- Other Errors
	- See {cpp:func}`SetTo() <BMediaEncoder::SetTo>`

:::
::::

::::{abi-group}
:::{cpp:function} status_t BMediaEncoder::SetFormat(media_format* inputFormat, media_format* outputFormat, media_file_format* mfi = NULL)
:::

{hmethod}`SetFormat()` sets the input and output formats to be used by the
encoder, as well as the {ref}`media_file_format` describing the file to
which the encoded data will be written.

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
	- {cpp:enumerator}`B_NO_INIT`
	- The {hclass}`BMediaEncoder` hasn't been initialized yet.

:::
::::

::::{abi-group}
:::{cpp:function} status_t BMediaEncoder::SetTo(const media_format* outputFormat)
:::

:::{cpp:function} status_t BMediaEncoder::SetTo(const media_codec_info* mci)
:::

{hmethod}`SetTo()` sets the format of media data that will be encoded by
the {hclass}`BMediaEncoder` object. This also causes the
{hclass}`BMediaEncoder` to locate an appropriate codec to use.

The first form accepts a {cpp:func}`media_format <media::format>`
structure, {hparam}`outputFormat`, that indicates the type of media data
that the encoder should output.

The second form of {hmethod}`SetTo()` accepts a {ref}`media_codec_info`
structure, {hparam}`mci`, that determines which codec should be used.

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
	- {cpp:enumerator}`B_NO_INIT`
	- The {hclass}`BMediaEncoder` isn't initialized.
-
	- Other Errors.
	- See {ref}`get_next_encoder()` and {ref}`get_image_symbol()`

:::
::::

::::{abi-group}
:::{cpp:function} virtual status_t BMediaEncoder::SetTo(const void* chunkData, size_t chunkLength, media_encode_info* info) = 0
:::

In derived classes, you should implement this function to write the chunk
of encoded data pointed to by {hparam}`chunkData` into the destination file
or buffer. {hparam}`chunkLength` indicates the size of the buffer, and info
provides information about the encoding process that you might need to
reference.

Return {cpp:enumerator}`B_OK` if the data is successfully written;
otherwise return an appropriate error code.
::::
