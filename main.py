from smart_home.core.cli import Cli
from smart_home.core.hub import Hub
from smart_home.core.observers import EventHandler

if __name__ == "__main__":
    print("__HUB__")

    cli = Cli()

    cli.menu()
