from browser_utils import *


def get_html_inspect(result):
    # Capture screenshot of specific monitor
    if result:
        pyautogui = get_auto_gui()
        pyautogui.click(clicks=1)
        pyautogui.click(button='right')
        pyautogui.press('esc')
        pyautogui.press('f2')
        pyautogui.hotkey('ctrl', 'i')
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.hotkey('ctrl', 'c')
        # Switch to a window
        print("Switching to window in 3 seconds...")
        # Paste extracted text
        print("Pasting extracted text in 1 second...")
        time.sleep(3)
        clipboard.custom_paste()
        return True
def get_paste_in_prompt(result):
    # Capture screenshot of specific monitor
    if result:
        pyautogui = get_auto_gui()
        pyautogui.click(clicks=1)
        pyautogui.click(button='right')
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(0.1)
        pyautogui.hotkey('ctrl', 'v')
        pyautogui.hotkey('Enter')
        # Switch to a window
        print("Switching to window in 3 seconds...")
        # Paste extracted text
        print("Pasting extracted text in 1 second...")
        
        clipboard.custom_paste()
        return True
def get_paste_in_prompt(result):
    
    # Capture screenshot of specific monitor
    if result:
        pyautogui = get_auto_gui()
        pyautogui.click(clicks=1)
        pyautogui.click(button='right')
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(0.1)
        pyautogui.hotkey('ctrl', 'v')
        pyautogui.hotkey('Enter')
        # Switch to a window
        print("Switching to window in 3 seconds...")
        # Paste extracted text
        print("Pasting extracted text in 1 second...")
        
        clipboard.custom_paste()
        return True

AUTO_DICTS = {
    "prompt":
    {
        "text":
        [
            'ask',
            ' ',
            'anything'],
        "image":
        [
            ],
        "functions":
        {
            "pre_functions":
            [
                ],
               "post_functions":
            [
                get_paste_in_prompt
                ]
            }
        },
    "enter":
    {
        "text":
        [
            ],
        "image":
        [
            "/home/computron/Pictures/Screenshots/Screenshot from 2025-06-09 06-37-25.png"
            ],
        "functions":
        {
            "pre_functions":
            [
                ],
               "post_functions":
            [
                get_html_inspect
                ]
            }
        },

    "inspect":
    {
        "text":
        [
            'ask',
            ' ',
            'anything'
            ],
        "image":
        [
            ],
        "functions":
        {
            "pre_functions":
            [
                ],

            "post_functions":
            [
                get_html_inspect
                ]
        }
    }
}
EXISTING_BROWSERS_DATA = [{'window_id': '0x0320003e', 'desktop': '0', 'pid': '6504', 'host': 'computron-System-Product-Name', 'window_title': 'ChatGPT — Mozilla Firefox'}, {'window_id': '0x0320003e', 'desktop': '0', 'pid': '6504', 'host': 'computron-System-Product-Name', 'window_title': 'ChatGPT — Mozilla Firefox'}, {'window_id': '0x0520676a', 'desktop': '0', 'pid': '0', 'host': 'N/A', 'window_title': 'excel_module.py - /home/computron/miniconda/lib/python3.12/site-packages/abstract_pandas/excel_module.py (3.12.4)'}, {'window_id': '0x0320003e', 'desktop': '0', 'pid': '6504', 'host': 'computron-System-Product-Name', 'window_title': 'ChatGPT — Mozilla Firefox'}, {'window_id': '0x0520676a', 'desktop': '0', 'pid': '0', 'host': 'N/A', 'window_title': 'excel_module.py - /home/computron/miniconda/lib/python3.12/site-packages/abstract_pandas/excel_module.py (3.12.4)'}, {'window_id': '0x0520676a', 'desktop': '0', 'pid': '0', 'host': 'N/A', 'window_title': 'excel_module.py - /home/computron/miniconda/lib/python3.12/site-packages/abstract_pandas/excel_module.py (3.12.4)'}, {'window_id': '0x02a00004', 'desktop': '0', 'pid': '44518', 'host': 'computron-System-Product-Name', 'window_title': 'auto_utils'}]
def check_instances(instances,key,value):
    for instance in instances:
        instance_value = instance.get(key)
        if instance_value and instance_value == value:
            return instance
def get_instance(sudo_name=None,window_name=None,window_id=None,window_title=None,instances=[]):
    user_instance = {'window_id':window_id,'window_name':window_name,'window_title':window_title,'sudo_name':sudo_name}
    for key,value in user_instance.items():
        result=check_instances(instances,key,value)
        if result:
            return result
def get_browser_component(existing_browser_info):
    window_id= existing_browser_info.get("window_id")
    geometry = get_window_geometry(window_id)
    monitors = get_monitors()
    existing_browser_info.update(get_monitor_location(window_id=window_id))
    existing_browser_info['window'] = get_window_geometry(window_id)
    control_browser_window(window_id=window_id,action="maximize")
    browser_name=existing_browser_info.get("window_title")
    open_new_tab_in_browser(url='https://example.com',
                            title=browser_name,
                            window_id=window_id)
    move_browser_to_monitor(window_id,
                            monitors[2])
    existing_browser_info.update(get_monitor_location(window_id=window_id))
    existing_browser_info['window'] = get_window_geometry(window_id)
    


class inspectManager(metaclass=SingletonMeta):
    def __init__(self,
                 url=None,
                 sudo_name=None,
                 window_name=None,
                 window_id=None,
                 window_title=None,
                 output_file=None,
                 target_text=None,
                 functions=None,
                 target_image=None,
                 *args,
                 **kwargs):
        
        

        if not hasattr(self, 'initialized'):
            self.initialized = True
            self.inspect_points = []
        self.sudo_name=sudo_name
        self.window_name=window_name
        self.window_id=window_id
        self.window_title=window_title
        self.url=url
        self.target_text=target_text
        self.functions=functions
        self.target_image=target_image
        self.output_file = output_file
    def get_inspect_points(self,*args,**kwargs):
        sudo_name = kwargs.get('sudo_name',self.sudo_name)
        window_name = kwargs.get('window_name',self.window_name)
        window_id = kwargs.get('window_id',self.window_id)
        window_title = kwargs.get('window_title',self.window_title)
        output_file = kwargs.get('output_file',self.output_file)
        url =kwargs.get('url',self.url)
        inspect_points = kwargs.get('inspect_points',self.inspect_points)
        target_text=kwargs.get('target_text',self.target_text)
        functions=kwargs.get('functions',self.functions)
        target_image=kwargs.get('target_image',self.target_image)
        output_file = kwargs.get('output_file',self.output_file)
        monitor_info = get_monitor_location(window_id=window_id)
        instance = get_instance(sudo_name=sudo_name,
                                window_name=window_name,
                                window_id=window_id,
                                window_title=window_title,
                                instances=inspect_points)
        if instance:
            inspect_points = instance.get('inspect')
            return inspect_points
        else:
            inspect_points = self.create_inspect_points(self,url=url,
                 sudo_name=sudo_name,
                 window_name=window_name,
                 window_id=window_id,
                 window_title=window_title,
                 output_file=output_file,
                 target_text=target_text,
                 functions=functions,
                 target_image=target_image)
            return inspect_points
    def create_inspect_points(self,*args,**kwargs):
        sudo_name = kwargs.get('sudo_name',self.sudo_name)
        window_name = kwargs.get('window_name',self.window_name)
        window_id = kwargs.get('window_id',self.window_id)
        window_title = kwargs.get('window_title',self.window_title)
        target_text=kwargs.get('target_text',self.target_text)
        functions=kwargs.get('functions',self.functions)
        target_image=kwargs.get('target_image',self.target_image)
        output_file = kwargs.get('output_file',self.output_file)
        monitor_info = get_monitor_location(window_id=window_id)
        screenshot_mgr = screenshotManager(
            output_file=output_file,
            target_text=target_text,
            functions=functions,
            target_image=target_image
            )
        url =kwargs.get('url',self.url)
        inspect_points = {'window_id':window_id,
             'window_name':window_name,
             'window_title':window_title,
             'sudo_name':sudo_name,
             "coords":{},
             "monitor_info":{},
             "output_file":output_file,
             "target_image":target_image,
             "functions":functions,
             "target_text":target_text,
             "screenshot_mgr":screenshot_mgr}
        self.inspect_points.append(inspect_points)
        return inspect_points
    def get_inspect(self,*args,**kwargs):
        inspect_points = self.get_inspect_points(self,*args,**kwargs)
        move_browser_to_monitor(inspect_points.get('window_id'),
                            monitors[2])
        right_half = randomize_pointer_in_browser_area(inspect_points.get('window_id'), area_offsets=None,
                                      half='right')
        pyautogui.click(button='right')
        pyautogui.hotkey('ctrl',
                         'shift',
                         'q')
        get_pointer_function(key="inspect",
                             index=1)
def get_browser_data(title,url=None,browsers_data=None):
    
    existing_browsers_data = browsers_data or get_existing_browsers_data(title=title, url=url) #or EXISTING_BROWSERS_DATA #
    if existing_browsers_data:
        input(existing_browsers_data)
        window_titles = [existing_browser_data.get('window_title') for existing_browser_data in existing_browsers_data]
        existing_title = [get_closest_match_from_list(title, total_list=window_titles,case_sensative=False)]
        if existing_title:
            existing_title = existing_title[0]
            existing_browser_data = [existing_browser_data for existing_browser_data in existing_browsers_data if existing_title == existing_browser_data.get('window_title')]
            if existing_browser_data:
                existing_browser_data = existing_browser_data[0]
                return existing_browser_data
class gptManager(metaclass=SingletonMeta):
    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.initialized = True
            self.gptUrl = 'https://chatgpt.com'
            self.title = "chatgpt"
            self.basic_id = {"url":self.gptUrl,"title":self.title}
            self.auto_dict = AUTO_DICTS.get("inspect")
            self.output_file=os.path.join(os.getcwd(),'GPT_screenshot.png')
            self.functions=self.auto_dict.get("post_functions")
            self.target_text=self.auto_dict.get("text")
            self.existing_browser_info = None
            self.existing_browser_info = self.get_existing_browser_info()
            self.inspect_points = None
    def get_existing_browser_info(self):
        if self.existing_browser_info== None:
            existing_browser_data = get_browser_data(browsers_data=None,**self.basic_id)
           
            if existing_browser_data:
                self.existing_browser_data = existing_browser_data
            else:
                browser_js = get_browser_tab_and_index(**self.basic_id)
                existing_browser_data = get_browser_data(self.title,browsers_data=None)
                if existing_browser_data:
                    self.existing_browser_data = existing_browser_data
        return existing_browser_data
    def get_inspect(self):
        combined = {**self.existing_browser_info,**self.basic_id,**{"output_file":self.output_file,"functions":self.functions,"target_text":self.target_text}}
        inspect_mgr = inspectManager(**combined)
        self.inspect_points = inspect_mgr.get_inspect_points()
        get_browser_component(self.existing_browser_info)
        self.get_inspect(**self.inspect_points)
        return True

def click_conversations(extracted_texts,
                        monitor_info):
    keys = [
        ["indexeddb","index","ed","db"],
        ["https://chatgpt.com","https://","chatgpt",".com"],
        ["conversationsDatabase (default)","convers","ations","Data","base"," (default)"],
        ["conversations","convers","ations"],
        ["color","-","sche","me",":"," ","dark",";"],
    ]
    for key_parts in keys:
        for key in key_parts:
            outcome = clipboard.move_mouse_to_text(
                extracted_texts,
                monitor_info,
                target_text=key
                )
            if outcome:
                break
def get_monitor_texts(comp):
    screenshot_file = "new_screen.png"
    for monitor_index in range(3):	  # Change to 2, 3, etc., for other monitors
        monitor_info = clipboard.screenshot_specific_screen(screenshot_file,
                                                            monitor_index)
        if monitor_info:
            dicts = clipboard.perform_ocr(screenshot_file=file_path,
                                          confidence_threshold=60)#clipboard.perform_ocr(file_path)
            texts = [text.get('text') for text in dicts]
            closest_match = get_closest_match_from_list(comp_obj=comp,
                                                        total_list=texts,case_sensative=False)
            best_dict = [item for item in dicts if item.get('text') == closest_match]
            if best_dict:
                best_dict = best_dict[0]
                x = best_dict['x'] + best_dict['width'] // 2
                y = best_dict['y'] + best_dict['height'] // 2
                # Adjust for monitor offset
                if monitor_info:
                    x += monitor_info['left']
                    y += monitor_info['top']
                # Move mouse
                pyautogui.moveTo(x, y, duration=0.5)  # Smooth movement over 0.5s
                return True
def get_monitor_text(target_text):
    # Capture screenshot of specific monitor
    get_monitor_texts()
            
    # Move mouse to first text (or specify target_text="some text")
    if extracted_texts:
        #clipboard.move_mouse_to_text(extracted_texts, monitor_info, text_index=0)
        # Example with specific text:
        result = clipboard.move_mouse_to_text(extracted_texts, monitor_info, target_text=target_text)
        if result:
            return True

def get_gpt_browser():
    browser_js = get_browser_tab_and_index(url='https://chatgpt.com',
                          title="chatgpt")
    return browser_js
def get_confidence(string,comp):
    found = ['']
    comp = comp.lower()
    string = string.lower()
    string_len = len(string)
   
    for i in range(string_len):
        if string_len>i:
            nustring = string[:i+1]
            nu_len = len(list(nustring))
            if nustring in comp:
                found.append(nustring)
    items = [len(item) for item in found] or [0]
    items.sort()
    if items[0] >0:
        return items[0]/strinresultg_len
    return 0
gpt_mgr = gptManager()
gpt_mgr.get_inspect()
