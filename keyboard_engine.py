import time
import threading
import datetime as dt
import keyboard
import pyperclip
from database import Database

class KeyboardEngine:
    def __init__(self, suggestion_callback=None):
        self.db = Database()
        self.running = False
        self.buffer = ""
        self.thread = None
        self.is_simulating = False
        self.suggestion_callback = suggestion_callback

    def start(self):
        if self.running:
            return
        self.running = True
        self.thread = threading.Thread(target=self._listen, daemon=True)
        self.thread.start()

    def stop(self):
        self.running = False

    def _listen(self):
        keyboard.hook(self._on_key_event)
        while self.running:
            time.sleep(0.1)
        keyboard.unhook_all()

    def _on_key_event(self, e):
        if self.is_simulating:
            return

        if e.event_type != keyboard.KEY_DOWN:
            return

        name = e.name

        if name == 'backspace':
            if len(self.buffer) > 0:
                self.buffer = self.buffer[:-1]
            self.check_suggestions()
            return

        if name == 'space':
            self.check_and_trigger()
            self.buffer = ""
            if self.suggestion_callback:
                self.suggestion_callback([])
            return

        if name in ('enter', 'tab', 'esc'):
            self.buffer = ""
            if self.suggestion_callback:
                self.suggestion_callback([])
            return

        ignored_keys = {
            'shift', 'right shift', 'ctrl', 'right ctrl', 'alt', 'alt gr',
            'caps lock', 'windows', 'left windows', 'right windows',
            'up', 'down', 'left', 'right', 'page up', 'page down',
            'home', 'end', 'insert', 'delete', 'f1', 'f2', 'f3', 'f4',
            'f5', 'f6', 'f7', 'f8', 'f9', 'f10', 'f11', 'f12', 'print screen',
            'scroll lock', 'pause'
        }
        if name in ignored_keys:
            return

        if len(name) == 1 or name in (':', '_', '-', '.', '@', '#', '!', '?', '/'):
            self.buffer += name
            if len(self.buffer) > 100:
                self.buffer = self.buffer[-100:]
            self.check_suggestions()

    def check_suggestions(self):
        if not self.suggestion_callback:
            return
        
        if not self.buffer.startswith(":"):
            self.suggestion_callback([])
            return

        shortcuts = self.db.get_all_shortcuts()
        suggestions = []
        for row in shortcuts:
            _, shortcut, replacement, category, is_sensitive, enabled, _ = row
            if not enabled or is_sensitive:
                continue
            if shortcut.startswith(self.buffer):
                suggestions.append((shortcut, replacement))

        self.suggestion_callback(suggestions)

    def check_and_trigger(self):
        if self.check_parameterized():
            return
        if self.check_dynamic_and_normal():
            return

    def check_parameterized(self):
        shortcuts = self.db.get_all_shortcuts()
        for row in shortcuts:
            shortcut_id, shortcut, replacement, category, is_sensitive, enabled, _ = row
            if not enabled:
                continue
            
            if shortcut in self.buffer and "{{arg}}" in replacement:
                idx = self.buffer.rfind(shortcut)
                after_shortcut = self.buffer[idx + len(shortcut):]
                after_shortcut_stripped = after_shortcut.strip()
                
                if after_shortcut_stripped:
                    parts = after_shortcut_stripped.split()
                    if parts:
                        arg = parts[0]
                        full_matched_str = shortcut + " " + arg
                        final_rep = replacement.replace("{{arg}}", arg)
                        
                        self.db.increment_usage(shortcut_id)
                        self.trigger_replacement(full_matched_str, final_rep)
                        return True
        return False

    def check_dynamic_and_normal(self):
        now = dt.datetime.now()
        dynamic_map = {
            ":d": now.strftime("%d.%m.%Y"),
            ":t": now.strftime("%H:%M"),
            ":dt": now.strftime("%d.%m.%Y %H:%M")
        }

        for dyn_key, dyn_val in dynamic_map.items():
            if self.buffer == dyn_key:
                self.trigger_replacement(dyn_key, dyn_val)
                return True

        shortcuts = self.db.get_all_shortcuts()
        for row in shortcuts:
            shortcut_id, shortcut, replacement, category, is_sensitive, enabled, _ = row
            if not enabled:
                continue

            if self.buffer == shortcut:
                self.db.increment_usage(shortcut_id)
                self.trigger_replacement(shortcut, replacement)
                return True

        return False

    def trigger_replacement(self, shortcut_to_delete, replacement):
        self.is_simulating = True
        
        backspace_count = len(shortcut_to_delete) + 1
        
        for _ in range(backspace_count):
            keyboard.send('backspace')
            time.sleep(0.01)

        try:
            old_clipboard = pyperclip.paste()
        except:
            old_clipboard = ""

        pyperclip.copy(replacement)
        time.sleep(0.03)
        
        keyboard.send('ctrl+v')
        time.sleep(0.05)
        keyboard.send('space')
        time.sleep(0.02)

        pyperclip.copy(old_clipboard)
        time.sleep(0.02)
        self.is_simulating = False