:::{cpp:class} BRefFilter
:::

# BRefFilter

## Hook Functions

::::{abi-group}
:::{cpp:function} virtual bool BRefFilter::Filter(const entry_ref* ref, BNode* node, struct stat* st, const char* filetype)
:::

{hmethod}`Filter()` is a hook function that's invoked whenever the file
panel to which it's been assigned reads the entries in its "panel
directory." The function is invoked once for each entry in the directory.
All the arguments to the function refer to the entry currently under
consideration. (Note that the function is never sent an abstract entry, so
the {hparam}`node`, {hparam}`st`, and {hparam}`filetype` arguments will
always be valid.)

Your implementation of {hmethod}`Filter()` can use any or all of the
arguments to figure out if the entry is a valid candidate for display in
the file panel's file list. Simply return {cpp:expr}`true` or
{cpp:expr}`false` to indicate if the entry is a winner or a loser.

Technically, {hmethod}`Filter()` is invoked when…

-   …the file panel's panel directory is set, either through the
{hclass}`BFilePanel` constructor or the {cpp:func}`SetPanelDirectory()
<BFilePanel::SetPanelDirectory>`, and when…

-   …the file panel's {cpp:func}`Refresh() <BFilePanel::Refresh>` function is
called.

A {hclass}`BRefFilter` can be assigned to more than one
{cpp:class}`BFilePanel` object (assignation is performed through
{cpp:class}`BFilePanel`'s constructor or {cpp:func}`SetRefFilter()
<BFilePanel::SetRefFilter>` function). But it's not probably not a great
idea to do so: At any particular invocation of {hmethod}`Filter()`, the
{hclass}`BRefFilter` doesn't which {cpp:class}`BFilePanel` object it's
working for.

You maintain ownership of the {hclass}`BRefFilter` objects that you
create. Assigning a ref filter to a file panel does not hand ownership of
the {hclass}`BRefFilter` to the {cpp:class}`BFilePanel`. You shouldn't
delete a {hclass}`BRefFilter` while a {cpp:class}`BFilePanel` is still
using it; but it's your responsibility to delete it when it's done.
::::
