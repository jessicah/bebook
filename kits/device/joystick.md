:::{cpp:class} BJoystick
:::

# BJoystick

## Data Members

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
	- bigtime_ttimestamp
	- The time of the most recent update, as measured in microseconds from the
		beginning of 1970.
-
	- int16horizontal
	- The horizontal position of the joystick at the time of the last update.
		Values increase as the joystick moves from left to right.
-
	- int16vertical
	- The vertical position of the joystick at the time of the last update.
		Values decrease as the joystick moves forward and increase as it's pulled
		back.
-
	- boolbutton1
	- {cpp:expr}`false` if the first button was pressed at the time of the last
		update, and {cpp:expr}`true` if not.
-
	- boolbutton2
	- {cpp:expr}`false` if the second button was pressed at the time of the last
		update, and {cpp:expr}`true` if not.

:::

The {hparam}`horizontal` and {hparam}`vertical` data members record values
read directly from the ports, values that simply digitize the analog output
of the joysticks. This class makes no effort to translate the values to a
standard scale or range. Values can range from 0 through 4,095, but
joysticks typically don't use the full range and some don't register all
values within the range that is used. The scale is not linear—identical
increments in different parts of the range can reflect differing amounts of
horizontal and vertical movement. The exact variance from linearity and the
extent of the usable range are partly characteristics of the individual
joystick and partly functions of the computer's hardware.

:::{admonition} Note
:class: note
Typically you won't use these data members if you're using enhanced mode;
they're provided primarily for backward compatibility.
:::

## Constructor and Destructor

::::{abi-group}
:::{cpp:function} BJoystick::BJoystick()
:::

Initializes the {hclass}`BJoystick` object so that all values are set to
0. Before using the object, you must call {cpp:func}`Open()
<BJoystick::Open>` to open a particular joystick port. For the object to
register any meaningful values, you must call {cpp:func}`Update()
<BJoystick::Update>` to query the open port.
::::

::::{abi-group}
:::{cpp:function} virtual BJoystick::~BJoystick()
:::

Closes the port, if it was not closed already.
::::

## Member Functions

::::{abi-group}
:::{cpp:function} int32 BJoystick::CountAxes()
:::

:::{cpp:function} status_t BJoystick::GetAxisValues(int16* outValues, int32 forStick = 0)
:::

{hmethod}`CountAxes()` returns the number of axes on the opened game port.

{hmethod}`GetAxisValues()` fills the array pointed to by
{hparam}`outValues` with the values of all the axes connected to the
specified joystick. The {hparam}`forStick` parameter lets you choose which
joystick on the game port to read the values from (the default is to read
from the first stick on the port).

The returned values range from -32,768 to 32,767.

The array {hparam}`outValues` must be large enough to contain the values
for all the axes. You can ensure that this is the case by using the
following code:

:::{code} cpp
int16* axes;

axes = (int16*) malloc(sizeof(int16) * stick->CountAxes());
stick->GetAxisValues(axes);
:::

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
	- The name was returned successfully.
-
	- {cpp:enumerator}`B_BAD_VALUE`.
	- The joystick specified by {hparam}`forStick` doesn't exist.

:::
::::

::::{abi-group}
:::{cpp:function} int32 BJoystick::CountButtons()
:::

:::{cpp:function} uint32 BJoystick::ButtonValues()
:::

{hmethod}`CountButtons()` returns the number of buttons on the opened game
port.

{hmethod}`ButtonValues()` returns a 32-bit number in which each bit
represents the state of one button. The {hparam}`forStick` parameter lets
you choose which joystick on the game port to read the values from (the
default is to read from the first stick on the port). You can deterimine if
a particular button is down by using the following code:

:::{code} cpp
uint32 buttonValues = stick->ButtonValues();

if (buttonValues & (1 << whichButton)) {
   /* button number whichButton is pressed */
}
:::
::::

::::{abi-group}
:::{cpp:function} int32 BJoystick::CountDevices()
:::

:::{cpp:function} status_t BJoystick::GetDeviceName(int32 index, char* outName, size_t bufSize = B_OS_NAME_LENGTH)
:::

{hmethod}`CountDevices()` returns the number of game ports on the
computer.

{hmethod}`GetDeviceName()` returns the name of the device specified by the
given {hparam}`index`. The buffer pointed to by {hparam}`outName` is filled
with the device name; {hparam}`bufSize` indicates the size of the buffer.

The names returned by {hmethod}`GetDeviceName()` can be passed into the
{cpp:func}`Open() <BJoystick::Open>` function to open a device.

:::{admonition} Note
:class: note
The {hclass}`BJoystick` doesn't need to have an open device before you use
these functions; in fact, your application will typically use these to
provide user interface allowing the user to choose the joystick device
they'd like to use.
:::

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
	- The name was returned successfully.
-
	- {cpp:enumerator}`B_BAD_INDEX`.
	- The specified {hparam}`index` is invalid.
-
	- {cpp:enumerator}`B_NAME_TOO_LONG`.
	- The device name is too long for the buffer.

:::
::::

::::{abi-group}
:::{cpp:function} int32 BJoystick::CountHats()
:::

:::{cpp:function} status_t BJoystick::GetHatValues(int8* outHats, int32 forStick = 0)
:::

{hmethod}`CountHats()` returns the number of hats on the opened game port.

{hmethod}`GetHatValues()` fills the array pointed to by {hparam}`outHats`
with the values of all the hats connected to the specified joystick. The
{hparam}`forStick` parameter lets you choose which joystick on the game
port to read the values from (the default is to read from the first stick
on the port).

The return value means the following:

:::{list-table}
---
header-rows: 1
align: left
widths: auto
---
-
	- Value

	- Description

-
	- 0

	- Centered

-
	- 1

	- Up

-
	- 2

	- Up and right

-
	- 3

	- Right

-
	- 4

	- Down and right

-
	- 5

	- Down

-
	- 6

	- Down and left

-
	- 7

	- Left

-
	- 8

	- Up and left


:::

The array {hparam}`outHats` must be large enough to contain the values for
all the hats. You can ensure that this is the case by using the following
code:

:::{code} cpp
int8* hats;

hats = (int8*) malloc(sizeof(int8) * stick->CountAxes());
stick->GetHatValues(hats);
:::

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
	- The name was returned successfully.
-
	- {cpp:enumerator}`B_BAD_VALUE`.
	- The joystick specified by {hparam}`forStick` doesn't exist.

:::
::::

::::{abi-group}
:::{cpp:function} int32 BJoystick::CountSticks()
:::

Returns the number of joysticks connected to the opened game port.
::::

::::{abi-group}
:::{cpp:function} status_t BJoystick::GetAxisNameAt(int32 index, BString* outName)
:::

:::{cpp:function} status_t BJoystick::GetHatNameAt(int32 index, BString* outName)
:::

:::{cpp:function} status_t BJoystick::GetButtonNameAt(int32 index, BString* outName)
:::

Returns the name of the control specified by the given {hparam}`index`.
The {cpp:class}`BString` object pointed to by {hparam}`outName` is set to
the control's name.

{hmethod}`GetAxisNameAt()` returns the specified axis' name,
{hmethod}`GetHatNameAt()` returns the specified hat's name, and
{hmethod}`GetButtonNameAt()` returns the specified button's name.

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
	- {cpp:enumerator}`B_BAD_INDEX`.
	- The name was returned successfully.
-
	- {cpp:enumerator}`B_BAD_INDEX`.
	- The specified {hparam}`index` is invalid.

:::
::::

::::{abi-group}
:::{cpp:function} status_t BJoystick::GetControllerModule(BString* outName)
:::

:::{cpp:function} status_t BJoystick::GetControllerName(BString* outName)
:::

{hmethod}`GetControllerModule()` returns the name of the joystick module
that represents the opened joystick device. If the device isn't in enhanced
mode, this always returns "Legacy".

{hmethod}`GetControllerName()` returns the name of the joystick that's
been configured for the opened device. This is the same string that appears
in the Joysticks preference application. The returned string is always
"2-axis" if the device isn't in enhanced mode.

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
	- The name was returned successfully.
-
	- {cpp:enumerator}`B_BAD_INDEX`.
	- The specified {hparam}`index` is invalid.

:::
::::

::::{abi-group}
:::{cpp:function} bool BJoystick::EnterEnhancedMode(const entry_ref* ref = NULL)
:::

Switches the device into enhanced mode. If {hparam}`ref` isn't
{cpp:expr}`NULL`, it's treated as a reference to a joystick description
file (such as those in /boot/beos/etc/joysticks). If {hparam}`ref` is
{cpp:expr}`NULL`, the currently-configured joystick settings (as per the
Joysticks preference application) are used.

If enhanced mode is entered successfully (or the device is already in
enhanced mode), {cpp:expr}`true` is returned. Otherwise,
{hmethod}`EnterEnhancedMode()` returns {cpp:expr}`false`.
::::

::::{abi-group}
:::{cpp:function} bool BJoystick::IsCalibrationEnabled()
:::

:::{cpp:function} status_t BJoystick::EnableCalibration(bool calibrates = true)
:::

{hmethod}`IsCalibrationEnabled()` returns {cpp:expr}`true` if axis values
returned by the joystick will be calibrated automatically into the range
-32,768 to 32,767, or {cpp:expr}`false` if the raw values will be returned.

{hmethod}`EnableCalibration()` enables or disables automatic calibration
for the joystick's axes. Specify a value of {cpp:expr}`true` for calibrates
to enable calibration; otherwise, specify {cpp:expr}`false`.

:::{admonition} Note
:class: note
The Joysticks preference application lets the user calibrate the joystick.
Calibration is enabled by default.
:::

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
	- The name was returned successfully.
-
	- {cpp:enumerator}`B_NO_INIT`.
	- The device isn't in enhanced mode.

:::
::::

::::{abi-group}
:::{cpp:function} status_t BJoystick::Open(const char* devName)
:::

:::{cpp:function} status_t BJoystick::Open(const char* devName, bool enterEnhanced)
:::

:::{cpp:function} void BJoystick::Close()
:::

These functions open the joystick port specified by {hparam}`devName` and
close it again. The {hparam}`devName` should be the name of a game port
device. The easiest way to determine valid device names is by using the
{cpp:func}`CountDevices() <BJoystick::CountDevices>` and
{cpp:func}`GetDeviceName() <BJoystick::GetDeviceName>` functions.

If it's able to open the port, {hmethod}`Open()` returns a positive
integer. If unable or if the {hparam}`devName` isn't valid, it returns
{cpp:enumerator}`B_ERROR`. If the {hparam}`devName` port is already open,
{hmethod}`Open()` tries to close it first, then open it again.

By default, {hmethod}`Open()` opens the device in enhanced mode. If you
want to use the old, unenhanced mode, you can use the second form of
{hmethod}`Open()` to specify whether or not you want to use enhanced mode;
set {hparam}`enterEnhanced` to {cpp:expr}`true` to use enhanced mode;
specify {cpp:expr}`false` if you don't want enhanced mode.

:::{admonition} Note
:class: note
Even in enhanced mode, the classic {hclass}`BJoystick` data members are
valid (for compatibility with older applications). However, they only give
you access to the first two axes and buttons of the joystick.
:::

To be able to obtain joystick data, a {hclass}`BJoystick` object must have
a port open.
::::

::::{abi-group}
:::{cpp:function} status_t BJoystick::SetMaxLatency(bigtime_t maxLatency)
:::

Specifies the maximum latency to allow when accessing the joystick.
Returns {cpp:enumerator}`B_OK` if the change is applied successfully,
otherwise returns an error code.
::::

::::{abi-group}
:::{cpp:function} status_t BJoystick::Update()
:::

Updates the data members of the object so that they reflect the current
state of the joystick. An application would typically call
{hmethod}`Update()` periodically to poll the condition of the device, then
read the values of the data members, or—if in enhanced mode—call the
various functions for obtaining joystick state information.

This function returns {cpp:enumerator}`B_ERROR` if the {hclass}`BJoystick`
object doesn't have a port open, and {cpp:enumerator}`B_OK` if it does.
::::
