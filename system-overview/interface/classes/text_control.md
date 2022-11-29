# BTextControl

A {cpp:class}`BTextControl` object displays a labeled text field that behaves like other control
devices. When the user presses certain keys after modifying the text in the field, it delivers a
message to a designated target.

There are two parts to the view: A static label on the left, which the user cannot modify, and an
editable field on the right, which behaves just like a one-line {cpp:class}`BTextView`. In fact, the
{cpp:class}`BTextControl` installs a {cpp:class}`BTextView` object as its child to handle editing
chores within this part of the view. It's this child view that responds to keyboard events for the
{cpp:class}`BTextControl` rather than the control object itself.

The child {cpp:class}`BTextView` must become the focus view for the window before the user can enter
or edit text in the field. If the user modifies the contents of the field and then causes the child
to cease being the focus view, the {cpp:class}`BTextControl` delivers a message to its target, just
like any other {cpp:class}`BControl` object when it's invoked. The message notifies the target that
the user has finished making changes to the text. (It doesn't matter what causes the change in
focus---a click in another text field, for example, or a {cpp:enum}`B_TAB` character that navigates
to another view.)

The {cpp:class}`BTextControl` is also invoked when the user types a {cpp:enum}`B_ENTER` character,
though this doesn't change the focus view. It selects all the text in the field.

You can arrange for another message---a "modification message"---to be sent when the usesr makes the
first change to the text after the child {cpp:class}`BTextView` has become the focus view (of after
{cpp:enum}`B_ENTER` caused all the text to be selected). This message notifies the target that
editing has begun.

Note that {cpp:class}`BTextControl`s only allow the user to edit a single line of text; newline
characters are automatically stripped from the text, if they're inserted.

Because the label is drawn by the {cpp:class}`BTextControl` itself and the editable text is drawn by
its child {cpp:class}`BTextView`, you can assign different properties (color or font, for example)
to each string. The {cpp:class}`BTextControl` has only one child; {cpp:func}`~BView::ChildAt()`
returns it when passed an index of 0.
