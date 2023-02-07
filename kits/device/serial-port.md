# BSerialPort
## Constructor and Destructor
::::{abi-group}

:::{cpp:function} BSerialPort::BSerialPort()
:::

Initializes the {hclass}`BSerialPort` object to the following default values:

- Hardware flow control (see {cpp:func}`~BSerialPort::SetFlowControl`)
- A data rate of 19,200 bits per second (see {cpp:func}`~BSerialPort::SetDataRate`)
- A serial unit with 8 bits of data, 1 stop bit, and no parity (see {cpp:func}`~BSerialPort::SetDataBits`)
- Blocking with no time limit—an infinite timeout—for reading data (see {cpp:func}`~BSerialPort::Read`)

The new object doesn't represent any particular serial port. After
construction, it's necessary to open one of the ports by name.

The type of flow control must be decided before a port is opened. But the
other default settings listed above can be changed before or after
opening a port.

See also:
{cpp:func}`~BSerialPort::Open`

::::

::::{abi-group}

:::{cpp:function} virtual BSerialPort::~BSerialPort()
:::

Makes sure the port is closed before the object is destroyed.

::::

## Member Functions
::::{abi-group}

:::{cpp:function} void BSerialPort::ClearInput()
:::
:::{cpp:function} void BSerialPort::ClearOutput()
:::

These functions empty the serial port driver's input and output buffers,
so that the contents of the input buffer won't be read (by the
{cpp:func}`~BSerialPort::Read`
function) and the contents of the output buffer (after having been
written by
{cpp:func}`~BSerialPort::Write`)
won't be transmitted over the connection.

The buffers are cleared automatically when a port is opened.

::::

::::{abi-group}

:::{cpp:function} int32 BSerialPort::CountDevices()
:::
:::{cpp:function} status_t BSerialPort::GetDeviceName(int32 index, char* outName, size_t bufSize = B_OS_NAME_LENGTH)
:::

{hmethod}`CountDevices()` returns the number of serial ports on the computer.

{hmethod}`GetDeviceName()` returns the name of the device specified by the given
{hparam}`index`. The buffer pointed to by {hparam}`outName` is filled with the device name;
{hparam}`bufSize` indicates the size of the buffer.

The names returned by {hmethod}`GetDeviceName()` can be passed into the
{cpp:func}`~BSerialPort::Open`
function to open a device.

:::{list-table}
---
header-rows: 1
---
-
	- Return Code
	- Description
-
	- {cpp:enum}`B_OK`.
	- The name was returned successfully.
-
	- {cpp:enum}`B_BAD_INDEX`.
	- The specified {hparam}`index` is invalid.
-
	- {cpp:enum}`B_NAME_TOO_LONG`.
	- The device name is too long for the buffer.
:::
::::

::::{abi-group}

:::{cpp:function} bool BSerialPort::IsCTS()
:::

Returns {cpp:enum}`true` if the Clear to Send (CTS) pin is asserted,
and {cpp:enum}`false` if not.

::::

::::{abi-group}

:::{cpp:function} bool BSerialPort::IsDCD()
:::

Returns {cpp:enum}`true` if the Data Carrier Detect (DCD) pin is asserted, and
{cpp:enum}`false` if not.

::::

::::{abi-group}

:::{cpp:function} bool BSerialPort::IsDSR()
:::

Returns {cpp:enum}`true` if the Data Set Ready (DSR) pin is asserted, and {cpp:enum}`false` if
not.

::::

::::{abi-group}

:::{cpp:function} bool BSerialPort::IsRI()
:::

Returns {cpp:enum}`true` if the Ring Indicator (RI) pin is asserted, and
{cpp:enum}`false` if not.

::::

::::{abi-group}

:::{cpp:function} status_t BSerialPort::Open(const char* name)
:::
:::{cpp:function} void BSerialPort::Close()
:::

These functions open the {hparam}`name` serial port and close it again. To get a
serial port name, use the {hmethod}`GetDeviceName()` function

To be able to read and write data, the {hclass}`BSerialPort` object must have a
port open. It can open first one port and then another, but it can have
no more than one open at a time. If it already has a port open when
{hmethod}`Open()` is called, that port is closed before an attempt is made to open
the {hparam}`name` port. (Thus, both {hmethod}`Open()` and {hmethod}`Close()`
close the currently open port.)

{hmethod}`Open()` can't open the {hparam}`name` port if some other entity already has it open.
(If the {hclass}`BSerialPort` itself has {hparam}`name` open, {hmethod}`Open()`
first closes it, then opens it again.)

When a serial port is opened, its input and output buffers are emptied
and the Data Terminal Ready (DTR) pin is asserted.

:::{list-table}
---
header-rows: 1
---
-
	- Return Code
	- Description
-
	- positive integers (not 0).
	- Success.
-
	- {cpp:enum}`B_PERMISSION_DENIED`.
	- The port is already open.
-
	- {cpp:enum}`B_ERROR`.
	- The port couldn't be opened for some other reason.
:::
::::

::::{abi-group}

:::{cpp:function} ssize_t BSerialPort::Read(void* buffer, size_t maxBytes)
:::
:::{cpp:function} void BSerialPort::SetBlocking(bool shouldBlock)
:::
:::{cpp:function} status_t BSerialPort::SetTimeout(bigtime_t timeout)
:::

{hmethod}`Read()` takes incoming data from the serial port driver and places it in
the data {hparam}`buffer` provided. In no case will it read more than
{hparam}`maxBytes`—a value that should reflect the capacity of the buffer.
The input buffer of the driver, from which {hmethod}`Read()` takes the data, holds a
maximum of 2,024 bytes (2048 on Mac hardware). This function fails if the
{hclass}`BSerialPort` object doesn't have a port open.

The number of bytes that {hmethod}`Read()` will read before returning depends not
only on {hparam}`maxBytes`, but also on the {hparam}`shouldBlock`
flag and the {hparam}`timeout` set by the other two functions.

- {hmethod}`SetBlocking()` determines whether {hmethod}`Read()` should block and wait for {hparam}`maxBytes` of data to arrive at the serial port if that number isn't already available to be read. If the {hparam}`shouldBlock` flag is {cpp:enum}`true`, {hmethod}`Read()` will block. However, if {hparam}`shouldBlock` is {cpp:enum}`false`, {hmethod}`Read()` will take however many bytes are waiting to be read, up to the maximum asked for, then return immediately. If no data is waiting at the serial port, it returns without reading anything.
- The default {hparam}`shouldBlock` setting is {cpp:enum}`true`.
- {hmethod}`SetTimeout()` sets a time limit on how long {hmethod}`Read()` will block while waiting for data to arrive at the port's input buffer. The timeout is relevant to {hmethod}`Read()` only if the {hparam}`shouldBlock` flag is {cpp:enum}`true`. However, the time limit also applies to the {cpp:func}`~BSerialPort::WaitForInput` function, which always blocks, regardless of the {hparam}`shouldBlock` setting.
- There is no time limit if the timeout is set to {cpp:enum}`B_INFINITE_TIMEOUT`—{hmethod}`Read()` and {cpp:func}`~BSerialPort::WaitForInput` will block forever. Otherwise, the timeout is expressed in microseconds and can range from a minimum of 100,000 (0.1 second) through a maximum of 25,500,000 (25.5 seconds); differences less than 100,000 microseconds are not recognized; they're rounded to the nearest tenth of a second.
- The default timeout is {cpp:enum}`B_INFINITE_TIMEOUT`.

{hmethod}`Read()` returns…

:::{list-table}
---
header-rows: 1
---
-
	- Return Code
	- Description
-
	- non-negative integer.
	- Success; the value is the number of bytes that were read.
-
	- {cpp:enum}`B_INTERRUPTED`.
	- The operation was interrupted by a signal.
-
	- {cpp:enum}`B_FILE_ERROR`.
	- The {hclass}`BSerialPort` doesn't have a port open.
:::

{hmethod}`SetTimeout()` returns…

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
	- {cpp:enum}`B_BAD_VALUE`.
	- Out of range value passed to {hmethod}`SetTimeout()`.
:::

(Note that it's not considered an error if a timeout expires.)

::::

::::{abi-group}

:::{cpp:function} void BSerialPort::SetDataBits(data_bits count)
:::
:::{cpp:function} void BSerialPort::SetStopBits(stop_bits count)
:::
:::{cpp:function} void BSerialPort::SetParityMode(parity_mode mode)
:::
:::{cpp:function} data_bits BSerialPort::DataBits()
:::
:::{cpp:function} stop_bits BSerialPort::StopBits()
:::
:::{cpp:function} parity_mode BSerialPort::ParityMode()
:::
:::{code}
typedef enum { B_DATA_BITS_7, B_DATA_BITS_8 } data_bits
:::
:::{code}
typedef enum { B_STOP_BITS_1, B_STOP_BITS_2 } stop_bits
:::
:::{code}
typedef enum { B_EVEN_PARITY, B_ODD_PARITY, B_NO_PARITY } parity_mode
:::

These functions set and return characteristics of the serial unit used to
send and receive data.

- {hmethod}`SetDataBits()` sets the number of bits of data in each unit; the default is {cpp:enum}`B_DATA_BITS_8`.
- {hmethod}`SetStopBits()` sets the number of stop bits in each unit; the default is {cpp:enum}`B_STOP_BITS_2`.
- {hmethod}`SetParityMode()` sets whether the serial unit contains a parity bit and, if so, the type of parity used; the default is {cpp:enum}`B_NO_PARITY`.

::::

::::{abi-group}

:::{cpp:function} status_t BSerialPort::SetDataRate(data_rate bitsPerSecond)
:::
:::{cpp:function} data_rate BSerialPort::DataRate()
:::
:::{code}
typedef enum {
    B_0_BPS,     B_50_BPS,    B_75_BPS,    B_110_BPS,    B_134_BPS,
    B_150_BPS,   B_200_BPS,   B_300_BPS,   B_600_BPS,    B_1200_BPS,
    B_1800_BPS,  B_2400_BPS,  B_4800_BPS,  B_9600_BPS,   B_19200_BPS,
    B_31250_BPS, B_38400_BPS, B_57600_BPS, B_115200_BPS, B_230400_BPS
} data_rate
:::

These functions set and return the rate (in bits per second) at which
data is both transmitted and received.

The default data rate is {cpp:enum}`B_19200_BPS`. If the rate is set to 0 ({cpp:enum}`B_0_BPS`),
data will be sent and received at an indeterminate number of bits per
second.

{hmethod}`SetDataRate()` returns…

:::{list-table}
---
header-rows: 1
---
-
	- Return Code
	- Description
-
	- {cpp:enum}`B_OK`.
	- The rate was successfully set.
-
	- {cpp:enum}`B_NO_INIT`.
	- The {hclass}`BSerialPort` object doesn't have a port open.
-
	- {cpp:enum}`B_ERROR`.
	- The data rate couldn't be set for any other reason.
:::
::::

::::{abi-group}

:::{cpp:function} status_t BSerialPort::SetDTR(bool pinAsserted)
:::

Asserts the Data Terminal Ready (DTR) pin if the {hparam}`pinAsserted` flag is
{cpp:enum}`true`, and de-asserts it if the flag is {cpp:enum}`false`.
The function should always
return {cpp:enum}`B_OK`.

::::

::::{abi-group}

:::{cpp:function} void BSerialPort::SetFlowControl(uint32 mask)
:::
:::{cpp:function} uint32 BSerialPort::FlowControl()
:::

These functions set and return the type of flow control the driver should
use. There are four possibilities:

:::{list-table}
---
header-rows: 1
---
-
	- Constant
	- Description
-
	- {cpp:enum}`B_SOFTWARE_CONTROL`
	- Control is maintained through XON and XOFF characters inserted into the data stream.
-
	- {cpp:enum}`B_HARDWARE_CONTROL`
	- Control is maintained through the Clear to Send (CTS) and Request to Send (RTS) pins.
-
	- {cpp:enum}`B_SOFTWARE_CONTROL`+{cpp:enum}`B_HARDWARE_CONTROL`
	- Both of the above.
-
	- 0 (zero)
	- No control.
:::

{hmethod}`SetFlowControl()` should be called before a specific serial port is
opened. You can't change the type of flow control the driver uses in
midstream.

::::

::::{abi-group}

:::{cpp:function} status_t BSerialPort::SetRTS(bool pinAsserted)
:::

Asserts the Request to Send (RTS) pin if the {hparam}`pinAsserted` flag is {cpp:enum}`true`,
and de-asserts it if the flag is {cpp:enum}`false`. The function always returns {cpp:enum}`B_OK`.

::::

::::{abi-group}

:::{cpp:function} ssize_t BSerialPort::WaitForInput()
:::

Waits for input data to arrive at the serial port and returns the number
of bytes available to be read. If data is already waiting, the function
returns immediately.

This function doesn't respect the flag set by
{cpp:func}`~BSerialPort::SetBlocking`; it blocks
even if blocking is turned off for the
{cpp:func}`~BSerialPort::Read` function. However, it does
respect the timeout set by {cpp:func}`~BSerialPort::SetTimeout`. If the timeout expires before
input data arrives at the serial port, it returns 0.

::::

::::{abi-group}

:::{cpp:function} ssize_t BSerialPort::Write(const void* data, size_t numBytes)
:::

Writes up to {hparam}`numBytes` of data to the serial port's output buffer. This
function will be successful in writing the data only if the {hclass}`BSerialPort`
object has a port open. The output buffer holds a maximum of 512 bytes
(1024 on Mac hardware).

:::{list-table}
---
header-rows: 1
---
-
	- Return Code
	- Description
-
	- non-negative integer.
	- Success; the value is the number of bytes that were written.
-
	- {cpp:enum}`B_INTERRUPTED`.
	- The operation was interrupted by a signal.
-
	- {cpp:enum}`B_FILE_ERROR`.
	- The {hclass}`BSerialPort` doesn't have a port open.
:::
::::
