from dataclasses import dataclass, field, InitVar
from typing import Dict, Type
from typing_extensions import Protocol
from dataclasses import Field
from decorators import param

@dataclass
class Config:
    test_int: int
    test_def_int: int = 1


@param(Config)
def testfunc(arg1, config):
    """This function allows you to call it in multiple ways.

    Examples:
    >>> testfunc(1, Config(1))
    1
    Config(test_int=1, test_def_int=1)
    >>> testfunc(1, test_int=1)
    1
    Config(test_int=1, test_def_int=1)
    >>> testfunc(1, test_int=1, test_def_int=2)
    1
    Config(test_int=1, test_def_int=2)

    """
    print(arg1)
    print(config)

print(testfunc.__doc__)
# Prints -
"""
This function allows you to call it in multiple ways.

    Examples:
    >>> testfunc(1, Config(1))
    1
    Config(test_int=1, test_def_int=1)
    >>> testfunc(1, test_int=1)
    1
    Config(test_int=1, test_def_int=1)
    >>> testfunc(1, test_int=1, test_def_int=2)
    1
    Config(test_int=1, test_def_int=2)
    >>> print(testfunc.__doc__)




Tip:
	It is possible to pass the Config parameters to the function as keyword arguments.
    Accepted keyword arguments to construct the parameter object are: ('test_int', 'test_def_int')
"""
