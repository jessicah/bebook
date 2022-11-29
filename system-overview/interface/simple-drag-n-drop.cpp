/* Drag the black square around using drag'n'drop--a very
   simple-minded program. The DETECTION, INITIATIOIN, DRAG,
   and DROP steps correspond to those of the same name given
   in the overview section, "Basics of Drag and Drop". */

#include <Application.h>
#include <InterfaceKit.h>

rgb_color black = {0, 0, 0, 64};
const char *APP_SIGNATURE = "application/x-vnd.Be-MyDragnDrop";
/* The constant below is arbitrary--the fact that is is 'drag' is
   meaningless. However, it MUST be chosen so as not to conflict
   with system-wide BMessage 'what' values--see the BMessage
   documentation for details. */
const uint32 MY_DRAG_ACTION = 'drag';

class MyDragDropView : public BView {
private:
   BPoint _button_click;
   BRect _SquareSides;

public:
   MyDragDropView(BRect rect) : BView(rect, "",
                     B_FOLLOW_ALL_SIDES, B_WILL_DRAW) {
      _SquareSides = BRect(20, 20, 90, 90);
   }

   void Draw(BRect where) {
      SetHighColor(black);
      FillRect(_SquareSides);
   }

   void MouseDown( BPoint where ) {
      /* 1. DETECTION : Our detection code is pretty
         simple-minded; if the user clicks in the black square,
         they're starting a drag. */
      if (_SquareSides.Contains(where)) {
         // Turn on the event mask for all pointer events,
         // so we'll know when
         // the user lets go of the mouse button.
         SetMouseEventMask( B_POINTER_EVENTS, 0 );

         /* 2. INITIATION : Create a BMessage instance, and
            pass it to BView::DragMessage() to start the drag. */
         BMessage* drag_message = new BMessage( MY_DRAG_ACTION );
         /* Remember, in the drag message,
            where the drag started */
         drag_message->AddPoint("click_location", where);
         DragMessage( drag_message, _SquareSides, this );
         /* 3. DRAG : this is handled by the user and system, we
            don't write any code at all to do the dragging. The
            next step will take place in the MessageReceived()
            function. */

         /* DON'T FORGET TO DELETE THE MESSAGE AFTER
            YOU'RE DONE*/
         delete drag_message;
      }
   }; /* end of MouseDown() */

   void MessageReceived(BMessage *msg) {
      /* 4. DROP : MessageReceived() can called for many
         different messages. We're only interested in ones with a
         'what' field of MY_DRAG_ACTION, as was created in
         the MouseDown() function. */
      if (msg->what == MY_DRAG_ACTION) {
         BPoint clicked;
         /* We put "click_location" into the original message,
            now we can get it out */
         msg->FindPoint("click_location", &clicked);
         BPoint whereto;
         /* The "_drop_point_" message field is automatically
            inserted by the OS; is is the screen point the
            mouse was on when the drag ended. */
         msg->FindPoint("_drop_point_", &whereto);
         /* Convert "_drop_point_" to view coordinates. */
         whereto = ConvertFromScreen(whereto);
         /* Move the square by the same amount the mouse moved
            in the drag. */
         _SquareSides.OffsetBy(whereto-clicked);
         /* Ensure the view is redrawn */
         Invalidate();
      }
   }; /* end of MessageReceived() */
}; /* end of MyDragDropView class */

class MyDragDropWindow : public BWindow {
   public:
      MyDragDropWindow(BRect frame)
         : BWindow(frame, "Drag'n'Drop Example",
                   B_TITLED_WINDOW, B_NOT_ZOOMABLE) {

         interior = new MyDragDropView(this->Bounds());
         AddChild(interior);
         Show();
      }

      bool QuitRequested() {
         be_app->PostMessage(B_QUIT_REQUESTED);
         return true;
      }
   private:
      BView* interior;
}; /* end of MyDragDropWindow class */

class MyDragDropApp : public BApplication {
   public:
      MyDragDropApp::MyDragDropApp() : BApplication(APP_SIGNATURE) {
         BRect windowRect;
         windowRect.Set(50,50,349,399);
         new MyDragDropWindow(windowRect);
      }
   private:
      MyDragDropWindow* theWindow;
}; /* end of MyDragDropApp class */

/* The "main" function creates and runs the application.*/
int main(void) {
   MyDragDropApp *theApp;
   theApp = new(MyDragDropApp);
   theApp->Run();
   delete theApp;
}