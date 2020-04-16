from types import ModuleType
import sys


class Module(ModuleType):
    def __init__(self, name, module, wrapper):
        super().__init__(name)
        self.__module = module
        self.__wrapper = wrapper

    def __getattr__(self, attr):
        orig = getattr(self.__module, attr)
        return lambda *args, **kwargs: self.__wrapper(orig, *args, **kwargs)


def wrap(name, module, wrapper):
    fullname = 'wrapper.'+name
    if fullname in sys.modules:
        return
    sys.modules[fullname] = Module(name, module, wrapper)
