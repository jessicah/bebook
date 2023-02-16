# BBuffer

A {cpp:class}`BBuffer` references a chunk of shared memory where media
data can be passed between applications and nodes. The control header for
these buffers is passed through the use of a safer IPC mechanism, but the
actual data these headers represent typically require a high data rate, and
for the sake of maximizing performance, shared memory is the method by
which the buffers are managed.

{cpp:class}`BBuffer`s originate at some {cpp:class}`BBufferProducer`,
which has a {cpp:class}`BBufferGroup` that acts as a source of
{cpp:class}`BBuffer`s (see
{cpp:func}`BBufferConsumer::SetOutputBuffersFor`). {cpp:class}`BBuffer`s
are sent through all participating nodes, possibly being sent down a long
chain—much like a bucket brigade—until finally the node arrives at a node
that chooses not to pass along the {cpp:class}`BBuffer` any further, at
which the buffer's {cpp:func}`Recycle() <BBuffer::Recycle>` function is
called to return the buffer to the {cpp:class}`BBufferGroup`'s store, where
it gets reused by another batch of data.

An application or custom node can set up {cpp:class}`BBuffer`s that
reference a specific area of memory, such as a low-level driver buffer, a
{cpp:class}`BBitmap`, or a {cpp:class}`BDirectWindow`'s area of a frame
buffer. This ability can provide for great optimization by avoiding
unnecessary copy operations.

The {cpp:class}`BSmallBuffer` class, derived from {cpp:class}`BBuffer`, is
used for very small buffers; they don't go in {cpp:class}`BBufferGroup`s,
and get handled specially to optimize performance.

:::{admonition} Warning
:class: warning
{cpp:class}`BBuffer` should never be subclassed, since they're mostly
owned and managed by the Media Server. Even if you create your own
{cpp:class}`BBuffer`, once you've called
{cpp:func}`BBufferConsumer::SetOutputBuffersFor`, the "same" buffer
received back by your {cpp:class}`BBufferConsumer` may actually be another
instance of the {cpp:class}`BBuffer` class.
:::
