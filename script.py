import sys


def show_help():
    print("Commands:")
    print("fetch")
    print("setup")
    print("help")


def fetch():
    print("fetching...")


def setup():
    print("setting up...")


if __name__ == "__main__":
    if len(sys.argv) <= 1:
        show_help()
    else:
        command = sys.argv[2].lower()
        if command == "fetch":
            fetch()
        elif command == "setup":
            setup()
        else:
            show_help()
