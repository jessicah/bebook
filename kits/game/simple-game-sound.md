:::{cpp:class} BSimpleGameSound
:::

# BSimpleGameSound

## Constructor and Destructor

::::{abi-group}
:::{cpp:function} BSimpleGameSound::BSimpleGameSound(const entry_ref* inFile, BGameSoundDevice* device = NULL)
:::

:::{cpp:function} BSimpleGameSound::BSimpleGameSound(const char* inFile, BGameSoundDevice* device = NULL)
:::

:::{cpp:function} BSimpleGameSound::BSimpleGameSound(const void* inData, size_t inFrameCount, const gs_audio_format* format, BGameSoundDevice* device = NULL)
:::

:::{cpp:function} BSimpleGameSound::BSimpleGameSound(const BSimpleGameSound& other)
:::

Prepares the object to play the specified sound. The first form of the
constructor preloads the entire sound specified by {hparam}`inFile` into
memory, while the second accepts a {hparam}`inFile` as a pathname string.

The third form takes {hparam}`inData` as a pointer to sound data already
in memory; this sound data is copied into a buffer owned by the
{hclass}`BSimpleGameSound` object; once the constructor returns, you can
delete the original data if you wish. The data is copied since some sound
cards have an onboard sound buffer, and the API allows support for these
devices (whether or not drivers exist that do this is another story).

{hparam}`inFrameCount` indicates how many frames of audio are in that
buffer, and {hparam}`format` indicates the format of the audio data. The
size of the {ref}`Media Kit` buffers used by the object is determined by
the {htype}`gs_audio_format` structure's {hparam}`buffer_size` field. If
the value this field is zero, the {ref}`Game Kit` determines an appropriate
buffer size for you.

In both cases, {hparam}`device` specifies the sound device that should be
used for playing the sound; {cpp:expr}`NULL` uses the default sound player.

:::{admonition} Note
:class: note
Currently, {hparam}`device` must always be {cpp:expr}`NULL`.
:::

The final form of the constructor duplicates another
{hclass}`BSimpleGameSound` object.

After instantiating the {hclass}`BSimpleGameSound` object, you should call
{cpp:func}`InitCheck() <BSimpleGameSound::InitCheck>` to determine whether
or not the sound was successfully created.
::::

::::{abi-group}
:::{cpp:function} virtual BSimpleGameSound::~BSimpleGameSound()
:::

A typical destructor.
::::

## Member Functions

::::{abi-group}
:::{cpp:function} status_t BSimpleGameSound::InitCheck() const
:::

Returns a {htype}`status_t` indicating whether or not the object was
successfully instantiated.

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
	- The sound was successfully initialized.
-
	- {cpp:enumerator}`B_ERROR`.
	- Unable to create a sound player.
-
	- {cpp:enumerator}`B_NO_MEMORY`.
	- Can't get enough memory to preload the sound.
-
	- Other errors.
	- The sound player may return errors.

:::
::::

::::{abi-group}
:::{cpp:function} status_t BSimpleGameSound::SetIsLooping(bool looping)
:::

:::{cpp:function} void BSimpleGameSound::IsLooping() const
:::

{hmethod}`SetIsLooping()` turns looping of the sound on if
{hparam}`looping` is {cpp:expr}`true`, or off if {hparam}`looping` is
{cpp:expr}`false`.

{hmethod}`IsLooping()` returns a flag indicating whether or not looping is
currently enabled.

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
	- Looping was turned on or off without error.
-
	- {cpp:enumerator}`B_ERROR`.
	- The player wasn't initialized properly.

:::
::::
