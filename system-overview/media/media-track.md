# BMediaTrack

The {cpp:class}`BMediaTrack` class provides access to a particular track
in a media file. It's always instantiated using the
{cpp:func}`BMediaFile::TrackAt` or {cpp:func}`BMediaFile::CreateTrack`
function.

The {cpp:class}`BMediaTrack` constructor searches for a codec that can
handle the encoded data in the track; once that's been done, the track is
ready to be used.

If you opened the file for writing, you can write data into the track. If
you specified the {cpp:enumerator}`B_MEDIA_FILE_REPLACE_MODE` flag when
constructing the {cpp:class}`BMediaFile`, you can both read and write from
the file. If no decoder is available for the track, you can still use
{cpp:func}`ReadChunk() <BMediaTrack::ReadChunk>` to access the encoded data
directly.

After instantiating the {cpp:class}`BMediaTrack`, using the
{cpp:class}`BMediaFile` functions for doing so, you should call
{cpp:func}`InitCheck() <BMediaTrack::InitCheck>` to be sure the track is
valid. You can then use {cpp:func}`ReadFrames() <BMediaTrack::ReadFrames>`
and {cpp:func}`WriteFrames() <BMediaTrack::WriteFrames>` to read and write
data to the file, as appropriate. For video data, you should work one frame
at a time.

You can also seek particular times or frames using {cpp:func}`SeekToTime()
<BMediaTrack::SeekToTime>` or {cpp:func}`SeekToFrame()
<BMediaTrack::SeekToFrame>`.

For an example of how to use {cpp:class}`BMediaTrack` to read and write
tracks in media files, see "{ref}`Reading and Writing Media Files`"

:::{admonition} Note
:class: note
As a general rule, you can't use wildcards in any structures used by
{cpp:class}`BMediaTrack` functions. You tell {cpp:class}`BMediaTrack` what
format you have, and {cpp:class}`BMediaTrack` will simply tell you whether
or not that format is supported.
:::
