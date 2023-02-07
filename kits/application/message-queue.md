# BMessageQueue
## Constructor and Destructor
::::{abi-group}

:::{cpp:function} BMessageQueue::BMessageQueue()
:::

Creates an empty {hclass}`BMessageQueue` object.

::::

::::{abi-group}

:::{cpp:function} virtual BMessageQueue::~BMessageQueue()
:::
Deletes all the objects in the queue and all the data structures used
to manage the queue.
::::

## Member Functions
::::{abi-group}

:::{cpp:function} void BMessageQueue::AddMessage(BMessage* message)
:::
:::{cpp:function} void BMessageQueue::RemoveMessage(BMessage* message)
:::

{hmethod}`AddMessage()` adds message to the far end of the
queue. {hmethod}`RemoveMessage()` removes a particular
message from the queue and deletes it.

::::

::::{abi-group}

:::{cpp:function} int32 BMessageQueue::CountMessages() const
:::
:::{cpp:function} bool BMessageQueue::IsEmpty() const
:::
{hmethod}`CountMessages()` returns the number of
messages currently in the queue.
{hmethod}`IsEmpty()` returns {cpp:enum}`true` if the
object doesn't contain any messages, and {cpp:enum}`false`
otherwise.
::::

::::{abi-group}

:::{cpp:function} BMessage* BMessageQueue::FindMessage(int32 index) const
:::
:::{cpp:function} BMessage* BMessageQueue::FindMessage(uint32 what, int32 index = 0) const
:::
{hmethod}`FindMessage()` returns a pointer to the
{hparam}`index`'th
{cpp:class}`BMessage` in the
queue, where index 0 signifies the message that's been in the queue the
longest. The second version lets you specify a {hparam}`what`
field value; in this case, only messages that match the {hparam}`what` argument are
counted. If no message matches the criteria, the functions return
{cpp:enum}`NULL`.

The message is not removed from the message queue.

::::

::::{abi-group}

:::{cpp:function} bool BMessageQueue::Lock()
:::
:::{cpp:function} void BMessageQueue::Unlock()
:::
These functions lock and unlock the {hclass}`BMessageQueue`,
so that another thread won't alter the contents of the queue while it's
being read. {hmethod}`Lock()` doesn't return until it has
the queue locked; it always returns {cpp:enum}`true`.
{hmethod}`Unlock()` releases the lock so that someone else
can lock it. Calls to these functions can be nested.
See also:
{cpp:func}`BLooper::Lock`
::::

::::{abi-group}

:::{cpp:function} BMessage* BMessageQueue::NextMessage()
:::
Removes and returns the oldest message from the queue. If the queue is
empty, the function returns {cpp:enum}`NULL`.
See also:
{cpp:func}`~BMessageQueue::FindMessage`
::::
