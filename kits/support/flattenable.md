# BFlattenable

## Member Functions

::::{abi-group}
:::{cpp:function} virtual status_t Flatten(void* buffer, ssize_t numBytes) const = 0
:::
:::{cpp:function} virtual status_t Unflatten(type_code code, const void* buffer, ssize_t numBytes) = 0
:::

{hmethod}`Flatten()` is implemented by derived classes to write the object into the buffer. There are {hparam}`numBytes` bytes of memory available at the buffer address. If this isn't at least as much memory as the {cpp:func}`~BFlattenable::FlattenedSize()` function says is necessary, {hmethod}`Flatten()` should return an error. If successful, it should return {cpp:enum}`B_OK`.

{hmethod}`Unflatten()` is implemented by derived classes to set object values from {hparam}`numBytes` bytes of data taken from the {hparam}`buffer`. However, it should read the data only if the type {hparam}`code` it's passed indicates that the data is a type that it supports---that is, only if it's {cpp:func}`~BFlattenable::AllowsTypeCode()` function returns {cpp:expr}`true` for the code. If successful in reconstructing the object from the flattened data, {hmethod}`Unflatten()` should return {cpp:enum}`B_OK`. If not, it should return {cpp:enum}`B_ERROR` or a more descriptive error code.
::::

::::{abi-group}
:::{cpp:function} virtual ssize_t BFlattenable::FlattenedSize() const = 0
:::

Implemented by derived classes to return the amount of memory needed to hold the flattened object. This is the minimal amount that must be allocated and passed to {cpp:func}`~BFlattenable::Flatten()`.
::::

::::{abi-group}
:::{cpp:function} virtual type_code BFlattenable::TypeCode() const = 0
:::
:::{cpp:function} virtual bool BFlattenable::AllowsTypeCode(type_code code) const
:::

{hmethod}`TypeCode()` is implemented by derived classes to return the type code that identifies the class type. The code is used to identify an instance of the class in its flattened state, for example when it's added to a {cpp:class}`BMessage`.

{hmethod}`AllowsType()` returns {cpp:expr}`true` if the code it's passed matches the code returned by {hmethod}`TypeCode()` and {cpp:expr}`false` if not. It can be modified in derived classes to apply a more liberal standard---to allow more than one type code to identify the object.

See also: {cpp:func}`BMessage::AddData()`
::::
