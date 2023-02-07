# BStreamingGameSound
## Constructor and Destructor
::::{abi-group}

:::{cpp:function} BStreamingGameSound::BStreamingGameSound(size_t inBufferFrameCount, const gs_audio_format* format, size_t inBufferCount = 2, BGameSoundDevice* device = NULL)
:::
:::{cpp:function} protected BStreamingGameSound::BStreamingGameSound(BGameSoundDevice device)
:::
Prepares the object to play streamed audio.
{hparam}`inBufferFrameCount` specifies the number of frames
each audio buffer should be able to hold. {hparam}`format`
indicates the audio format that will be streamed.
{hparam}`inBufferCount` specifies the number of buffers to
use, and, as always, {hparam}`device` is the sound device to
use for playback.
By default, two audio buffers are used.
:::{admonition} Note
:class: note
Currently, {hparam}`device` must always be
{cpp:enum}`NULL` to indicate that the default
playback device should be used.
:::
::::

::::{abi-group}

:::{cpp:function} virtual BStreamingGameSound::~BStreamingGameSound()
:::
Stops playing the sound.
::::

## Member Functions
::::{abi-group}

:::{cpp:function} virtual void BStreamingGameSound::FillBuffer(void* inBuffer, size_t byteCount)
:::

Fills the buffer specified by {hparam}`inBuffer` with {hparam}`byteCount` bytes of audio data.

In the {hclass}`BStreamingGameSound` implemenation, this function calls the stream
hook, if one exists.

See also: {cpp:func}`~BStreamingGameSound::SetStreamHook`

::::

::::{abi-group}

:::{cpp:function} status_t BStreamingGameSound::InitCheck() const
:::

Returns a status_t indicating whether or not the object was successfully
instantiated.

:::{list-table}
---
header-rows: 1
---
-
	- Return Code
	- Description
-
	- {cpp:enum}`B_OK`.
	- The sound was successfully initialized.
-
	- {cpp:enum}`B_ERROR`.
	- Unable to create a sound player.
-
	- Other errors.
	- The sound player may return errors.
:::

See also: the {hclass}`BStreamingGameSound`
{cpp:func}`~BStreamingGameSound::Constructor`

::::

::::{abi-group}

:::{cpp:function} bool BStreamingGameSound::Lock()
:::
:::{cpp:function} void BStreamingGameSound::Unlock()
:::

{hmethod}`Lock()` locks the {hclass}`BStreamingGameSound` to prevent unpleasant collisions in
the land of multithreadedness; it returns {cpp:enum}`true` if it was able to lock the
object, otherwise {cpp:enum}`false` is returned. {hmethod}`Unlock()` releases the lock.

::::

::::{abi-group}

:::{cpp:function} virtual status_t BStreamingGameSound::SetAttributes(gs_attribute* inAttributes, size_t inAttributeCount)
:::

{hmethod}`SetAttributes()` is implemented to disallow the {cpp:enum}`B_GS_LOOPING` attribute,
since streamed sounds can't loop.

See also:
{cpp:func}`BGameSound::SetAttributes`

::::

::::{abi-group}

:::{cpp:function} virtual status_t BStreamingGameSound::SetParameters(size_t inBufferFrameCount, const gs_audio_format* fmt, size_t inBufferCount)
:::

Changes the {hclass}`BStreamingGameSound` object's parameters. This lets you change
the buffer size, audio format, and number of buffers after the object has
been instantiated.

:::{list-table}
---
header-rows: 1
---
-
	- Return Code
	- Description
-
	- {cpp:enum}`B_OK`.
	- No error.
-
	- {cpp:enum}`B_ERROR`.
	- Couldn't change the parameters.
:::
::::

::::{abi-group}

:::{cpp:function} virtual status_t BStreamingGameSound::SetStreamHook(void (*hook)(void * cookie, void* inBuffer, size_t byteCount, BStreamingGameSound* object), void* cookie)
:::
Specfies the hook function to be called to fill buffers with audio
data.

The inputs to the hook function are:

:::{list-table}
---
header-rows: 1
---
-
	- Parameter
	- Description
-
	- cookie
	- A user-defined value. Indicates the cookie pointer that will be passed to the hook function.
-
	- inBuffer
	- A pointer to the buffer to be filled with audio data.
-
	- byteCount
	- The size of the buffer in bytes.
-
	- object
	- A pointer to the {hclass}`BStreamingGameSound` object.
:::
And returns...
:::{list-table}
---
header-rows: 1
---
-
	- Return Code
	- Description
-
	- {cpp:enum}`B_OK`.
	- The hook function was set without error.
:::
::::
