# BScrollBar

A {cpp:class}`BScrollBar` object displays a vertical or horizontal scroll
bar that users can operate to scroll the contents of another view, a target
view. Scroll bars usually are grouped as siblings of the target view under
a common parent. That way, when the parent is resized, the target and
scroll bars can be automatically resized to match. (A companion class,
{cpp:class}`BScrollView`, defines just such a container view; a
{cpp:class}`BScrollView` object sets up the scroll bars for a target view
and makes itself the parent of the target and the scroll bars.)

## The Update Mechanism

{cpp:class}`BScrollBar`s are different from other views in one important
respect: All their drawing and event handling is carried out within the
Application Server, not in the application. A {cpp:class}`BScrollBar`
object doesn't receive {cpp:func}`Draw() <BView::Draw>` or
{cpp:func}`MouseDown() <BView::MouseDown>` notifications; the server
intercepts updates and interface messages that would otherwise be reported
to the {cpp:class}`BScrollBar` and handles them itself. As the user moves
the knob on a scroll bar or presses a scroll arrow, the Application Server
continuously refreshes the scroll bar's image on-screen and informs the
application with a steady stream of {cpp:enumerator}`B_VALUE_CHANGED`
messages.

The window dispatches these messages by calling the
{cpp:class}`BScrollBar`'s {cpp:func}`ValueChanged()
<BScrollBar::ValueChanged>` function. Each function call notifies the
{cpp:class}`BScrollBar` of a change in its value and, consequently, of a
need to scroll the target view.

Confining the update mechanism for scroll bars to the Application Server
limits the volume of communication between the application and server and
enhances the efficiency of scrolling. The application's messages to the
server can concentrate on updating the target view as its contents are
being scrolled, rather than on updating the scroll bars themselves.

## Value and Range

A scroll bar's value determines what the target view displays. The
assumption is that the left coordinate value of the target view's bounds
rectangle should match the value of the horizontal scroll bar, and the top
of the target view's bounds rectangle should match the value of the
vertical scroll bar. When a {cpp:class}`BScrollBar` is notified of a change
of value (through {cpp:func}`ValueChanged() <BScrollBar::ValueChanged>`),
it calls the target view's {cpp:func}`ScrollTo() <BView::ScrollTo>`
function to put the new value at the left or top of the bounds rectangle.

The value reported in a {cpp:func}`ValueChanged()
<BScrollBar::ValueChanged>` notification and passed to
{cpp:func}`ScrollTo() <BView::ScrollTo>` depends on where the user moves
the scroll bar's knob and on the range of values the scroll bar represents.
The range is first set in the {cpp:class}`BScrollBar` constructor and can
be modified by the {cpp:func}`SetRange() <BScrollBar::SetRange>` function.

The range must be large enough to bring all the coordinate values where
the target view can draw into its bounds rectangle. If everything the
target view can draw is conceived as being enclosed in a "data rectangle",
the range of a horizontal scroll bar must extend from a minimum that makes
the left side of the target's bounds rectangle coincide with the left side
of its data rectangle, to a maximum that puts the right side of the bounds
rectangle at the right side of the data rectangle. This is illustrated in
part below:

![Scrolling A View](./images/TheInterfaceKit/scrollbar.png)

As this illustration helps demonstrate, the maximum value of a horizontal
scroll bar can be no less than the right coordinate value of the data
rectangle minus the width of the bounds rectangle. Similarly, for a
vertical scroll bar, the maximum value can be no less than the bottom
coordinate of the data rectangle minus the height of the bounds rectangle.
The range of a scroll bar subtracts the dimensions of the target's bounds
rectangle from its data rectangle. (The minimum values of horizontal and
vertical scroll bars can be no greater than the left and top sides of the
data rectangle.)

What the target view can draw may change from time to time as the user
adds or deletes data. As this happens, the range of the scroll bar should
be updated with the {cpp:func}`SetRange() <BScrollBar::SetRange>` function.
The range may also need to be recalculated when the target view is resized.

## Coordination

Scroll bars control the target view, but a target can also be scrolled
without the intervention of its scroll bars (by calling
{cpp:func}`ScrollTo() <BView::ScrollTo>` or {cpp:func}`ScrollBy()
<BView::ScrollBy>` directly). Therefore, not only must a scroll bar know
about its target, but a target view must know about its scroll bars. When a
{cpp:class}`BScrollBar` sets its target, the target {cpp:class}`BView` is
notified and records the identity of the {cpp:class}`BScrollBar`.

The two objects communicate whenever the display changes: When the scroll
bar is the instrument that initiates scrolling, {cpp:func}`ValueChanged()
<BScrollBar::ValueChanged>` calls the target view's {cpp:func}`ScrollTo()
<BView::ScrollTo>` function. To cover cases of target-initiated scrolling,
{cpp:func}`ScrollTo() <BView::ScrollTo>` calls the BScrollBar's
{cpp:func}`SetValue() <BScrollBar::SetValue>` function so that the scroll
bars can be updated on-screen. {cpp:func}`SetValue()
<BScrollBar::SetValue>` in turn calls {cpp:func}`ValueChanged()
<BScrollBar::ValueChanged>`, which makes sure the exchange of function
calls doesn't get too circular.

## Scroll Bar Options

Users have control over some aspects of how scroll bars look and behave.
With the ScrollBar preferences application, they can choose:

-   Whether the knob should be a fixed size, or whether it should grow and
shrink to proportionally represent how much of a document (how much of the
data rectangle) is visible within the target view. A proportional knob is
the default.

-   Whether double, bidirectional scroll arrows should appear on each end of
the scroll bar, or whether each end should have only a single,
unidirectional arrow. Double arrows are the default.

-   Which of three patterns should appear on the knob.

-   What the size of the knob should be—the minimum length of a proportional
knob or the fixed length of a knob that's not proportional. The default
length is 15 pixels.

When this class constructs a new {cpp:class}`BScrollBar`, it conforms the
object to the choices the user has made.

See also: {ref}`set_scroll_bar_info()`, {cpp:func}`BView::ScrollBar`, the
{cpp:class}`BScrollView` class
