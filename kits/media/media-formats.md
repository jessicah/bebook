# BMediaFormats
## Constructor and Destructor
::::{abi-group}

:::{cpp:function} BMediaFormats::BMediaFormats()
:::
Constructor. Call
{cpp:func}`~BMediaFormats::InitCheck`
to ensure that the object was initialized properly after you instantiate it.
::::

::::{abi-group}

:::{cpp:function} virtual BMediaFormats::~BMediaFormats()
:::
Destructor.
::::

## Member Functions
::::{abi-group}

:::{cpp:function} status_t BMediaFormats::GetBeOSFormatFor(uint32 format, media_format* outFormat, media_type type = B_MEDIA_UNKNOWN_TYPE)
:::
:::{cpp:function} status_t BMediaFormats::GetAVIFormatFor(uint32 format, media_format* outFormat, media_type type = B_MEDIA_UNKNOWN_TYPE)
:::
:::{cpp:function} status_t BMediaFormats::GetQuicktimeFormatFor(uint32 vendor, uint32 codec, media_format* outFormat, media_type type = B_MEDIA_UNKNOWN_TYPE)
:::
{hmethod}`GetBeOSFormatFor()` returns in
{hparam}`outFormat` a
{cpp:func}`~media::format`
structure that describes the media format corresponding to the given BeOS
{hparam}`format` ID and
{cpp:func}`~Constants::media`.
{hmethod}`GetAVIFormatFor()` returns in
{hparam}`outFormat` a
{cpp:func}`~media::format`
structure that describes the media format corresponding to the given AVI
{hparam}`format` ID and
{cpp:func}`~Constants::media`.
{hmethod}`GetQuicktimeormatFor()` returns in
{hparam}`outFormat` a
{cpp:func}`~media::format`
structure that describes the media format corresponding to the given QuickTime
{hparam}`vendor` ID, {hparam}`codec` ID, and
{cpp:func}`~Constants::media`.
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
	- {cpp:enum}`B_BAD_TYPE`
	- The specified {cpp:func}`~Constants::media`. isn't supported.
-
	- {cpp:enum}`B_MEDIA_BAD_FORMAT`
	- The specified combination of parameters isn't  supported.
-
	- Other errors
	- The format couldn't be determined.
:::
::::

::::{abi-group}

:::{cpp:function} status_t BMediaFormats::GetCodeFor(const media_format& format, media_format_family family, media_format_description* outDescription)
:::
Given the specified media format, returns
in {hparam}`outDescription` the media
format description for the specified {hparam}`format` family.
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
	- The specified format isn't recognized.
-
	- Other errors
	- The code couldn't be determined.
:::
::::

::::{abi-group}

:::{cpp:function} status_t BMediaFormats::GetFormatFor(const media_format_description& description, media_format* outFormat)
:::
Returns in {hparam}`outFormat` a
{cpp:func}`~media::format`
structure that describes the media format specified by
{hparam}`description`. This lets you easily obtain a
{cpp:func}`~media::format`
structure from file-native description information.
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
	- The specified description isn't recognized.
-
	- Other errors
	- The format couldn't be determined.
:::
::::

::::{abi-group}

:::{cpp:function} status_t BMediaFormats::GetFormatFor(media_format* outFormat, media_format_description* outDescription)
:::
Fills {hparam}`outFormat` and
{hparam}`outDescription` with the
{cpp:func}`~media::format`
and
{cpp:func}`~media::format`
of the next supported media format.
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
	- {cpp:enum}`B_BAD_INDEX`
	- No more formats to return.
-
	- Other errors
	- The format couldn't be determined.
:::
::::

::::{abi-group}

:::{cpp:function} status_t BMediaFormats::InitCheck()
:::
Returns the status code from the constructor; you should call this to be
sure the object was properly initialized before issuing any other calls.
:::{list-table}
---
header-rows: 1
---
-
	- Return Code
	- Description
-
	- {cpp:enum}`B_OK`
	- The object is ready to use.
-
	- {cpp:enum}`B_BAD_HANDLER`
	- The object isn't ready.
-
	- Other errors
	- The Media Server couldn't be contacted.
:::
::::

::::{abi-group}

:::{cpp:function} bool BMediaFormats::Lock()
:::
:::{cpp:function} void BMediaFormats::Lock()
:::
{hmethod}`Lock()` locks the
{hclass}`BMediaFormats` object so you can use it with the
assurance that it won't change while you're working. You should call this
before using any of the other {hclass}`BMediaFormats` functions.
Returns {cpp:enum}`true` if it's safe to use the
{hclass}`BMediaFormats` object; otherwise returns
{cpp:enum}`false`.
{hmethod}`Unlock()` releases the
{hclass}`BMediaFormats` object when you're done with it; be
sure to call it when you've finished your work.
:::{admonition} Note
:class: note
You only need to {hmethod}`Lock()` and
{hmethod}`Unlock()` the {hclass}`BMediaFormats` object when
you're using
{cpp:func}`~BMediaFormats::RewindFormats` and
{cpp:func}`~BMediaFormats::GetNextFormat`.
:::
::::

::::{abi-group}

:::{cpp:function} status_t BMediaFormats::MakeFormatFor(const media_format_description* descriptions, int32 descCount, media_format* ioFormat, uint32 flags = 0, void* _reserved = 0)
:::
Given the media format descriptions in the {hparam}`descriptions` array, the number
of descriptions in the list, {hparam}`descCount`, and the
{cpp:func}`~media::format`
{hparam}`ioFormat`,
registers your format description and supported
{cpp:func}`~media::format`
with the Media Kit, and returns a
{cpp:func}`~media::format`
you can use from then on.
This function is called to let the Media Server assign you an encoding
value for your
{cpp:func}`~media::format`.
If you're implementing a codec
add-on or a file parser, you should call this function to let the Media
Kit know what you handle.
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
	- {cpp:enum}`B_BAD_VALUE`
	- The {hparam}`descriptions` pointer is {cpp:enum}`NULL`, the {hparam}`descCount` is less than 1, or {hparam}`ioFormat` is {cpp:enum}`NULL`.
-
	- {cpp:enum}`B_ERROR`
	- Some other unfortunate incident occurred.
:::
::::

::::{abi-group}

:::{cpp:function} status_t BMediaFormats::RewindFormats()
:::
Resets format scanning to the first supported format; this causes
{cpp:func}`~BMediaFormats::GetNextFormat`
to start at the beginning of the list.
:::{list-table}
---
header-rows: 1
---
-
	- Return Code
	- Description
-
	- {cpp:enum}`B_OK`
	- The object is ready to use.
-
	- Other errors.
	- Unable to communicate with the Media Server.
:::
::::

## Constants
::::{abi-group}

Declared in: media/MediaFormats.h
:::{list-table}
---
header-rows: 1
---
-
	- Constant
	- Description
-
	- {cpp:enum}`B_EXCLUSIVE`
	- Fail if this format has already been registered.
-
	- {cpp:enum}`B_NO_MERGE`
	- Don't renumber any formats if there are multiple clashing previous registrations, but fail instead.
-
	- {cpp:enum}`B_SET_DEFAULT`
	- Set the first format to be the default for the format family when registering more than one in the same family. Use only in encoder add-ons.
:::
These constants provide options for how to go about adding new formats.
::::

## Defined Types
::::{abi-group}


Declared in: media/MediaFormats.h
:::{code}
typedef struct {
   uint32 codec;
} media_aiff_description;
:::
Describes the format of media data as an AIFF codec ID.
::::

::::{abi-group}


Declared in: media/MediaFormats.h
:::{code}
typedef struct {
   GUID guid;
} media_asf_description;
:::
Describes the format of media data as a 128-bit ASF GUID.
::::

::::{abi-group}


Declared in: media/MediaFormats.h
:::{code}
typedef struct {
   uint32 codec;
} media_avi_description;
:::
Describes the format of media data as an AVI codec ID.
::::

::::{abi-group}


Declared in: media/MediaFormats.h
:::{code}
typedef struct {
   uint32 id;
} media_avr_description;
:::
Describes the format of media data as an AVR codec ID.
::::

::::{abi-group}


Declared in: media/MediaFormats.h
:::{code}
typedef struct {
   int32 format;
} media_beos_description;
:::
Describes the format of media data in a way the BeOS Media Kit
understands and appreciates. The format field has no predetermined
meaning; it's a magic number that only the Media Kit understands.
::::

::::{abi-group}


Declared in: media/MediaFormats.h
:::{code}
struct encoder_info {
   char pretty_name[96];
   char short_name[32];
   int32 id;
   int32 sub_id;
   int32 pad[63];
};
:::
Provides information about an encoder. The pretty_name is a complete
human-readable name (such as "SuperSqueeze by Applied Interdynamic
Systems, Inc."), and the short_name is a short-form version of the
encoder's name (such as "SuperSqueeze").
The id is an opaque ID number that gets passed to
{cpp:func}`BMediaFile::CreateTrack`
so the track can identify the encoder.
The padding is reserved space for future expansion of the structure.
::::

::::{abi-group}


Declared in: media/MediaFormats.h
:::{code}
struct media_file_format_info {
   char mimetype[64];
   char pretty_name[64];
   char short_name[32];
   char file_extension[8];
   media_format_family family;
   int64 capabilities;
   int32 id;
   int32 pad[64];
};
:::
Describes a media file format. This is used when using
{cpp:class}`BMediaFile`
objects to determine the type of media file being used.
:::{list-table}
---
header-rows: 1
---
-
	- Field
	- Description
-
	- mimetype
	- Is the file format's MIME type string.
-
	- pretty_name
	- Is a human-readable file format name, such as "QuickTime file".
-
	- short_name
	- Is a human-readable short name, such as "QuickTime".
-
	- file_extension
	- Indicates the dot-extension that untyped files of this format might have, such as ".mov".
-
	- family
	- Indicates the BeOS file format family of the format, such as {cpp:enum}`B_MEDIA_QUICKTIME_FAMILY`.
-
	- capabilities
	- Contains flags indicating what features the format supports.
-
	- id
	- Is a unique ID number for the format.
-
	- pad
	- Pads out the structure, and is reserved.
:::
::::

::::{abi-group}


Declared in: media/MediaFormats.h
:::{code}
typedef struct _media_format_description {
#if defined(__cplusplus)
   _media_format_description();
   ~_media_format_description();
   _media_format_description(const _media_format_description& other);
   _media_format_description& operator=(const _media_format_description& other);
#endif
   media_format_family family;
   uint32 _reserved_[3];
   union {
      media_beos_description beos;
      media_quicktime_description quicktime;
      media_avi_description avi;
      media_asf_description asf;
      media_mpeg_description mpeg;
      media_wav_description wav;
      media_aiff_description aiff;
      media_misc_description misc;
      media_avr_description avr;
      uint32 _reserved_[12];
   } u;
} media_format_description;
:::
Describes a media format. The family indicates which media family in the
union the description uses to identify the format.
::::

::::{abi-group}


Declared in: media/MediaFormats.h
:::{code}
typedef struct {
   uint32 file_format;
   uint32 codec;
} media_misc_description;
:::
Describes the format of a miscellaneous media file.
::::

::::{abi-group}


Declared in: media/MediaFormats.h
:::{code}
typedef struct {
   uint32 id;
} media_mpeg_description;
:::
Describes the format of media data as an MPEG format ID; this can be any
of the following values:
:::{list-table}
---
header-rows: 1
---
-
	- Constant
	- Description
-
	- {cpp:enum}`B_MPEG_ANY`
	- An MPEG format not listed among these choices.
-
	- {cpp:enum}`B_MPEG_1_AUDIO_LAYER_1`
	- MPEG 1 Layer 1 audio format.
-
	- {cpp:enum}`B_MPEG_1_AUDIO_LAYER_2`
	- MPEG 1 Layer 2 audio format.
-
	- {cpp:enum}`B_MPEG_1_AUDIO_LAYER_3`
	- MPEG 1 Layer 3 audio format (commonly known as "MP3").
-
	- {cpp:enum}`B_MPEG_1_VIDEO`
	- An MPEG 1 viedo stream.
:::
::::

::::{abi-group}


Declared in: media/MediaFormats.h
:::{code}
typedef struct {
   uint32 file_format;
   uint32 codec;
} media_misc_description;
:::
Describes the format of media data as a file format/codec pair.
::::

::::{abi-group}


Declared in: media/MediaFormats.h
:::{code}
typedef struct {
   uint32 codec;
} media_wav_description;
:::
Describes the format of media data as a WAV codec ID.
::::

## Global C Functions
::::{abi-group}


:::{cpp:function} bool BMediaFormats::does_file_accept_format(const media_file_format* mfi, const media_format* format)
:::
Returns {cpp:enum}`true` if the given
{cpp:func}`~media::file`
can contain data in the specified
{cpp:func}`~media::format`.
Otherwise, {cpp:enum}`false` is returned.
::::

::::{abi-group}


:::{cpp:function} status_t BMediaFormats::get_next_encoder(int32* cookie, media_file_format* mfi, media_format* outputFormat, media_codec_info* codecInfo)
:::
:::{cpp:function} status_t BMediaFormats::get_next_encoder(int32* cookie, media_file_format* mfi, media_format* inputFormat, media_format* outputFormat, media_codec_info* codecInfo, media_format* acceptedInputFormat, media_format* acceptedOutputFormat)
:::
:::{cpp:function} status_t BMediaFormats::get_next_encoder(int32* cookie, media_codec_info* codecInfo)
:::
Given a
{cpp:func}`~media::file`,
{hparam}`mfi`, describing the format of a media file, a
{cpp:func}`~media::format`,
{hparam}`outputFormat`, describing the desired output format, and
optionally a
{cpp:func}`~media::format`,
{hparam}`inputFormat` describing the desired input
format, returns in {hparam}`codecInfo` information about the next encoder capable
of handling the format.
You should set the int32 pointed to by
{hparam}`cookie` to 0 initially, and pass
the same pointer each time you call
get_next_encoder(),
to scan through
all possible encoders. When there are no more encoders left to check,
{cpp:enum}`B_BAD_INDEX` is returned.
If you use the second form of this function, on return the
{hparam}`acceptedInputFormat` and
{hparam}`acceptedOutputFormat`
{cpp:func}`~media::format`,
structures will
be filled out to indicate the formats that the codec will accept. This
form of the function supports wildcards, while the first does not.
The third form of the function is less specific, and can be used to get a
complete list of codecs. This can be handy if you're constructing a user
interface to allow the user to select the codec they'd like to use, to
get a full list of all the possible formats they can create.
:::{list-table}
---
header-rows: 1
---
-
	- Return Code
	- Description
-
	- {cpp:enum}`B_OK`
	- An encoder was found and returned.
-
	- {cpp:enum}`B_BAD_INDEX`
	- The cookie was invalid, or no more encoders found.
:::
See also:
{cpp:func}`~get::next`
in the global C functions section.
::::
