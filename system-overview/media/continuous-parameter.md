# BContinuousParameter

The {cpp:class}`BContinuousParameter` class represents parameters whose
values can vary along a continuous range. Examples include gain or
equalizer controls, turntable pitch controls, and the like.

The default system theme implements {cpp:class}`BContinuousParameter`s as
{cpp:class}`BSlider` controls.

Call {cpp:func}`BParameterGroup::MakeContinuousParameter` to create a
{cpp:class}`BContinuousParameter` control.
