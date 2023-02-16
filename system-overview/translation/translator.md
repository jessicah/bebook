# BTranslator

{cpp:class}`BTranslator` is an abstract superclass that you subclass to
define your own proprietary translator objects, one translator per
{cpp:class}`BTranslator` subclass. You add instances of your
{cpp:class}`BTranslator` subclasses to a {cpp:class}`BTranslatorRoster`
through {cpp:func}`BTranslatorRoster::AddTranslators`.
{cpp:class}`BTranslator` objects that your app creates and adds to the
Roster are not visible to other applications.

Note that the {cpp:class}`BTranslator` destructor is protected; you never
delete a {cpp:class}`BTranslator` from outside the class. Insead, you
{cpp:func}`Release() <BTranslator::Release>` it. See {cpp:func}`Acquire()
<BTranslator::Acquire>` for details.

The primary {cpp:class}`BTranslator` functions are similar to the
functions and data that a translator add-on supplies. Most of the
{cpp:class}`BTranslator` functions take you to the Translator Add-ons
descriptions.
