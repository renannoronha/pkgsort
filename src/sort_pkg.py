def sort(width, height, length, mass) -> str:
    """
    Rules:
      - Bulky: volume >= 1_000_000 cm³ OR any dimension >= 150 cm
      - Heavy: mass >= 20 kg
    Stacks:
      - REJECTED: bulky AND heavy
      - SPECIAL:  bulky OR heavy (but not both)
      - STANDARD: neither
    """
    width = float(width)
    height = float(height)
    length = float(length)
    mass = float(mass)
    volume = width * height * length
    bulky = (volume >= 1_000_000.0) or (width >= 150.0 or height >= 150.0 or length >= 150.0)
    heavy = (mass >= 20.0)

    if bulky and heavy:
        return "REJECTED"
    if bulky or heavy:
        return "SPECIAL"
    return "STANDARD"
