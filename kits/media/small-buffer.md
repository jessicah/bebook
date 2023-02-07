# BSmallBuffer
## Constructor and Destructor
::::{abi-group}

:::{cpp:function} BSmallBuffer::BSmallBuffer()
:::
Constructor. Creates a small buffer that can hold up to
{cpp:func}`~BSmallBuffer::SmallBufferSizeLimit`
bytes.
::::

## Static Functions
::::{abi-group}

:::{cpp:function} size_t* BSmallBuffer::SmallBufferSizeLimit()
:::
Returns the maximum number of bytes a
{hclass}`BSmallBuffer` can contain.
::::
