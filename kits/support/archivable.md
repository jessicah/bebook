# BArchivable

## Constructor and Destructor

::::{abi-group}
:::{cpp:function} BArchivable::BArchivable()
:::
:::{cpp:function} BArchivable::BArchivable(BMessage* archive)
:::

Does nothing.
::::

::::{abi-group}
:::{cpp:function} virtual BArchivable::~BArchivable()
:::

Does nothing
::::

## Member Functions

::::{abi-group}
:::{cpp:function} virtual status_t BArchivable::Archive(BMessage* archive, bool deep = true) const
:::
 The default implementation adds the name of the object's class to archive's {hfield}`class` field. Derived classes must override {hmethod}`Archive()` to augment this implementation by adding, to the {cpp:class}`BMessage`, data that describes the current state of the object. Each implementation of this function should begin by incorporting the inherited version:

 :::{code} cpp
 /* We'll assume that MyView inherits from {cpp:class}`BView`. */
 status_t MyView::Archive({cpp:class}`BMessage`* archive, bool deep)
 {
    {cpp:class}`BVeiew`::Archive(archive, deep);
    
    // . . .
 }
 :::

 If the class can be instantiated directly from a derived class, it should also add its name to the "class" array:

 :::{code} cpp
 archive->AddString("class", "MyView");
 :::

 The {hparameter}`deep` flag declares whether {hmethod}`Archive()` should include objects that "belong" to the archiving object. For example, a deep {cpp:class}`BView` archive would include archived forms of the view's children.

 {hmethod}`Archive()` should return {cpp:enum}`B_OK` if it's successful; otherwise, it should return {cpp:enum}`B_ERROR` or a more descriptive error code.
 ::::

 ## Static Functions

::::{abi-group}
:::{cpp:function} static BArchivable* BArchivable::Instantiate(BMessage* archive)
:::

Derived classes should implement {hmethod}`Instantiate()` to return a new {hclass}`BArchivable` object that was constructed from the {cpp:class}`BMessage` archive. For example:

:::{code} cpp
BArchivable* TheClass::Instantiate(BMessage* archive)
{
    if (!validate_instantiation(archive, "TheClass"))
        return NULL;
    
    return new TheClass(archive);
}
:::

:::{warning}
{hmethod}`Instantiate()` must return a {hclass}`BArchivable`*, regardless of the actual class in which it's implemented.
:::

This function depends on a constructor that can initialize the new object from the {hparam}`archive` {cpp:class}`BMessage`. See "Instantiability" **TODO** for more information.

The default implementation returns {cpp:enum}`NULL`.
::::
