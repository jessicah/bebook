# BMenuItem

A {cpp:class}`BMenuItem` object displays one item within a menu and
contains the state associated with that item. By default, menu items
display text; a derived class can reimplement the {cpp:func}`Draw()
<BMenuItem::Draw>` and {cpp:func}`DrawContent() <BMenuItem::DrawContent>`
hook functions to draw something else.

Each {cpp:class}`BMenuItem` object can have its own invocation message and
target. A menu item needn't send any message—it can be used simply for its
visual presence (see {cpp:class}`BSeparatorItem` for an example).

Menu items can't be used outside of a menu; to add a
{cpp:class}`BMenuItem` to a {cpp:class}`BMenu`, call
{cpp:func}`BMenu::AddItem`.

## Kinds of Items

Some menu items set up the menu hierarchy by giving users access to
submenus. A submenu remains hidden until the user operates the item that
controls it.

Other items accomplish specific actions. When the user invokes the item,
it sends a message to a target {cpp:class}`BLooper` and
{cpp:class}`BHandler`, usually the window where the menu at the root of the
hierarchy (a {cpp:class}`BMenuBar` object) is displayed. The action that
the item initiates, or the state that it sets, depends entirely on the
message and the target's response to it.

## Shortcuts and Triggers

Any menu item (except for those that control submenus) can be associated
with a keyboard shortcut, a character the user can type in combination with
a {hkey}`Command` key (and possibly other modifiers) to invoke the item.
The shortcut character is displayed in the item to the right of the label.

A shortcut works even when the item it invokes isn't visible on-screen.
It, therefore, has to be unique within the window (within the entire menu
hierarchy).

Every menu item is also associated with a trigger, a character that the
user can type (without the {hkey}`Command` key) to invoke the item. The
trigger works only while the menu is both open on-screen and can be
operated using the keyboard. It therefore must be unique only within a
particular branch of the menu hierarchy (within the menu).

The trigger is one of the characters that's displayed within the
item—either the keyboard shortcut or a character in the label. When it's
possible for the trigger to invoke the item, the character is underlined.
Like shortcuts, triggers are case-insensitive.

For an item to have a keyboard shortcut, the application must explicitly
assign one. However, by default, the Interface Kit chooses and assigns
triggers for all items. The default choice can be altered by the
{cpp:func}`SetTrigger() <BMenuItem::SetTrigger>` function.

## Marked Items

An item can also be marked (with a check mark drawn to the left of the
label) in order to indicate that the state it sets is currently in effect.
Items are marked by the {cpp:func}`SetMarked() <BMenuItem::SetMarked>`
function. A menu can be set up so that items are automatically marked when
they're selected and exactly one item is marked at all times. (See
{cpp:func}`SetRadioMode() <BMenu::SetRadioMode>` in the {cpp:class}`BMenu`
class.)

## Disabled Items

Items can also be enabled or disabled (by the {cpp:func}`SetEnabled()
<BMenuItem::SetEnabled>` function). A disabled item is drawn in muted tones
to indicate that it doesn't work. It can't be selected or invoked. If the
item controls a specific action, it won't post the message that initiates
the action. If it controls a submenu, it will still bring the submenu to
the screen, but all the items in submenu will be disabled. If an item in
the submenu brings its own submenu to the screen, items in that submenu
will also be disabled. Disabling the superitem for a submenu in effect
disables a whole branch of the menu hierarchy.
