# BInputServerDevice

{hclass}`BInputServerDevice` is a base class for input devices; these are
instances of {hclass}`BInputServerDevice` subclasses that generate input
events. In most cases, an input device corresponds to a device driver that
handles a specific brand or model of hardware (mouse, keyboard, tablet,
etc.), but it doesn't have to: an input device can get events from the Net,
or generate them algorithmically, for example. Also, a single
{hclass}`BInputServerDevice` can handle more than one device driver.

{hclass}`BInputServerDevice` objects are created and deleted by the Input
Server only—you never create or delete these objects themselves.

## Starting and Sending Messages

For each device that your object registers, it gets a
{cpp:func}`~BInputServerDevice::Start()` function call. This is the Input
Server's way of telling your object that it can begin generating input
events (for the designated device). So far, all of this—from the add-on
load to the {cpp:func}`~BInputServerDevice::Start()` call—happens within a
single Input Server thread (for all input devices). When your
{cpp:func}`~BInputServerDevice::Start()` function is called, you should
spawn a thread so your object can generate events without blocking the
Server. Events are generated and sent through the
{cpp:func}`~BInputServerDevice::EnqueueMessage()` function.

## Device Types and Control Messages

The Input Server knows about two types of devices: keyboards, and pointing
devices (mice, tablets, etc). When you register your object's devices
(through {cpp:func}`~BInputServerDevice::RegisterDevices()`) you have to
indicate the device type. The Input Server uses the device type to
predicate the input device control messages it sends to the devices. These
messages, delivered in {cpp:func}`~BInputServerDevice::Control()` calls,
tell a device that there's been a change downstream that applies
specifically to that type of device. For example, when the user changes the
mouse speed, each pointing device receives a
{cpp:enumerator}`B_MOUSE_SPEED_CHANGED` notification.

The Be-defined control messages are predicated on device type only.

If your {cpp:class}`BInputServerDevice` object manages a device other than
a pointer or a keyboard, you tell the Input Server that the device is
undefined. In this case, the Input Server won't send your device any
device-specific messages; to send your device a message you (or an
application that knows about your device) have to use a
{cpp:class}`BInputServerDevice` object.

### Pointing Devices

Pointing devices such as mice, trackballs, drawing tablets, etc. generate
{cpp:enumerator}`B_MOUSE_MOVED` messages (which trigger a BView's
MouseMoved() function) featuring a where field representing the cursor's
location in view co-ordinates. Unfortunately, your
{cpp:class}`BInputServerDevice` doesn't know anything about views; that's
the App Server's job. You'll still need to add this information to the
{cpp:enumerator}`B_MOUSE_MOVED` messages generated by your
{cpp:class}`BInputServerDevice`, and the App Server will adjust it to view
co-ordinates for you.

When generating a {cpp:enumerator}`B_MOUSE_MOVED` message, you add x and y
fields in one of two ways:

- an offset relative to the cursor's previous position
  ({cpp:enumerator}`B_INT32_TYPE` values)

- an absolute position expressed in the range 0.0 to 1.0
  ({cpp:enumerator}`B_FLOAT_TYPE` values)

Mice always use relative locations; tablets can use either (though they
usually provide absolute values).

### Relative Locations

All mice (and some drawing tablets) express the pointer location relative
to its previous position. If your pointing device is operating in relative
co-ordinate mode, you add x and y entries as {cpp:enumerator}`B_INT32_TYPE`
values in device-defined units. The App Server interprets these units as
pixels, so you may need to scale your output:

:::{code} cpp
int32 xVal, yVal;
...
event->AddInt32( "x", xVal );
event->AddInt32( "y", yVal );
:::

### Absolute Locations

Drawing tablets or other pointing devices that provide absolute locations
add the x and y entries as {cpp:enumerator}`B_FLOAT_TYPEs`:

:::{code} cpp
float xVal, yVal;
...
event->AddFloat( "x", xVal );
event->AddFloat( "y", yVal );
:::

These values must be in the range [0.0 to 1.0]. The app_server scales them
to the screen's co-ordinate system so (0.0, 0.0) is the left-top, and (1.0,
1.0) is the right-bottom of the screen. This lets the pointing device work
with any screen resolution, automatically.

### Now where?

When the Application Server receives one of these
{cpp:enumerator}`B_MOUSE_MOVED` messages, it converts the x and y values
into absolute values in the target view's co-ordinate system, and then
throws away the x and y entries in the message. Because of this, and the
fact that some applications might want more accurate positional information
from tablets, fill in the {hparam}`be:tablet_x` and {hparam}`be:tablet_y`
fields as well:

:::{code} cpp
float xVal, yVal;
...
event->AddFloat( "x", xVal );
event->AddFloat( "y", yVal );
event->AddFloat( "be:tablet_x", xVal );
event->AddFloat( "be:tablet_y", yVal );
:::

### Other Useful Information

Pressure information is stored in the {hparam}`be:tablet_pressure` field,
as a float in the range [0.0 to 1.0] (minimum pressure to maximum
pressure):

:::{code} cpp
float pressure;
...
event->AddFloat( "be:tablet_pressure", pressure );
:::

If the tablet supports tilt information, store it in
{hparam}`be:tablet_tilt_x` and {hparam}`be:tablet_tilt_y`, scaling the
information to the range [0.0 to 1.0]. A tilt of (-1.0, -1.0) tilts to the
left-top, (1.0, 1.0) tilts to the right-bottom, and (0.0, 0.0) is no tilt.

:::{code} cpp
float tilt_x, tilt_y;
...
event->AddFloat( "be:tablet_tilt_x", tilt_x );
event->AddFloat( "be:tablet_tilt_y", tilt_y );
:::

Tablets with pens that support an eraser store the eraser's state in the
{hparam}`be:tablet_eraser` field. A value of 1 means the pen is reversed
(i.e. the eraser is on), and 0 means it should behave normally.

:::{code} cpp
int32 erase_mode;
...
event->AddInt32( "be:tablet_eraser", erase_mode );
:::

## Device State

The {cpp:func}`~BInputServerDevice::Control()` protocol is designed to
accommodate queries (in addition to commands). Currently, however, the
Input Server maintains the keyboard and pointing device state and answers
these queries itself; it doesn't forward any of the Be-defined query
messages. For example, when an application asks for the current mouse speed
setting (through {cpp:func}`get_mouse_speed()`), the query gets no further
than the Input Server itself—it doesn't get passed as a control message to
a pointing device.

If you're designing a {cpp:class}`BInputServerDevice` that manages a
keyboard or pointing device, you must keep in mind that your device is not
responsible for its "Be-defined" state. The elements of the state—mouse
speed, key map, etc.—correspond to the control messages listed in "Input
Device Control Messages".

## Dynamic Devices

As hardware devices are attached and detached from the computer, you can
add and remove items from your {cpp:class}`BInputServerDevice`'s list of
registered devices (by calling {cpp:func}`RegisterDevice()
<BInputServerDevice::RegisterDevices>` / {cpp:func}`UnregisterDevice()
<BInputServerDevice::UnregisterDevices>`). But your object has to first
notice that a physical device has been added or removed. It does this by
placing a node monitor on the device directory (/dev). As a convenience—and
to help conserve resources—the {cpp:class}`BInputServerDevice` class
provides the {cpp:func}`Start/StopMonitoringDevices()
<BInputServerDevice::StartMonitoringDevice>` functions which install and
remove node monitors for you.

## Creating and Registering

To create a new input device, you must:

- create a subclass of {cpp:class}`BInputServerDevice`

- implement the {cpp:func}`instantiate_input_device()` C function to create
  an instance of your {cpp:class}`BInputServerDevice` subclass

- compile the class and the function as an add-on

- install the add-on in one of the input device directories

At boot time, the Input Server loads the add-ons it finds in the input
device directories. For each add-on it loads, the Server invokes
{cpp:func}`instantiate_input_device()` to get a pointer to the add-on's
{cpp:class}`BInputServerDevice` object. After constructing the object, the
Server calls {cpp:func}`~BInputServerDevice::InitCheck()` to give the
add-on a chance to bail out if the constructor failed. If the add-on wants
to continue, it calls {cpp:func}`~BInputServerDevice::RegisterDevices()`
(from within {cpp:func}`~BInputServerDevice::InitCheck()`) to tell the
Server which physical or virtual devices it handles.

## Installing an Input Device

The input server looks for input devices in the input_server/devices
subdirectories of {cpp:enumerator}`B_BEOS_ADDONS_DIRECTORY`,
{cpp:enumerator}`B_COMMON_ADDONS_DIRECTORY`, and
{cpp:enumerator}`B_USER_ADDONS_DIRECTORY`.

- You can install your input devices in the latter two directories—i.e.
  those under {cpp:enumerator}`B_COMMON_ADDONS_DIRECTORY`, and
  {cpp:enumerator}`B_USER_ADDONS_DIRECTORY`.

- The {cpp:enumerator}`B_BEOS_ADDONS_DIRECTORY` is reserved for add-ons
  that are supplied by the BeOS.
