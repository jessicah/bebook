# BListItem

A {cpp:class}`BListItem` represents a single item in a
{cpp:class}`BListView` (or {cpp:class}`BOutlineListView`). The
{cpp:class}`BListItem` object provides drawing instructions that can draw
the item (through {cpp:func}`DrawItem() <BListItem::DrawItem>`), and keeps
track of the item's state. To use a {cpp:class}`BListItem`, you must add it
to a {cpp:class}`BListView` through {cpp:func}`BListView::AddItem`
({cpp:class}`BOutlineListView` provides additional item-adding functions).
The {cpp:class}`BListView` object provides the drawing context for the
{cpp:class}`BListItem`'s {cpp:func}`DrawItem() <BListItem::DrawItem>`
function.

{cpp:class}`BListItem` is abstract; each subclass must implement
{cpp:func}`DrawItem() <BListItem::DrawItem>`. {cpp:class}`BStringItem`—the
only {cpp:class}`BListItem` subclass provided by Be—implements the function
to draw the item as a line of text. For an example of a custom
{cpp:class}`BListView` subclass, see "{ref}`Creating a Custom List Item`".

## Synchronizing a List Item with its List View

A {cpp:class}`BListItem` object doesn't automatically get redrawn when the
item changes. If you change a list item's content or state, you must tell
the item's owner (the {cpp:class}`BListView` object) to redraw the item by
calling {cpp:func}`BListView::InvalidateItem`. For example:

:::{code} cpp
/* listItem belongs to listView.
   We change the state of the item... */
listItem->SetEnabled(false);

/* ...so we have to tell the list view to redraw it. */
listView->LockLooper();
listView->InvalidateItem(listView->IndexOf(listItem));
listView->UnlockLooper();
:::

If you're making a lot of changes, you can flush them all at the same time
through a single {cpp:func}`BView::Invalidate` call:

:::{code} cpp
listItemA->SetEnabled(false);
listItemB->SetEnabled(false);
listItemC->SetEnabled(false);
listView->LockLooper();
listView->Invalidate();
listView->UnlockLooper();
:::

Note that you don't have to lock the list view's window to change one of
its items—you only have to lock the window when you talk to the list view
itself.

{cpp:class}`BListView` provides its own smart version

## Creating a Custom List Item

Although much of the time all you need to draw in a list are strings (in
which case you can use the {cpp:class}`BStringItem` class), from
time-to-time you may need to display more than a simple text string—maybe
you need to display multiple pieces of information per item, or maybe you
just want to jazz up the display with some icons.

For example, let's say you need to let the user select a city from a list,
but also need to display the part of the world that each city is in. You
could just use {cpp:class}`BStringItem` objects with strings like "Chicago
(USA)", but it might look nicer if you could lay out your list items in two
colums, maybe with a splash of color:

![Custom ListItem](./images/TheInterfaceKit/custlistitem.png)

To change the appearance of a list item, you override the
{cpp:func}`DrawItem() <BListItem::DrawItem>` function to draw the item's
contents however you want it to look.

The following sections define the class that creates these list items.

### The CityItem Declaration

The declaration for our {hclass}`CityItem` class looks like this:

:::{code} cpp
#include <String.h>
#include <ListItem.h>

class CityItem : public BListItem
{
   public:
      CityItem(const char *city, int32 region = 0);
      virtual void DrawItem(BView *owner,
            BRect frame,
            bool complete = false);
      enum { USA, ASIA, EUROPE, AUSTRALIA, OTHER };

   private:
      BString kCity;
      int32 kRegion;
};

const char *region_names[] = {
   "USA", "Asia", "Eur.", "Aust.", "Other"
};
:::

A {hclass}`CityItem` object contains two pieces of data: a city name, and
a region code. The region code is used as an index into the array of region
names.

### The CityItem Definition

The constructor looks like this:

:::{code} cpp
CityItem::CityItem(const char *city, int32 region)
         : BListItem()
{
   kCity = city;
   kRegion = region;
}
:::

The {cpp:func}`DrawItem() <BListItem::DrawItem>` function does the actual
work of drawing the item. {cpp:func}`DrawItem() <BListItem::DrawItem>`
receives three parameters:

-   A {cpp:class}`BView` "owner"; this is the view that contains the
{cpp:class}`BListItem`. All drawing calls you issue should be made through
this BView. For example:

  :::{code} cpp
owner->DrawString(item_text);
:::

-   A {cpp:class}`BRect`, which is the rectangle in which the item should be
drawn.

-   A {htype}`bool`, which is {cpp:expr}`true` if the item needs to be erased
and redrawn, or {cpp:expr}`false` if the item's contents can be safely
redrawn without erasing the current contents.

{cpp:func}`DrawItem() <BListItem::DrawItem>` begins by checking to see if
the item is selected (by calling {cpp:func}`IsSelected()
<BListItem::IsSelected>`) or if a complete redraw is required. In either of
these cases, we want to redraw the background, to either the highlight
color, or the owner's view color:

:::{code} cpp
void CityItem::DrawItem(BView *owner, BRect frame,
                        bool complete)
{
   if (IsSelected() || complete) {
      rgb_color color;
      if (IsSelected()) {
         color = kHighlight;
      }
      else {
         color = owner->ViewColor();
      }
      owner->SetHighColor(color);
      owner->FillRect(frame);
   }
:::

Now we draw the text. First, we move the owner view's pen so it's inset
from the bottom left corner of the item's frame. (In a real application,
you would want to make the inset adjustments based on the font that's being
used; see the {cpp:class}`BFont` class for more information.):

:::{code} cpp
owner->MovePenTo(frame.left+4, frame.bottom-2);
:::

If the item is enabled (selectable), we set the owner view's high color to
a shade of medium red; if it's disabled, we use a lighter red color (the
color definitions aren't shown). Then we use {cpp:func}`DrawString()
<BView::DrawString>` to draw the region name:.

:::{code} cpp
if (IsEnabled()) {
      owner->SetHighColor(kRedColor);
   }
   else {
      owner->SetHighColor(kDimRedColor);
   }
   owner->DrawString(region_names[kRegion]);
:::

Move the pen to the right column and draw the city name:

:::{code} cpp
owner->MovePenTo(frame.left+38, frame.bottom-2);
   if (IsEnabled()) {
      owner->SetHighColor(kBlackColor);
   }
   else {
      owner->SetHighColor(kMedGray);
   }
   owner->DrawString(kCity.String());
}
:::

### Using a CityItem Object

To use a {hclass}`CityItem` object, simply construct a new object and pass
it to {cpp:func}`BListView::AddItem`:

:::{code} cpp
listView->AddItem(new CityItem("Chicago", CityItem::USA));
:::
