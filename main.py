# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from src.book import Book
from src.book_manager import BookManager
from src.data import DataImporter


def main() -> None:
    data_importer = DataImporter()
    orders = data_importer.read()
    min_price, max_price = data_importer.find_min_max_prices()
    order_book: Book = Book()
    book_manager: BookManager = BookManager(order_book)
    book_manager.pre_allocate_with_boundaries(min_price, max_price)
    book_manager.populate(orders)


if __name__ == '__main__':
    main()
