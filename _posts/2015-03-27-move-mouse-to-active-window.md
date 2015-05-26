---
layout: post
title: Move Mouse to Active Window
author: Shahzeb Ihsan
---

**Dependencies: pywin32, pyhook**

I have a weird 3 screen setup at work (don't ask me why):
...a docked laptop with a 27" monitor to its right and a 19" monitor *above* the 27" monitor.

I hate having to move the mouse from window to window when switching between windows using Alt-Tab, specially when the mouse has to be moved from the 1st screen to the 3rd screen.

So... I created this simple script to move the mouse to the middle of the new window if Alt-Tab is being used.

## Usage:
<pre>
$ python  mouse_to_active_win.py  True
</pre>

The parameter (True or False) enables/disables debug prints.

<!--more-->

## How it works
<u>**Setting the mouse position:**</u> We'll use the Windows [SetCursorPos](https://msdn.microsoft.com/en-us/library/windows/desktop/ms648394%28v=vs.85%29.aspx) API to set the mouse position. PyWin32 provides bindings for Win32 API functions, so we just have to make the API call i.e.

{% highlight python %}
# Set cursor position to (100, 100)
win32api.SetCursorPos((100, 100))
{% endhighlight %}

<u>**Getting the active (foreground) window:**</u> [GetForegroundWindow](https://msdn.microsoft.com/en-us/library/windows/desktop/ms633505(v=vs.85).aspx) returns a handle to the currently active window. The [GetWindowText](https://msdn.microsoft.com/en-us/library/windows/desktop/ms633520(v=vs.85).aspx) and [GetWindowRect](https://msdn.microsoft.com/en-us/library/windows/desktop/ms633519(v=vs.85).aspx) APIs can be used to get the window title and dimensions, respectively.

<u>**Keyboard hook for Alt-Tab:**</u> This is where PyHook comes in; it wraps low-level mouse and keyboard hooks in the Windows Hooking API for use in Python applications.

{% highlight python %}
# Create the hook manager
hm = pyHook.HookManager()

# Register keyboard callback
hm.KeyUp = on_keyboard_event()

pythoncom.PumpMessages()

# Hook into keyboard events
hm.HookKeyBoard()

# The callback...
def on_keyboard_event(event):
    # Check for the Alt-Tab key combination (basically we check for the Tab key event with Alt held down)
    if event.Key == 'Tab' and event.Alt != 0
        # Handle key event
        pass

    # Exit if SIGINT was received
    if sigint_rcvd:
        pass

    return True
{% endhighlight %}

<u>**Putting it all together:**</u> The function that sets the mouse position, **set\_mouse\_position**, is run in its own thread.

{% highlight python %}
thread = threading.Thread(target = set_mouse_position, args = (debug, ))
thread.start()
{% endhighlight %}

The set\_mouse\_position function is more or less straight forward save for one minor peculiarity: we need to make sure that the "Task Switching" window has closed before we position the mouse:

{% highlight python %}
# Wait for the 'Task Switching' window to close
while(GetWindowText(GetForegroundWindow()).split('-')[-1] == 'Task Switching'):
    pass
time.sleep(0.25)   # --> Slight delay before continuing...
{% endhighlight %}

The rest of the implementation is self-explanatory, **on\_keyboard\_event** posts a switch event on Alt-Tab and a quit event on SIGINT (Ctrl-C). A signal handler is installed for handling SIGINT (Ctrl-C).

If you don't want to download or clone the whole repository, you can view the complete source for this script on GitHub [here](https://github.com/schaazzz/script_magic/blob/master/mouse_to_active_win.py) or download the file [here](https://raw.githubusercontent.com/schaazzz/script_magic/master/mouse_to_active_win.py)
