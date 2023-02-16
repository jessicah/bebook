:::{cpp:class} BParameter
:::

# BParameter

## Constructor and Destructor

{hclass}`BParameter` objects may only be created by using the appropriate
functions in the {cpp:class}`BParameterGroup` class.

## Member Functions

::::{abi-group}
:::{cpp:function} status_t BParameter::AddInput(BParameter* input)
:::

:::{cpp:function} status_t BParameter::AddOutput(BParameter* output)
:::

{hmethod}`AddInput()` adds the {hclass}`BParameter` specified by
{hparam}`input` to the set of {hclass}`BParameter`s that transmit data into
the {hclass}`BParameter`. The specified input parameter's
{hmethod}`AddOutput()` function is called to let it know that it's sending
data to this parameter.

{hmethod}`AddOutput()` adds the {hclass}`BParameter` specified by
{hparam}`output` to the set of {hclass}`BParameter`s to which the
{hclass}`BParameter` outputs data. The specified {hparam}`output`
parameter's {hmethod}`AddInput()` function is called to let it know that
it's receiving data from this parameter.

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
	- The item was successfully added to the list.
-
	- {cpp:enumerator}`B_ERROR`
	- The item couldn't be added to the list.

:::
::::

::::{abi-group}
:::{cpp:function} int32 BParameter::CountChannels()
:::

:::{cpp:function} void BParameter::SetChannelCount(int32 numChannels)
:::

Some {hclass}`BParameter`s have more than one channel of the same type.
For example, a stereo volume parameter with independent left and right gain
would have two channels, while a single parameter value that affects both
the left and right by the same amount would have only one channel.
{hmethod}`CountChannels()` returns the number of channels manipulated by
the {hclass}`BParameter`.

The default is one channel; if your node provides more channels, call
{hmethod}`SetChannelCount()` after creating the {hclass}`BParameter`.
{hmethod}`SetChannelCount()` specifies the number of channels the parameter
manipulates.
::::

::::{abi-group}
:::{cpp:function} int32 BParameter::CountInputs()
:::

:::{cpp:function} int32 BParameter::CountOutputs()
:::

These two functions return the number of inputs or outputs currently
connected to the {hclass}`BParameter`. The number of inputs or outputs may
be different from the number of channels, since an input or output might be
comprised of multiple channels (a single stereo sound input or output might
consist of a left channel and a right channel, for example).
::::

::::{abi-group}
:::{cpp:function} status_t BParameter::GetValue(void* buffer, size_t* ioSize, bigtime_t* lastChange)
:::

:::{cpp:function} status_t BParameter::SetValue(const void* buffer, size_t size, bigtime_t changeWhen)
:::

{hmethod}`GetValue()` returns the current value of the
{hclass}`BParameter`. On entry, {hparam}`buffer` points to {hparam}`ioSize`
bytes of memory, indicating where the current value of the
{hclass}`BParameter` should be stored. On return, {hparam}`ioSize`
indicates the actual number of bytes returned in the buffer, and
{hparam}`lastChange` indicates the time at which the {hclass}`BParameter`'s
value last changed.

{hmethod}`SetValue()` changes the value of the {hclass}`BParameter`. The
new value, which is {hparam}`size` bytes long, is obtained from the
specified {hparam}`buffer`. The change occurs at the performance time
specified by {hparam}`changeWhen`.

In either case, if the parameter is a multichannel parameter, the buffer
should be large enough to contain the values for all the channels, and
{hparam}`ioSize` or {hparam}`size` should indicate the total size of the
buffer.

These calls simply dispatch to the
{cpp:func}`BControllable::GetParameterValue` and
{cpp:func}`BControllable::SetParameterValue` functions.

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
	- No errors.
-
	- {cpp:enumerator}`B_NO_MEMORY`
	- The buffer is too small ({hmethod}`GetValue()`).
-
	- {cpp:enumerator}`B_BAD_VALUE`
	- The parameter doesn't have a value ({hmethod}`GetValue()`).
-
	- Port errors.
	- See {ref}`Ports` in the {ref}`The Kernel Kit`

:::
::::

::::{abi-group}
:::{cpp:function} BParameterGroup* BParameter::Group() const
:::

Returns the {cpp:class}`BParameterGroup` that most directly contains the
{hclass}`BParameter`.
::::

::::{abi-group}
:::{cpp:function} int32 BParameter::ID() const
:::

Returns the {hclass}`BParameter`'s ID number. This ID is used by the node
to route value change requests to the right place. This value should be
unique within the {cpp:class}`BParameterWeb` containing the
{hclass}`BParameter`.
::::

::::{abi-group}
:::{cpp:function} BParameter* BParameter::InputAt(int32 index)
:::

:::{cpp:function} BParameter* BParameter::OutputAt(int32 index)
:::

{hmethod}`InputAt()` returns the {hclass}`BParameter` that feeds data into
the input number specified by {hparam}`index`, which can range from zero to
{cpp:func}`CountInputs() <BParameter::CountInputs>`-1.

{hmethod}`OutputAt()` returns the {hclass}`BParameter` that receives data
from the output number specified by {hparam}`index`, which can range from
zero to {cpp:func}`CountOutputs() <BParameter::CountInputs>`-1.

Both functions return {cpp:expr}`NULL` if an invalid {hparam}`index` is
specified.
::::

::::{abi-group}
:::{cpp:function} const char* BParameter::Kind() const
:::

Returns the {hclass}`BParameter`'s kind. The kind isn't necessarily
user-readable, but it can be used to figure out what kind of
{cpp:class}`BControl` to create to visually represent the configuration
option provided by the {hclass}`BParameter`.

See the {cpp:func}`BParameterGroup::MakeNullParameter`,
{cpp:func}`BParameterGroup::MakeDiscreteParameter`, and
{cpp:func}`BParameterGroup::MakeContinuousParameter` functions for more
detailed information about the available kinds.
::::

::::{abi-group}
:::{cpp:function} media_type BParameter::MediaType()
:::

:::{cpp:function} void BParameter::SetMediaType(media_type type)
:::

{hmethod}`MediaType()` returns the type of media data that flows through
the {hclass}`BParameter`.

{hmethod}`SetMediaType()` changes the recorded type of media data. The
default, if it hasn't been changed, is {cpp:enumerator}`B_MEDIA_NO_TYPE`.

The {ref}`media_type` of a {hclass}`BParameter` is used to inform
interested parties as to the format of the data; it's an informational
setting, and doesn't alter the data flowing through the
{hclass}`BParameter` in any way.
::::

::::{abi-group}
:::{cpp:function} const char* BParameter::Name() const
:::

Returns the {hclass}`BParameter`'s name, which is suitable for display to
the user (for example, it can be used as the label in a user interface
object).
::::

::::{abi-group}
:::{cpp:function} media_parameter_type BParameter::Type() const
:::

Returns the kind of parameter the object represents.

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
	- {cpp:enumerator}`B_NULL_PARAMETER`
	- The {hclass}`BParameter` is a {cpp:class}`BNullParameter`.
-
	- {cpp:enumerator}`B_DISCRETE_PARAMETER`
	- The {hclass}`BParameter` is a {cpp:class}`BDiscreteParameter`.
-
	- {cpp:enumerator}`B_CONTINUOUS_PARAMETER`
	- The {hclass}`BParameter` is a {cpp:class}`BContinuousParameter`.

:::
::::

::::{abi-group}
:::{cpp:function} const char* BParameter::Unit() const
:::

Returns the unit of measurement used by the {hclass}`BParameter`. This
might be, for example, "dB," "kHz," or "fps." It should be human-readable,
as it may be displayed in a user interface.
::::

::::{abi-group}
:::{cpp:function} virtual type_code BParameter::ValueType() = 0
:::

Returns a type code indicating the type of data type of the
{hclass}`BParameter`'s value. This is usually
{cpp:enumerator}`B_INT32_TYPE` for selectors or
{cpp:enumerator}`B_FLOAT_TYPE` for sliders.
::::

::::{abi-group}
:::{cpp:function} BParameterWeb* BParameter::Web() const
:::

Returns the {cpp:class}`BParameterWeb` that contains the
{hclass}`BParameter`.
::::

## Constants

### Parameter Kinds

Declared in: media/ParameterWeb.h

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
	- {cpp:enumerator}`B_MASTER_GAIN`
	- The parameter represents the main volume control.
-
	- {cpp:enumerator}`B_GAIN`
	- The parameter represents a gain control.
-
	- {cpp:enumerator}`B_BALANCE`
	- The parameter represents a balance control.
-
	- {cpp:enumerator}`B_FREQUENCY`
	- The parameter represents a frequency, like a radio tuner.
-
	- {cpp:enumerator}`B_LEVEL`
	- The parameter represents a level, as in EQ and effects.
-
	- {cpp:enumerator}`B_SHUTTLE_SPEED`
	- The parameter represents playback speed. A value of 1.0 indicates normal
		speed; less than 1.0 is slower, greater than 1.0 is faster.
-
	- {cpp:enumerator}`B_CROSSFADE`
	- The parameter indicates a crossfade for mixing audio or video; 0 indicates
		that the the first of a pair of streams should be presented, 100 indicates
		that the other should be presented, and values in between indicate the
		degree of mixing that should occur.
-
	- {cpp:enumerator}`B_COMPRESSION`
	- The parameter indicates compression ratio; the value is 0 for no
		compression, 99 for 100:1 compression.
-
	- {cpp:enumerator}`B_QUALITY`
	- The parameter indicates quality level; the value is 0 for maximum
		compression, 100 for no compression.
-
	- {cpp:enumerator}`B_BITRATE`
	- The parameter indicates bit rate in bits per second.
-
	- {cpp:enumerator}`B_GOP_SIZE`
	- The parameter indicates a "group of pictures" such as how many frames
		apart a keyframe should be inserted into a video stream.
-
	- {cpp:enumerator}`B_MUTE`
	- The parameter represents a mute control; a value of 0 passes data through
		unchanged, while a value of 1 mutes the data.
-
	- {cpp:enumerator}`B_ENABLE`
	- The parameter represents an enable toggle; a value of 0 disables the
		function while a value of 1 enables it.
-
	- {cpp:enumerator}`B_INPUT_MUX`
	- The parameter represents an input MUX. The value specifies which input
		should pass through.
-
	- {cpp:enumerator}`B_OUTPUT_MUX`
	- The parameter represents an output MUX; the value specifies which output
		should receive the incoming data.
-
	- {cpp:enumerator}`B_TUNER_CHANNEL`
	- The parameter represents a channel tuner (like a TV channel); the value
		indicates the channel number.
-
	- {cpp:enumerator}`B_TRACK`
	- The parameter's value indicates a track number.
-
	- {cpp:enumerator}`B_RECSTATE`
	- The parameter indicates whether the node is silent (0), playing (1), or
		recording (2).
-
	- {cpp:enumerator}`B_SHUTTLE_MODE`
	- The parameter indicates performance mode: -1 for backwards, 0 for stop, 1
		for playing, and 2 for paused.
-
	- {cpp:enumerator}`B_RESOLUTION`
	- The parameter indicates video or audio resolution.
-
	- {cpp:enumerator}`B_COLOR_SPACE`
	- The parameter indicates video color space.
-
	- {cpp:enumerator}`B_FRAME_RATE`
	- The parameter represents a selector for picking frame rate.
-
	- {cpp:enumerator}`B_VIDEO_FORMAT`
	- The parameter represents a selector for choosing a video format.

		The {cpp:enumerator}`B_VIDEO_FORMAT` kind has specific video format values
		associated with it:

		:::{list-table}
		---
		header-rows: 0
		align: left
		widths: auto
		---
		-
			- 1
			- NTSC-M
		-
			- 2
			- NTSC-J
		-
			- 3
			- PAL-BDGHI
		-
			- 4
			- PAL-M
		-
			- 5
			- PAL-N
		-
			- 6
			- SECAM
		-
			- 7
			- MPEG-1
		-
			- 8
			- MPEG-2

		:::
-
	- 1
	- NTSC-M
-
	- 2
	- NTSC-J
-
	- 3
	- PAL-BDGHI
-
	- 4
	- PAL-M
-
	- 5
	- PAL-N
-
	- 6
	- SECAM
-
	- 7
	- MPEG-1
-
	- 8
	- MPEG-2
-
	- {cpp:enumerator}`B_WEB_PHYSICAL_INPUT`
	- The parameter represents a physical input (such as a microphone jack or
		line input jack).
-
	- {cpp:enumerator}`B_WEB_PHYSICAL_OUTPUT`
	- The parameter represents a physical output (such as a line output jack or
		headphone jack).
-
	- {cpp:enumerator}`B_WEB_LOGICAL_INPUT`
	- The parameter represents a point at which bits of data are transferred
		between the computer and the A/V input hardware.
-
	- {cpp:enumerator}`B_WEB_LOGICAL_OUTPUT`
	- The parameter represents a point at which bits of data are transferred
		between the computer and the A/V output hardware.
-
	- {cpp:enumerator}`B_WEB_ADC_CONVERTER`
	- The parameter represents an analog to digital converter.
-
	- {cpp:enumerator}`B_WEB_DAC_CONVERTER`
	- The parameter represents a digital to analog converter.
-
	- {cpp:enumerator}`B_WEB_BUFFER_INPUT`
	- The parameter represents a {cpp:func}`media_input <media::input>`.
-
	- {cpp:enumerator}`B_WEB_BUFFER_OUTPUT`
	- The parameter represents a {cpp:func}`media_output <media::output>`.
-
	- {cpp:enumerator}`B_SIMPLE_TRANSPORT`
	- A discrete parameter indicating one of five states: rewinding, stopped,
		playing, paused, and fast-forwarding.
-
	- {cpp:enumerator}`B_GENERIC`
	- The parameter's kind isn't one of the above.

:::

Indicates the kind of parameter represented by a {hclass}`BParameter`
object.

### media_parameter_type

Declared in: media/ParameterWeb.h

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
	- {cpp:enumerator}`B_NULL_PARAMETER`
	- The {hclass}`BParameter` is a {cpp:class}`BNullParameter`.
-
	- {cpp:enumerator}`B_DISCRETE_PARAMETER`
	- The {hclass}`BParameter` is a {cpp:class}`BDiscreteParameter`.
-
	- {cpp:enumerator}`B_CONTINUOUS_PARAMETER`
	- The {hclass}`BParameter` is a {cpp:class}`BContinuousParameter`.

:::

These are the possible parameter types, which are returned by the
{cpp:func}`Type() <BParameter::Type>` function. They indicate what subclass
of {hclass}`BParameter` the object is.

:::{admonition} Note
:class: note
Keep in mind that because these constants are members of the
{hclass}`BParameter` class, if you need to reference them from outside a
BParameter, you need to preface the reference with "BParameter::", such as
`BParameter::B_NULL_PARAMETER`.
:::
