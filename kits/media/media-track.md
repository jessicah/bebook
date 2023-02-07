# BMediaTrack
## Constructor and Destructor
::::{abi-group}

:::{cpp:function} virtual BMediaTrack::BMediaTrack()
:::
Destructor. You shouldn't delete a {hclass}`BMediaTrack` directly; instead, use
{cpp:func}`BMediaFile::ReleaseTrack` or
{cpp:func}`BMediaFile::ReleaseAllTracks`,
or let
{cpp:class}`BMediaFile`
destroy the track objects when it's deleted.
::::

## Member Functions
::::{abi-group}

:::{cpp:function} status_t BMediaTrack::AddCopyright(const char* data) const
:::
Sets the track's copyright notice to the text specified by data,
replacing the existing copyright notice if one exists.
:::{admonition} Warning
:class: warning
The {hclass}`BMediaTrack` class doesn't automatically perform any locking to
prevent multiple writes to the track from occurring at the same time. If
you have multiple threads writing into the same {hclass}`BMediaTrack`, you must use
a locking mechanism (such as a semaphore) to keep writes from overlapping.
:::
:::{list-table}
---
header-rows: 1
---
-
	- Return Code
	- Description
-
	- {cpp:enum}`B_OK`
	- The copyright was set.
-
	- {cpp:enum}`EPERM`
	- The file isn't opened for writing.
-
	- Other errors.
	- Are codec dependant.
:::
::::

::::{abi-group}

:::{cpp:function} status_t BMediaTrack::AddTrackInfo(uint32 code, const void* data, size_t size, uint32 flags = 0) const
:::
Adds an informational record of the specified type to the track. The
record is specified by the {hparam}`data` pointer,
and is {hparam}`size` bytes long. flags
contains flags that modify the operation (none are defined at this time).
:::{admonition} Warning
:class: warning
The {hclass}`BMediaTrack` class doesn't automatically perform any locking to
prevent multiple writes to the track from occurring at the same time. If
you have multiple threads writing into the same {hclass}`BMediaTrack`, you must use
a locking mechanism (such as a semaphore) to keep writes from overlapping.
:::
:::{list-table}
---
header-rows: 1
---
-
	- Return Code
	- Description
-
	- {cpp:enum}`B_OK`
	- The format was successfully returned.
-
	- Other errors.
	- The error returned depends on the codec interpreting the data.
:::
::::

::::{abi-group}

:::{cpp:function} int64 BMediaTrack::CountFrames() const
:::
Returns the total number of frames in the track.
::::

::::{abi-group}

:::{cpp:function} int64 BMediaTrack::CurrentFrame() const
:::
Returns the current frame in the track (the frame that will be read next
by {cpp:func}`~BMediaTrack::ReadFrames`.
::::

::::{abi-group}

:::{cpp:function} bigtime_t BMediaTrack::CurrentTime() const
:::
Returns the current position within the track, expressed in microseconds
since the start of the track.
::::

::::{abi-group}

:::{cpp:function} status_t BMediaTrack::DecodedFormat(media_format* ioFormat) const
:::
Negotiates the format that the codec will output when decoding the
track's data. Pass in {hparam}`ioFormat` the format that you want (with wildcards
as applicable). The codec will find and return in {hparam}`ioFormat` its best
matching format; this format will then be used when outputting decoded
data via
{cpp:func}`~BMediaTrack::ReadFrames`.
The format is typically of a
{cpp:enum}`B_MEDIA_RAW_AUDIO`
or {cpp:enum}`B_MEDIA_RAW_VIDEO`
flavor.
:::{list-table}
---
header-rows: 1
---
-
	- Return Code
	- Description
-
	- {cpp:enum}`B_OK`
	- The format was successfully negotiated and returned.
-
	- {cpp:enum}`B_ERROR`
	- The {hclass}`BMediaTrack` wasn't properly initialized, or there's no codec for the track's data.
-
	- Other errors.
	- The error returned depends on the codec interpreting the data.
:::
::::

::::{abi-group}

:::{cpp:function} bigtime_t BMediaTrack::Duration() const
:::
Returns the total duration of the track, in microseconds.
::::

::::{abi-group}

:::{cpp:function} status_t BMediaTrack::EncodedFormat(media_format* outFormat) const
:::
Returns the "native" encoded format of the track's data. This is the
format of the data returned by
{cpp:func}`~BMediaTrack::ReadChunk`.
:::{list-table}
---
header-rows: 1
---
-
	- Return Code
	- Description
-
	- {cpp:enum}`B_OK`
	- The format was successfully returned.
-
	- Other errors.
	- The error returned depends on the codec interpreting the data.
:::
::::

::::{abi-group}

:::{cpp:function} status_t BMediaTrack::FindKeyFrameForTime(bigtime_t* inOutTime, int32 flags = 0) const
:::
:::{cpp:function} status_t BMediaTrack::FindKeyFrameForFrame(int64* inOutFrame, int32 flags = 0) const
:::
{hmethod}`FindKeyFrameForTime()` accepts in
{hparam}`inOutTime` a time, and returns in
{hparam}`inOutTime` the time at which the closest key
frame to that time begins. Likewise,
{hmethod}`FindKeyFrameForFrame()` returns the closest key
frame number to the specified frame.
The {hparam}`flags` argument lets you indicate
whether to seek forward or backward for the key frame.
If you want to find the nearest key frame before the indicated
frame or time, specify
{cpp:func}`~B::MEDIA`
in flags. If you want to find the nearest key frame after the indicated frame or time,
specify
{cpp:func}`~B::MEDIA`.
::::

::::{abi-group}

:::{cpp:function} status_t BMediaTrack::Flush()
:::
Flushes all buffered encoded data to disk; you should call this function
after you've finished writing the last frame to the track. This ensures
that everything's flushed at the right offset into the file.
:::{list-table}
---
header-rows: 1
---
-
	- Return Code
	- Description
-
	- {cpp:enum}`B_OK`
	- The buffers were flushed.
-
	- Other errors.
	- Are codec dependant
:::
::::

::::{abi-group}

:::{cpp:function} status_t BMediaTrack::GetCodecInfo(media_codec_info* codecInfo) const
:::
Returns information about the codec being used to read or write the
track's data.
:::{list-table}
---
header-rows: 1
---
-
	- Return Code
	- Description
-
	- {cpp:enum}`B_OK`
	- The codec info was returned.
-
	- {cpp:enum}`B_BAD_TYPE`
	- There's no valid codec in use by the track.
:::
::::

::::{abi-group}

:::{cpp:function} status_t BMediaTrack::GetEncodeParameters(encode_parameters* parameters) const
:::
:::{cpp:function} status_t BMediaTrack::SetEncodeParameters(encode_parameters* parameters)
:::
{hmethod}`GetEncodeParameters()` returns the
encode_parameters
being used when encoding data on the track.
{hmethod}`SetEncodeParameters()` changes the
encode_parameters
being used while encoding data.
::::

::::{abi-group}

:::{cpp:function} BView* BMediaTrack::GetParameterView()
:::
Returns a
{cpp:class}`BView`
containing controls for adjusting the codec's and track's
parameters. Returns {cpp:enum}`NULL` if there isn't a view available.
::::

::::{abi-group}

:::{cpp:function} status_t BMediaTrack::InitCheck() const
:::
Returns a status code indicating whether or not the track was
successfully and completely instantiated.
:::{list-table}
---
header-rows: 1
---
-
	- Return Code
	- Description
-
	- {cpp:enum}`B_OK`
	- The track was constructed properly.
-
	- {cpp:enum}`B_BAD_VALUE`
	- An error occurred setting up the track.
:::
::::

::::{abi-group}

:::{cpp:function} status_t BMediaTrack::ReadChunk(char** outBuffer, int32* ioSize, media_header* header = NULL)
:::
Returns in {hparam}`outBuffer` a pointer
to the next {hparam}`ioSize` bytes of the media
track; the actual number of bytes returned is returned in {hparam}`ioSize`; this
may be different if the end of the track is reached. The header is set to
describe the returned buffer.
The data returned by this function isn't decoded. Typically you'll only
use this function if there's no codec available to decode the media data.
:::{list-table}
---
header-rows: 1
---
-
	- Return Code
	- Description
-
	- {cpp:enum}`B_OK`
	- The format was successfully negotiated and returned.
-
	- {cpp:enum}`B_ERROR`
	- The {hclass}`BMediaTrack` wasn't properly initialized, or there's no codec for the track's data.
-
	- Other errors.
	- The error returned depends on the codec interpreting the data.
:::
::::

::::{abi-group}

:::{cpp:function} status_t BMediaTrack::ReadFrames(void* outBuffer, int64* outFrameCount, media_header* outHeader = NULL)
:::
:::{cpp:function} status_t BMediaTrack::ReadFrames(void* outBuffer, int64* outFrameCount, media_header* outHeader, media_decode_info* info)
:::
Fills the buffer pointed to by {hparam}`outBuffer` with the next frames or samples
from the track, starting at the current position. For video tracks, the
next frame of video is decoded and stored into the output buffer. For
audio tracks, the buffer is filled with the number of frames negotiated
using
{cpp:func}`~BMediaTrack::DecodedFormat`.
If the end of the track is reached before the
buffer is filled, a partial buffer will be returned.
On return, {hparam}`outFrameCount` indicates the number of frames returned, and
{hparam}`outHeader`, if you specified a non-{cpp:enum}`NULL` value, contains the header of the
buffer containing the frame or frames. You can obtain useful information
(such as the media start time for the buffer) from the header.
The second form of this function lets you provide a
{cpp:func}`~media::decode`
structure to provide additional information to the decoder, such as how
much time it's allowed to use to decode the data and format- and
codec-specific information.
:::{list-table}
---
header-rows: 1
---
-
	- Return Code
	- Description
-
	- {cpp:enum}`B_OK`
	- The frames have been returned.
-
	- {cpp:enum}`EPERM`
	- The file wasn't opened for reading.
-
	- Other errors.
	- The error returned depends on the codec interpreting the data.
:::
::::

::::{abi-group}

:::{cpp:function} status_t BMediaTrack::ReplaceFrames(void* inBuffer, int64* ioFrameCount, media_header* header)
:::
Replaces the number of frames specified in {hparam}`ioFrameCount` in the track.
{hparam}`inBuffer` points to the source buffer for the new frames.
::::

::::{abi-group}

:::{cpp:function} status_t BMediaTrack::SeekToFrame(int64* ioFrame, int32 flags = 0)
:::
:::{cpp:function} status_t BMediaTrack::SeekToTime(bigtime_t* ioTime, int32 flags = 0)
:::
Seeks to the specified position in the track.
{hmethod}`SeekToFrame()` accepts a destination position
as a frame number, and {hmethod}`SeekToTime()` accepts a
destination position as time in microseconds. They each return (in
{hparam}`ioFrame` or in {hparam}`ioTime`)
the position to which they actually moved.
For example, if a video codec is only capable of seeking to key
frames, the returned {hparam}`ioFrame` might be different
than the one specified on input.
If you want to seek explicitly to the nearest key frame before the
current frame, specify
{cpp:func}`~B::MEDIA`
in {hparam}`flags`. If you want to find the nearest key frame
after the current time, specify
{cpp:func}`~B::MEDIA`.
:::{list-table}
---
header-rows: 1
---
-
	- Return Code
	- Description
-
	- {cpp:enum}`B_OK`
	- The format was successfully returned.
-
	- Other errors.
	- The error returned depends on the codec interpreting the data.
:::
::::

::::{abi-group}

:::{cpp:function} status_t BMediaTrack::SetParameterValue(int32 id, const void* value, size_t* size)
:::
:::{cpp:function} status_t BMediaTrack::GetParameterValue(int32 id, const void* value, size_t* size)
:::
{hmethod}`SetParameterValue()` sets the value
of the parameter specified by {hparam}`id` to
the data pointed to by {hparam}`value`; this data is
{hparam}`size` bytes long.
{hmethod}`GetParameterValue()` returns
in {hparam}`value` the value of the specified
parameter, and the size of the value in bytes in the
{hparam}`size` argument.
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
	- {cpp:enum}`EPERM`
	- The codec isn't configurable.
-
	- Other errors.
	- Are codec dependant.
:::
::::

::::{abi-group}

:::{cpp:function} status_t BMediaTrack::SetQuality(float quality)
:::
:::{cpp:function} status_t BMediaTrack::GetQuality(float* quality)
:::
These functions set and return the codec's quality setting (where 1.0
means maximum quality).
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
	- {cpp:enum}`B_ERROR`
	- The codec doesn't support a quality setting.
-
	- Other errors.
	- Are codec dependant.
:::
::::

::::{abi-group}

:::{cpp:function} BParameterWeb* BMediaTrack::Web()
:::
Returns a
{cpp:class}`BParameterWeb`
that can be used for configuring the track and
codec. Returns {cpp:enum}`NULL` if the codec doesn't support user configuration.
::::

::::{abi-group}

:::{cpp:function} status_t BMediaTrack::WriteChunk(void* data, size_t size, int32 flags = 0)
:::
Writes the data pointed to by {hparam}`data`,
which contains {hparam}`size` bytes of data,
into the track. Specify {cpp:enum}`B_MEDIA_KEY_FRAME`
for {hparam}`flags` if the frame is a key
frame. It's assumed that the data is already encoded.
:::{admonition} Note
:class: note
The {hclass}`BMediaTrack` class doesn't automatically perform any locking to
prevent multiple writes to the track from occurring at the same time. If
you have multiple threads writing into the same {hclass}`BMediaTrack`, you must use
a locking mechanism (such as a semaphore) to keep writes from overlapping.
:::
In general, you should only use {hmethod}`WriteChunk()` if you're reading compressed
data from one file and copying it into another, without trying to
interpret the data.
:::{list-table}
---
header-rows: 1
---
-
	- Return Code
	- Description
-
	- {cpp:enum}`B_OK`
	- The data has been written.
-
	- {cpp:enum}`EPERM`
	- The file wasn't opened for writing.
-
	- Other errors.
	- The error returned depends on the codec interpreting the data.
:::
::::

::::{abi-group}

:::{cpp:function} status_t BMediaTrack::WriteFrames(void* data, int32 numFrames, int32 flags = 0)
:::
Writes the data pointed to by {hparam}`data`,
which contains {hparam}`numFrame` frames, into
the track. Specify {cpp:enum}`B_MEDIA_KEY_FRAME` for
{hparam}`flags` if the frame is a key frame.
:::{admonition} Note
:class: note
The {hclass}`BMediaTrack` class doesn't automatically perform any locking to
prevent multiple writes to the track from occurring at the same time. If
you have multiple threads writing into the same {hclass}`BMediaTrack`, you must use
a locking mechanism (such as a semaphore) to keep writes from overlapping.
:::
You always have to select an encoder before writing frames into a media
track, even if the data is raw audio or video. When writing raw audio or
video data into a {hclass}`BMediaTrack`, you need to use the raw encoder. Even
though this doesn't transform the data, it sets up internal data that's
necessary for the file to be played back properly after it's created.
:::{list-table}
---
header-rows: 1
---
-
	- Return Code
	- Description
-
	- {cpp:enum}`B_OK`
	- The frames have been written.
-
	- {cpp:enum}`EPERM`
	- The file wasn't opened for writing.
-
	- Other errors.
	- The error returned depends on the codec interpreting the data.
:::
::::

## Constants
::::{abi-group}

Declared in: media/MediaTrack.h
:::{list-table}
---
header-rows: 1
---
-
	- Constant
	- Description
-
	- {cpp:enum}`B_MEDIA_SEEK_CLOSEST_FORWARD`
	- Seek to the nearest key frame after the current position in the track.
-
	- {cpp:enum}`B_MEDIA_SEEK_CLOSEST_BACKWARD`
	- Seek to the nearest key frame before the current position in the track.
-
	- {cpp:enum}`B_MEDIA_SEEK_DIRECTION_MASK`
	- Mask the seek flags with this value to obtain the seek direction.
:::
These flags, used when calling
{cpp:func}`~BMediaTrack::SeekToTime` and
{cpp:func}`~BMediaTrack::SeekToFrame`,
let you
look for the nearest key frame after or before the current position in
the file, without having to guess the time or frame number at which it's
located.
::::
