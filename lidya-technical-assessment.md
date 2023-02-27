# The Problem

An integral part of algorithmic trading is having a robust and timely representation of the market, commonly referred to
as "the book".

In it's simplest form the book is a collection of orders that are currently open on the market where each order consists
of a unique id, a price and an amount. This represents a trader's intent to buy or sell that amount at that price.

For the purposes of executing trades the exchange queues orders. An order's position in the queue is based in the first
instance on it's price, whereby orders with a higher price appear earlier in the queue that those of a lower price.
Orders with equal prices are discriminated based on the time at which they were added to the market, such that orders
added earlier appear in the queue ahead of those added later.

The exchange provides a stream of updates that enumerate market changes that affect the book. These updates take one of
two different forms:

* Add Order - indicates that a new order has been added to the market. It has four fields, the order's unique id, its
  price, its que place and its volume.
* Delete Order - indicates that an existing order has been cancelled and has been removed from the market. It has one
  field, the order's unique id.
* Execution - indicates that an existing order has been executed and has been removed from the market. It has two
  fields, the order's unique id and its execution size.

At any given time it is useful for an algorithm to know two things:

* Top Of Book - What are the four best prices in the book and what is the total amount available at each of those
  prices?
* Queue Position - Given an order's unique id, what amount needs to be traded before it is at the front of the queue?

# The Task

Design and implement a system that, given a series of "Add Order", "Execution" and
"Remove Order" updates detailing the state of the market, can provide the answer to the "Top Of Book" and "Queue
Position" queries.

You are free to implement the system in any of the following: C, C++, Java, Python, Rust, Javascript or Typescript.

## Specifics

Unique order ids are a string of 16 alpha-numeric characters.

Prices are signed integers.

Amounts are unsigned integers.

# Requirements

Correctness - the system must produce the correct answer to the queries. Incorrect answers can result in significant
losses.

Efficiency - latency is very important. Focus on keeping run-time complexity as low as possible. Include an indication
of how the speed of each operation varies with respect to the number of orders on the market.

Good practice - use this as an opportunity to showcase what you believe to be software development best practice.

Document any assumptions you make.

The system should consist of cleanly presented, portable code including commentary where appropriate. It's expected
that (where applicable) the code compiles and any unit tests run without failures.

# Data

data.csv file has the following information; Time(nanoseconds), A/D/E (A-Add D-Delete E-Execution) messages, price, que
position, size, orderID

Delete messages have no price, que position and size information, they are given as zero. Execution messages have no
price and que position information, they are given as zero.