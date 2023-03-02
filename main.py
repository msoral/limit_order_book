from loguru import logger

import config
from src.book import Book
from src.book_manager import BookManager
from src.data import DataImporter


@logger.catch()
def main() -> None:
    config.configure_logger()
    data_importer = DataImporter()
    orders = data_importer.read()
    min_price, max_price = data_importer.find_min_max_prices()
    order_book: Book = Book()
    book_manager: BookManager = BookManager(order_book)
    book_manager.pre_allocate_with_boundaries(min_price, max_price)
    book_manager.populate(orders)
    if config.SHOW_FINAL_ORDER_BOOK:
        book_manager.show_order_book_limits()
        book_manager.show_order_book_entries()
    logger.info(f"Top of the book: {order_book.get_top_of_the_book()}")
    order_id = config.ORDER_ID_FOR_QUEUE_POSITION_QUERY
    queue_position: int = order_book.get_queue_position(order_id)
    if queue_position is not None:
        logger.info(f"Queue position of order({order_id}): {queue_position}")


if __name__ == '__main__':
    main()

