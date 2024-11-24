# Restate: A Pythonic implementation of Redux Pattern

## Installation

```bash
pip install git+https://github.com/Microwave-WYB/restate.git
# pip install restate  # TODO: publish to PyPI
```

## Usage

### Basic Usage

Here's an example of a simple counter app using Restate:

```python
from dataclasses import dataclass
from restate import Store, Middleware

# Define actions using Union of dataclasses
@dataclass
class Increase:
    amount: int = 1

@dataclass
class Decrease:
    amount: int = 1

@dataclass
class Reset: ...

type CounterAction = Increase | Decrease | Reset

# Define a reducer
def counter_reducer(state: int, action: CounterAction) -> int:
    match action:
        case Increase(amount):
            return state + amount
        case Decrease(amount):
            return state - amount
        case Reset:
            return 0

store = Store(counter_reducer, 0)
store.subscribe(lambda state: print(f"Counter: {state}"))

# Dispatch actions
store.dispatch(Increase())
store.dispatch(Increase(2))
store.dispatch(Decrease(3))
store.dispatch(Reset())
```
