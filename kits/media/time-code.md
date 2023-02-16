:::{cpp:class} BTimeCode
:::

# BTimeCode

## Constructor and Destructor

::::{abi-group}
:::{cpp:function} BTimeCode::BTimeCode()
:::

:::{cpp:function} BTimeCode::BTimeCode(bigtime_t us, timecode_type type = B_TIMECODE_DEFAULT)
:::

:::{cpp:function} BTimeCode::BTimeCode(int hours, int minutes, int seconds, int frames, timecode_type type = B_TIMECODE_DEFAULT)
:::

:::{cpp:function} BTimeCode::BTimeCode(const BTimeCode& clone)
:::

The constructor prepares the {hclass}`BTimeCode` object for use. If you
use the first form of the constructor, without arguments, you'll have to
call an appropriate function to set the {hclass}`BTimeCode`'s time
information before using it for translation purposes. This can be done by
calling one or more of {cpp:func}`SetData() <BTimeCode::SetData>`,
{cpp:func}`SetType() <BTimeCode::SetType>`, {cpp:func}`SetMicroseconds()
<BTimeCode::SetMicroseconds>`, or {cpp:func}`SetLinearFrames()
<BTimeCode::SetLinearFrames>`.

The second form of the constructor accepts as input a time in
microseconds, {hparam}`us`, and the timecode {hparam}`type`.

The third form accepts as input a time in {hparam}`hours`,
{hparam}`minutes`, {hparam}`seconds`, and {hparam}`frames`, as well as the
timecode {hparam}`type`.

The fourth form of the constructor duplicates an existing
{hclass}`BTimeCode` object.
::::

::::{abi-group}
:::{cpp:function} BTimeCode::~BTimeCode()
:::

A typical destructor
::::

## Member Functions

::::{abi-group}
:::{cpp:function} void BTimeCode::GetData(int* outHours, int* outMinutes, int* outSeconds, int* outFrames, timecode_type* outType)
:::

:::{cpp:function} void BTimeCode::SetData(int hours, int minutes, int seconds, int frames)
:::

{hmethod}`GetData()` returns the timecode's value in {hparam}`hours`,
{hparam}`minutes`, {hparam}`seconds`, and {hparam}`frames`, and also
returns the timecode type, if you specify a valid pointer for
{hparam}`outType`. {hmethod}`SetData()` lets you set the timecode's value.
::::

::::{abi-group}
:::{cpp:function} void BTimeCode::GetString(char* str) const
:::

Fills {hparam}`str`, which must be at least 24 bytes long, with a string
indicating the current time in hours, minutes, seconds, and frames. The
string is formatted in a manner appropriate to the timecode type. A typical
example would be "01:24:09.18", which is 1 hour, 24 minutes, 9 seconds, and
18 frames.
::::

::::{abi-group}
:::{cpp:function} void BTimeCode::Hours() const
:::

:::{cpp:function} void BTimeCode::Minutes() const
:::

:::{cpp:function} void BTimeCode::Seconds() const
:::

:::{cpp:function} void BTimeCode::Frames() const
:::

These functions return the time's hours, minutes, seconds, and frames
portions.
::::

::::{abi-group}
:::{cpp:function} int32 BTimeCode::LinearFrames() const
:::

:::{cpp:function} void BTimeCode::SetLinearFrames(int32 linearFrames)
:::

{hmethod}`LinearFrames()` returns the {hclass}`BTimeCode` object's time in
linear frames. {hmethod}`SetLinearFrames()` lets you change the time,
specifying the new time in linear frames.
::::

::::{abi-group}
:::{cpp:function} bigtime_t BTimeCode::LinearFrames() const
:::

:::{cpp:function} void BTimeCode::SetMicroseconds(bigtime_t us)
:::

{hmethod}`Microseconds()` returns the {hclass}`BTimeCode` object's time,
in microseconds. {hmethod}`SetMicroseconds()` lets you change the time,
specifying the new time in microseconds.
::::

::::{abi-group}
:::{cpp:function} timecode_type BTimeCode::Type() const
:::

:::{cpp:function} status_t BTimeCode::SetType(timecode_type type)
:::

{hmethod}`Type()` returns the {hclass}`BTimeCode` object's timecode type.
{hmethod}`SetType()` lets you change the timecode type.

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
	- The type was returned safely.
-
	- {cpp:enumerator}`B_ERROR`
	- The timecode type specified is invalid.

:::
::::

## Operators

::::{abi-group}
:::{cpp:function} BTimeCode& operator =(const BTimeCode& clone)
:::

Makes the current {hclass}`BTimeCode` identical to the {hclass}`BTimeCode`
object specified
::::

::::{abi-group}
:::{cpp:function} BTimeCode& operator ==(const BTimeCode& other)
:::

Determines whether or not the two {hclass}`BTimeCode` objects are equal
(their times are the same, regardless of their timecode types).
::::

::::{abi-group}
:::{cpp:function} BTimeCode& operator <(const BTimeCode& other)
:::

Indicates whether or not one {hclass}`BTimeCode`'s time, in microseconds,
is less than the other's.
::::

::::{abi-group}
:::{cpp:function} BTimeCode& operator +=(const BTimeCode& other)
:::

Adds the time of the {hclass}`BTimeCode` object other to the current
{hclass}`BTimeCode`'s time.
::::

::::{abi-group}
:::{cpp:function} BTimeCode& operator -=(const BTimeCode& other)
:::

Subtracts the time of the {hclass}`BTimeCode` object other from the
current {hclass}`BTimeCode`'s time.
::::

::::{abi-group}
:::{cpp:function} BTimeCode& operator +(const BTimeCode& other)
:::

Adds two {hclass}`BTimeCode` values together, returning a new
{hclass}`BTimeCode`.
::::

::::{abi-group}
:::{cpp:function} BTimeCode& operator <(const BTimeCode& other)
:::

Subtracts two {hclass}`BTimeCode` values, returning a new one.
::::

## Global C Functions

::::{abi-group}
:::{cpp:function} status_t count_timecodes()
:::

Returns the number of recognized time code types.
::::

::::{abi-group}
:::{cpp:function} status_t frames_to_timecode(int32 linearFrames, int* hours, int* minutes, int* seconds, int* frames, const timecode_info code = NULL)
:::

:::{cpp:function} status_t timecode_to_frames(int hours, int minutes, int seconds, int frames, const timecode_info code = NULL)
:::

frames_to_timecode() converts the frame offset {hparam}`linearFrames` into
{hparam}`hours`, {hparam}`minutes`, {hparam}`seconds`, and
{hparam}`frames`.

timecode_to_frames() converts the time from {hparam}`hours`,
{hparam}`minutes`, {hparam}`seconds`, and {hparam}`frames` into a linear
frame offset, storing the result in {hparam}`linearFrames`.

The {htype}`timecode_info` structure code is used to determine how the
conversion should be made, if you specify it. Otherwise
{cpp:enumerator}`B_TIMECODE_DEFAULT` is assumed.

Currently these functions always return {cpp:enumerator}`B_OK`, but you
should still check for errors because you'd hate it if your app broke in
the future, wouldn't you?
::::

::::{abi-group}
:::{cpp:function} status_t get_timecode_description(timecode_type type, timecode_info* outTimeCode)
:::

Fills out the {htype}`timecode_info` structure specified by
{hparam}`outTimeCode` with information describing the specified timecode
type.

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
	- No error.
-
	- {cpp:enumerator}`B_ERROR`
	- The specified timecode type isn't valid.

:::
::::

::::{abi-group}
:::{cpp:function} status_t us_to_timecode(bigtime_t micros, int* hours, int* minutes, int* seconds, int* frames, const timecode_info code = NULL)
:::

:::{cpp:function} status_t timecode_to_us(int hours, int minutes, int seconds, int frames, bigtime_t* micros, const timecode_info code = NULL)
:::

us_to_timecode() converts the time {hparam}`micros`, which is specified in
microseconds, into {hparam}`hours`, {hparam}`minutes`, {hparam}`seconds`,
and {hparam}`frames`.

timecode_to_us() converts the time from {hparam}`hours`,
{hparam}`minutes`, {hparam}`seconds`, and {hparam}`frames` into
microseconds, storing the result in {hparam}`micros`.

The {htype}`timecode_info` structure code is used to determine how the
conversion should be made, if you specify it. Otherwise
{cpp:enumerator}`B_TIMECODE_DEFAULT` is assumed.

Currently these functions always return {cpp:enumerator}`B_OK`, but you
should still check for errors because you'd hate it if your app broke in
the future, wouldn't you?
::::

## Constants

### timecode_type

Declared in: media/TimeCode.h

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
	- {cpp:enumerator}`B_TIMECODE_DEFAULT`
	- The default time code
-
	- {cpp:enumerator}`B_TIMECODE_100`
	- 100 frames per second.
-
	- {cpp:enumerator}`B_TIMECODE_75`
	- CD audio
-
	- {cpp:enumerator}`B_TIMECODE_30`
	- MIDI
-
	- {cpp:enumerator}`B_TIMECODE_30_DROP_2`
	- NTSC
-
	- {cpp:enumerator}`B_TIMECODE_30_DROP_4`
	- Brazil
-
	- {cpp:enumerator}`B_TIMECODE_25`
	- PAL
-
	- {cpp:enumerator}`B_TIMECODE_24`
	- Film
-
	- {cpp:enumerator}`B_TIMECODE_18`
	- Super8

:::

Constants identifying the various timecode types supported by
{hclass}`BTimeCode`.

## Defined Types

### timecode_info

Declared in: media/TimeCode.h

:::{code} c
struct timecode_info {
    timecode_type type;
    int drop_frames;
    int every_nth;
    int except_nth;
    int fps_div;
    char name[32];
    char format[32];
    char _reserved_[64];
};
:::

The {htype}`timecode_info` structure describes the attributes of a
timecode type. You probably should just use the {hclass}`BTimeCode` class,
or the global C functions, though. It just makes your life easier.

:::{list-table}
---
header-rows: 1
align: left
widths: auto
---
-
	- Field

	- Description

-
	- type
	- Indicates the timecode type described by the structure.
-
	- drop_frames
	- Indicates how many frames this timecode drops every {hparam}`every_nth`
		minute, {hparam}`except_nth` minute.
-
	- fps_div
	- Indicates the nominal frame rate of the format.
-
	- name
	- Is a printable name that can be used in constructing user interfaces.
-
	- format
	- Is a format to be used in calling sprintf(); it's used by
		{cpp:func}`GetString() <BTimeCode::GetString>`.

:::
