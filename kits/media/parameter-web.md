:::{cpp:class} BParameterWeb
:::

# BParameterWeb

## Constructor and Destructor

::::{abi-group}
:::{cpp:function} BParameterWeb::BParameterWeb()
:::

The {hclass}`BParameterWeb` constructor. You'll usually create one
{hclass}`BParameterWeb` object per {cpp:class}`BControllable` node; to
attach a {hclass}`BParameterWeb` to a {cpp:class}`BControllable` node, you
should call {cpp:func}`BControllable::SetParameterWeb`.
::::

::::{abi-group}
:::{cpp:function} BParameterWeb::~BParameterWeb()
:::

Once you've called {cpp:func}`BControllable::SetParameterWeb`, the node
takes responsibility for the parameter web object and you shouldn't delete
it.

If you don't call {cpp:func}`BControllable::SetParameterWeb`, then delete
the {hclass}`BParameterWeb` object when you're done with it.
::::

## Member Functions

::::{abi-group}
:::{cpp:function} int32 BParameterWeb::CountGroups()
:::

Returns the number of {cpp:class}`BParameterGroup` objects that are
currently attached to the {hclass}`BParameterWeb`.
::::

::::{abi-group}
:::{cpp:function} int32 BParameterWeb::CountParameters()
:::

Returns the number of {cpp:class}`BParameter`s in the entire web,
including those in all {cpp:class}`BParameterGroup`s attached to it.
::::

::::{abi-group}
:::{cpp:function} BParameterGroup* BParameterWeb::GroupAt(int32 index)
:::

Returns the {cpp:class}`BParameterGroup` located at the specified
{hparam}`index` within the list of groups contained by the
{hclass}`BParameterWeb`.

The first group is numbered 0, so the maximum legal value for
{hparam}`index` is {cpp:func}`CountGroups()
<BParameterGroup::CountGroups>`-1. If the specified {hparam}`index` is
outside that range, {cpp:expr}`NULL` is returned.
::::

::::{abi-group}
:::{cpp:function} BParameterGroup* BParameterWeb::MakeGroup(const char* name)
:::

Creates a new {cpp:class}`BParameterGroup` object to be used for grouping
parameters within the {hclass}`BParameterWeb`, and attaches it to the
{hclass}`BParameterWeb`.

All {cpp:class}`BParameter`s created in the group will belong to that
group, and, by recursion, to the web itself.

:::{admonition} Note
:class: note
You can nest {cpp:class}`BParameterGroup`s if you want to; however,
{cpp:class}`BParameter`s can't be shared among multiple groups.
:::
::::

::::{abi-group}
:::{cpp:function} media_node BParameterWeb::Node()
:::

Returns the {cpp:func}`media_node <media::node>` for the
{cpp:class}`BControllable` node that owns this {hclass}`BParameterWeb`
object.

If the {hclass}`BParameterWeb` hasn't been attached to a
{cpp:class}`BControllable` node yet, `media_node::null` is returned.
::::

::::{abi-group}
:::{cpp:function} BParameter* BParameterWeb::ParameterAt(int32 index)
:::

Returns the {cpp:class}`BParameter` at the specified {hparam}`index`
within the entire {hclass}`BParameterWeb`, including those in all attached
groups. The first parameter is numbered 0, so the maximum legal value for
{hparam}`index` is {cpp:func}`CountParameters()
<BParameterGroup::CountParameters>`-1. If the specified {hparam}`index` is
outside that range, {cpp:expr}`NULL` is returned.
::::
