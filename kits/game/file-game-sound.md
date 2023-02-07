# BFileGameSound
## Constructor and Destructor
::::{abi-group}

:::{cpp:function} BFileGameSound::BFileGameSound(const entry_ref* inFile, bool looping = true, BGameSoundDevice* device = NULL)
:::
:::{cpp:function} BFileGameSound::BFileGameSound(const char* inFile, bool looping = true, BGameSoundDevice* device = NULL)
:::
Prepares the object to play the specified sound file, which can be
specified either by entry_ref or pathname in the
{hparam}`inFile` argument.
If the {hparam}`looping` flag is {cpp:enum}`true` (which it is by default), the sound
automatically loops back to the beginning and replays when the end of the
sound is reached. This is useful for easily playing background music (for
example).
In both cases, {hparam}`device` specifies the sound device that should be used for
playing the sound; {cpp:enum}`NULL` uses the default sound player.
:::{admonition} Note
:class: note
Currently, {hparam}`device` must always be {cpp:enum}`NULL`.
:::
After instantiating the {hclass}`BFileGameSound` object, you should call
{cpp:func}`~BFileGameSound::InitCheck` to determine whether or not the sound was successfully
created.
::::

::::{abi-group}

:::{cpp:function} virtual BFileGameSound::~BFileGameSound()
:::
A typical destructor.
::::

## Member Functions
::::{abi-group}

:::{cpp:function} status_t BFileGameSound::InitCheck() const
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
	- {cpp:enum}`B_NO_MEMORY`.
	- Can't get enough memory to preload the sound.
-
	- Other errors.
	- The sound player may return errors.
:::
::::

::::{abi-group}

:::{cpp:function} status_t BFileGameSound::Preload()
:::
{hmethod}`Preload()` preloads enough of the sound file into memory that starting
playback of the sound won't cuase a delay while the first chunk of data
is fetched from disk.
:::{list-table}
---
header-rows: 1
---
-
	- Return Code
	- Description
-
	- {cpp:enum}`B_OK`.
	- Preloading was successful.
-
	- Port errors.
	- Unable to communicate with the streaming sound port.
:::
::::

::::{abi-group}

:::{cpp:function} status_t BFileGameSound::SetPaused(bool isPaused, bigtime_t rampTime)
:::
:::{cpp:function} int32 BFileGameSound::IsPaused()
:::
{hmethod}`SetPaused()` pauses if {hparam}`isPaused`
is {cpp:enum}`true`, and unpauses if {hparam}`isPaused` is
{cpp:enum}`false`. If {hparam}`rampTime` is nonzero, the sound ramps up to speed (or down to
stopped) instead of instantly changing state. The number of microseconds
specified by {hparam}`rampTime` indicates how long the change should take to
complete.
{hmethod}`IsPaused()` returns value indicating whether or not the sound is paused,
or if a pause is in process of being initiated (if ramping is underway).
The result is one of these values:
:::{list-table}
---
header-rows: 1
---
-
	- Constant
	- Description
-
	- {cpp:enum}`B_NOT_PAUSED`
	- The sound is playing normally.
-
	- {cpp:enum}`B_PAUSE_IN_PROGRESS`
	- The sound is ramping toward or away from a paused state.
-
	- {cpp:enum}`B_PAUSED`
	- The sound is paused.
:::
Because these constants are members of the {hclass}`BFileGameSound` class, be sure
to refer to them as
`BFileGameSound::B_NOT_PAUSED`
and so forth.
:::{list-table}
---
header-rows: 1
---
-
	- Return Code
	- Description
-
	- {cpp:enum}`B_OK`.
	- The pause occurred without error.
-
	- {cpp:enum}`EALREADY`.
	- The sound is already in the requested state.
:::
::::
