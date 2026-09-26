import sys


def validate(NESTED_MORSE: dict) -> str:
    """Check the dictionary and CLI for invalid inputs
    and raise AssertionError in case of fail"""
    args = sys.argv[1:]
    if len(args) != 1:
        raise AssertionError("the arguments are bad")
    for c in args[0]:
        if c.upper() not in NESTED_MORSE:
            raise AssertionError("the arguments are bad")
    return args[0]


def encode():
    """Encode text into Morse code, joined by single spaces."""
    NESTED_MORSE = {
     "A": ".-", "B": "-...", "C": "-.-.", "D": "-..", "E": ".",
     "F": "..-.", "G": "--.", "H": "....", "I": "..", "J": ".---",
     "K": "-.-", "L": ".-..", "M": "--", "N": "-.", "O": "---",
     "P": ".--.", "Q": "--.-", "R": ".-.", "S": "...", "T": "-",
     "U": "..-", "V": "...-", "W": ".--", "X": "-..-", "Y": "-.--",
     "Z": "--..",
     "0": "-----", "1": ".----", "2": "..---", "3": "...--", "4": "....-",
     "5": ".....", "6": "-....", "7": "--...", "8": "---..", "9": "----.",
     " ": "/",
    }
    text = validate(NESTED_MORSE)
    codes = [NESTED_MORSE[c.upper()] for c in text]
    print(" ".join(codes))


def main():
    """The function that launch the program"""
    try:
        encode()
    except AssertionError as error:
        print(f"AssertionError: {error}")


if __name__ == "__main__":
    main()
