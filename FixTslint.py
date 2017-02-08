import sublime
import subprocess
import os
import sublime_plugin


def plugin_loaded():
    pref.load()


class Pref:
    keys = [
        "node_executable_path",
        "tslint_executable_path",
        "extensions_to_execute"
    ]

    def load(self):
        self.settings = sublime.load_settings('FixTslint.sublime-settings')
        for key in self.keys:
            self.settings.clear_on_change(key)
            setattr(self, key, self.settings.get(key))
            self.settings.add_on_change(key, pref.load)


pref = Pref()


class FixTslintEventListener(sublime_plugin.EventListener):
    """Event listener for the plugin"""
    def on_post_save(self, view):
        file_name = view.file_name()
        file_extension = os.path.splitext(file_name)[1]
        if file_extension in pref.extensions_to_execute:
            print("FixTslint" + file_name)
            subprocess.Popen(
                [pref.node_executable_path, pref.tslint_executable_path, file_name, '--fix'],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT
            )
