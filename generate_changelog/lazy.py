"""
Lazy object evaluation.

Derived from: https://coderbook.com/python/2020/04/23/how-to-make-lazy-python.html
which is derived from https://github.com/django/django/blob/main/django/utils/functional.py#L274
"""
from typing import Any, Callable

import operator


class LazyObject:
    """
    A wrapper for another class that can be used to delay instantiation of the wrapped object.

    Example:
        ::
            context = LazyObject(lambda: Context())

            # Do some other stuff. Context is not evaluated yet.
            some_other_code()

            # Only now is Context instantiated and evaluated,
            # since we attempt to access an attribute on it
            # using __getattr__ which in turn calls _setup().
            print(context.run_id)
    """

    _wrapped = None
    _is_init = False

    def __init__(self, factory):
        # Assign using __dict__ to avoid the setattr method.
        self.__dict__["_factory"] = factory

    def _setup(self):
        """Instantiate the wrapped object."""
        self._wrapped = self._factory()
        self._is_init = True

    def new_method_proxy(func: Callable):  # NOQA
        """Util function to help us route functions to the nested object."""

        def inner(self, *args):
            if not self._is_init:
                self._setup()
            return func(self._wrapped, *args)

        return inner

    def __setattr__(self, name: str, value: Any):
        """
        Route setting special names for LazyObject.

        Every other attribute should be on the wrapped object.

        Args:
            name: The name of the attribute to set.
            value: The value of the attribute.
        """
        if name in {"_is_init", "_wrapped"}:
            self.__dict__[name] = value
        else:
            if not self._is_init:
                self._setup()
            setattr(self._wrapped, name, value)

    def __delattr__(self, name: str):
        """Delete attributes on the wrapped object."""
        if name == "_wrapped":
            raise TypeError("can't delete _wrapped.")
        if not self._is_init:
            self._setup()
        delattr(self._wrapped, name)

    __getattr__ = new_method_proxy(getattr)
    __bytes__ = new_method_proxy(bytes)
    __str__ = new_method_proxy(str)
    __bool__ = new_method_proxy(bool)
    __dir__ = new_method_proxy(dir)
    __hash__ = new_method_proxy(hash)
    __class__ = property(new_method_proxy(operator.attrgetter("__class__")))
    __eq__ = new_method_proxy(operator.eq)
    __lt__ = new_method_proxy(operator.lt)
    __gt__ = new_method_proxy(operator.gt)
    __ne__ = new_method_proxy(operator.ne)
    __getitem__ = new_method_proxy(operator.getitem)
    __setitem__ = new_method_proxy(operator.setitem)
    __delitem__ = new_method_proxy(operator.delitem)
    __iter__ = new_method_proxy(iter)
    __len__ = new_method_proxy(len)
    __contains__ = new_method_proxy(operator.contains)
