JSON Handling
=============

Potential API Break
-------------------

Jessica Hamilton: after reading this document, it is clear that the current
implementation of JSON to BMessage conversion is completely broken, and needs
rewriting. An array should **not** be encoded with stringified integer keys.

Resumption of Play
------------------

JSON is a simple textual description of a data structure. An example of some
JSON would be::

	[ "apple", "orange", { "drink": "tonic water", "count": 1 } ]

This example is a list that contains two strings followed by an object. The
term object refers to a construct akin to a dictionary or a map. It is also
possible for top-level objects to be non-collection types such as strings. The
following is also valid JSON::

	"feijoa"

This page details how Haiku provides facilities for both parsing and writing
data encoded as JSON.

Parsing with Generic In-Memory Model
------------------------------------

For some applications, parsing to an in-memory data structure is ideal. In such
cases, the :cpp:class:`BJson` class provides static methods for parsing a block
on JSON data into a :cpp:class:`BMessage` object. The application is then able
to introspect the :cpp:class:`BMessage` to obtain values.

BMessage Structure
~~~~~~~~~~~~~~~~~~

The :cpp:class:`BMessage` class has the ability to carry a collection of
key-value pairs. In the case of a JSON object type, the key-value pairs
correlate to a JSON object or array. In the case of a JSON array type, the
key-value pairs are the index of the elements in the JSON array, represented as
strings.

For example, the following JSON array::

	[ "a", "b", "c" ]

would be represented by the following :cpp:class:`BMessage`:

+-----+-------+
| Key | Value |
+=====+=======+
| "0" |  "a"  |
+-----+-------+
| "1" |  "b"  |
+-----+-------+
| "2" | "c"   |
+-----+-------+

A JSON object that, in its entirety, consists of a non-collection type such as a
simple string or a boolean is not able to be represented by a
:cpp:class:`BMessage`; at the top level, there must be an array or an object for
the parse to be successful.

Stream-based Parsing
--------------------

