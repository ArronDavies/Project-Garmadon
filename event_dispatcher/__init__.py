import inspect
import weakref
from typing import Any, Callable, Dict, MutableSequence

class EventDispatcher:
	def __init__(self):
		self._listeners: Dict[Any, MutableSequence[Callable[..., None]]] = {}

	def add_listener(self, event, func) -> None:
		if inspect.ismethod(func):
			func = weakref.WeakMethod(func)
		else:
			func = weakref.ref(func)
		self._listeners.setdefault(event, []).append(func)

	def dispatch(self, event, *args, **kwargs) -> None:
		if event not in self._listeners:
			return
		removed = []
		for ref in self._listeners[event]:
			listener = ref()
			if listener is None:
				removed.append(ref)
			else:
				listener(*args, **kwargs)
		for ref in removed:
			self._listeners[event].remove(ref)

	def dispatch_callable(self, event, callable) -> None:
		if event not in self._listeners:
			return
		removed = []
		for ref in self._listeners[event]:
			listener = ref()
			if listener is None:
				removed.append(ref)
			else:
				args, kwargs = callable()
				listener(*args, **kwargs)
		for ref in removed:
			self._listeners[event].remove(ref)
