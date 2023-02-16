:::{cpp:class} BSoundPlayer
:::

# BSoundPlayer

## Constructor and Destructor

::::{abi-group}
:::{cpp:function} BSoundPlayer::BTimeSource(const char* name = NULL, void (*PlayBuffer) (void* , void* buffer, size_t size, const media_raw_audio_format& format) = NULL, void (*Notifier) (void* , sound_player_notification what) = NULL, void* cookie = NULL)
:::

:::{cpp:function} BSoundPlayer::BTimeSource(const media_raw_audio_format* format, const char* name = NULL, void (*PlayBuffer) (void* , void* buffer, size_t size, const media_raw_audio_format& format) = NULL, void (*Notifier) (void* , sound_player_notification what) = NULL, void* cookie = NULL)
:::

:::{cpp:function} BSoundPlayer::BTimeSource(const media_node& toNode, const media_multi_audio_format* format = NULL, const char* name = NULL, const media_input* input = NULL, void (*PlayBuffer) (void* , void* buffer, size_t size, const media_raw_audio_format& format) = NULL, void (*Notifier) (void* , sound_player_notification what) = NULL, void* cookie = NULL)
:::

Initializes the {hclass}`BSoundPlayer` object. The {hparam}`name` argument
specifies the name to be assigned to the sound player node (if you specify
{cpp:expr}`NULL`, a generic name will be assigned).

The {hparam}`PlayBuffer` argument specifies a pointer to a member function
that processes data and inserts it into buffers for playback; specify NULL
if you want to use the BSoundPlayer for playing BSounds. The parameters to
the {hparam}`PlayBuffer` function are (in order):

-   Pointer to the cookie.

-   Pointer to the buffer to play.

-   Size of the buffer.

-   Format of the audio data in the buffer.

The {hparam}`Notifier` parameter specifies a pointer to a member function
that receives notifications when events of interest occur, such as playback
starting or stopping. Specify {cpp:expr}`NULL` to use the default
notification handler. There are three possible notifications:

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
	- {cpp:enumerator}`B_STARTED`and{cpp:enumerator}`B_STOPPED`
	- Indicate that the {hclass}`BSoundPlayer` was started or stopped. These
		receive a pointer to the {hclass}`BSoundPlayer` object as an argument.
-
	- {cpp:enumerator}`B_SOUND_DONE`
	- Indicates that a sound has finished playing. In this case, there are two
		arguments: the first is a {htype}`play_id` indicating which sound finished
		playing, and the other is a boolean which is {cpp:expr}`true` if the sound
		played at all, and {cpp:expr}`false` if the sound never played.

:::

:::{admonition} Note
:class: note
If the callback handlers are members of a class, they must be static
members.
:::

The {hparam}`cookie` parameter is a pointer that you can use for your own
purposes; it's most useful if you're using a custom {hparam}`PlayBuffer` or
{hparam}`Notifier`.

The second form of the constructor lets you specify in the
{hparam}`format` argument the format of the audio that the
{hclass}`BSoundPlayer` will perform. Since {hclass}`BSoundPlayer` can only
play raw sound formats, this is specified using the
{ref}`media_raw_audio_format` structure.

The third form of the constructor lets you specify a node through which
the sound should be played, and also uses a {ref}`media_multi_audio_format`
to specify the sound's format, instead of the older
{ref}`media_raw_audio_format`.

You should call {cpp:func}`InitCheck() <BSoundPlayer::InitCheck>` before
using your {hclass}`BSoundPlayer` object; this will let you determine
whether or not the object was successfully constructed. One situation in
which {cpp:func}`InitCheck() <BSoundPlayer::InitCheck>` might indicate an
error is if the user doesn't have a sound card installed.
::::

::::{abi-group}
:::{cpp:function} BSoundPlayer::~BSoundPlayer()
:::

Stops playback, if sound is playing, releases references to any BSound
objects that are in use by the BSoundPlayer, and frees all memory used by
the {hclass}`BSoundPlayer`.
::::

## Member Functions

::::{abi-group}
:::{cpp:function} BufferPlayerFunc BSoundPlayer::BufferPlayer() const
:::

:::{cpp:function} void BSoundPlayer::SetBufferPlayer(void (*PlayBuffer) (void* , void* buffer, size_t size, const media_raw_audio_format& format))
:::

{hmethod}`BufferPlayer()` returns a pointer to the current play buffer
function, or {cpp:expr}`NULL` if the default player is in use.

{hmethod}`SetBufferPlayer()` lets you change the play buffer function.
::::

::::{abi-group}
:::{cpp:function} void* BSoundPlayer::Cookie() const
:::

:::{cpp:function} void BSoundPlayer::SetCookie(void* cookie)
:::

{hmethod}`Cookie()` returns the current cookie assigned to the
{hclass}`BSoundPlayer`.

{hmethod}`SetCookie()` lets you change the cookie assigned to the
{hclass}`BSoundPlayer`.
::::

::::{abi-group}
:::{cpp:function} bigtime_t BSoundPlayer::CurrentTime()
:::

:::{cpp:function} bigtime_t BSoundPlayer::PerformanceTime()
:::

{hmethod}`CurrentTime()` returns the current media time, and
{hmethod}`PerformanceTime()` returns the current performance time of the
sound player node being used by the {hclass}`BSoundPlayer`.

{hmethod}`PerformanceTime()` will return {cpp:enumerator}`B_ERROR` if the
{hclass}`BSoundPlayer` object hasn't been properly initialized.
::::

::::{abi-group}
:::{cpp:function} EventNotifierFunc BSoundPlayer::EventNotifier() const
:::

:::{cpp:function} void BSoundPlayer::SetNotifier(void (*Notifier)(void* , sound_player_notification what, ...)))
:::

{hmethod}`EventNotifier()` returns a pointer to the current event
notification handler function, or {cpp:expr}`NULL` if the default player is
in use.

{hmethod}`SetNotifier()` lets you change the event notification handler
function.
::::

::::{abi-group}
:::{cpp:function} media_raw_audio_format BSoundPlayer::Format() const
:::

Returns the {hclass}`BSoundPlayer`'s format. Since the sound is always a
raw sound format, the {ref}`media_raw_audio_format` structure is used.
::::

::::{abi-group}
:::{cpp:function} EventNotifierFunc BSoundPlayer::EventNotifier(media_node* outNode, int32* outParameter, float* outMinDB, float* outMaxDB) const
:::

Returns information about the {hclass}`BSoundPlayer`'s volume control.
Pass pointers to variables to be filled ({cpp:expr}`NULL` is not
permitted), and on return these values will be set to describe the player
as follows:

:::{list-table}
---
header-rows: 1
align: left
widths: auto
---
-
	- Parameter

	- Description

-
	- outNode
	- Is the node to which the {hclass}`BSoundPlayer`'s audio output will be
		directed.
-
	- outParameter
	- Is the parameter ID for the volume control.
-
	- outMinDB
	- Is the minimum volume in decibels.
-
	- outMaxDB
	- Is the maximum volume in decibels.

:::
::::

::::{abi-group}
:::{cpp:function} bool BSoundPlayer::HasData()
:::

:::{cpp:function} void BSoundPlayer::SetHasData(bool hasData)
:::

{hmethod}`HasData()` returns {cpp:expr}`true` if there's sound queued for
playback, or {cpp:expr}`false` otherwise.

{hmethod}`SetHasData()` specifies whether or not there's sound scheduled
for playback.

The purpose of these functions is to optimize the {hclass}`BSoundPlayer`;
if there's no data queued for playback, the sound player node is told this,
which lets it optimize its performance. If you're using a buffer player
function, you must use {hmethod}`SetHasData()` to indicate that there's
data to play:

:::{code} cpp
SetHasData(true);
:::
::::

::::{abi-group}
:::{cpp:function} status_t BSoundPlayer::InitCheck()
:::

Returns the status code resulting from constructing the
{hclass}`BSoundPlayer` object. You should call this after constructing the
object; if the returned value is anything other than
{cpp:enumerator}`B_OK`, you shouldn't use the object.
::::

::::{abi-group}
:::{cpp:function} bigtime_t BSoundPlayer::Latency()
:::

Returns the {hclass}`BSoundPlayer`'s latency.
::::

::::{abi-group}
:::{cpp:function} void BSoundPlayer::SetCallbacks(void (*PlayBuffer) (void* , void* buffer, size_t size, const media_raw_audio_format& format) = NULL, void (*Notifier) (void* , sound_player_notification what) = NULL, void* cookie = NULL)
:::

Sets the play buffer handler function, the event notification handler
function, and the cookie all in one atomic operation.
::::

::::{abi-group}
:::{cpp:function} void BSoundPlayer::SetInitError(status_t inError)
:::

Sets the status code that will be returned by {cpp:func}`InitCheck()
<BSoundPlayer::InitCheck>`.
::::

::::{abi-group}
:::{cpp:function} status_t BSoundPlayer::SetSoundVolume(play_id sound, float volume)
:::

Sets the volume (from 0.0 to 1.0) of the specified sound.
::::

::::{abi-group}
:::{cpp:function} status_t BSoundPlayer::Start()
:::

:::{cpp:function} void BSoundPlayer::Stop(bool block = true, bool flush = true)
:::

{hmethod}`Start()` activates the {hclass}`BSoundPlayer` by starting the
time source and the sound player node. The {cpp:enumerator}`B_STARTED`
notification is sent to the {hclass}`BSoundPlayer`'s notification handler.

{hmethod}`Stop()` deactivates the {hclass}`BSoundPlayer` by stopping the
player node (if {hparam}`block` is {cpp:expr}`true`, the {hmethod}`Stop()`
function blocks until the node is stopped). If {hparam}`flush` is
{cpp:expr}`true`, the queued sounds are all deleted from memory.

While the {hclass}`BSoundPlayer` is running, the play buffer function (if
you've specified one) will be called for each buffer that passes through
the {hclass}`BSoundPlayer`'s playback node. This hook function can be used
to implement code that performs more advanced playback of sound, such as
sound that's generated on-the-fly, or is filtered before playback.

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
	- The sound playback was started.
-
	- Other errors.
	- As returned by the {hclass}`BMediaRoster`'s {cpp:func}`StartNode()
		<BMediaRoster::StartNode>` function.

:::
::::

::::{abi-group}
:::{cpp:function} play_id BSoundPlayer::StartPlaying(BSound* sound, bigtime_t atTime = 0)
:::

:::{cpp:function} play_id BSoundPlayer::StartPlaying(BSound* sound, bigtime_t atTime, float withVolume)
:::

:::{cpp:function} status_t BSoundPlayer::StopPlaying(play_id id)
:::

:::{cpp:function} status_t BSoundPlayer::WaitForSound(play_id id)
:::

:::{cpp:function} bool BSoundPlayer::IsPlaying(play_id id)
:::

{hmethod}`StartPlaying()` schedules the specified {hclass}`BSound` to
begin playback at the performance time specified by {hparam}`atTime`; if
{hparam}`atTime` is 0, the sound begins playing immediately (or as soon as
{hmethod}`Start()` is called, if the {hclass}`BSoundPlayer` hasn't been
started yet). The {htype}`play_id` returned by this function is used to
identify the sound later. If it's negative, an error occurred (see the list
below for possible values). The second form of {hmethod}`StartPlaying()`
lets you specify a volume at which the sound should play.

{hmethod}`StopPlaying()` stops playing the sound specified by the given
{hparam}`id`.

{hmethod}`WaitForSound()` waits until the specified sound stops playing.

{hmethod}`IsPlaying()` returns {cpp:expr}`true` if the specified sound is
playing; otherwise, it returns {cpp:expr}`false`.

:::{list-table}
---
header-rows: 0
align: left
widths: auto
---
-
	- {cpp:enumerator}`B_OK`
	- No error.
-
	- {cpp:enumerator}`B_MEDIA_BAD_FORMAT`
	- The audio isn't in a supported format ({hmethod}`StartPlaying()`).
-
	- {cpp:enumerator}`B_BAD_VALUE`
	- The specified id doesn't exist ({hmethod}`WaitForSound()` and
		{hmethod}`IsPlaying()`).

:::
::::

::::{abi-group}
:::{cpp:function} float BSoundPlayer::Volume()
:::

:::{cpp:function} void BSoundPlayer::SetVolume(float newVolume)
:::

{hmethod}`Volume()` returns the current playback volume.

{hmethod}`SetVolume()` changes the playback volume.

This volume is the overall volume of all the sounds being played by the
{hclass}`BSoundPlayer`.To control the volumes of individual sounds, use the
SetSoundVolume() function.

:::{admonition} Note
:class: note
The volume can range from 0.0 to 1.0, where 0.0 is silent and 1.0 is
maximum loudness.
:::

If you'd rather handle the volume using decibels instead of the percentage
range, you can use the {cpp:func}`VolumeDB() <BSoundPlayer::VolumeDB>` and
{cpp:func}`SetVolumeDB() <BSoundPlayer::SetVolumeDB>` functions.
::::

::::{abi-group}
:::{cpp:function} float BSoundPlayer::VolumeDB()
:::

:::{cpp:function} void BSoundPlayer::SetVolumeDB(float newVolume)
:::

{hmethod}`VolumeDB()` returns the current playback volume in decibels.

{hmethod}`SetVolumeDB()` sets the playback volume, in decibels.

This volume is the overall volume of all the sounds being played by the
{hclass}`BSoundPlayer`. To control the volumes of individual sounds, use
the {cpp:func}`SetSoundVolume() <BSoundPlayer::SetSoundVolume>` function.

:::{admonition} Note
:class: note
The possible range of volumes can be obtained by calling
{cpp:func}`GetVolumeInfo() <BSoundPlayer::GetVolumeInfo>`.
:::

If you'd rather handle the volume using a percentage range instead of
decibels, you can use the {cpp:func}`Volume() <BSoundPlayer::Volume>` and
{cpp:func}`SetVolume() <BSoundPlayer::SetVolume>` functions.
::::

## Constants

### sound_player_notification

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
	- {cpp:enumerator}`B_STARTED`
	- The {hclass}`BSoundPlayer` has been started via the Start() function.
-
	- {cpp:enumerator}`B_STOPPED`
	- The {hclass}`BSoundPlayer`'s Stop() function has been called.
-
	- {cpp:enumerator}`B_SOUND_DONE`
	- A sound has finished playing.

:::

These constants are passed to event notification handler functions to
indicate what sort of interesting event has occurred.

## Defined Types

### play_id

:::{code} c
typedef int32 play_id;
:::

Identifies a particular sound that's being played by the
{hclass}`BSoundPlayer`; {cpp:func}`StartPlaying()
<BSoundPlayer::StartPlaying>` returns values of this type.
