import argparse
from src.sort_pkg import sort


def main() -> int:
	parser = argparse.ArgumentParser(description="Classify a package as STANDARD, SPECIAL, or REJECTED.")
	parser.add_argument("width", type=float, help="Width in cm")
	parser.add_argument("height", type=float, help="Height in cm")
	parser.add_argument("length", type=float, help="Length in cm")
	parser.add_argument("mass", type=float, help="Mass in kg")
	args = parser.parse_args()

	label = sort(args.width, args.height, args.length, args.mass)
	print(label)
	return 0


if __name__ == "__main__":
	raise SystemExit(main())

