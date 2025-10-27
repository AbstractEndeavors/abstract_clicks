from src import *
info = get_open_browser_tab(url="https://example.com",title=None)
get_window_mgr().move_window_with_mouse(**info, monitor_index=3)
#clipboard = get_clipboard()
