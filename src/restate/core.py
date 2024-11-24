from collections.abc import Callable
from dataclasses import dataclass
from typing import Any


@dataclass
class Middleware[S, A]:
    """Middleware class to add side effects to the store."""

    before_reduce: Callable[[S, A], A | None] | None = None
    after_reduce: Callable[[S, A], None] | None = None


class Store[S, A]:
    """A single source of truth for the application state."""

    def __init__(self, reducer: Callable[[S, A], S], initial_state: S):
        self._reducer = reducer
        self._state = initial_state
        self._subscribers: list[Callable[[S], Any]] = []
        self._middlewares: list[Middleware[S, A]] = []

    @property
    def state(self) -> S:
        """Expose read-only state property."""
        return self._state

    def get_state(self) -> S:
        """Get the current state."""
        return self._state

    def dispatch(self, action: A | None) -> None:
        """Dispatch an action to the store."""
        for middleware in self._middlewares:
            if middleware.before_reduce:
                if not action:
                    return
                action = middleware.before_reduce(self._state, action)

        if not action:
            return

        self._state = self._reducer(self.state, action)

        for middleware in self._middlewares:
            if middleware.after_reduce:
                middleware.after_reduce(self._state, action)

        for subscriber in self._subscribers:
            subscriber(self._state)

    def subscribe(self, subscriber: Callable[[S], Any]) -> Callable[[], None]:
        """Subscribe to state changes."""
        self._subscribers.append(subscriber)
        return lambda: self._subscribers.remove(subscriber)

    def add_middleware(self, *middlewares: Middleware[S, A]) -> None:
        """Add middlewares to the store."""
        for m in middlewares:
            self._middlewares.append(m)
