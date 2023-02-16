# BTimeSource

The {cpp:class}`BTimeSource` class represents a clock to which nodes can
be slaved. By slaving all your nodes to a single master time source, they
can be kept in sync with each other.

If a node can, either by design or as a side benefit of the underlying
hardware, provide reliable timing services, it might make sense for it to
be derived from {cpp:class}`BTimeSource` as well as from whatever other
classes it might be derived from, such as {cpp:class}`BBufferProducer` or
{cpp:class}`BBufferConsumer`. Doing so will allow other nodes to be slaved
to your node's conception of time.

Note that although a {cpp:class}`BTimeSource` is implemented as a real
object (and is therefore not a purely abstract class), other nodes won't
call your {cpp:class}`BTimeSource`'s member functions directly—instead,
your {cpp:class}`BTimeSource` will provide data that other nodes will then
read.

There are invisible system implementations of the {cpp:class}`BTimeSource`
protocol that serve as stand-ins for other nodes, so if you call
{cpp:func}`BMediaRoster::SetTimeSourceFor` to make one of your nodes (which
is derived from {cpp:class}`BTimeSource`) a time source for some other
node, the other node might see a system stand-in object, not the actual
{cpp:class}`BTimeSource`-derived object.

This abstraction layer serves a valuable purpose: it enforces the desire
to prevent any two nodes from having to know anything about each other
beyond the Media Kit protocols defined in this chapter; this sort of
low-level interdependency is discouraged, because it decreases
interoperability.

## Keeping Time

Although it can be confusing at first, keep in mind that a node derived
from both {cpp:class}`BTimeSource` and {cpp:class}`BBufferProducer` (or
{cpp:class}`BBufferConsumer`)—which is therefore a time source, as well as
a producer or consumer of buffers—has to deal with two different time
concepts. As a {cpp:class}`BTimeSource`, it needs to understand requests in
real time, while as a {cpp:class}`BBufferProducer` or
{cpp:class}`BBufferConsumer`, it needs to accept requests in performance
time.

Real time refers to the actual passage of time, as reported by
{cpp:func}`system_time() <system::time>` or the
{cpp:func}`BTimeSource::RealTime` function. It's measured in microseconds.

Performance time runs in "time units" which aren't necessarily directly
related to real time. Since your code will have to deal with both kinds of
time, you need to be sure to convert between the two time systems when it's
necessary to do so. Use the {cpp:func}`BTimeSource::RealTimeFor` function
to do this.

For example, to calculate a timeout value, given a desired performance
time, and an estimated latency on the connection, you might use the
following code:

:::{code}
bigtime_t timeout = TimeSource()->RealTimeFor(performance_time,
         estimated_latency) - TimeSource()->RealTime();
:::

This code converts the {hparam}`performance_time` into the driving time
source's units, then subtracts the current real time, which results in the
desired timeout value.
