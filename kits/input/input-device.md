# BInputDevice
## Constructor and Destructor
::::{abi-group}

:::{cpp:function} BInputDevice::BInputDevice()
:::

The constructor is private. Use
{cpp:func}`~find::input` or
{cpp:func}`~get::input`
to retrieve a {hclass}`BInputDevice` instance.

::::

::::{abi-group}

:::{cpp:function} BInputDevice::BInputDevice()
:::

Deletes the {hclass}`BInputDevice` object. Deleting this object doesn't affect the
device that it represents.

::::

## Member Functions
::::{abi-group}

:::{cpp:function} status_t BInputDevice::Control(uint32 code, BMessage* message)
:::
:::{cpp:function} status_t BInputDevice::Control(input_device_type type, uint32 code, BMessage* message)
:::
Sends an input device control message to the object's input device or, in
the static version, to all devices of the given type, where, type can be
{cpp:enum}`B_POINTING_DEVICE`, {cpp:enum}`B_KEYBOARD_DEVICE`,
or {cpp:enum}`B_UNDEFINED_DEVICE`. Input
devices receive these messages in their
{hmethod}`Control()` function.
The control message is described by the {hparam}`code` value; it can be
supplemented or refined by {hparam}`message`.
For example, {hparam}`code` can indicate that a
certain parameter should be set, and message can supply the requested
value.
:::{admonition} Note
:class: note
In general, you only use this function to send custom messages to a
(custom) device. You never use it to send messages to a Be-defined input
device since the messages that these devices respond to are covered by
Be-defined functions. See
"Input Device Control Messages"
for a list of
the messages that the Be-defined devices respond to, the functions that
cover them, and the German women who love them.
:::
::::

::::{abi-group}

:::{cpp:function} const char* BInputDevice::Name() const
:::
:::{cpp:function} input_device_type BInputDevice::Type() const
:::
{hmethod}`Name()` returns a pointer to the input device's name. The name,
which is set when the device is registered, is meant to be human-readable
and appropriate for use as the label of a UI element (such as a menu
field). Device names are not unique.
{hmethod}`Type()` returns the input device's type, one of
{cpp:enum}`B_POINTING_DEVICE`,
{cpp:enum}`B_KEYBOARD_DEVICE`, and {cpp:enum}`B_UNDEFINED_DEVICE`.
::::

::::{abi-group}

:::{cpp:function} status_t BInputDevice::Start()
:::
:::{cpp:function} static status_t BInputDevice::Start(input_device_type type)
:::
:::{cpp:function} bool BInputDevice::IsRunning() const
:::
:::{cpp:function} static status_t BInputDevice::Stop(input_device_type type)
:::
{hmethod}`Start()` tells the object's input device to
start generating events; {hmethod}`Stop()` tells it to stop
generating events. {hmethod}`IsRunning()` returns
{cpp:enum}`true` if the device is currently generating events
(i.e. if it has been started and hasn't been stopped).
The static versions of {hmethod}`Start()` and
{hmethod}`Stop()` start and stop all devices of the given
type.
:::{admonition} Warning
:class: warning
The Input Server tells a device to start and stop without asking the
device if the operation was successful. This means, for example, that
{hmethod}`Start()` can return {cpp:enum}`B_OK` (and
{hmethod}`IsRunning()` can return {cpp:enum}`true`)
even if the device isn't really running. For the Be-provided devices this
isn't an issue—starting and stopping always succeeds (as long as the
device exists).
:::
:::{list-table}
---
header-rows: 1
---
-
	- Return Code
	- Description
-
	- {cpp:enum}`B_OK`.
	- The device is now started ({hmethod}`Start()`) or stopped ({hmethod}`Stop()`)—even if the device was already started or stopped.
-
	- {cpp:enum}`B_ERROR`.
	- The device couldn't be found.
:::
::::

## C Functions
::::{abi-group}



:::{cpp:function} BInputDevice* BInputDevice::find_input_device(const char * name)
:::
:::{cpp:function} status_t BInputDevice::get_input_devices(BList * list)
:::
These functions get {hclass}`BInputDevice` objects for you.
find_input_device() creates and hands
you a {hclass}`BInputDevice` object that
represents the Input Server device registered as name. If name is
invalid, the function returns {cpp:enum}`NULL`. The caller is responsible for
deleting the object. Note that find_input_device() returns a new
{hclass}`BInputDevice` object for each (valid) call, even if you ask for the same
device more than once.
get_input_devices() creates a new BInputDevice object for each registered
device, and puts the objects in your list argument. list must already be
allocated, and is automatically emptied by the function (even if the
function fails). If the function succeeds, the caller owns the contents,
and needs to delete the items in the list:
:::{code}
#include <interface/Input.h>
#include <support/List.h>
...
static bool del_InputDevice( void *ptr )
{
   if( ptr ) {
      BInputDevice *dev = (BInputDevice *)ptr;
      delete dev;
      return false;
   }
   return true;
}
...
void SomeFunc( void )
{
   // Get a list of all input devices.
   BList list_o_devices;
   status_t retval = get_input_devices( &list_o_devices );
   if( retval != B_OK ) return;
   // Do something with the input devices.
   ...
   // Dispose of the device list.
   list_o_devices.DoForEach( del_InputDevice );
   list_o_devices.MakeEmpty();
}
:::
get_input_devices() returns:
:::{list-table}
---
header-rows: 1
---
-
	- Return Code
	- Description
-
	- {cpp:enum}`B_OK`.
	- Success.
-
	- {cpp:enum}`B_ERROR`.
	- General failure.
-
	- {cpp:enum}`B_BAD_PORT_ID`.
	- Couldn't talk to the Input Server.
-
	- {cpp:enum}`B_TIMED_OUT`.
	- The Input Server is no longer on speaking terms with your application.
-
	- {cpp:enum}`B_WOULD_BLOCK`.
	- More trouble communicating with the Input Server.
:::
::::

::::{abi-group}


:::{cpp:function} status_t BInputDevice::watch_input_devices(BMessenger target, bool start)
:::
Tells the Input Server to start or stop watching (as
{hparam}`start` is {cpp:enum}`true` or
{cpp:enum}`false`) for changes to the set of registered devices.
Change notifications are sent to {hparam}`target`. The set of messages that the
Server may send are listed in Input Server Messages.
:::{admonition} Note
:class: note
watch_input_devices() is not currently implemented.
:::
::::
