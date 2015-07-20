Backend Recruiting Task
=======================

The story
---------

At Tictail we organize bi-annual Demo Weeks where we hack on creative projects. It's a
good way to get that side project going or validate an idea for a new feature. One of the
ideas for the upcoming Demo Week is spatial search for Tictail products around you. You
will be building the backend for that!


Provided goodies
----------------

1. A server boilerplate using `Flask`. To run the server:

  ```
  $ python runserver.py
  ```

2. A rudimentary client so you can visualize the results more easily. The client does not
have any way to communicate with the API so you will need to implement that. To run the
client:

  ```
  $ cd client
  $ python -m SimpleHTTPServer
  ```

3. Four datasets in CSV format: `shops.csv`, `products.csv`, `tags.csv` and `taggings.csv`.


What you need to do
-------------------

1. Implement the `Searcher.search()` method in the client so it can communicate with your
API. We've included `jQuery` on the page so you can use that if you like.

2. Build an endpoint that returns a number of most popular products given some coordinates,
a search radius and, optionally, some tags. If tags are provided, a shop needs to have at
least one of them to be considered a candidate. The number of products to return should be
given as a parameter as well. You can use popular Python libraries to your aid but you
can't use any external databases or search engines (e.g PostGIS, Elasticsearch, etc).

3. Document your design and thought process in `THOUGHTS.md`. Keep it short :-)

*You should deliver your solution as a `git` repository, preferably hosted on GitHub.*

What we look for
----------------

1. **Correctness**: Your solution should return the correct results and deal with as many edge
cases as you can think of.

2. **Quality & design:** Imagine that your solution will be delivered to production as-is,
and maintained by your fellow engineers. What are the things you need to consider and implement 
to make it production-quality (tests, code quality, input validation, documentation, etc)?

3. **Performance:** In real-life the datasets will be big enough to cause problems to a
simple brute-force approach, so your solution should account for that. Can you do any
preprocessing or use specialized data structures?

A good rule of thumb is to submit something that you're proud of. Good luck!

*N.B: Your code is provided solely for the purposes of this exercise and will not be used by
Tictail under any circumstances.*
