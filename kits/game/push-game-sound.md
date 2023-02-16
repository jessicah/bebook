:::{cpp:class} BPushGameSound
:::

# BPushGameSound

## Constructor and Destructor

::::{abi-group}
:::{cpp:function} BPushGameSound::BPushGameSound(size_t inBufferFrameCount, const gs_audio_format* format, size_t inBufferCount = 2, BGameSoundDevice* device = NULL)
:::

Prepares the object to play audio pushed by your application.
{hparam}`inBufferFrameCount` specifies the number of frames each audio
buffer should be able to hold. {hparam}`format` indicates the audio format
that will be streamed. {hparam}`inBufferCount` specifies the number of
buffers to use, and, as always, {hparam}`device` is the sound device to use
for playback.

:::{admonition} Note
:class: note
Currently, {hparam}`device` must always be {cpp:expr}`NULL` to indicate
that the default playback device should be used.
:::

By default, two audio buffers are used.

Be sure to call {cpp:func}`InitCheck() <BPushGameSound::InitCheck>` before
using the {hclass}`BPushGameSound` object.
::::

::::{abi-group}
:::{cpp:function} virtual BPushGameSound::~BPushGameSound()
:::

Deletes the semaphore used to lock the object.
::::

## Member Functions

::::{abi-group}
:::{cpp:function} status_t BPushGameSound::InitCheck() const
:::

Returns a {htype}`status_t` indicating whether or not the object was
successfully initialized. A return value of {cpp:enumerator}`B_OK` means
everything's fine; any other value means an error occurred in the
constructor.
::::

::::{abi-group}
:::{cpp:function} virtual lock_status BPushGameSound::LockForCyclic(void** outBasePtr, size_t* outSize)
:::

:::{cpp:function} virtual status_t BPushGameSound::UnlockCyclic()
:::

:::{cpp:function} virtual size_t BPushGameSound::CurrentPosition()
:::

{hmethod}`LockForCyclic()` gives you access to the entire sound buffer;
audio playback continues while you have access. Use
{hmethod}`CurrentPosition()` to determine where the playback is currently
located in the buffer area, and be sure to stay well ahead of it. See the
{ref}`overview` for a more in-depth discussion. If
{cpp:enumerator}`lock_failed` is returned, you can't access the audio area,
but if {cpp:enumerator}`lock_ok` is returned, you can start pushing audio.

On return, {hparam}`outBasePtr` points to the first byte of the audio
buffer area, and {hparam}`outSize` indicates the total size of the audio
buffer area.

{hmethod}`UnlockCyclic()` releases the audio area.

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
	- {cpp:enumerator}`B_OK`.
	- {hmethod}`UnlockCyclic()` succeeded.

:::
::::

::::{abi-group}
:::{cpp:function} virtual lock_status BPushGameSound::LockNextPage(void** outPagePtr, size_t* outPageSize)
:::

:::{cpp:function} virtual status_t BPushGameSound::UnlockPage(void* inPagePtr)
:::

{hmethod}`LockNextPage()` requests access to the next page of the sound
buffer. The {ref}`lock_status` return value is {cpp:enumerator}`lock_ok` or
{cpp:enumerator}`lock_ok_frames_dropped` if a valid page has been returned.
If either of these values is returned, you can then write up to
{hparam}`outPageSize` bytes of audio data into the audio page returned in
{hparam}`outPagePtr`.

If {cpp:enumerator}`lock_failed` is returned, you can't access an audio
page.

{hmethod}`UnlockPage()` releases the audio page pointed to by
{hparam}`inPagePtr` and returns {cpp:enumerator}`B_OK` if it succeeds in
unlocking the page.
::::

## Constants

### lock_status

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
	- {cpp:enumerator}`lock_failed`
	- Couldn't get the lock; it's not time to update yet.
-
	- {cpp:enumerator}`lock_ok`
	- Locked; you can update.
-
	- {cpp:enumerator}`lock_ok_frames_dropped`
	- Locked; you can update, but you may have missed some buffers.

:::

These values are returned by the locking functions in the
{hclass}`BPushGameSound` class ( {cpp:func}`LockNextPage()
<BPushGameSound::LockNextPage>` and {cpp:func}`LockForCyclic()
<BPushGameSound::LockForCyclic>`). If either function returns
{cpp:enumerator}`lock_failed`, there isn't a buffer to be filled; your code
is pushing buffers too fast.

If {cpp:enumerator}`lock_ok` is returned, the next buffer is ready. The
{cpp:enumerator}`lock_ok_frames_dropped` result is received if a buffer is
available but some buffers have been lost; this can happen if you're not
pushing fast enough.
