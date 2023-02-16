# BRefFilter

The {hclass}`BRefFilter` class lets you filter the items that a file panel
is about to display. This filtering is performed by the class' only
function, {cpp:func}`Filter() <BRefFilter::Filter>`. {cpp:func}`Filter()
<BRefFilter::Filter>` is a hook function; to use a {hclass}`BRefFilter`,
you have to create a derived class and implement the {cpp:func}`Filter()
<BRefFilter::Filter>` function.

To assign your {hclass}`BRefFilter` object to a file panel, you invoke
{cpp:class}`BFilePanel`'s {cpp:func}`SetRefFilter()
<BFilePanel::SetRefFilter>` function. (The {cpp:class}`BFilePanel`
constructor also lets you set the filter.) If you don't specifically assign
a filter, the file panel will not have one—there is no "default" ref filter
object. You maintain ownership of the {hclass}`BRefFilter` that you assign
to a file panel; the file panel doesn't delete or otherwise change your
object.

You can assign the same filter to more than file panel. However, the
{cpp:func}`Filter() <BRefFilter::Filter>` function isn't told which panel
it's being invoked for.
