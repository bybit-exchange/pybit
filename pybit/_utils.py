""" Utility classes and functions. """

import inspect
from abc import abstractmethod, ABC
from typing import Optional, Any
from warnings import warn
from packaging import version
from . import VERSION

DEPRECATION_CONFIG = 'deprecation_config'


class DeprecationConfig(ABC):
    """ Base deprecation configuration class model """

    modification_version: str
    details: Optional[str]

    def __init__(
        self,
        modification_version: str,
        details: Optional[str] = None,
    ) -> None:
        self.modification_version = modification_version
        self.details = details

    @property
    def should_be_modified(self) -> bool:
        """ Check if there is a need to modify the function/class(remove, or replace some arguments)."""
        return version.parse(VERSION) >= version.parse(self.modification_version)

    @property
    @abstractmethod
    def warn_message(self) -> Optional[str]:
        """ Return the deprecation message. 
        This method should be implemented in the subclass.

        Returns:
            Optional[str]: 
                The deprecation message. 
                If there is no message to be shown, return None.
        """

    def warn(self):
        """ Warn the user about the deprecation. """
        msg = self.warn_message
        if msg:
            warn(msg, DeprecationWarning, 2)


class ClassDeprecationConfig(DeprecationConfig):
    """ Configuration class model for deprecated classes. 

    Args:
        remove_version (str): The version in which the class will be removed.
        cls (type): The class to be deprecated.
        details (Optional[str]): Additional details about the deprecation.
        replacement (Optional[str | type]): The class to be used as a replacement(if any).
    """

    cls: type
    replacement: Optional[str | type]

    def __init__(
        self,
        remove_version: str,
        cls: type,
        details: Optional[str] = None,
        replacement: Optional[str] = None,
    ) -> None:
        self.cls = cls
        self.replacement = replacement
        super().__init__(remove_version, details)

    @property
    def warn_message(self) -> str:
        message = f'"{self.cls.__name__}" is deprecated and will be removed in version {self.modification_version}.'
        if self.replacement:
            replacement = self.replacement if isinstance(
                self.replacement, str) else self.replacement.__name__
            message += f' Use "{replacement}" instead.'
        if self.details:
            message += f' {self.details}'
        return message


class FunctionArgumentsDeprecationConfig(DeprecationConfig):
    """ Configuration class model for deprecated function arguments. 

    Args:
        modification_version (str): 
            The version in which the arguments will be removed/replaced.
        to_be_removed (Optional[list[str] | str]): 
            The arguments to be removed. Either a list of arguments 
            or a single argument(if there is only one arg to be removed).
        to_be_replaced (Optional[list[tuple[str, str]] | tuple[str, str]]): 
            The arguments to be replaced. 
            Either a list of tuples of arguments to be replaced or a single tuple
            (if there is only one arg to be replaced). First element of the tuple is 
            the argument to be replaced and the second element is the argument to be replaced with.
        function_name (str): The name of the function.
        kwargs (dict[str, Any]): The keyword arguments of the function.
        details (Optional[str]): Additional details about the deprecation.
    """
    kwargs: dict[str, Any]
    function_name: str
    to_be_removed: list[str]
    to_be_replaced: list[tuple[str, str]]

    def __init__(
        self,
        modification_version: str,
        to_be_removed: list[str] | str,
        to_be_replaced: list[tuple[str, str]] | tuple[str, str],
        function_name: str,
        kwargs: dict[str, Any],
        details: Optional[str] = None,
    ) -> None:
        self.kwargs = kwargs
        self.function_name = function_name
        self.to_be_removed = to_be_removed if isinstance(
            to_be_removed, list) else [to_be_removed]
        self.to_be_replaced = to_be_replaced if isinstance(
            to_be_replaced, list) else [to_be_replaced]
        super().__init__(modification_version, details)

    @property
    def warn_message(self) -> Optional[str]:
        replace_args = list(
            filter(lambda x: x[0] in self.kwargs, self.to_be_replaced)
        )
        if len(self.to_be_removed) + len(replace_args) == 0:
            return None

        message = (
            f'The following arguments from function "{self.function_name}" '
            'are deprecated and will be removed/replaced in version '
            f'{self.modification_version}:'
        )
        if len(self.to_be_removed) > 0:
            message += '\nArguments to be removed:\n\t'
            message += '\n\t'.join(
                [f'- "{x}"' for x in self.to_be_removed]
            )
        if len(replace_args) > 0:
            message += '\nArguments to be replaced:\n\t'
            message += '\n\t'.join(
                [f'- "{x[0]}"(Replace with "{x[1]}")' for x in replace_args]
            )
        if self.details:
            message += f' {self.details}'

        return message


def deprecate_class(
        remove_version: str,
        details: Optional[str] = None,
        replacement: Optional[str | type] = None
):
    """ Decorator to deprecate a class. 

    Args:
        remove_version (str): The version in which the class will be removed.
        details (Optional[str]): Additional details about the deprecation.
        replacement (Optional[str | type]): The class to be used as a replacement(if any).
    """
    def decorator(cls):
        if not inspect.isclass(cls):
            raise AssertionError(
                "This decorator can only be applied to classes.")
        setattr(
            cls,
            DEPRECATION_CONFIG,
            ClassDeprecationConfig(
                remove_version=remove_version,
                cls=cls,
                details=details,
                replacement=replacement,
            )
        )
        init = cls.__init__

        def __init__(self, *args, **kwargs):
            if cls is self.__class__:
                getattr(self, DEPRECATION_CONFIG).warn()
            init(self, *args, **kwargs)
        cls.__init__ = __init__
        return cls
    return decorator


def deprecate_function_arguments(
    modification_version: str,
    to_be_removed: Optional[list[str] | str] = None,
    to_be_replaced: Optional[list[tuple[str, str]] | tuple[str, str]] = None,
    details: Optional[str] = None,
):
    """ Decorator to deprecate function arguments. 

    Args:
        modification_version (str): 
            The version in which the arguments will be removed/replaced.
        to_be_removed (Optional[list[str] | str]): 
            The arguments to be removed. Either a list of arguments 
            or a single argument(if there is only one arg to be removed).
        to_be_replaced (Optional[list[tuple[str, str]] | tuple[str, str]]): 
            The arguments to be replaced. 
            Either a list of tuples of arguments to be replaced or a single tuple
            (if there is only one arg to be replaced). First element of the tuple is 
            the argument to be replaced and the second element is the argument to be replaced with.
        details (Optional[str]): Additional details about the deprecation.
    """
    if to_be_removed is None and to_be_replaced is None:
        raise ValueError(
            'At least one of "to_be_removed" or "to_be_replaced" must be provided.'
        )

    def decorator(func):
        if not inspect.isfunction(func):
            raise AssertionError(
                "This decorator can only be applied to functions.")
        config = FunctionArgumentsDeprecationConfig(
            modification_version=modification_version,
            to_be_removed=to_be_removed or [],
            to_be_replaced=to_be_replaced or [],
            function_name=func.__qualname__,
            kwargs={},
            details=details,
        )

        def wrapper(*args, **kwargs):
            config.kwargs = kwargs
            config.warn()
            return func(*args, **kwargs)

        setattr(
            wrapper,
            DEPRECATION_CONFIG,
            config,
        )
        return wrapper
    return decorator
