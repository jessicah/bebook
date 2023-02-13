# BPopUpMenu

A {cpp:class}`BPopUpMenu` is a menu that's typically used in isolation,
rather than as part of an extensive menu hierarchy. By default, it operates
in radio mode—the last item selected by the user, and only that item, is
marked in the menu.

A menu of this kind can be used to choose one from a set of mutually
exclusive states—to pick a paper size or paragraph style, for example. It
shouldn't be used to group different kinds of choices (as other menus may),
nor should it include items that initiate actions rather than set states,
except in certain well-defined cases.

A pop-up menu can be used in any of three ways:



Other than {cpp:func}`~BPopUpMenu::Go` (and the
{cpp:func}`~BPopUpMenu::Constructor`), this class implements no functions
that you ever need to call from application code. In all other respects, a
{cpp:class}`BPopUpMenu` can be treated like any other {cpp:class}`BMenu`.
