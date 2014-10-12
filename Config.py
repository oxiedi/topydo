"""
This module contains some definitions to configure the application.
"""

DEFAULT_ACTION = 'ls'
COLORS = True
HIGHLIGHT_PROJECTS_CONTEXTS = True

FILENAME = 'todo.txt'
ARCHIVE_FILENAME = 'done.txt'

TAG_START = 't'
TAG_DUE = 'due'
TAG_STAR = 'star'

SORT_STRING = 'desc:importance,due,desc:priority'
IGNORE_WEEKENDS = True # for calculating the importance value
