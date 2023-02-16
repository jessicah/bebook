:::{cpp:class} BNetDebug
:::

# BNetDebug

## Static Functions

::::{abi-group}
:::{cpp:function} static void BNetDebug::Dump(const char* data, size_t size, const char* title) const
:::

Dumps {hparam}`size` bytes of raw {hparam}`data` to stderr. The dump is
prefaced by the given {hparam}`title`. The text is only output if debug
output is currently enabled.
::::

::::{abi-group}
:::{cpp:function} static void BNetDebug::Enable(bool enable)
:::

:::{cpp:function} static bool BNetDebug::IsEnabled()
:::

{hmethod}`Enable()` enables debug output if {hparam}`enable` is
{cpp:expr}`true`, otherwise it disables debug output.

{hmethod}`IsEnabled()` reports the current state of debug output.
::::

::::{abi-group}
:::{cpp:function} static void BNetDebug::Print(const char* message)
:::

Prints the specified {hparam}`message` to stderr, if debug output is
currently enabled.
::::
