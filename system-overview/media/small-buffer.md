# BSmallBuffer

The {cpp:class}`BSmallBuffer` class provides small, efficient buffers for
MIDI and other small packet-based media types.

To use {cpp:class}`BSmallBuffer`s, create a {cpp:class}`BSmallBuffer`,
then fill it with up to {cpp:func}`SmallBufferSizeLimit()
<BSmallBuffer::SmallBufferSizeLimit>` bytes of data. Then call
{cpp:func}`SendBuffer() <BBufferProducer::SendBuffer>`. You can then
immediately reuse the buffer.

How is this possible? {cpp:class}`BSmallBuffer`s don't go in buffer
groups. The receiver immediately either processes the buffer (if it's time)
or caches it until it's needed, then recycles the buffer.

:::{admonition} Note
:class: note
If you're writing a node, and receive a buffer with the
{cpp:enumerator}`B_SMALL_BUFFER` flag set, you must recycle the buffer in
your {cpp:func}`BufferReceived() <BBufferConsumer::BufferReceived>`
function.
:::
