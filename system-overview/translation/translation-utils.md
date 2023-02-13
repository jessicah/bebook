# BTranslationUtils

{cpp:class}`BTranslationUtils` contains a set of static functions which
load bitmap images. The functions use the Translation Kit to convert the
data from its native format to a {cpp:class}`BBitmap` via a
{cpp:class}`BBitmapStream`, the upshot of which is that if you can convert
the data to a translator bitmap, you can successfully use these functions.
The image may come from a file, resource, or {cpp:class}`BPositionIO`. The
application is always responsible for deallocating the returned
{cpp:class}`BBitmap`.
