:::{cpp:class} BContinuousParameter
:::

# BContinuousParameter

## Constructor and Destructor

You never create or delete a {hclass}`BContinuousParameter` object
yourself. Use the appropriate {cpp:class}`BParameterGroup` functions to
create these objects and add them to groups.

## Member Functions

::::{abi-group}
:::{cpp:function} void BContinuousParameter::GetResponse(response* response, float* factor, float* offset)
:::

:::{cpp:function} void BContinuousParameter::SetResponse(response response, float factor, float offset)
:::

{hmethod}`GetResponse()` returns in {hparam}`response`, {hparam}`factor`,
and {hparam}`offset` the response type, factor, and offset currently in
effect for the {hclass}`BContinuousParameter`.

{hmethod}`SetResponse()` sets these values.

The {hparam}`response` describes how the {hclass}`BContinuousParameter`'s
value is displayed to me the user. For example, if your parameter is
polynomial in scale, you may wish to record only the base value, and let
the {hclass}`BContinuousParameter` handle presenting the value to the user
as a polynomial by raising the value to the power specified by
{hparam}`factor` before displaying the value on the screen.

The {hparam}`offset` is added to the value after the transformation
specified by response is computed, but before displaying the value.

If you wish the displayed value to be v2+1, you would use the following
call:

:::{code} cpp
SetResponse(B_POLYNOMIAL, 2.0, 1.0);
:::

:::{admonition} Note
:class: note
The mapping specified by these functions is only used for controls that
display the current value of the control. The default system theme doesn't
currently display this information. Since this information is only used for
display purposes, you will still have to handle (as appropriate for your
needs) mapping between the value of the control and the parameter value it
represents.

For example, a {hclass}`BContinuousParameter` that selects a frequency
between 20 Hz and 20,000 Hz might use a range from 0 to 3, with an exponent
base of 10 and a multiplication factor of 20. In this case, the parameter
will receive values from 0.0 to 3.0, which the UI control knows to map to
the values 20 through 20,000 for display purposes.
:::
::::

::::{abi-group}
:::{cpp:function} float BContinuousParameter::MaxValue()
:::

Returns the maximum possible value the {hclass}`BContinuousParameter` can
take, which was specified when the control was created. The value is in the
units specified when the control was created, such as "dB" or "Hz."
::::

::::{abi-group}
:::{cpp:function} float BContinuousParameter::MinValue()
:::

Returns the minimum possible value the {hclass}`BContinuousParameter` can
take, which was specified when the object was created. The value is in the
units specified when the object was created, such as "dB" or "Hz."
::::

::::{abi-group}
:::{cpp:function} float BContinuousParameter::ValueStep()
:::

Returns the granularity of values between {hmethod}`MinValue()` and
{hmethod}`MaxValue()` supported by the hardware.
::::

::::{abi-group}
:::{cpp:function} virtual type_code BContinuousParameter::ValueType()
:::

Return a {htype}`type_code` indicating the data type of the control's
value; by default, this is {cpp:enumerator}`B_FLOAT_TYPE`.
::::

## Constants

### response

Declared in: media/ParameterWeb.h

:::{list-table}
---
header-rows: 1
align: left
widths: auto
---
-
	- Constant

	- Description

-
	- {cpp:enumerator}`B_LINEAR`.
	- For every unit of change in the parameter's value, the displayed value
		also changes by 1. The factor should be 1.

		Indicates that the user interface will display the parameter's value
		as-is.
-
	- {cpp:enumerator}`B_POLYNOMIAL`.
	- The {hparam}`factor` is a power to which the control's value is raised
		before being displayed.

		Displays the parameter's value raised to the factor power. For instance,
		if factor is 2, the displayed value would be the parameter's value squared.
-
	- {cpp:enumerator}`B_EXPONENTIAL`.
	- The {hparam}`factor` is the base; the displayed value is the factor raised
		to the power of the parameter's value.

		Displays the factor raised to the power of the parameter's value. If the
		parameter's value is 3 and the factor is 2, the displayed value would be 23
		or 8.
-
	- {cpp:enumerator}`B_LOGARITHMIC`.
	- The {hparam}`factor` is the base; the displayed value is the base factor
		logarithm of the parameter's value.

		Displays the base factor logarithm of the parameter's value; if the factor
		is 10 and the parameter's value is 3, the displayed value would be
		log10(3).

:::
