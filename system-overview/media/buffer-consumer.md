# BBufferConsumer

{cpp:class}`BBufferConsumer` is the counterpart to the
{cpp:class}`BBufferProducer` class—it receives {cpp:class}`BBuffer`s from
the {cpp:class}`BBufferProducer`s that are connected to it, manipulates
them in some fashion (either by altering the contents of the buffer or by
playing the buffer's data to the speakers or to the screen), and possibly
then passes them along to another {cpp:class}`BBufferConsumer` (if the node
also inherits from {cpp:class}`BBufferProducer`).

:::{admonition} Note
:class: note
The functions in this class aren't called by applications or by other
nodes; they're called exclusively by the Media Kit to control and obtain
information about a buffer consumer.
:::

A {cpp:class}`BBufferConsumer` publishes certain inputs, identified by
{cpp:func}`media_destination <media::destination>` structures, on which
connections may be requested by a client application.

## Dealing With Multiple Time Sources

Sometimes you'll find that the producer that's sending buffers to your
{cpp:class}`BBufferConsumer` is using a different time source than you are.
It's relatively easy to cope with this situation—you just have to be aware
that it can occur and compensate when it does:

:::{code} cpp
bigtime_t time;
media_node producerNode;
BTimeSource *producerTimeSource;
media_node_id producerTSID = buffer->Header()->time_source;

if (producerTSID != myTSID) {
   roster->GetNodeFor(producerTSID, &producerNode);
   producerTimeSource = roster->MakeTimeSourceFor(&producerNode);
   time = buffer->Header()->start_time;
   time = producerTimeSource->RealTimeFor(time, myLatency);
   time = myTimeSource->PerformanceTimeFor(time);
}
else {
   time = buffer->Header()->start_time;
:::

After this code has executed, time contains the start time for the buffer,
in your node's time base.

You should probably, for performance's sake, cache the producer's time
source the first time {cpp:func}`BufferReceived()
<BBufferConsumer::BufferReceived>` is called.
