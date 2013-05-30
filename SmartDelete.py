import sublime
import sublime_plugin
import re


class SmartDeleteCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        for s in self.view.sel():
            if s.empty():
                line = self.view.line(s)
                after = self.view.substr(line)[s.end() - line.end():]

                if(len(line) > 0 and (re.match(r"^\s+$", after) or line.end() == s.end())):
                    b = s.begin()
                    while(self.view.substr(b - 1).isspace()):
                        b = b - 1
                        self.view.sel().add(sublime.Region(b, s.end()))

                    e = s.end()
                    while(self.view.substr(e).isspace()):
                        e = e + 1
                        self.view.sel().add(sublime.Region(s.begin(), e))
                else:
                    self.view.run_command('right_delete')

        for s in self.view.sel():
            edit = self.view.begin_edit()
            self.view.erase(edit, s)
            self.view.end_edit(edit)
