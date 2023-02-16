:::{cpp:class} BMediaFile
:::

# BMediaFile

## Constructor and Destructor

::::{abi-group}
:::{cpp:function} BMediaFile::BMediaFile(const entry_ref* ref)
:::

:::{cpp:function} BMediaFile::BMediaFile(BDataIO* source)
:::

:::{cpp:function} BMediaFile::BMediaFile(const entry_ref* ref, int32 flags = 0)
:::

:::{cpp:function} BMediaFile::BMediaFile(BDataIO* source, int32 flags = 0)
:::

:::{cpp:function} BMediaFile::BMediaFile(const entry_ref* ref, const media_file_format* fileFormat, int32 flags = 0)
:::

:::{cpp:function} BMediaFile::BMediaFile(BDataIO* source, const media_file_format* fileFormat, int32 flags = 0)
:::

The first four forms of the constructor initializes the
{hclass}`BMediaFile` to read the file specified by {hparam}`ref` or by
{hparam}`source`. Once this has been done, be sure to call
{cpp:func}`InitCheck() <BMediaFile::InitCheck>` to ensure that the file was
successfully sniffed. If sniffing was successful, the {hclass}`BMediaFile`
object can then be used to instantiate the {cpp:class}`BMediaTrack` objects
necessary to read the file's data.

The second two forms prepare a {hclass}`BMediaFile` object for writing to
a media file, which is specified by either {hparam}`ref` or
{hparam}`destination`. The format of the file to be written is specified by
{hparam}`fileFormat`.

The flags can be a combination of the following values:

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
	- {cpp:enumerator}`B_MEDIA_FILE_REPLACE_MODE`
	- Replace any existing media file, if writing.
-
	- {cpp:enumerator}`B_MEDIA_FILE_NO_READ_AHEAD`
	- Don't read ahead in the file.
-
	- {cpp:enumerator}`B_MEDIA_FILE_UNBUFFERED`
	- Use smaller reads. This can be handy if you're trying to stream
		low-bitrate files without waiting for the extractor to fill a large
		outgoing buffer.
-
	- {cpp:enumerator}`B_MEDIA_FILE_BIG_BUFFERS`
	- Use large buffers.

:::
::::

::::{abi-group}
:::{cpp:function} virtual BMediaFile::~BMediaFile()()
:::

Destructor.
::::

## Member Functions

::::{abi-group}
:::{cpp:function} status_t BMediaFile::AddChunk(int32 type, const void* data, size_t size)
:::

Writes a user-defined chunk of data to the file (if doing so is supported
by the encoder). The {hparam}`type` argument indicates the chunk type,
{hparam}`data` points to the data to be written, and {hparam}`size`
indicates the size of the data to write to the file.

:::{admonition} Warning
:class: warning
The {hclass}`BMediaFile` class doesn't automatically perform any locking
to prevent multiple writes to the file from occurring at the same time. If
you have multiple threads writing into the same {hclass}`BMediaFile`, you
must use a locking mechanism (such as a {ref}`semaphore`) to keep writes
from overlapping.
:::

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
	- {cpp:enumerator}`B_BAD_TYPE`
	- The {hclass}`BMediaFile` doesn't reference a valid file.
-
	- Other errors
	- Are codec specific.

:::
::::

::::{abi-group}
:::{cpp:function} status_t BMediaFile::AddCopyright(const char* data)
:::

:::{cpp:function} const char* BMediaFile::Copyright() const
:::

{hmethod}`AddCopyright()` sets the file's copyright notice to the string
specified by {hparam}`data`. Any existing notice is replaced. The string is
copied, so the original belongs to you.

{hmethod}`Copyright()` returns the media file's copyright notice, or
{cpp:expr}`NULL` if there isn't one. This string belongs to the
{hclass}`BMediaFile`, so don't delete or change it.

:::{admonition} Warning
:class: warning
The {hclass}`BMediaFile` class doesn't automatically perform any locking
to prevent multiple writes to the file from occurring at the same time. If
you have multiple threads writing into the same {hclass}`BMediaFile`, you
must use a locking mechanism (such as a {ref}`semaphore`) to keep writes
from overlapping.
:::

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
	- No error. ({hmethod}`AddCopyright()` only)
-
	- {cpp:enumerator}`B_BAD_TYPE`
	- The {hclass}`BMediaFile` doesn't reference a valid file.
		({hmethod}`AddCopyright()` only)
-
	- Other errors
	- Are codec specific. ({hmethod}`AddCopyright()` only)

:::
::::

::::{abi-group}
:::{cpp:function} status_t BMediaFile::CloseFile()
:::

Once all media data has been written to all tracks, you need to call
{hmethod}`CloseFile()` so the {hclass}`BMediaFile` object can tidy up the
file and finish the writing tasks. If you forget to call
{hmethod}`CloseFile()`, the resulting file may not be complete.

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
	- {cpp:enumerator}`B_BAD_TYPE`
	- The {hclass}`BMediaFile` doesn't reference a valid file.
-
	- Other errors
	- Are codec specific.

:::
::::

::::{abi-group}
:::{cpp:function} status_t BMediaFile::CommitHeader()
:::

After you've finished adding new tracks to a file, you need to call
{hmethod}`CommitHeader()` to let the {hclass}`BMediaFile` set up the file's
header. This helps optimize the file writing process.

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
	- {cpp:enumerator}`B_BAD_TYPE`
	- The {hclass}`BMediaFile` doesn't reference a valid file.
-
	- Other errors
	- Are codec specific.

:::
::::

::::{abi-group}
:::{cpp:function} int32 BMediaFile::CountTracks() const
:::

Returns the number of tracks in the media file. The return value is
undefined if the initialization failed.
::::

::::{abi-group}
:::{cpp:function} BMediaTrack* BMediaFile::CreateTrack(media_format* mediaFormat, const media_codec_info* codecInfo)
:::

:::{cpp:function} BMediaTrack* BMediaFile::CreateTrack(media_format* mediaFormat)
:::

Creates a new track in the file and returns a {cpp:class}`BMediaTrack`
object referencing it. The track is configured to use the media format
specified by {hparam}`mediaFormat`, and will be written using the codec
described by {hparam}`codecInfo`. You can only use
{cpp:func}`BMediaTrack::WriteFrames` to write into the track.

If you use the second form of the constructor, without a
{hparam}`codecInfo` argument, the track will be written containing raw
media data. You can only use {cpp:func}`BMediaTrack::WriteChunk` to write
into the track.

The {hparam}`mediaFormat` indicates the format of the buffers you'll be
passing along to the write function, and {hparam}`codecInfo` specifies the
codec you want to use to encode the data into the track.

:::{admonition} Note
:class: note
The {hparam}`mediaFormat` can't contain any wildcards; you have to specify
the exact format that you're going to be providing. {hparam}`mediaFormat`
must also be the same structure you passed to {ref}`get_next_encoder()`.
:::

When writing new media files, you should create all your tracks at once
before writing any media data. Once all the tracks have been created, be
sure to call {cpp:func}`CommitHeader() <BMediaFile::CommitHeader>` to write
the header to disk. This is necessary since the header size may vary
depending on the number of tracks you put in the file, and once you start
writing media data into the tracks, it would be difficult (and inefficient)
to resize the header.

If an error occurs while creating the new track, {cpp:expr}`NULL` is
returned.
::::

::::{abi-group}
:::{cpp:function} status_t BMediaFile::GetFileFormatInfo(media_file_format* info) const
:::

Fills the specified {htype}`media_file_format` structure with information
describing the file format of the file referenced by the
{hclass}`BMediaFile` object.

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
	- The {hclass}`BMediaFile` doesn't reference a valid file.

:::
::::

::::{abi-group}
:::{cpp:function} BView* BMediaFile::GetParameterView() const
:::

Returns a {cpp:class}`BView` containing controls for adjusting the file
format's parameters. Returns {cpp:expr}`NULL` if there isn't a view
available.
::::

::::{abi-group}
:::{cpp:function} status_t BMediaFile::InitCheck() const
:::

Returns the result code from the constructor. You should always call this
after instantiating a {hclass}`BMediaFile` object, but before using it.

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
	- {cpp:enumerator}`B_MEDIA_NO_HANDLER`
	- No codec available for the required or requested format.
-
	- {cpp:enumerator}`B_NO_MEMORY`
	- Not enough memory to set up the codec (writing).
-
	- {cpp:enumerator}`B_BAD_INDEX`
	- The required add-on wasn't found (writing).
-
	- {cpp:enumerator}`B_MISSING_SYMBOL`
	- The add-on doesn't support writing.

:::
::::

::::{abi-group}
:::{cpp:function} status_t BMediaFile::ReleaseTrack(BMediaTrack* track)
:::

:::{cpp:function} status_t BMediaFile::ReleaseAllTracks()
:::

{hmethod}`ReleaseTrack()` releases the resources used by the specified
{hparam}`track`. Doing so reduces your application's memory usage. If you
want to release every track you're using, you can call
{hmethod}`ReleaseAllTracks()`.

Once released, a track can't be used any longer until you use
{cpp:func}`TrackAt() <BMediaFile::TrackAt>` again.

If the {hclass}`BMediaFile` wasn't properly initialized, or the index is
invalid, {cpp:expr}`NULL` is returned.

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
	- {cpp:enumerator}`B_ERROR`
	- Couldn't release the track (it may be invalid, or not actually in use).

:::
::::

::::{abi-group}
:::{cpp:function} status_t BMediaFile::SetParameterValue(int32 id, const void* value, size_t size)
:::

:::{cpp:function} status_t BMediaFile::GetParameterValue(int32 id, const void* value, size_t size)
:::

{hmethod}`SetParameterValue()` sets the value of the parameter specified
by {hparam}`id` to the data pointed to by {hparam}`value`; this data is
{hparam}`size` bytes long.

{hmethod}`GetParameterValue()` returns in {hparam}`value` the value of the
specified parameter, and the size of the value in bytes in the
{hparam}`size` argument.

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
	- The {hclass}`BMediaFile` doesn't reference a valid file.

:::
::::

::::{abi-group}
:::{cpp:function} BMediaTrack* BMediaFile::TrackAt(int32 index)
:::

Returns a {cpp:class}`BMediaTrack` object referencing the track at the
specified {hparam}`index` into the file. The index must be a value between
0 and {cpp:func}`CountTracks() <BMediaFile::CountTracks>` - 1.

If the {hclass}`BMediaFile` wasn't properly initialized, or the
{hparam}`index` is invalid, {cpp:expr}`NULL` is returned.

:::{admonition} Note
:class: note
You must call {cpp:func}`ReleaseTrack() <BMediaFile::ReleaseTrack>` when
you're finished with the track.
:::
::::

::::{abi-group}
:::{cpp:function} BParameterWeb* BMediaFile::Web()
:::

Returns a {cpp:class}`BParameterWeb` that can be used for configuring the
file format's parameters. Returns {cpp:expr}`NULL` if the codec doesn't
support user configuration.
::::

## Constants

### Constructor Flags

Declared in: media/MediaFile.h

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
	- {cpp:enumerator}`B_MEDIA_FILE_REPLACE_MODE`
	- Replace any existing media file, if writing.
-
	- {cpp:enumerator}`B_MEDIA_FILE_NO_READ_AHEAD`
	- Don't read ahead in the file.
-
	- {cpp:enumerator}`B_MEDIA_FILE_UNBUFFERED`
	- Use smaller reads. This can be handy if you're trying to stream
		low-bitrate files without waiting for the extractor to fill a large
		outgoing buffer.
-
	- {cpp:enumerator}`B_MEDIA_FILE_BIG_BUFFERS`
	- Use large buffers.

:::

These flags control the behavior of the constructor.
