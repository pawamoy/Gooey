'''The command line interface.'''

import sys
from importlib import import_module
from importlib.metadata import entry_points

from gooey import Gooey


def main(args=None):
    args = args or sys.argv[1:]
    if not args:
        script_name = "gooey"
    else:
        script_name = args[0]
    scripts = {script.name: script for script in entry_points().get('console_scripts')}
    if script_name in scripts:
        script = scripts[script_name]
        module_path = script.module
        function_name = script.attr
        prog = script_name
    elif ':' in script_name:
        module_path, function_name = args[0].split(':')
        prog = module_path.split('.', 1)[0]
    if len(args) > 1:
        if args[1] == '--':
            del args[1]
    sys.argv = [prog, *args[1:]]
    module = import_module(module_path)
    function = getattr(module, function_name)
    return Gooey(use_cmd_args=True)(function)
