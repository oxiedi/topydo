# Topydo - A todo.txt client written in Python.
# Copyright (C) 2014 Bram Schoenmakers <me@bramschoenmakers.nl>
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import Command
from Config import config
import Filter
import Sorter

class ListCommand(Command.Command):
    def __init__(self, p_args, p_todolist,
                 p_out=lambda a: None,
                 p_err=lambda a: None,
                 p_prompt=lambda a: None):
        super(ListCommand, self).__init__(p_args, p_todolist, p_out, p_err, p_prompt)

        self.sort_expression = config().sort_string()
        self.show_all = False

    def _process_flags(self):
        opts, args = self.getopt('s:x')

        for o, a in opts:
            if o == '-x':
                self.show_all = True
            elif o == '-s':
                self.sort_expression = a

        self.args = args


    def _filters(self):
        filters = []

        def grep_filters():
            for arg in self.args:
                if len(arg) > 1 and arg[0] == '-':
                    # when a word starts with -, exclude it
                    grep = Filter.NegationFilter(Filter.GrepFilter(arg[1:]))
                else:
                    grep = Filter.GrepFilter(arg)

                filters.append(grep)

        if not self.show_all:
            filters.append(Filter.DependencyFilter(self.todolist))
            filters.append(Filter.RelevanceFilter())

        grep_filters()

        if not self.show_all:
            filters.append(Filter.LimitFilter(config().list_limit()))

        return filters

    def execute(self):
        if not super(ListCommand, self).execute():
            return False

        self._process_flags()

        sorter = Sorter.Sorter(self.sort_expression)
        filters = self._filters()

        self.out(self.todolist.view(sorter, filters).pretty_print())

    def usage(self):
        return """Synopsis: ls [-x] [-s <sort_expression>] [expression]"""

    def help(self):
        return """Lists all relevant todos. A todo is relevant when:

* has not been completed yet;
* the start date (if present) has passed;
* there are no subitems that need to be completed.

When an expression is given, only the todos matching that expression are shown.

-s : Sort the list according to a sort expression. Defaults to the expression
     in the configuration.
-x : Show all todos (i.e. do not filter on dependencies or relevance)."""
