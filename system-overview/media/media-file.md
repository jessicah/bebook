# BMediaFile

The {cpp:class}`BMediaFile` class represents a file containing media data.
When instantiated a {cpp:class}`BMediaFile` with an {cpp:func}`entry_ref
<entry::ref>` to an existing media file, it sniffs the file and figures out
the right codecs to use when accessing that file.

To read an existing media file, you can then call {cpp:func}`TrackAt()
<BMediaFile::TrackAt>` to instantiate {cpp:class}`BMediaTrack` objects fot
the file's tracks; these can in turn be used to decode media data from the
file.

You can also write data to the file. In this case, you construct the
object by specifying an {cpp:func}`entry_ref <entry::ref>` and a
{ref}`media_file_format` specification describing the format of the media
data you plan to write into the file. You then call
{cpp:func}`CreateTrack() <BMediaFile::CreateTrack>` to create each track
you want to write into the file. Once each track has been created (but is
still empty), you call {cpp:func}`CommitHeader()
<BMediaFile::CommitHeader>` to write the file's header to disk, and you can
use {cpp:class}`BMediaTrack` functions to write the actual media data into
the tracks.

Call {cpp:func}`CloseFile() <BMediaFile::CloseFile>` when you're finished
writing to it (you don't need to call this if you're reading the file).

For an example of how to use {cpp:class}`BMediaFile` to read and write
media files, see "{ref}`Reading and Writing Media Files`"

:::{admonition} Note
:class: note
As a general rule, you can't use wildcards in any structures used by
{cpp:class}`BMediaFile` functions. You tell {cpp:class}`BMediaFile` what
format you have, and {cpp:class}`BMediaFile` will simply tell you whether
or not that format is supported.
:::
