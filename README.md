# Lidya Trading Technical Assessment

---

## Usage

Program reads the csv file under the root folder, path can be configured in config.py. When program runs, it reads the
given csv file and populates the order book. It then writes top of the book and queue position of an order to the std
out. Unique id of the order used for queue position can be configured in config.py

## Performance

According to my calculations approximate complexities of order book operations are as follows:

- Add: O(N) if the price is not pre allocated where N is the size of the array, O(1) otherwise.
- Delete: O(1)
- Execute: O(1)
- Top of the book: O(k) where k is the number of prices requested
- Queue position: O(k) + O(l) where k is the number of limit price points between best bid and requested order's limit
  and l is the number of orders from head of the limit price to requested order.

### Assumptions

1. Normally an order book would have buy and sell sides, however provided data only has buy orders. I modelled the order
   book to have both sides but will only populate buy side
2. Provided data set includes queue positions however, assuming the requests the system receives will be in order with
   respect to their execution time. I chose to sort the data in the same time frame by queue position. Therefore, I did
   not perform a search operation within the limit to place the order. Instead, I placed the order at the tail of limit
   list.

### Data structure arguments

I chose to hold limits in a list sorted by their price. I considered using some sort of self-balancing binary tree as
well because statistically average lookup for an item in balanced binary tree is O(log N)
whereas for a list it is O(n). However, in practice list will have better average performance because list is cache
friendly and fast at slicing. Also, drawbacks of the list can be reduced by storing pointers of commonly accessed
elements, such as the best bid/ask.

### Performance optimization for given data

Most of the cost of using lists in python come from dynamically allocating memory for the list. This cost can be removed
completely, if the size of the list is known beforehand. Instead of dynamically constructing a list of limit prices, I
will pre allocate the list for the given dataset. This optimization can be performed for Borsa Istanbul as well because
of the daily min/max price change rule. One drawback of this optimization is best bid/ask will not be at the start of
the list. I mitigate this drawback by keeping a separate pointer to the best bid/ask which keeps the execute operation
at O(1).

---

### Improvements

Notes about general improvements for the project

#### Structure and configuration of the project

- Use an environment variable to store a path for the home directory of the program.
- Include all configurable values in the home directory in text file such as yaml/json.
- Separate data parsing and reading into another package, define an interface for reading and parsing data. So switching
  to different input formats is easy.

#### Deployment

- Define a Dockerfile so the program can run in different targets easily.

#### Performance

- Write performance tests that can run at different targets
- Visualize the performance metrics of critical parts of the program to easily identify bottlenecks.

