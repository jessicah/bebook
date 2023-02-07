# Message Constants
## Input Device Event Messages
::::{abi-group}

- {cpp:func}`~B::MOUSE`
- {cpp:func}`~B::MOUSE`
- {cpp:func}`~B::MOUSE`

Note that a pointing device isn't expected to send the
{cpp:enum}`B_MOUSE_ENTER_EXIT` message.
::::

::::{abi-group}

- {cpp:enum}`B_KEY_DOWN`
- {cpp:enum}`B_UNMAPPED_KEY_DOWN`
- {cpp:enum}`B_KEY_UP`
- {cpp:enum}`B_UMAPPED_KEY_UP`
- {cpp:enum}`B_MODIFIERS_CHANGED`

::::

## Input Device Control Messages
::::{abi-group}

:::{list-table}
---
header-rows: 1
---
-
	- Constant
	- Description
-
	- {cpp:enum}`B_CLICK_SPEED_CHANGED`
	- Requests that the receiver change the mouse double-click speed to the value retrieved through {cpp:func}`~get::click`.
-
	- {cpp:enum}`B_MOUSE_MAP_CHANGED`
	- Requests that the receiver change the mouse map (the correspondence between physical mouse buttons and the {cpp:enum}`B_PRIMARY_MOUSE_BUTTON`, et. al., constants) to the map retrieved through {cpp:func}`~get::mouse`.
-
	- {cpp:enum}`B_MOUSE_SPEED_CHANGED`
	- Requests that the receiver change the mouse speed to the value retrieved through {cpp:func}`~get::mouse`.
-
	- {cpp:enum}`B_MOUSE_TYPE_CHANGED`
	- Requests that the receiver change the mouse type (the number of buttons) to the type retrieved through {cpp:func}`~get::mouse`.
:::
::::

::::{abi-group}

:::{list-table}
---
header-rows: 1
---
-
	- Constant
	- Description
-
	- {cpp:enum}`B_KEY_LOCKS_CHANGED`
	- Requests that the receiver change the state of the locked keys (caps lock, num lock, etc.). To get the desired state of the locking keys, read the states out of the key map returned by {cpp:func}`~get::key`.
-
	- {cpp:enum}`B_KEY_MAP_CHANGED`
	- Requests that the receiver change the keyboard's key map—the mapping between physical keys and the character codes they generate. The new key map is returned by {cpp:func}`~get::key`.
-
	- {cpp:enum}`B_KEY_REPEAT_DELAY_CHANGED`
	- Requests that the receiver change the delay before a held key starts generating repeated characters to the value retrieved through {cpp:func}`~get::key`.
-
	- {cpp:enum}`B_KEY_REPEAT_RATE_CHANGED`
	- Requests that the receiver change the speed at which a held key generates repeated characters to the value retrieved through {cpp:func}`~get::key`.
:::
::::

::::{abi-group}

The {cpp:func}`~watch::input`
function lets you ask the Input Server to send
you a message when a device starts or stops, or when the set of
registered devices changes. These "device monitoring" notifications are
sent to the target specified in the function. The command constant is
always {cpp:enum}`B_INPUT_DEVICES_CHANGED.`
The be:opcode field will be one of:
:::{list-table}
---
header-rows: 1
---
-
	- Constant
	- Description
-
	- {cpp:enum}`B_INPUT_DEVICE_ADDED`
	- An input device has been added to the system.
-
	- {cpp:enum}`B_INPUT_DEVICE_REMOVED`
	- An input device has been removed from the system.
-
	- {cpp:enum}`B_INPUT_DEVICE_STARTED`
	- An input device has been started.
-
	- {cpp:enum}`B_INPUT_DEVICE_STOPPED`
	- An input device has been stopped.
:::
::::

::::{abi-group}

Active input methods send input method events
({cpp:enum}`B_INPUT_METHOD_EVENT`
messages) downstream to application views to help integrate the method's
work with the view's display. Inside each
{cpp:enum}`B_INPUT_METHOD_EVENT` message is
a be:opcode field indicating the type of
input method event:
:::{list-table}
---
header-rows: 1
---
-
	- Constant
	- Description
-
	- {cpp:enum}`B_INPUT_METHOD_CHANGED`
	- Sent whenever the user changes the text during an input transaction.
-
	- {cpp:enum}`B_INPUT_METHOD_LOCATION_REQUEST`
	- Sent whenever the input method needs to know the on-screen locations of characters in the input transaction.
-
	- {cpp:enum}`B_INPUT_METHOD_STARTED`
	- Sent when a new input transaction is beginning.
-
	- {cpp:enum}`B_INPUT_METHOD_STOPPED`
	- Sent when an input transaction is completed.
:::
::::
