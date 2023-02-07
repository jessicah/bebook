# BStringItem
## Constructor and Destructor
::::{abi-group}

:::{cpp:function} BStringItem::BStringItem(const char* text, uint32 level = 0, bool expanded = true)
:::
:::{cpp:function} BStringItem::BStringItem(BMessage* archive)
:::

Initializes the {hclass}`BStringItem` by making a copy of the text string passed as
an argument. This is the string the item will display. The level and
expanded arguments are passed unchanged to the {hclass}`BListItem` constructor; see
that function for an explanation.

::::

::::{abi-group}

:::{cpp:function} virtual BStringItem::~BStringItem()
:::

Frees the text the item displays.

::::

## Member Functions
::::{abi-group}

:::{cpp:function} virtual status_t BStringItem::Archive(BMessage* archive, bool deep = true) const
:::

Calls the inherited version of {hmethod}`Archive()` and stores the
{hclass}`BStringItem` in the
{cpp:class}`BMessage` archive.

See also:
{cpp:func}`BArchivable::Archive`,
{cpp:func}`~BStringItem::Instantiate` static function

::::

::::{abi-group}

:::{cpp:function} virtual void BStringItem::DrawItem(BView* owner, BRect frame, bool complete = false)
:::

Draws the text string, dimming it if the item is disabled and
highlighting it if the item is selected.

See also:
{cpp:func}`BListItem::DrawItem`

::::

::::{abi-group}

:::{cpp:function} virtual void BStringItem::SetText(const char* text)
:::
:::{cpp:function} const char* BStringItem::Text() const
:::

These functions set and return the text that the {hclass}`BStringItem` draws.
{hmethod}`SetText()` copies the string it's passed. {hmethod}`Text()` returns a pointer to the
string owned by the {hclass}`BStringItem`.

::::

::::{abi-group}

:::{cpp:function} virtual void BStringItem::Update(BView* owner, const BFont* font)
:::

Overrides the {hclass}`BListItem` version of
{cpp:func}`~BListItem::Update` to recalculate the width and
height of the {hclass}`BStringItem` and the placement of the text. The width of the
item is based on the width of the owner
{cpp:class}`BView`. The height and text
placement are based on the owner's font. The item must be tall enough to
display the string in the current font.

::::

## Static Functions
::::{abi-group}

:::{cpp:function} static BArchivable* BStringItem::Instantiate(BMessage* archive)
:::

Returns a new {hclass}`BStringItem` object, allocated by new and created with the
version of the constructor that takes a {cpp:class}`BMessage` archive. However, if the
archive message doesn't contain archived data for a BStringItem,
Instantiate() returns {cpp:enum}`NULL`.

See also
{cpp:func}`BArchivable::Instantiate`,
{cpp:func}`~instantiate::object`,
{cpp:func}`~BStringItem::Archive`

::::

## Archived Fields