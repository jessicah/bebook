# BDragger
## Constructor and Destructor
::::{abi-group}

:::{cpp:function} BDragger::BDragger(BRect frame, BView* target, uint32 resizingMode = B_FOLLOW_NONE, uint32 flags = B_WILL_DRAW)
:::
:::{cpp:function} BDragger::BDragger(BMessage* archive)
:::

Creates a new {hclass}`BDragger` and sets its target view.
The {hclass}`BDragger` and the
target {cpp:class}`BView` must be
directly related in the view hierarchy (as
parent-child or as siblings); but, note well, the constructor doesn't
establish this relationship for you. After you construct you {hclass}`BDragger`,
you have to do one of three things:

add the target as a child of the dragger, add the dragger as a child of the target, or add the dragger as a sibling of the target.

If you add the target as a child of {hclass}`BDragger`, it should be the only child
that the {hclass}`BDragger` has.

A {hclass}`BDragger` draws in the right bottom corner of its frame rectangle. If
the {hparam}`target` view is a parent or a sibling of the {hclass}`BDragger`, that rectangle
needs to be no larger than the image the {hclass}`BDragger` draws (the handle).
However, if the target is the {hclass}`BDragger`'s child, the dragger's frame
rectangle must enclose the target's frame (so that the dragger doesn't
clip the target).

A {hclass}`BDragger` is fully functional once it has been constructed and attached
to the view hierarchy of its target. You don't need to call any other
functions. However, the whole endeavor fails if the target
{cpp:class}`BView` can't be
archived.

::::

::::{abi-group}

:::{cpp:function} virtual BDragger::~BDragger()
:::

Frees all memory the {hclass}`BDragger` allocated (principally for the bitmap image
it draws).

::::

## Hook Functions
::::{abi-group}

:::{cpp:function} virtual void BDragger::AttachedToWindow()
:::
:::{cpp:function} virtual void BDragger::DetachedFromWindow()
:::

{hmethod}`AttachedToWindow()` makes sure that the
{hclass}`BDragger` is under the control of
the {cpp:func}`~BDragger::HideAllDraggers`
and {cpp:func}`~BDragger::ShowAllDraggers`
functions, makes its low and
background view colors match the view color of its parent, and determines
the {hclass}`BDragger`'s precise relationship to its target view. To make this
determination, the target must be in the view hierarchy; it can't be
added to the window after the {hclass}`BDragger` is. For example, if the target is
the {hclass}`BDragger`'s child, it should be added to the
{hclass}`BDragger` and then the
{hclass}`BDragger` added to the window.

{hmethod}`DetachedFromWindow()` removes the {hclass}`BDragger`
from the control of the
{cpp:func}`~BDragger::HideAllDraggers`
and {cpp:func}`~BDragger::ShowAllDraggers` functions.

::::

::::{abi-group}

:::{cpp:function} virtual void BDragger::Draw(BRect updateRect)
:::

Draws the handle—or fails to draw it and has the parent view draw
in that area instead, if all {hclass}`BDragger`s are hidden.

::::

::::{abi-group}

:::{cpp:function} virtual void BDragger::MessageReceived(BMessage* message)
:::

Responds to messages that regulate the visibility of the {hclass}`BDragger` handle.

::::

::::{abi-group}

:::{cpp:function} virtual void BDragger::MouseDown(BPoint where)
:::

Responds to a {cpp:enum}`B_MOUSE_DOWN` message by archiving the target view (and the
{hclass}`BDragger`) and initiating a drag-and-drop operation, or by taking other
appropriate action.

::::

## Member Functions
::::{abi-group}

:::{cpp:function} virtual status_t BDragger::Archive(BMessage* archive, bool deep = true) const
:::

Records the {hclass}`BDragger`'s hierarchical relationship to the target view and
then calls
{cpp:func}`BView::Archive`
. The {hparam}`deep` flag has no significance for
{hclass}`BDragger` itself, but note that the flag is passed on to the
{cpp:class}`BView` version.

::::

::::{abi-group}

:::{cpp:function} bool BDragger::IsVisibilityChanging() const
:::

Returns {cpp:enum}`true` if two things are true:

The BDragger is the parent of its target. The BDragger handle was visible but now should not be, or it wasn't visible and now should be.

Otherwise, this function returns {cpp:enum}`false`.

What's this function for? It's in the API so derived classes can
implement their own versions of
{cpp:func}`~BDragger::Draw`.
If the {hclass}`BDragger` isn't the parent
of its target, the visibility of the {hclass}`BDragger` view can be controlled by
the
{cpp:func}`~BView::Hide` and
{cpp:func}`~BView::Show`
functions rather than
{cpp:func}`~BDragger::Draw`.

::::

::::{abi-group}

:::{cpp:function} BPopUpMenu* BDragger::PopUp() const
:::
:::{cpp:function} status_t BDragger::SetPopUp(BPopUpMenu* context_menu)
:::

Returns and sets the {cpp:class}`BPopUpMenu`
displayed when the user right clicks on
the {hclass}`BDragger` view after it has been attached to a
{cpp:class}`BShelf`.

::::

## Static Functions
::::{abi-group}

:::{cpp:function} static status_t BDragger::HideAllDraggers()
:::
:::{cpp:function} static status_t BDragger::ShowAllDraggers()
:::
:::{cpp:function} static bool BDragger::AreDraggersDrawn()
:::

These functions communicate with all {hclass}`BDragger` objects in all applications
(provided they're attached to windows). {hmethod}`HideAllDraggers()` hides the
{hclass}`BDragger` objects so that they're not visible on-screen. {hmethod}`ShowAllDraggers()`
undoes the effect of {hmethod}`HideAllDraggers()` and causes all {hclass}`BDragger` objects to
draw their handles. The Show Replicants / Hide Replicants menu item does
its work through these functions.

{hmethod}`HideAllDraggers()` may or may not hide the {hclass}`BDragger` view in the way that
{cpp:class}`BView's`
{cpp:func}`~BView::Hide`
function does. The {hclass}`BDragger` may still be visible, although
it won't draw anything until {hmethod}`ShowAllDraggers()` is called. Therefore, if
the target {cpp:class}`BView` is the
{hclass}`BDragger`'s child, it will not be hidden when
{hmethod}`HideAllDraggers()` erases its parent.

{hmethod}`AreDraggersDrawn()` returns {cpp:enum}`true`
when the {hclass}`BDragger`s are shown and {cpp:enum}`false`
when they're hidden.

::::

::::{abi-group}

:::{cpp:function} static BArchivable* BDragger::Instantiate(BMessage* archive)
:::

Returns a new {hclass}`BDragger` object, allocated by new and created with the
version of the constructor that takes a
{cpp:class}`BMessage` archive. If the archive
message doesn't contain an archived {hclass}`BDragger`,
{hmethod}`Instantiate()` returns {cpp:enum}`NULL`.

::::

## Archived Fields