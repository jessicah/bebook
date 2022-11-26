BCursor
=======

You can use a BCursor to represent a mouse cursor as an object instead
of as a block of pixel data; this can be more convenient in some situations.
Also, if you want to call BApplication::SetCursor() without forcing an immediate
sync of the Application Server, you have to use a BCursor.

The default BCursors are B_CURSOR_SYSTEM_DEFAULT for the hand cursor and
B_CURSOR_I_BEAM for the I-beam text editing cursor.

Cursor Data Format
==================

The first four bytes of cursor data give information about the cursor:

.. |table_r1_c2| replace:: Size in pixels-per-side. Cursors are always square;
    currently, only 16-by-16 cursors are allowed.

.. |table_r2_c2| replace:: Color depth in bits-per-pixel. Currently, only
   one-bit monochrome is allowed.

.. |table_r3_c2| replace:: Hot spot coordinates. Given in "cursor coordinates"
   where (0,0) is the upper left corner of the cursor grid, byte 3 is the hot
   spot's y coordinate, and byte 4 is its x coordinate. The hot spot is a single
   pixel that's "activated" when the user clicks the mouse. To push a button,
   for example, the hot spot must be within the button's bounds.

+------+---------------+
| Byte | Description   |
+======+===============+
| 1    | |table_r1_c2| |
+------+---------------+
| 2    | |table_r2_c2| |
+------+---------------+
| 3--4 | |table_r3_c2| |
+------+---------------+

Next comes an array of pixel color data. Pixels are specified from left to right
in rows starting at the top of the image and working downward. The size of an
array element is the depth of the image. In one-bit depth…

the 16x16 array fits in 32 bytes. 1 is black and 0 is white.

Then comes the pixel transparency bitmask, given left-to-right and
top-to-bottom. 1 is opaque, 0 is transparent. Transparency only applies to white
pixels, black pixels are always opaque.