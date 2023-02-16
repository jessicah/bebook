# BGLView

The {cpp:class}`BGLView` class provides a means for rendering graphics
using OpenGL calls in a view.

## The Graphics Buffers

A {cpp:class}`BGLView` automatically manages video buffers and interfaces
to supported hardware acceleration chipsets; all you have to do is call the
appropriate OpenGL calls to render your graphics.

The frontbuffer is the graphics buffer that is currently visible on the
screen. A backbuffer is a graphics buffer that is located offscreen.

In a single-buffered context, drawing commands are performed in the
frontbuffer. Drawing performed in single-buffered mode immediately appears
on the screen.

In double-buffered contexts, drawing is performed in the backbuffer and is
not visible onscreen until the {cpp:func}`SwapBuffers()
<BGLView::SwapBuffers>` function is called to swap the two buffers and
refresh the screen image.

:::{admonition} Note
:class: note
The BGLView class currently only supports double-buffered OpenGL contexts.
:::

### BGLView & BDirectWindow

The {cpp:class}`BGLView` class provides a function,
{cpp:func}`DirectConnected() <BGLView::DirectConnected>`, that your
{cpp:func}`BDirectWindow::DirectConnected` function can call to handle the
work of refreshing the OpenGL display.

## Using OpenGL

Long-winded discussion of how to use OpenGL is well beyond the realm of
what this book is intended to cover; for complete information on OpenGL,
see the OpenGL web site at http://www.opengl.org, where you'll find
complete documentation and sample code.

However, it's important to understand how OpenGL fits into the framework
of a BeOS application. The example that follows will draw a pattern of
lines around a central point, as seen in the picture below.

![Info Icon](./images/TheOpenGLKit/gltest.png)

This code has been structured to make it relatively easy to port sample
programs from the OpenGL web site; however, most of those samples use GLUT
features, which aren't available yet in the BeOS implementation of OpenGL.
In particular, most of the samples on the OpenGL web site use GLUT
functions to handle user interface of some form. You'll have to add code
for this yourself.

The complete source code and project file can be found on the Be web site
at <<<insert URL here>>>.

The first thing that's needed, as always, is an application object, which
we establish as follows:

:::{code} cpp
class SampleGLApp : public BApplication {
   public:
                     SampleGLApp();
      private:
         SampleGLWindow      theWindow;
};
:::

The {hclass}`SampleGLApp` class has a constructor and a private pointer to
the application's window. The constructor looks like this:

:::{code} cpp
SampleGLApp::SampleGLApp()
         : BApplication("application/x-vnd.Be-GLSample") {
   BRect windowRect;
   uint32 type;

   // Set type to the appropriate value for the
   // sample program you're working with.

   type = BGL_RGB|BGL_DOUBLE;

   windowRect.Set(50,50,350,350);
   theWindow = new SampleGLWindow(windowRect, type);
}
:::

The first thing the constructor here does is set the variable
{hparam}`type` to describe the context we need. In this example, we want an
RGB context with double-buffering on, so we specify
{cpp:enumerator}`BGL_RGB` and {cpp:enumerator}`BGL_DOUBLE`. Then we create
the window using the new function.

The {hclass}`SampleGLWindow` class is almost as simple:

:::{code} cpp
class SampleGLWindow : public BWindow {
   public:
                  SampleGLWindow(BRect frame, uint32 type);
      virtual bool   QuitRequested();

   private:
      SampleGLView* theView;
};
:::

The constructor accepts a {hparam}`frame` rectangle for the window and the
OpenGL context type parameter that will be passed to
{hclass}`SampleGLView`'s constructor. As always, {cpp:func}`QuitRequested()
<BApplication::QuitRequested>` is overridden to post a
{cpp:enumerator}`B_QUIT_REQUESTED` message to the application and return
true. A pointer to the {hclass}`SampleGLView` object is maintained as well.

The constructor is fairly trivial:

:::{code} cpp
SampleGLWindow::SampleGLWindow(BRect frame, uint32 type)
         : BWindow(frame, "OpenGL Test", B_TITLED_WINDOW, 0) {
   AddChild(theView=new SampleGLView(Bounds(), type));
   Show();
   theView->Render();
}
:::

This code establishes the window, then creates the {hclass}`SampleGLView`
and adds it as a child of the window. Once that's done, the window is made
visible by calling {hmethod}`Show()`. Finally, the {hclass}`SampleGLView`'s
contents are drawn by calling the {hclass}`SampleGLView`'s
{cpp:func}`Render() <SampleGLView::Render>` function.

The meat of this program is in the {hclass}`SampleGLView` class, which
follows:

:::{code} cpp
class SampleGLView : public BGLView {
   public:
                   SampleGLView(BRect frame, uint32 type);
      virtual void AttachedToWindow(void);
      virtual void FrameResized(float newWidth, float newHeight);
      virtual void ErrorCallback(GLenum which);

      void         Render(void);

   private:
      void         gInit(void);
      void         gDraw(void);
      void         gReshape(int width, int height);

      float        width;
      float        height;
};
:::

The {hclass}`SampleGLView` class implements the constructor and
reimplements three of the functions of the {cpp:class}`BGLView` class:
{cpp:func}`AttachedToWindow() <BGLView::AttachedToWindow>`,
{cpp:func}`FrameResized() <BGLView::FrameResized>`, and
{cpp:func}`ErrorCallback() <BGLView::ErrorCallback>`. An additional public
method, {cpp:func}`Render() <SampleGLView::Render>`, will contain the
actual code for drawing the contents of the view.

In addition, there are three private methods that will contain the actual
OpenGL calls for initializing, drawing, and resizing the
{cpp:class}`BGLView`'s contents and a pair of values to represent the width
and height of the {cpp:class}`BGLView`.

The constructor is very simple:

:::{code} cpp
SampleGLView::SampleGLView(BRect frame, uint32 type)
         : BGLView(frame, "SampleGLView", B_FOLLOW_ALL_SIDES, 0,
            type) {
   width = frame.right-frame.left;
   height = frame.bottom-frame.top;
}
:::

For the most part, the constructor defers to the {cpp:class}`BGLView`
constructor, setting the {hparam}`resizingMode` to
{cpp:enumerator}`B_FOLLOW_ALL_SIDES` and the OpenGL context type to the
value specified.

The only addition is that the width and height of the view are cached,
based upon the frame rectangle specified. This is done because we'll need
that information when the view is attached to the window, and the
{cpp:class}`BGLView` class doesn't include {hmethod}`Width()` and
{hmethod}`Height()` functions.

The {cpp:func}`AttachedToWindow() <BGLView::AttachedToWindow>` function,
which is called when the {hclass}`SampleGLView` is attached to its parent
window, looks like this:

:::{code} cpp
void SampleGLView::AttachedToWindow(void) {
   LockGL();
   BGLView::AttachedToWindow();
   gInit();
   gReshape(width, height);
   UnlockGL();
}
:::

This performs the initialization of the OpenGL context. First,
{cpp:func}`LockGL() <BGLView::LockGL>` is called to lock the context and
let the OpenGL Kit know which view should be targeted by future OpenGL
calls. Then the inherited version of {cpp:func}`AttachedToWindow()
<BView::AttachedToWindow>` is called to let {cpp:class}`BGLView` set up the
view normally.

Once that's done, the {hmethod}`gInit()` and {cpp:func}`gReshape()
<SampleGLView::gReshape>` functions are called. {cpp:func}`gInit()
<SampleGLView::gInit>`, as we'll see shortly, is responsible for
initializing the context. {cpp:func}`gReshape() <SampleGLView::gReshape>`
is called to configure the OpenGL coordinate system for the
{cpp:class}`BGLView` given the current width and height of the view.

Finally, {cpp:func}`UnlockGL() <BGLView::UnlockGL>` is called to release
the OpenGL context for the {hclass}`SampleGLView` and to indicate that
we're done using the context for the time being.

The {cpp:func}`FrameResized() <BGLView::FrameResized>` function is called
automatically whenever the {hclass}`SampleGLView` is resized:

:::{code} cpp
void SampleGLView::FrameResized(float newWidth, float newHeight) {
   LockGL();
   BGLView::FrameResized(width, height);
   width = newWidth;
   height = newHeight;

   gReshape(width,height);

   UnlockGL();
   Render();
}
:::

As always, this function begins by locking the OpenGL context. It then
calls the inherited version of {hmethod}`FrameResized()` to let
{cpp:class}`BGLView` perform whatever tasks it may need to do.

The new width and height of the view are saved in the {hparam}`width` and
{hparam}`height` variables, then the {cpp:func}`gReshape()
<SampleGLView::gReshape>` function is called to adjust the OpenGL context
given the new size of the view.

Finally, the context is unlocked, and {cpp:func}`Render()
<SampleGLView::Render>` is called to redraw the view's contents at the new
size.

Although the default {cpp:func}`ErrorCallback() <BGLView::ErrorCallback>`
function provided by {cpp:class}`BGLView` would be acceptable, we include
one of our own anyway:

:::{code} cpp
void SampleGLView::ErrorCallback(GLenum whichError) {
   fprintf(stderr, "Unexpected error occured (%d):\n", whichError);
   fprintf(stderr, " %s\n", gluErrorString(whichError));
}
:::

Note the use of the gluErrorString() OpenGL function to obtain an
appropriate error message for the error code. You can use this function to
avoid displaying error messages for errors that are acceptable or expected.

The gInit() function sets up the OpenGL context and initializes variables
that will be used later:



:::{code} cpp
void SampleGLView::gInit(void) {
   glClearColor(0.0, 0.0, 0.0, 0.0);
   glLineStipple(1, 0xF0E0);
   glBlendFunc(GL_SRC_ALPHA, GL_ONE);
   use_stipple_mode = GL_FALSE;
   use_smooth_mode = GL_TRUE;
   linesize = 2;
   pointsize = 4;
}
:::

Briefly, this sets the clear color (the background color) of the view to
black, configures the pattern for stippled lines and the blending function
to be used when blending is enabled. It also selects not to use stippled
lines (you can change this by setting {hparam}`use_stipple_mode` to
{cpp:enumerator}`GL_TRUE`) and to use anti-aliasing when drawing the lines
(you can change this by setting {hparam}`use_smooth_mode` to
{cpp:enumerator}`GL_FALSE`). It also chooses to use 2 pixel wide lines, and
4 pixel wide points.

This function doesn't call {cpp:func}`LockGL() <BGLView::LockGL>` and
{cpp:func}`UnlockGL() <BGLView::UnlockGL>`, so they must be called by the
calling function (and if you look at the {cpp:func}`AttachedToWindow()
<BGLView::AttachedToWindow>` code above, you'll see that this is the case).

There are some global variables used by this program (some of them
accessed in the above code), so lets' take a quick look at those:

:::{code} cpp
GLenum float use_stipple_mode;      // GL_TRUE to use dashed lines
GLenum float use_smooth_mode;     // GL_TRUE to use anti-aliased lines
GLint float linesize;             // Line width
GLint float pointsize;            // Point diameter

float float pntA[3] = {
   -160.0, 0.0, 0.0
};
float pntB[3] = {
   -130.0, 0.0, 0.0
};
:::

The varaibles {hparam}`use_stipple_mode`, {hparam}`use_smooth_mode`,
{hparam}`linesize`, and {hparam}`pointsize` are discussed in the
{hmethod}`gInit()` function above. The two {htype}`float` arrays define
points in three-dimensional space. These points will be used as the
endpoints of the lines drawn by the {hmethod}`gDraw()` function.

The {hmethod}`gDraw()` function does the actual drawing into the OpenGL
context:



:::{code} cpp
void SampleGLView::gDraw(void) {
   GLint i;

   glClear(GL_COLOR_BUFFER_BIT);
   glLineWidth(linesize);

   if (use_stipple_mode) {
      glEnable(GL_LINE_STIPPLE);
   } else {
      glDisable(GL_LINE_STIPPLE);
   }

   if (use_smooth_mode) {
      glEnable(GL_LINE_SMOOTH);
      glEnable(GL_BLEND);
   } else {
      glDisable(GL_LINE_SMOOTH);
      glDisable(GL_BLEND);
   }

   glPushMatrix();

   for (i = 0; i < 360; i += 5) {
      glRotatef(5.0, 0,0,1);     // Rotate right 5 degrees
      glColor3f(1.0, 1.0, 0.0);  // Set color for line
      glBegin(GL_LINE_STRIP);    // And create the line
      glVertex3fv(pntA);
      glVertex3fv(pntB);
      glEnd();

      glPointSize(pointsize);    // Set size for point
      glColor3f(0.0, 1.0, 0.0);  // Set color for point
      glBegin(GL_POINTS);
      glVertex3fv(pntA);         // Draw point at one end
      glVertex3fv(pntB);         // Draw point at other end
      glEnd();
   }

   glPopMatrix();                // Done with matrix
}
:::

Without getting too deeply-involved in OpenGL specifics, this code begins
by clearing the context's buffer and setting the line width. It then
enables the features selected by the {hparam}`use_stipple_mode` and
{hparam}`use_line_mode` variables.

Once that's done, it establishes a matrix to be used for rotating the
lines and draws the lines with points at each end, drawing one every five
degrees in a 360-degree circle around the center of the window. After
drawing all the lines, the matrix is destroyed and the function returns.

The {hmethod}`gReshape()` function handles adjusting the OpenGL context's
coordinate system and viewport when the {hclass}`SampleGLView` is first
created, and whenever the view is resized:



:::{code} cpp
void SampleGLView::gReshape(int width, int height) {
   glViewport(0, 0, width, height);
   glMatrixMode(GL_PROJECTION);
   glLoadIdentity();
   gluOrtho2D(-175, 175, -175, 175);
   glMatrixMode(GL_MODELVIEW);
}
:::

This code simply sets the viewport's coordinate system to reflect the new
width and height of the view, and establishes a projection matrix such that
no matter what the size and shape of the window, the center of the window
is considered to be (0,0) and the window is 300 units wide and 300 units
tall. This lets the rendering code draw without having to worry about
scaling; OpenGL handles it for us.

The details of how this works are, again, beyond the scope of this
chapter.

Finally, the {hmethod}`Render()` function is the high-level function used
to actually update the contents of the {hclass}`SampleGLView` whenever we
wish to redraw it:



:::{code} cpp
void SampleGLView::Render(void) {
   LockGL();
   gDraw();
   SwapBuffers();
   UnlockGL();
}
:::

{cpp:func}`LockGL() <BGLView::LockGL>` is called to lock the context
before calling {hmethod}`gDraw()` to do the actual OpenGL calls to draw the
view. Then the {cpp:func}`SwapBuffers() <BGLView::SwapBuffers>` function is
called to swap the backbuffer that was just drawn to the screen, and the
context is unlocked.

## Adapting OpenGL Sample Code

The program described above can easily be adapted to be used with other
sample code from the OpenGL web site. First, replace the code in the
{hmethod}`gInit()`, {hmethod}`gDraw()`, and {cpp:func}`gReshape()
<SampleGLView::gReshape>` functions with the code from the
{cpp:func}`gInit() <SampleGLView::gInit>`, {cpp:func}`gDraw()
<SampleGLView::gDraw>`, and {cpp:func}`gReshape() <SampleGLView::gReshape>`
functions in the sample code (some of the sample programs give these
functions slightly different names).

Keep in mind that the current implementation of OpenGL under BeOS doesn't
support single-buffered graphics, so you'll need to make whatever
adjustments are necessary to use double-buffering.

Once these functions have been implemented, copy any global variables from
the sample program into your project. Finally, in the {hclass}`SampleGLApp`
constructor, fix the OpenGL context type and window size information to
match that used by the sample program.

You may also wish to implement code to handle user interface to let you
configure the sample program; that's beyond the scope of this chapter—see
the Interface Kit chapter of the Be Developer's Guide for further
information on handling user input.
