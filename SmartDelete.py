import sublime
import sublime_plugin
import re


class SmartDeleteCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        if len(self.view.sel()) is not 1:
            # Default Delete if there are multiple selections.
            self.view.run_command('right_delete')
            return

        # Has only 1 sel
        for s in self.view.sel():
            if s.empty():
                line = self.view.line(s)
                after = self.view.substr(line)[s.end() - line.end():]
                next_line = self.view.line(sublime.Region(line.end() + 1, line.end() + 1))
                next_line_is_not_empty = re.match(r'^\s*$', self.view.substr(next_line)) is None

                if(len(line) > 0 and next_line_is_not_empty and (after.isspace() or line.end() == s.end())):
                    b = s.begin()
                    e = s.end()

                    while(self.view.substr(b - 1).isspace()):
                        b = b - 1

                    while(self.view.substr(e).isspace()):
                        e = e + 1

                    self.view.sel().clear()
                    self.view.sel().add(sublime.Region(b, e))
                else:
                    self.view.run_command('right_delete')

        for s in self.view.sel():
            #edit = self.view.begin_edit()
            self.view.erase(edit, s)
            #self.view.end_edit(edit)
