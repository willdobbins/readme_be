# ReadMe Backend - PyFlask
A simple flask based backend for a book order builder.  Mostly consists of two endpoints of any significance.

## GET /lookup/[ISBN:int]
* Expects an int as an argument.
* Takes that int and first checks redis to see if there are any books with that ISBN.
* If not, it queries Google Books API and caches the information for later reuse.

## POST /order
* Expects a JSON payload.
* Given this payload, it generates an XLS and serves it to the client.

##Example JSON For /order
{
  "events": [
  {
    "date": "10/29/2019",
    "location": "Store",
    "books": [
      {
        "isbn": 9780761169086,
        "count": 10 
      }
    ]
  }
  ]
}

For a single event on 10/29/2019 which will only require 10 copies of a single book.