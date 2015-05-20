#--------------------------------------------------------------------------
# The MIT License (MIT)
#
# Copyright (c) 2014 Shahzeb Ihsan
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

#--------------------------------------------------------------------------
## @file    mouse_to_active_win.py
#  @brief   Moves the mouse to the new foreground window, if selected using
#           Alt-Tab (only tested with Windows 7). Pressing causes the script
#           to exit (this will probably change to handling Ctrl-C in the near
#           future).
#
#  @author  Shahzeb Ihsan [shahzeb.ihsan@gmail.com]
#  @version 0.1

#--------------------------------------------------------------------------
# Module Imports
import time, sys, threading
import pyHook, win32con, pythoncom
from win32gui import GetForegroundWindow, GetWindowText, GetWindowRect
from win32api import SetCursorPos, GetCurrentThreadId, PostThreadMessage

#--------------------------------------------------------------------------
# Module Global Attributes
# --- N/A

#--------------------------------------------------------------------------
# Module Global Variables
# --- N/A

#--------------------------------------------------------------------------
# Module Local Attributes
# --- N/A

#--------------------------------------------------------------------------
# Module Internal Variables
# Initialize events for the "set_mouse_position" thread
event_switch = threading.Event()
event_quit = threading.Event()

# Main thread ID - required for sending WM_QUIT for stopping pythoncom.PumpMessages()
main_thread_id = GetCurrentThreadId()

#--------------------------------------------------------------------------
# Function: set_mouse_position
def set_mouse_position(show_log):
    """
    Threaded function which sets the mouse position on receiving the "event_switch" event
    from the keyboard event handler. Will exit if it recieves the "event_quit" event.

    @param args tuple: Only first value is used - bool, enables/disables debug log
    """

    global event_switch, event_quit
    current_win = ''
    previous_win = ''

    # Runs as long as "event_quit" has not been received
    while not event_quit.is_set():
        if event_switch.is_set():
            # Wait for the 'Task Switching' window to close
            while(GetWindowText(GetForegroundWindow()).split('-')[-1] == 'Task Switching'):
                pass
            time.sleep(0.25)

            # Get the foreground window's text again
            current_win = GetWindowText(GetForegroundWindow())

            # Make sure we didn't end up with the same window as before
            if current_win != previous_win:
                # Get the foreground window's dimensions
                l, t, r, b = GetWindowRect(GetForegroundWindow())

                # Calculate mouse position
                x = l + (r - l) / 2
                y = t + (b - t) / 2

                # Print the window information and new mouse co-ordinates
                if(show_log):
                    print 'Window: ', current_win.split('-')[-1], ' @[', l, t, r, b, ']'
                    print 'Setting mouse position to: (', x, ', ', y, ')'
                    print '---\n'

                # Set the new mouse position
                SetCursorPos((x, y))

                # Set the previous window to the current window
                previous_win = current_win

            # Clear "event_switch" event
            event_switch.clear()

#--------------------------------------------------------------------------
# Function: on_keyboard_event
def on_keyboard_event(event):
    """
    Keyboard event handler

    @param event KeyboardEvent: Keyboard event
    """

    global event_switch, event_quit
    global main_thread_id

    # Check for the Alt-Tab key combination
    if event.Key == 'Tab' and event.Alt != 0:
        event_switch.set()

    # Exit if Escape was preseed
    if event.Key == 'Escape':
        event_quit.set()
        PostThreadMessage(main_thread_id, win32con.WM_QUIT, 0, 0);

    return True

#--------------------------------------------------------------------------
#--- Script entry point
if __name__ == '__main__':
    """
    Script entry point.
    """

    debug = False

    # Create the hook mananger
    hm = pyHook.HookManager()

    # Register keyboard callback
    hm.KeyUp = on_keyboard_event

    # Hook into the keyboard events
    hm.HookKeyboard()

    # Create the "set_mouse_position" thread
    if(len(sys.argv) > 1):
        debug = (sys.argv[1] == "True")

    thread = threading.Thread(target = set_mouse_position, args = (debug, ))
    thread.start()

    pythoncom.PumpMessages()

    thread.join()
