# BDragger

A {cpp:class}`BDragger` is a view that lets users drag and drop some other
view. The other view is the target of the {cpp:class}`BDragger` and its
immediate relative—a sibling, a parent, or an only child. The
{cpp:class}`BDragger` draws a handle, usually at the corner of the target
view, that the user can grab. When the user drags the handle the target
view appears to move with the handle.

When dragged in this way, the target view itself doesn't actually move.
Instead, the view is archived in a {cpp:class}`BMessage` object and the
{cpp:class}`BMessage` is dragged. When the {cpp:class}`BMessage` is
dropped, the target {cpp:class}`BView` can be reconstructed from the
archive (along with the {cpp:class}`BDragger`). The new object is a
duplicate—a replicant—of the target view.

This class works closely with the {cpp:class}`BShelf` class. A
{cpp:class}`BShelf` object accepts dragged {cpp:class}`BView`s,
reconstructs them from their archives, and installs them in another view
hierarchy.

{cpp:class}`BDragger`s are under the control of DeskBar's "Show
Replicants" / "Hide Replicants" menu item. Showing replicants means that
the {cpp:class}`BDragger` handles are visible on-screen; hiding replicants
means that the handles are hidden.
