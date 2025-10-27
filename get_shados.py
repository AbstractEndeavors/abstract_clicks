def get_manager_defs():
    texts ='''class titleManager(metaclass=SingletonMeta):
    """Comprehensive title manager for browser windows."""
    def __init__(self, storage_path=None):
        if not hasattr(self, 'initialized'):
            self.initialized = True
            self.titles = {}  # {sudo_title: {url, title, browser_title, window_id, pid, html, soup}}
            self.storage_path = storage_path or "title_manager_data.json"
            self.load_titles()

    def load_titles(self):
        """Load titles from storage file."""
        try:
            if read_from_file(self.storage_path):
                with open(self.storage_path, 'r') as f:
                    data = json.load(f)
                    self.titles = {k: v for k, v in data.items() if isinstance(v, dict)}
        except Exception as e:
            print(f"Error loading titles: {e}")

    def save_titles(self):
        """Save titles to storage file."""
        try:
            with open(self.storage_path, 'w') as f:
                json.dump(self.titles, f, indent=2)
        except Exception as e:
            print(f"Error saving titles: {e}")

    def make_title(self, title=None, url=None, html_content=None, html_file_path=None):
        """Create or update a title entry with associated metadata."""
        if not title and not url:
            print("Title or URL required")
            return False

        try:
            # Get browser title from URL
            browser_title = get_title(url=url) if url else title
            sudo_title = title or browser_title or str(uuid.uuid4())  # Fallback to UUID

            # Check if window exists
            info = is_window_open(url=url, title=title, browser_title=browser_title)
            if not info and url:
                # Open new tab if no window found
                info = self.open_browser_tab(url=url, title=sudo_title, html_content=html_content, html_file_path=html_file_path)

            # Update title entry
            self.titles[sudo_title] = {
                "url": url or info.get("url", "Unknown"),
                "title": sudo_title,
                "browser_title": browser_title,
                "window_id": info.get("window_id"),
                "pid": info.get("pid"),
                "html": info.get("html"),
                "soup": None  # Avoid serializing soup
            }
            self.save_titles()
            return self.titles[sudo_title]
        except Exception as e:
            print(f"Error making title: {e}")
            return False

    def get_window_info(self, url=None, title=None, browser_title=None):
        """Retrieve information about an existing window."""
        try:
            info = is_window_open(url=url, title=title, browser_title=browser_title)
            if info:
                sudo_title = title or browser_title or info.get("title")
                if sudo_title:
                    self.titles[sudo_title] = self.titles.get(sudo_title, {})
                    self.titles[sudo_title].update(info)
                    self.save_titles()
                return info
            return {}
        except Exception as e:
            print(f"Error getting window info: {e}")
            return {}

    def get_title_from_url(self, url):
        """Get the title for a given URL."""
        try:
            browser_title = get_title(url=url)
            if browser_title:
                self.titles[browser_title] = self.titles.get(browser_title, {})
                self.titles[browser_title].update({"url": url, "browser_title": browser_title})
                self.save_titles()
            return browser_title
        except Exception as e:
            print(f"Error getting title from URL: {e}")
            return ""

    def open_browser_tab(self, url=None, title="My Permanent Tab", html_file_path=None, html_content=None, duplicate=False):
        """Open a new browser tab or return existing window info."""
        try:
            soup = call_soup(url=url)
            browser_title = get_title(soup=soup)
            info = self.get_window_info(title=title, browser_title=browser_title, url=url)
            if info and not duplicate:
                return info

            html_content = get_html_content(html_content=html_content, title=title)
            if html_content and html_file_path:
                write_to_file(contents=html_content, file_path=html_file_path)
                url = url or f"file://{html_file_path}"

            webbrowser.open_new_tab(url)
            time.sleep(1.0)  # Wait for tab to open
            info = self.get_window_info(title=title, browser_title=browser_title, url=url)
            return info
        except Exception as e:
            print(f"Error opening browser tab: {e}")
            return {"window_id": None, "title": title, "pid": None, "url": url}

    def switch_window(self, title):
        """Switch focus to a window by title."""
        try:
            if platform.system() == 'Linux':
                result = subprocess.run(
                    ['xdotool', 'search', '--name', title],
                    capture_output=True, text=True
                )
                window_ids = result.stdout.strip().split()
                if window_ids:
                    subprocess.run(['xdotool', 'windowactivate', window_ids[0]])
                    print(f"Switched to window: {title}")
                    return True
                print(f"No window found: {title}")
                return False
            elif platform.system() == 'Windows' and win32gui:
                def callback(hwnd, target):
                    if title.lower() in win32gui.GetWindowText(hwnd).lower():
                        win32gui.SetForegroundWindow(hwnd)
                        return False
                win32gui.EnumWindows(callback, None)
                print(f"Switched to window: {title}")
                return True
            elif platform.system() == 'Darwin' and NSWorkspace:
                workspace = NSWorkspace.sharedWorkspace()
                for app in workspace.runningApplications():
                    if title.lower() in app.localizedName().lower():
                        app.activateWithOptions_(0)
                        print(f"Switched to window: {title}")
                        return True
                print(f"No window found: {title}")
                return False
            else:
                print("Unsupported platform for window switching")
                return False
        except Exception as e:
            print(f"Error switching window: {e}")
            return False

    def delete_title(self, title):
        """Remove a title entry."""
        try:
            if title in self.titles:
                del self.titles[title]
                self.save_titles()
                return True
            return False
        except Exception as e:
            print(f"Error deleting title: {e}")
            return False

    def get_all_titles(self):
        """Return all stored titles."""
        return self.titles'''
    def eliminate_space(obj,del_obj):
        del_obj_space = f"{del_obj} "
        while True:
            if del_obj_space in obj:
                obj.replace(del_obj_space,obj)
            else:
               
                return obj.replace(f"{del_obj},",'')
    from abstract_utilities import eatAll
    all_funcs = []
    for text in texts.split('def ')[1:]:
        title_spl = text.split('(')
        func_name = title_spl[0]
        variables = title_spl[1].split(')')[0].replace('\n','').split(',')
        variables = [eatAll(str(variable),['',' ','\n','\t']) for variable in variables]
        kwargs={}
        for i,variable in enumerate(variables):
            key = variable.split('=')[0].split(':')[0]
            if key != 'self':
                value = variable.split(':')[0].split('=')[-1]
                if key == value:
                    value == None
                kwargs[key]=value
            var_strings=[]
            var_strings2=[]
            
        for key,value in kwargs.items():
            key=eatAll(key,['',' ','\n','\t'])
            value=eatAll(value,['',' ','\n','\t'])
            var_strings.append(f"{key}={value}")
            var_strings2.append(f"{key}={key}")
        variables = [eliminate_space(vari,'self') for vari in variables]
        if 'self'in variables:
            variables.remove('self')

        var_string = f"({','.join(variables)})"
        var_strings2 = f"({','.join(var_strings2)})"
        all_funcs.append(f"""def {func_name}{var_string}:
        return titlemanager.{func_name}{var_strings2}""")
    return '\n\n'.join(all_funcs)
input(get_manager_defs())
