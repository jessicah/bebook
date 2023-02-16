:::{cpp:class} BParameterGroup
:::

# BParameterGroup

## Constructor and Destructor

::::{abi-group}
:::{cpp:function} BParameterGroup::BParameterGroup()
:::

Rather than directly creating a {hclass}`BParameterGroup` object via the
new operator, you should call {cpp:func}`BParameterWeb::MakeGroup` to
create a top-level group, or {cpp:func}`BParameterGroup::MakeGroup` if you
want to create a subgroup.
::::

::::{abi-group}
:::{cpp:function} BParameterGroup::~BParameterGroup()
:::

You don't need to delete a {hclass}`BParameterGroup` object; the
{cpp:class}`BParameterWeb` that owns it will do this for you when the web
is deleted.
::::

## Member Functions

::::{abi-group}
:::{cpp:function} int32 BParameterGroup::CountGroups()
:::

Returns the number of subgroups in the group. This count doesn't subgroups
nested within subgroups.
::::

::::{abi-group}
:::{cpp:function} int32 BParameterGroup::CountParameters()
:::

Returns the number of {cpp:class}`BParameter`s in the group. This count
doesn't include {cpp:class}`BParameter`s in subgroups.
::::

::::{abi-group}
:::{cpp:function} BParameterGroup* BParameterGroup::GroupAt(int32 index)
:::

Returns the subgroup at the specified index within the
{hclass}`BParameterGroup`. If the {hparam}`index` is negative, or is
greater than {cpp:func}`CountGroups() <BParameterGroup::CountGroups>`-1,
{cpp:expr}`NULL` is returned.
::::

::::{abi-group}
:::{cpp:function} BNullParameter* BParameterGroup::MakeNullParameter(int32 id, media_type type, const char* name, const char* kind)
:::

Creates a new {cpp:class}`BNullParameter` within the group, with the
internal ID specified by {hparam}`id`, which should be unique within the
{cpp:class}`BParameterWeb` that owns the group.

The type of media data that travels through the null parameter is
indicated by {hparam}`type`, which could be
{cpp:enumerator}`B_MEDIA_UNKNOWN_TYPE` or
{cpp:enumerator}`B_MEDIA_NO_TYPE`. The parameter's {hparam}`name` will be
displayed by client applications that display information about the node,
and the parameter has the specified {hparam}`kind`.

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
	- {cpp:enumerator}`B_GENERIC`
	- The parameter's kind isn't one of the above.

:::

These kinds are used when a control panel needs to draw a signal flow
diagram, so it can use the appropriate symbols for these points in the
flow.

:::{admonition} Note
:class: note
If you create your own kind, you won't break anything, but you should
contact Be Developer Support for guidance, so we can standardize given your
needs.
:::
::::

::::{abi-group}
:::{cpp:function} BDiscreteParameter* BParameterGroup::MakeDiscreteParameter(int32 id, media_type type, const char* name, const char* kind)
:::

Creates a new {cpp:class}`BDiscreteParameter` object and attaches it to
the group. The {cpp:class}`BDiscreteParameter` will have the specified
internal {hparam}`id`, which should be unique within the
{cpp:class}`BParameterWeb` that owns the group.

The {cpp:class}`BDiscreteParameter` will affect media data of the
specified {hparam}`type`, and will have the specified {hparam}`name`.

The kind of discrete parameter is specified by {hparam}`kind`, and may be
any of the following values:

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

:::
::::

::::{abi-group}
:::{cpp:function} BContinuousParameter* BParameterGroup::MakeContinuousParameter(int32 id, media_type type, const char* name, const char* kind, const char* unit, float minValue, float maxValue, float step)
:::

Creates a new {cpp:class}`BContinuousParameter` object and attaches it to
the group. The {cpp:class}`BContinuousParameter` will have the specified
internal {hparam}`id`, which should be unique within the
{cpp:class}`BParameterWeb` that owns the group.

The {cpp:class}`BContinuousParameter` will affect media data of the
specified {hparam}`type`, and will have the specified {hparam}`name`.

The kind of parameter the {cpp:class}`BContinuousParameter` represents is
specified by {hparam}`kind`, and may be any of the following values:

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
	- {cpp:enumerator}`B_GOP_SIZE`
	- The parameter indicates a "group of pictures" such as how many frames
		apart a keyframe should be inserted into a video stream.
-
	- {cpp:enumerator}`B_TUNER_CHANNEL`
	- The parameter represents a channel tuner (like a TV channel); the value
		indicates the channel number.

:::

The units of measurement are specified by {hparam}`unit`, and the
parameter's value can range from {hparam}`minValue` to {hparam}`maxValue`,
with a granularity of {hparam}`step`.
::::

::::{abi-group}
:::{cpp:function} BParameterGroup BParameterGroup::MakeGroup(const char* name)
:::

Creates a sub-group with the specified {hparam}`name`
::::

::::{abi-group}
:::{cpp:function} const char* BParameterGroup::Name()
:::

Returns the name of the {hclass}`BParameterGroup`. This name can be
displayed to the user; for example, it could be used as the label of a
{cpp:class}`BTab`.
::::

::::{abi-group}
:::{cpp:function} BParameter* BParameterGroup::ParameterAt(int32 index)
:::

Returns the {cpp:class}`BParameter` at the specified {hparam}`index`
within the {hclass}`BParameterGroup`. If the {hparam}`index` is negative,
or is greater than {cpp:func}`CountParameters()
<BParameterGroup::CountParameters>`-1, {cpp:expr}`NULL` is returned.
::::

::::{abi-group}
:::{cpp:function} BParameterWeb* BParameterGroup::Web()
:::

Returns the {cpp:class}`BParameterWeb` that owns the group.
::::
