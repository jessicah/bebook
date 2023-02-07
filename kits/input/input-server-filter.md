# BInputServerFilter
## Constructor and Destructor
::::{abi-group}

:::{cpp:function} BInputServerFilter::BInputServerFilter()
:::
Creates a new {hclass}`BInputServerFilter` object. You can initialize the
object—set initial values, spawn threads, etc.—either here or
in the
{cpp:func}`~BInputServerFilter::InitCheck`
function, which is called immediately after the constructor.
::::

::::{abi-group}

:::{cpp:function} BInputServerFilter::BInputServerFilter()
:::
Deletes the {hclass}`BInputServerFilter` object. The
destructor is invoked by the Input Server only—you never delete a
{hclass}`BInputServerFilter` object from your own code. If
this object has spawned its own threads or allocated memory on the heap, it
must clean up after itself here.
::::

## Hook Functions
::::{abi-group}

:::{cpp:function} virtual filter_result BInputServerFilter::Filter(BMessage* message, BList* outList)
:::
The {hmethod}`Filter()` hook function is invoked by the Input Server to filter the
in-coming message. You can discard the message, allow it to pass
downstream (as is or modified), or replace it with one or more other
messages:
- To discard message, implement {hmethod}`Filter()` to return {cpp:enum}`B_SKIP_MESSAGE` (don't delete the {cpp:class}`BMessage` yourself—it's owned by the Input Server).
- If you implement {hmethod}`Filter()` to return {cpp:enum}`B_DISPATCH_MESSAGE` (and if you leave {hparam}`outList` unchanged), {hparam}`message` is allowed to continue downstream. You're allowed to modify (but not destroy or replace) {hparam}`message`.
- To replace {hparam}`message`, place one or more {cpp:class}`BMessage` in {hparam}`outList` and return {cpp:enum}`B_DISPATCH_MESSAGE`. {hparam}`message` is discarded; the messages in {hparam}`outList` are passed downstream in the order that they appear in the list. The Input Server owns all of the messages you pass back in {hparam}`outList`, so don't delete them yourself. Note that if you want to include {hparam}`message` in {hparam}`outList`, you must copy the object before adding it to the list.

The default implementation returns
{cpp:enum}`B_DISPATCH_MESSAGE` without modifying the
message.
::::

::::{abi-group}

:::{cpp:function} virtual status_t BInputServerFilter::InitCheck()
:::
Invoked by the Input Server immediately after the object is constructed
to test the validity of the initialization. If the object is properly
initialized (i.e. all required resources are located or allocated), this
function should return {cpp:enum}`B_OK`. If the object returns
non-{cpp:enum}`B_OK`, the object
is deleted and the add-on is unloaded.
The default implementation returns {cpp:enum}`B_OK`.
::::

## Member Functions
::::{abi-group}

:::{cpp:function} status_t BInputServerFilter::GetScreenRegion(BRegion* region) const
:::
The {hmethod}`GetScreenRegion()` function returns the
screen's region in {hparam}`region`. This is the most
efficient way for an input filter to get the screen's region. The system
screen saver's input filter uses this for its
"sleep now"/"sleep never" corners.
{hmethod}`GetScreenRegion()` returns
{cpp:enum}`B_OK`.
::::
