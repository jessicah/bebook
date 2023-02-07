# BInputServerDevice
## Constructor and Destructor
::::{abi-group}

:::{cpp:function} BInputServerDevice::BInputServerDevice()
:::
Creates a new BInputServerDevice object. You can initialize your
object—set initial values, spawn (but not necessarily resume; do
that in {cpp:func}`~BInputServerDevice::Start`)
threads, open drivers, etc.—either here or in the
{cpp:func}`~BInputServerDevice::InitCheck`
function, which is called immediately after the constructor.
::::

::::{abi-group}

:::{cpp:function} BInputServerDevice::BInputServerDevice()
:::
Deletes the {hclass}`BInputServerDevice` object. The
destructor is invoked by the Input Server only—you never delete a
{hclass}`BInputServerDevice` object from your own code. When
the destructor is called, the object's devices will already be unregistered
and {cpp:func}`~BInputServerDevice::Stop`
will already have been called. If this object spawned its own threads or
allocated memory on the heap, it must clean up after itself here.
::::

## Hook Functions
::::{abi-group}

:::{cpp:function} status_t BInputServerDevice::Control(const char* name, voi* cookie, uint32 command, BMessage* message)
:::
The {hmethod}`Control()` hook function is invoked by the Input Server to send an
input device control message or a Node Monitor message to this object.
name and cookie are the readable name and pointer-to-whatever-you-want
that you used when registering the device (with the
{cpp:func}`~BInputServerDevice::RegisterDevices`
function).
:::{admonition} Warning
:class: warning
The function's return value is ignored.
:::
Input Device Control MessagesAn input device control message is sent when a downstream change needs to be propagated to an input device. For example, when the user resets the mouse speed (through the Mouse preference), a {cpp:enum}`B_MOUSE_SPEED_CHANGED` control message is sent to all objects that have registered a {cpp:enum}`B_POINTING_DEVICE` device (see {cpp:func}`~BInputServerDevice::RegisterDevices`). {hparam}`name` and {hparam}`cookie` identify the device that this message applies to. The control message itself is represented by the {hparam}`command` constant, optionally supplemented by {hparam}`message`.See "Input Device Control Messages" for a list of the control messages that the BeOS defines, and instructions for how to respond to them. An application can send a custom control message through a {cpp:class}`BInputDevice` object; see {cpp:func}`BInputDevice::Control` for details.
Node Monitor MessagesA Node Monitor message is sent if an entry is added to or removed from one of the device directories that the object is monitoring, as set through {cpp:func}`~BInputServerDevice::StartMonitoringDevice`. In this case, {hparam}`name` and {hparam}`cookie` are {cpp:enum}`NULL`, {hparam}`command` is {cpp:enum}`B_NODE_MONITOR`, and {hparam}`message` describes the file that was added or deleted. The {hparam}`message`'s opcode field will be {cpp:enum}`B_ENTRY_CREATED` or {cpp:enum}`B_ENTRY_REMOVED` (or, potentially but nonsensically, {cpp:enum}`B_ENTRY_MOVED`). For instructions on how to read these messages, see "The Node Monitor" in the Storage Kit (or click on the opcode constants).
::::

::::{abi-group}

:::{cpp:function} virtual status_t BInputServerDevice::InitCheck()
:::
Invoked by the Input Server immediately after the object is constructed
to test the validity of the initialization. If the object is properly
initialized (i.e. all required resources are located or allocated), this
function should return {cpp:enum}`B_OK`.
{cpp:func}`~BInputServerDevice::Start`
will be invoked soon if you need to
do any extra initialization. If the object returns non-{cpp:enum}`B_OK`, the object
is deleted and the add-on is unloaded.
The default implementation returns {cpp:enum}`B_OK`.
::::

::::{abi-group}

:::{cpp:function} virtual status_t BInputServerDevice::Start(const char* name, void* cookie)
:::
:::{cpp:function} virtual status_t BInputServerDevice::Stop(const char* name, void* cookie)
:::
{hmethod}`Start()` is invoked by the Input Server to tell the object that it can
begin sending events for the registered device identified by the
arguments. The values of the arguments are taken from the
input_device_ref structure you used to register the device (see
{cpp:func}`~BInputServerDevice::RegisterDevices`).
If your object needs to resume a thread (spawned in the constructor, in
{cpp:func}`~BInputServerDevice::InitCheck`,
or here), this is the place to do it.
{hmethod}`Stop()` is invoked to tell the object to stop sending events for the
registered device. The device is not unregistered—you can still
receive {cpp:func}`~BInputServerDevice::Control`
messages for the device while it's stopped. You should
pause or kill any threads associated with the device (that were spawned
by this object) from here.
The return value (for both of these functions) is ignored.
::::

::::{abi-group}

:::{cpp:function} virtual status_t BInputServerDevice::SystemShuttingDown() const
:::
Tells the object that the Input Server is in the process of shutting
down. Unless something interrupts the shutdown, this notification will be
followed by a
{cpp:func}`~BInputServerDevice::Stop`
and delete, thus you don't have to do much from this
function (other than note that the end is near).
:::{admonition} Warning
:class: warning
The return value is ignored.
:::
::::

## Member Functions
::::{abi-group}

:::{cpp:function} status_t BInputServerDevice::EnqueueMessage(BMessage* message)
:::
Sends an event message to the Input Server, which passes it through the
input methods and input filters before sending it to the App Server. The
message you create should be appropriate for the action you're trying to
depict. For example, if the user presses a key, you should create and
send a {cpp:enum}`B_KEY_DOWN` message. A list of the system-defined event messages
that an input device is expected to create and send is given in
"Input Device Event Messages".
:::{list-table}
---
header-rows: 1
---
-
	- Return Code
	- Description
-
	- {cpp:enum}`B_OK`.
	- The message was sent.
-
	- Anything else.
	- The connection to the App Server has been broken—this isn't good, and you may want to check the {cpp:func}`~is::computer` function found in the Kernel Kit.
:::
::::

::::{abi-group}

:::{cpp:function} status_t BInputServerDevice::RegisterDevices(input_device_ref ** devices)
:::
:::{cpp:function} status_t BInputServerDevice::UnregisterDevices(input_device_ref ** devices)
:::
{hmethod}`RegisterDevices()` tells the Input Server that this object is responsible
for the listed devices. This means that when a control message is sent
back upstream, the message—which is tagged as being relevant for a
specific device, or type of device—will be forwarded (through the
{cpp:func}`~BInputServerDevice::Control`
hook) to the responsible {hclass}`BInputServerDevice` object(s).
Typically, you initially register your devices as part of the constructor
or
{cpp:func}`~BInputServerDevice::InitCheck`.
Registration is cumulative—each {hmethod}`RegisterDevices()`
call adds to the object's current list of devices.
{hmethod}`UnregisterDevices()` tells the Input Server that this object is no longer
responsible for the listed devices. The devices are automatically
unregistered when your object is deleted.
{hmethod}`RegisterDevices()` invokes
{cpp:func}`~BInputServerDevice::Start`
for each device in the devices list;
{hmethod}`UnregisterDevices()` invokes
{cpp:func}`~BInputServerDevice::Stop`.
For both functions, the devices list must be {cpp:enum}`NULL`-terminated, and the
caller retains ownership of the list and its contents.
Note that the BeOS currently only targets the device types when sending a
{cpp:func}`~BInputServerDevice::Control`
message. For example, let's say you've registered two pointing
devices and a keyboard:
:::{code}
status_t MyISDevice::InitCheck()
{
...
   input_device_ref **devices =
      (input_device_ref **)malloc(sizeof(*input_device_ref * 4));
   input_device_ref mouse1 = {"Mouse 1", B_POINTING_DEVICE,
                              (void *)this)};
   input_device_ref mouse2 = {"Mouse 2", B_POINTING_DEVICE,
                              (void *)this)};
   input_device_ref keyboard = {"Keyboard", B_KEYBOARD_DEVICE,
                              (void *)this)};
   devices[0] = &mouse1;
   devices[1] = &mouse2;
   devices[2] = &keyboard;
   devices[3] = NULL;
   RegisterDevices(devices);
   ...
}
:::
When the user fiddles with the Mouse preference (more specifically, if an
application calls
{cpp:func}`~set::mouse`
et. al.), this object will receive two
{cpp:func}`~BInputServerDevice::Control`
messages: one targets "Mouse 1", and the other targets
"Mouse 2". That's because the mouse and keyboard functions (as defined by
the BeOS and as used by the system preferences) know which type of device
to control, but they don't provide a means for more granular
identification. If you need a UI that identifies specific devices, you
have to create the UI yourself, and use a
{cpp:class}`BInputDevice` object to tune the
control messages that are sent back upstream.
:::{admonition} Warning
:class: warning
The functions don't let you un/register the same device definition
twice, and {hmethod}`RegisterDevices()` won't register a device that doesn't have a
name (although the name can be ""). However, the functions don't complain
about violations of these conditions as long as at least one definition
is properly formed.
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
	- At least one of the devices was registered.
-
	- {cpp:enum}`B_ERROR`.
	- None of the devices were registered.
:::
::::

::::{abi-group}

:::{cpp:function} status_t BInputServerDevice::StartMonitoringDevice(const char* deviceDir)
:::
:::{cpp:function} status_t BInputServerDevice::StopMonitoringDevice(const char* deviceDir)
:::
These are convenient covers for the
{ref}`Node Monitor`'s
{cpp:func}`~watch::node` and
{cpp:func}`~stop::watching`
functions. You use them to watch for physical devices
that are attached and detached, as indicated by changes to subdirectories
of the system device directory (/dev).
{hparam}`deviceDir` is the name of the device subdirectory that you want to watch.
The /dev/ root is automatically prepended; for example, if you want to
watch for new ps2 mice, you would pass
input/mouse/ps2 as the {hparam}`deviceDir`
name. The Node Monitor is told to look for changes to the directory
({cpp:enum}`B_WATCH_DIRECTORY` opcode). When an entry is added or removed, this
object receives a {cpp:enum}`B_NODE_MONITOR` message delivered to its
{cpp:func}`~BInputServerDevice::Control`
function.
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
	- Unspecified failure.
-
	- {cpp:enum}`B_NOT_A_DIRECTORY`.
	- You're trying to monitor a node that isn't a directory.
-
	- {cpp:enum}`B_BAD_VALUE`.
	- {hparam}`deviceDir` not found.
:::
::::
