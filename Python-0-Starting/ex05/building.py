import sys
import string


def count_text(text: str) -> None:
    """Analyze a string and count various characters"""
    upper = 0
    lower = 0
    digit = 0
    space = 0
    punct = 0
    for char in text:
        if char.isupper():
            upper += 1
        elif char.islower():
            lower += 1
        elif char.isdigit():
            digit += 1
        elif char.isspace():
            space += 1
        elif char in string.punctuation:
            punct += 1
    print(f"The text contains {len(text)} characters:\n"
          f"{upper} upper letters\n"
          f"{lower} lower letters\n"
          f"{punct} punctuation marks\n"
          f"{space} spaces\n"
          f"{digit} digits")


def read_text():
    """Read command-line or standard-input text and count its characters."""
    if len(sys.argv) == 2:
        count_text(sys.argv[1])
    elif len(sys.argv) > 2:
        raise AssertionError("more than one argument is provided")
    else:
        print("What is the text to count?")
        count_text(sys.stdin.readline())


def main():
    try:
        read_text()
    except AssertionError as error:
        print(f"AssertionError: {error}")


if __name__ == "__main__":
    main()
