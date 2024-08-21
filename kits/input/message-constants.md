# Message Constants

This section describes the messages that your Input Server objects are
expected to create and send, and that they're expected to respond to.

## Input Device Event Messages

Declared in: app/AppDefs.h

This section lists the event messages that a
{cpp:class}`BInputServerDevice` is expected to create and send through its
{cpp:func}`~BInputServerDevice::EnqueueMessage()` function.

### Pointing Device Event Messages

- {cpp:enumerator}`B_MOUSE_DOWN`

- {cpp:enumerator}`B_MOUSE_UP`

- {cpp:enumerator}`B_MOUSE_MOVED`

Note that a pointing device isn't expected to send the
{cpp:enumerator}`B_MOUSE_ENTER_EXIT` message.

### Keyboard Device Event Messages

- {cpp:enumerator}`B_KEY_DOWN`

- {cpp:enumerator}`B_UNMAPPED_KEY_DOWN`

- {cpp:enumerator}`B_KEY_UP`

- {cpp:enumerator}`B_UMAPPED_KEY_UP`

- {cpp:enumerator}`B_MODIFIERS_CHANGED`

## Input Device Control Messages

Declared in: add-ons/input_server/InputServerDevice.h

This section lists the control messages that are defined by the BeOS for
pointing and keyboard devices. These are messages that appear in the
{cpp:func}`BInputServerDevice::Control()` function. Each control message is
identified by the value that appears as the command argument in the
{cpp:func}`~BInputDevice::Control()` function. None of the Be-defined
control messages use the additional {cpp:class}`BMessage` argument.

Control messages are used to notify input devices of downstream requests.
For example, when the user changes the mouse speed, a
{cpp:enumerator}`B_MOUSE_SPEED_CHANGED` command is sent back upstream. It's
expected that an input device that receives this message will tune
subsequent event messages that it generates to match the requested mouse
speed.

The messages listed below are defined by the BeOS; you can send custom
control messages back upstream through the {hmethod}`BInput::Control()`
function. Of course, this is only effective if you install a custom input
device that can handle the messages.

Note that the Be-defined control messages ask a device to set parameters
(such as mouse speed), but they never ask a device for the value of a
parameter. For example, a pointing device is never asked what the mouse
speed is. This is because the Input Server maintains the state of the
keyboard and pointing device environments and can answer these requests
itself.

Furthermore, the Be-defined control messages don't contain the value of the
parameter that's being set. For example, the
{cpp:enumerator}`B_MOUSE_SPEED_CHANGED` message doesn't contain the
requested mouse speed. The input device must ask the Input Server for the
new value through a global function ({cpp:func}`get_mouse_speed()`, in this
case). The functions that correspond to the messages are listed in the
descriptions below.

### Pointing Device Control Messages

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
	- {cpp:enumerator}`B_CLICK_SPEED_CHANGED`
	- Requests that the receiver change the mouse double-click speed to the value
		retrieved through {cpp:func}`get_click_speed()`.
-
	- {cpp:enumerator}`B_MOUSE_MAP_CHANGED`
	- Requests that the receiver change the mouse map (the correspondence between
		physical mouse buttons and the {cpp:enumerator}`B_PRIMARY_MOUSE_BUTTON`,
		et. al., constants) to the map retrieved through
		{cpp:func}`get_mouse_map()`.
-
	- {cpp:enumerator}`B_MOUSE_SPEED_CHANGED`
	- Requests that the receiver change the mouse speed to the value retrieved
		through {cpp:func}`get_mouse_speed()`.
-
	- {cpp:enumerator}`B_MOUSE_TYPE_CHANGED`
	- Requests that the receiver change the mouse type (the number of buttons) to
		the type retrieved through {cpp:func}`get_mouse_type()`.

:::

### Keyboard Device Control Messages

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
	- {cpp:enumerator}`B_KEY_LOCKS_CHANGED`
	- Requests that the receiver change the state of the locked keys (caps lock,
		num lock, etc.). To get the desired state of the locking keys, read the
		states out of the key map returned by {cpp:func}`get_key_map()`.
-
	- {cpp:enumerator}`B_KEY_MAP_CHANGED`
	- Requests that the receiver change the keyboard's key map—the mapping
		between physical keys and the character codes they generate. The new key
		map is returned by {cpp:func}`get_key_map()`.
-
	- {cpp:enumerator}`B_KEY_REPEAT_DELAY_CHANGED`
	- Requests that the receiver change the delay before a held key starts
		generating repeated characters to the value retrieved through
		{cpp:func}`get_key_repeat_delay()`.
-
	- {cpp:enumerator}`B_KEY_REPEAT_RATE_CHANGED`
	- Requests that the receiver change the speed at which a held key generates
		repeated characters to the value retrieved through
		{cpp:func}`get_key_repeat_rate()`.

:::

### Device Monitoring

The {cpp:func}`watch_input_devices()` function lets you ask the Input
Server to send you a message when a device starts or stops, or when the set
of registered devices changes. These "device monitoring" notifications are
sent to the target specified in the function. The command constant is
always {cpp:enumerator}`B_INPUT_DEVICES_CHANGED.` The {hparam}`be:opcode`
field will be one of:

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
	- {cpp:enumerator}`B_INPUT_DEVICE_ADDED`
	- An input device has been added to the system.
-
	- {cpp:enumerator}`B_INPUT_DEVICE_REMOVED`
	- An input device has been removed from the system.
-
	- {cpp:enumerator}`B_INPUT_DEVICE_STARTED`
	- An input device has been started.
-
	- {cpp:enumerator}`B_INPUT_DEVICE_STOPPED`
	- An input device has been stopped.

:::

### Input Method Events

Active input methods send input method events
({cpp:enumerator}`B_INPUT_METHOD_EVENT` messages) downstream to application
views to help integrate the method's work with the view's display. Inside
each {cpp:enumerator}`B_INPUT_METHOD_EVENT` message is a
{hparam}`be:opcode` field indicating the type of input method event:

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
	- {cpp:enumerator}`B_INPUT_METHOD_CHANGED`
	- Sent whenever the user changes the text during an input transaction.
-
	- {cpp:enumerator}`B_INPUT_METHOD_LOCATION_REQUEST`
	- Sent whenever the input method needs to know the on-screen locations of
		characters in the input transaction.
-
	- {cpp:enumerator}`B_INPUT_METHOD_STARTED`
	- Sent when a new input transaction is beginning.
-
	- {cpp:enumerator}`B_INPUT_METHOD_STOPPED`
	- Sent when an input transaction is completed.

:::
