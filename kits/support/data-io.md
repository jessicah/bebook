# BDataIO

## Constructor and Destructor

::::{abi-group}
:::{cpp:function} BDataIO::BDataIO()
:::

Does nothing.
::::

::::{abi-group}
:::{cpp:function} virtual BDataIO::~BDataIO()
:::

Does nothing.
::::

## Member Functions

::::{abi-group}
:::{cpp:function} virtual ssize_t BDataIO::Read(void* buffer, size_t numBytes) = 0
:::

{hmethod}`Read()` is implemented by derived classes to copy {hparam}`numBytes` bytes of data from the object to the {hparam}`buffer`. It should return the number of bytes actually read, which may be 0, or an error code if something goes wrong.
::::

::::{abi-group}
:::{cpp:function} virtual ssize_t Write(const void* buffer, size_t numBytes) = 0
:::

{hmethod}`Write()` is implemented by derived classes to copy {hparam}`numBytes` bytes of data from the {hparam}`buffer` to the object. It should return the number of bytes actually written, which may be 0, or an error code if the operation fails.
::::
