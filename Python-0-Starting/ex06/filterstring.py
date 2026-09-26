import sys
import string


def filter_words(text: str, n: int) -> list:
    """Tells if the words in text have letters bigger than n"""
    return [w for w in text.split() if (lambda x: len(x) > n)(w)]


def validate_args():
    """Validate CLI arguments and return (text, n) if they're valid"""
    args = sys.argv[1:]
    if len(args) != 2:
        raise AssertionError("the arguments are bad")
    bad_chars = [c for c in args[0] if c in string.punctuation
                or not c.isprintable() or (c.isspace() and c != ' ')]
    if bad_chars:
        raise AssertionError("the arguments are bad")
    try:
        n = int(args[1])
    except ValueError:
        raise AssertionError("the arguments are bad")
    print(filter_words(args[0], n))


def main():
    """The main function that check for exception"""
    try:
        validate_args()
    except AssertionError as error:
        print(f"AssertionError: {error}")


if __name__ == "__main__":
    main()
