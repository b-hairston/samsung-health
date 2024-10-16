from prefect import Flow, task
from flows.load import load_data
def main():
    load_data()


if __name__ == "__main__":
    main()