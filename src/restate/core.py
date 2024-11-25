from collections.abc import Callable
from dataclasses import dataclass
from typing import Any


@dataclass
class Middleware[A]:
    """Middleware class to add side effects to the store."""

    before_reduce: Callable[["Store", A], A | None] | None = None
    """Function to run before the reducer."""
    after_reduce: Callable[["Store", A], None] | None = None
    """Function to run after the reducer."""


class Store[T, A]:
    """A single source of truth for the application state."""

    def __init__(self, reducer: Callable[[T, A], T], initial_state: T):
        self.reducer = reducer
        self._state = initial_state
        self._subscribers: list[Callable[[T], Any]] = []
        self._middlewares: list[Middleware[A]] = []

    @property
    def state(self) -> T:
        """Expose read-only state property."""
        return self._state

    def get_state(self) -> T:
        """Get the current state."""
        return self._state

    def dispatch(self, action: A | None) -> None:
        """Dispatch an action to the store."""
        for middleware in self._middlewares:
            if middleware.before_reduce:
                if not action:
                    return
                action = middleware.before_reduce(self, action)

        if not action:
            return

        new_state = self.reducer(self.state, action)

        for middleware in self._middlewares:
            if middleware.after_reduce:
                middleware.after_reduce(self, action)

        self._state = new_state

        for subscriber in self._subscribers:
            subscriber(self._state)

    def subscribe(self, subscriber: Callable[[T], Any]) -> Callable[[], None]:
        """Subscribe to state changes."""
        self._subscribers.append(subscriber)
        return lambda: self._subscribers.remove(subscriber)

    def add_middleware(self, *middlewares: Middleware[A]) -> None:
        """Add middlewares to the store."""
        for m in middlewares:
            self._middlewares.append(m)
