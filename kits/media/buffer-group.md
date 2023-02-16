:::{cpp:class} BBufferGroup
:::

# BBufferGroup

## Constructor and Destructor

::::{abi-group}
:::{cpp:function} BBufferGroup::BBufferGroup(size_t size, int32 numBuffers = 3, uint32 placement = B_ANY_ADDRESS, uint32 lock = B_FULL_LOCK)
:::

:::{cpp:function} BBufferGroup::BBufferGroup()
:::

:::{cpp:function} BBufferGroup::BBufferGroup(int32 numBuffers, const buffer_id * bufferList)
:::

The first form of the constructor creates a {hclass}`BBufferGroup` with
some number of {cpp:class}`BBuffer`s already allocated by the group. These
buffers will all live within a single Kernel Kit area, allocated by the
group. The group tries to allocate an area with properties specified by the
{hparam}`placement` and {hparam}`lock` arguments, large enough to hold
{hparam}`numBuffers` buffers of the specified {hparam}`size` (there may be
some padding added).

The second form of the constructor creates a {hclass}`BBufferGroup` but
doesn't create any buffers for it. You should add {cpp:class}`BBuffer`s to
the group before trying to use it.

The third form of the constructor creates a {hclass}`BBufferGroup` that
contains the specified list of buffers. {hparam}`bufferList` points to an
array of buffer IDs for the buffers to be controlled by the group, and
{hparam}`numBuffers` is the number of buffers in the list. This version of
the constructor isn't one you'll use very often.

Before using any buffers from a new {hclass}`BBufferGroup`, call
{cpp:func}`InitCheck() <BBufferGroup::InitCheck>` to determine if any
errors occurred while creating the group.
::::

::::{abi-group}
:::{cpp:function} BBufferGroup::~BBufferGroup()
:::

Releases all memory used by the {hclass}`BBufferGroup`, including the
{cpp:class}`BBuffer`s it controls.

Keep in mind that {cpp:func}`AddBuffer() <BBufferGroup::AddBuffer>` clones
the buffer area. This destructor releases the clones, but it's your
application's job to release the original area you added.

:::{admonition} Warning
:class: warning
Your node needs to delete the buffer group corresponding to any connection
that is disconnected or whenever the node is deleted. Until your node does
so, the other end of the connection will be blocked waiting for the buffer
group to be deleted.
:::
::::

## Member Functions

::::{abi-group}
:::{cpp:function} status_t BBufferGroup::AddBuffer(const buffer_clone_info& info)
:::

Given the {htype}`buffer_clone_info`, this function clones the buffer and
adds the clone to the {hclass}`BBufferGroup`. Normally you'll fill out the
{htype}`buffer_clone_info` structure yourself.

Since the buffer is cloned, you'll need to delete the original memory area
specified by the {htype}`buffer_clone_info` structure yourself when you're
no longer using it; the {hclass}`BBufferGroup` won't do it for you.

:::{admonition} Note
:class: note
You shouldn't pass the result of a {cpp:func}`BBuffer::CloneInfo` call to
this function, as doing so would create an "alias" buffer for the same
memory area. This is probably not the effect you want.
:::

:::{list-table}
---
header-rows: 1
align: left
widths: auto
---
-
	- Return Code

	- Description

-
	- {cpp:enumerator}`B_OK`.
	- No error adding the buffer to the group.
-
	- {cpp:enumerator}`B_NO_MEMORY`.
	- Couldn't clone the buffer into the {hclass}`BBufferGroup`'s address space.

:::
::::

::::{abi-group}
:::{cpp:function} status_t BBufferGroup::AddBuffersTo(BMessage* message, const char* name, bool needLock = true)
:::

Adds the group's buffers to the specified {hparam}`message`, storing them
in an array with the specified {hparam}`name`. If {hparam}`needLock` is
{cpp:expr}`true`, the {hclass}`BBufferGroup` is locked before performing
the operation, then unlocked when finished; otherwise, you guarantee that
the buffers won't go anywhere during the {hmethod}`AddBuffersTo()` call.

The buffers are added by ID number, and are therefore in {htype}`int32`
format.

:::{list-table}
---
header-rows: 1
align: left
widths: auto
---
-
	- Return Code

	- Description

-
	- {cpp:enumerator}`B_OK`.
	- No error adding the buffers to the message.

:::

Errors from {cpp:func}`AddInt32() <BMessage::AddInt32>`.
::::

::::{abi-group}
:::{cpp:function} status_t BBufferGroup::CountBuffers(int32* outBufferCount)
:::

Returns, in {hparam}`outBufferCount`, the number of buffers in the group.

:::{list-table}
---
header-rows: 1
align: left
widths: auto
---
-
	- Return Code

	- Description

-
	- {cpp:enumerator}`B_OK`.
	- The number of buffers was returned successfully.
-
	- {cpp:enumerator}`B_BAD_VALUE`.
	- Invalid {hparam}`outBufferCount` pointer

:::
::::

::::{abi-group}
:::{cpp:function} status_t BBufferGroup::GetBufferList(int32 listCount, BBuffer** outBuffers)
:::

Returns a list of all the buffers in the group. When calling
{hmethod}`GetBufferList()`, pass in {hparam}`outBuffers` a pointer to an
array of {cpp:class}`BBuffer` pointers that you want to be filled with
pointers to the group's buffers, and specify the number of elements in the
array in {hparam}`listCount`.

:::{list-table}
---
header-rows: 1
align: left
widths: auto
---
-
	- Return Code

	- Description

-
	- {cpp:enumerator}`B_OK`.
	- No errors.
-
	- {cpp:enumerator}`B_BAD_VALUE`.
	- {hparam}`listCount` is less than 1, or {hparam}`outBuffers` is
		{cpp:expr}`NULL`

:::
::::

::::{abi-group}
:::{cpp:function} status_t BBufferGroup::InitCheck()
:::

Returns the error code resulting from the construction of the
{hclass}`BBufferGroup`.

:::{list-table}
---
header-rows: 1
align: left
widths: auto
---
-
	- Return Code

	- Description

-
	- {cpp:enumerator}`B_OK`.
	- The new group was created successfully.
-
	- {cpp:enumerator}`B_ERROR`.
	- Couldn't allocate the buffers for the group.
-
	- Area errors.
	- See {ref}`Areas` in The Kernel Kit.

:::
::::

::::{abi-group}
:::{cpp:function} status_t BBufferGroup::ReclaimAllBuffers()
:::

If you pass a buffer group to some other {cpp:class}`BBufferProducer` but
pass {cpp:expr}`true` for {hparam}`willReclaim` in the
{cpp:func}`BBufferConsumer::SetOutputBuffersFor` call, you can later
reclaim the buffers into the {hclass}`BBufferGroup` by calling
{hmethod}`ReclaimAllBuffers()`.

{hmethod}`ReclaimAllBuffers()` will return {cpp:enumerator}`B_OK` when all
buffers are accounted for, or return an error if buffers can't be
reclaimed.

If you have buffers that reference some object that might go away (such as
a {cpp:class}`BBitmap`), you should call {hmethod}`ReclaimAllBuffers()` on
the group and delete the {hclass}`BBufferGroup` before that object goes
away.

:::{admonition} Note
:class: note
Before reclaiming your buffers, be sure to call
`BBufferConsumer::SetOutputBuffersFor(output, NULL)` to let the Media Kit
know your producer no longer has permission to use them. If you forget this
step, the producer will hang onto the buffers until it's deleted, and your
{hmethod}`ReclaimAllBuffers()` call will hang, possibly forever.
:::

:::{list-table}
---
header-rows: 1
align: left
widths: auto
---
-
	- Return Code

	- Description

-
	- {cpp:enumerator}`B_OK`.
	- All buffers reclaimed successfully.
-
	- {cpp:enumerator}`B_MEDIA_CANNOT_RECLAIM_BUFFERS`.
	- Some buffers couldn't be reclaimed.

:::
::::

::::{abi-group}
:::{cpp:function} BBuffer* BBufferGroup::RequestBuffer(size_t size, bigtime_t timeout = B_INFINITE_TIMEOUT)
:::

:::{cpp:function} status_t BBufferGroup::RequestBuffer(BBuffer* outBuffer, bigtime_t timeout = B_INFINITE_TIMEOUT)
:::

Returns a pointer to a {cpp:class}`BBuffer` of at least the specified size
that your {cpp:class}`BBufferProducer` subclass can put data into, then
pass on to a {cpp:func}`media_destination <media::destination>`. If there
isn't a suitable buffer available, the call will block until either a
buffer becomes available (in which case the buffer is returned) or the
specified {hparam}`timeout` is reached.

If you pass a {hparam}`timeout` value that's less than zero,
{hmethod}`RequestBuffer()` will return {cpp:expr}`NULL` immediately if
there's no buffer available, otherwise it will return a pointer to a buffer
you can use.

:::{admonition} Note
:class: note
In BeOS Release 4.5, the timeout is ignored (unless you specify a negative
value); {cpp:enumerator}`B_INFINITE_TIMEOUT` is always used, regardless of
the value you specify.
:::

{hmethod}`RequestBuffer()` doesn't use the buffer flags; instead, you can
look at the buffers within a {hclass}`BBufferGroup` to find a specific
buffer to request yourself, based on the value returned by
{cpp:func}`BBuffer::Flags` or {cpp:func}`BBuffer::SizeUsed`, for example.
Use the second form of {hmethod}`RequestBuffer()` to obtain a specific
buffer.

The first version of {hmethod}`RequestBuffer()` returns {cpp:expr}`NULL`
if no buffer can be obtained, and sets {hparam}`errno` to the appropriate
error code. The second version returns an appropriate error code.

:::{admonition} Warning
:class: warning
Don't call {hmethod}`RequestBuffer()` while an outstanding
{cpp:func}`ReclaimAllBuffers() <BBufferGroup::ReclaimAllBuffers>` request
is pending. To make sure that doesn't happen, a buffer producer should be
designed to not know about the old group anymore once
{cpp:func}`SetBufferGroup() <BBufferProducer::SetBufferGroup>` is called to
change its buffer group.
:::

:::{list-table}
---
header-rows: 1
align: left
widths: auto
---
-
	- Return Code

	- Description

-
	- {cpp:enumerator}`B_OK`.
	- No errors.
-
	- {cpp:enumerator}`B_MEDIA_BUFFERS_NOT_RECLAIMED`.
	- Buffers are in the process of being reclaimed.
-
	- {cpp:enumerator}`B_ERROR`.
	- A miscellaneous error occurred.

:::
::::

::::{abi-group}
:::{cpp:function} status_t BBufferGroup::RequestError()
:::

Returns the last {cpp:func}`RequestBuffer() <BBufferGroup::RequestBuffer>`
error. This is useful if {cpp:func}`RequestBuffer()
<BBufferGroup::RequestBuffer>` returns {cpp:expr}`NULL`.
::::

::::{abi-group}
:::{cpp:function} status_t BBufferGroup::WaitForBuffers()
:::

Waits until the currently pending buffer reclamation is finished, then
returns. If there isn't a buffer reclamation in progress, returns
immediately.

:::{list-table}
---
header-rows: 1
align: left
widths: auto
---
-
	- Return Code

	- Description

-
	- {cpp:enumerator}`B_OK`.
	- No errors.
-
	- Semaphore errors.
	- Unable to acquire the semaphore used to detect that buffer reclamation is
		done.

:::
::::
