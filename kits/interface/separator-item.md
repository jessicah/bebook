# BSeparatorItem
## Constructor and Destructor
::::{abi-group}

:::{cpp:function} BSeparatorItem::BSeparatorItem()
:::
:::{cpp:function} BSeparatorItem::BSeparatorItem(BMessage* data)
:::
::::

::::{abi-group}

:::{cpp:function} virtual BSeparatorItem::~BSeparatorItem()
:::
::::

## Member Functions
::::{abi-group}

:::{cpp:function} virtual status_t BSeparatorItem::Archive(BMessage* archive, bool deep = true) const
:::


::::

::::{abi-group}

:::{cpp:function} virtual void BSeparatorItem::SetEnabled(bool state)
:::
::::

::::{abi-group}

:::{cpp:function} virtual void BSeparatorItem::GetContentSize(float* width, float* height)
:::
::::

::::{abi-group}

:::{cpp:function} virtual void BSeparatorItem::Draw()
:::
::::

## Static Functions
::::{abi-group}

:::{cpp:function} static BArchivable* BSeparatorItem::Instantiate(BMessage* data)
:::
::::
