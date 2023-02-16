# BMenuField

A {cpp:class}`BMenuField` object displays a labeled pop-up menu. It's a
simple object that employs a {cpp:class}`BMenuBar` object to control a
{cpp:class}`BMenu`. All it adds to what a {cpp:class}`BMenuBar` can do on
its own is a label and a more control-like user interface that includes
keyboard navigation.

The functions defined in this class resemble those of a
{cpp:class}`BControl` ({cpp:func}`SetLabel() <BMenuField::SetLabel>`,
{cpp:func}`IsEnabled() <BMenuField::IsEnabled>`), especially a BTextControl
({cpp:func}`SetDivider() <BMenuField::SetDivider>`, {cpp:func}`Alignment()
<BMenuField::Alignment>`). However, unlike a real {cpp:class}`BControl`
object, a {cpp:class}`BMenuField` doesn't maintain a current value and it
can't be invoked to send a message. All the control work is done by items
in the {cpp:class}`BMenu`.
