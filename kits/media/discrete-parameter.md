:::{cpp:class} BDiscreteParameter
:::

# BDiscreteParameter

## Constructor and Destructor

You never create or delete a {hclass}`BDiscreteParameter` object yourself.
Instead, call the {cpp:func}`BParameterGroup::MakeDiscreteParameter`
function to create a {hclass}`BDiscreteParameter` within the desired
{cpp:class}`BParameterGroup`.

## Member Functions

::::{abi-group}
:::{cpp:function} status_t BDiscreteParameter::AddItem(int32 value, const char* name)
:::

Adds a new {hparam}`name`/{hparam}`value` pair to the list of possible
values the control can take. Whenever the selection named name is chosen,
the user interface application will send a value change message to the
control with the specified value.

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
	- The item was added successfully.
-
	- {cpp:enumerator}`B_NO_MEMORY`
	- Not enough memory to add the item to the list.

:::
::::

::::{abi-group}
:::{cpp:function} int32 BDiscreteParameter::CountItems()
:::

Returns the number of discrete values the control can take.
::::

::::{abi-group}
:::{cpp:function} const char* BDiscreteParameter::CountItems(int32 value)
:::

:::{cpp:function} int32 BDiscreteParameter::ItemValueAt(int32 value)
:::

These functions return the name and value of the item at the specified
index, where index ranges from 0 to {cpp:func}`CountItems()
<BDiscreteParameter::CountItems>`-1.

:::{admonition} Note
:class: note
Selection values aren't necessarily in any sort of order, nor are they
necessarily unique.
:::
::::

::::{abi-group}
:::{cpp:function} void BDiscreteParameter::MakeEmpty()
:::

Removes all items from the {hclass}`BDiscreteParameter`.
::::

::::{abi-group}
:::{cpp:function} void BDiscreteParameter::MakeItemsFromInputs()
:::

:::{cpp:function} void BDiscreteParameter::MakeItemsFromOutputs()
:::

These functions add all inputs or outputs as selections, where the input
or output's name is used as the item's name, and the input or output's
index number is used as the value of the item.

These shortcuts let you easily create the item lists for MUX-like
controls, which allow the user to choose one of a number of inputs or
outputs.

:::{admonition} Note
:class: note
It's important to note that the correct inputs and outputs must already be
connected to the parameter when you call either of these functions,
otherwise no items will be added, since the inputs and outputs aren't
there.
:::
::::

::::{abi-group}
:::{cpp:function} virtual type_code BDiscreteParameter::ValueType()
:::

Returns {cpp:enumerator}`B_INT32_TYPE`, which is the data type a
{hclass}`BDiscreteParameter`'s value is maintained in.
::::
