# BCursor
## Constructor and Destructor
::::{abi-group}

:::{cpp:function} BCursor::BCursor(const void* cursorData)
:::
:::{cpp:function} BCursor::BCursor(BMessage* archive)
:::

Initializes the new cursor object. If you specify a
non-{cpp:enum}`NULL` value for {hparam}`cursorData`,
the cursor is initialized with the specified cursor data.

If you specify a {cpp:enum}`NULL` value for
{hparam}`cursorData`, the cursor is useless; since this class
doesn't currently provide a means of setting the cursor data once the
object is instantiated, you're out of luck, so why bother?

{hclass}`BCursor` doesn't currently implement archiving, so
you shouldn't use the second form.

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

Not currently implemented; always returns {cpp:enum}`NULL`.

See also: {cpp:func}`BArchivable::Instantiate`,
{cpp:func}`BArchivable::Archive`

::::

## Constants