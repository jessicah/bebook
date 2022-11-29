# BShelf
A {cpp:class}`BShelf` is an object that you "attach" to a view in order to make the view accept
dropped {cpp:class}`BDragger` objects. In user-talk, a shelf receives and displays replicants.
Attaching a {cpp:class}`BShelf` to a view (called the "container" view) is remarkably simple:

:::{code} cpp
BShelf *shelf = new BShelf(container_view);
:::

That's all there is to it: With this single line of code, `container_view` is primed to accept and
(automatically) display dropped replicants. A dropped replicant becomes a child of the container
view. The container view itself can be any {cpp:class}`BView` object—you don't alter the view in any
way, or even tell it that it's going to be a container.

:::{admonition} Note
:class: note
Attaching a shelf to a view is performed by the {cpp:class}`BShelf` constructor only. You can't create
a {cpp:class}`BShelf` and then decide which view you want it to serve.
:::

## Dropping into the View Hierarchy

When the user drops a replicant on a container view, the view receives a
{cpp:enum}`B_ARCHIVED_OBJECT` message that contains a {cpp:class}`BDragger` and the dragger's target
(a {cpp:class}`BView`). These two views (the {cpp:class}`BDragger` and its target) are related as
parent-child, child-parent, or as siblings (as explained in the {cpp:class}`BDragger` class). The
"more elderly" of the two objects is added as a child of the container view; if they're siblings,
the two objects are both added as children.

You can also send or post {cpp:enum}`B_ARCHIVED_OBJECT` messages to a {cpp:class}`BShelf` to
simulate a drag and drop.

## Other BShelf Features

Settings.

: A {cpp:class}`BShelf` can configure itself from a "settings" file, and can write its contents to
that file. Your only chance to associate a {cpp:class}`BShelf` with a settings file is during
construction. You can save the contents at any time through the {cpp:func}`~BShelf::Save()`
function.

Replicant rejection.

: A {cpp:class}`BShelf` can reject replicants, and can adjust the position of the replicants that it
accepts. These features are provided through the hook functions
{cpp:func}`~BShelf::CanAcceptReplicantMessage()`, {cpp:func}`~BShelf::CanAcceptReplicantView()`, and
{cpp:func}`~BShelf::AdjustReplicantBy()`. A named shelf can also reject replicants, as explained
next.

BShelf names.

: When a replicant message is dropped on the shelf, the shelf's name (set in the constructor) is
compared to the dropped message's "shelf_type" field (if it has one). If the two don't match, the
replicant rejects the shelf. In this way, individual replicants can be picky about the shelves that
they want to be displayed on. By default, a shelf accepts replicants that don't have a "shelf_type"
field. However, if a {cpp:class}`BShelf` is set to "enforce type" (set through
{cpp:func}`~BShelf::SetTypeEnforced()`), then it will only accept replicants that name the shelf (in
their "shelf_type" fields).

Persistent IDs

: A {cpp:class}`BShelf` assigns each replicant a unique id that's valid for as long as the replicant
is attached to the shelf. Replicant ids don't change, even if the shelf is
{cpp:func}`~BShelf::Save()`'d and then later restored (through the constructor).
