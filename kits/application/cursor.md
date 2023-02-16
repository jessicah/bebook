:::{cpp:class} BCursor
:::

# BCursor

## Constructor and Destructor

::::{abi-group}
:::{cpp:function} BCursor::BCursor(const void* cursorData)
:::

:::{cpp:function} BCursor::BCursor(BMessage* archive)
:::

Initializes the new cursor object. If you specify a non-{cpp:expr}`NULL`
value for {hparam}`cursorData`, the cursor is initialized with the
specified cursor data.

If you specify a {cpp:expr}`NULL` value for {hparam}`cursorData`, the
cursor is useless; since this class doesn't currently provide a means of
setting the cursor data once the object is instantiated, you're out of
luck, so why bother?

{hclass}`BCursor` doesn't currently implement archiving, so you shouldn't
use the second form.
::::

::::{abi-group}
:::{cpp:function} virtual BCursor::~BCursor()
:::

Releases any resources used by the cursor.
::::

## Static Functions

::::{abi-group}
:::{cpp:function} static BArchivable* BCursor::Instantiate(BMessage* archive)
:::

Not currently implemented; always returns {cpp:expr}`NULL`.

See also: {cpp:func}`BArchivable::Instantiate`,
{cpp:func}`BArchivable::Archive`
::::

## Constants









Declared in: app/AppDefs.h

:::{code} c
const unsigned char B_HAND_CURSOR[]
const unsigned char B_I_BEAM_CURSOR[]
:::

These constants contain all the data needed to set the cursor to the
default hand image or to the standard I-beam image for text selection.

:::{code} cpp
const BCursor* B_CURSOR_SYSTEM_DEFAULT
const BCursor* B_CURSOR_I_BEAM
:::

The second two constants are {cpp:class}`BCursor` objects and produce the
same cursors the first two constants.

See also: {cpp:func}`BApplication::SetCursor`
