# Global Functions

## set_mouse_position()

Declared in: game/WindowScreen.h



Moves the cursor hot spot to ({hparam}`x`, {hparam}`y`) in the screen
coordinate system, where {hparam}`x` is a left-to-right index to a pixel
column and {hparam}`y` is a top-to-bottom index to a pixel row. The origin
of the coordinate system is the left top pixel of the display area of the
main screen.

This function should be called only while the application has a direct
connection to the frame buffer through a {cpp:class}`BWindowScreen` object.
