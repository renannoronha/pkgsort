# pkgsort

I wrote a function that classifies packages as STANDARD, SPECIAL, or REJECTED based on dimensions and mass. It’s a single function with tests.

## What it does
- Bulky when:
  - volume >= 1,000,000 cm³, or
  - any single dimension >= 150 cm
- Heavy when:
  - mass >= 20 kg
- Classification:
  - REJECTED if bulky AND heavy
  - SPECIAL if exactly one of bulky/heavy
  - STANDARD if neither

Function signature:
- `sort(width, height, length, mass) -> str`
- Accepts numbers or strings convertible to float.
- Returns one of: `"STANDARD" | "SPECIAL" | "REJECTED"`.

## Project layout
- `sort_pkg.py` — the implementation
- `test/` — unit tests (pytest)

## Quick start
```python
from sort_pkg import sort
print(sort(10, 10, 10, 1))          # STANDARD
print(sort(150, 1, 1, 0))           # SPECIAL (bulky by dimension)
print(sort(100, 100, 100, 25))      # REJECTED (bulky by volume + heavy)
```

## Run the tests
I use pytest for the suite in `test/test_sort_pkg.py`.

- Install pytest (if needed):
```bash
python -m pip install -U pytest
```

- Run the tests:
```bash
python -m pytest -q
```