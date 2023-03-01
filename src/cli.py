import argparse


class CommandLineInterface:
    def __init__(self):
        self.parser = argparse.ArgumentParser(
            prog='Limit Order Book',
            description='This program can calculate top of the book and queue position queries given a dataset of add, '
                        'execute and delete orders.'
        )
        self.__define_arguments()
        self.args = self.parser.parse_args()

    def __define_arguments(self) -> None:
        self.parser.add_argument("-d", "--dataset")
