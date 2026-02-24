import warnings
warnings.filterwarnings("ignore", message="Core Pydantic V1 functionality")

from noteweaver import Logger, RefineNote, App

def main():
    logger = Logger().get()
    refiner = RefineNote()
    app = App(refiner, logger)
    app.run()


if __name__ == "__main__":
    main()
