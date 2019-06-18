# LWPSplitter
Splits an arbitrary amount of Littlewood Polynomials and stores the result in a database.

## Usage
Create a Splitter object, giving it a username and password for a PostgreSQL server.
By default, the Splitter object will try to connect to a database named "lwp_roots" on 127.0.0.1 through port 5432.
You can pass in a different database, host, or port using the optional arguments for 

`splitter = Splitter.Splitter(username, password, host='127.0.0.1', port='5432', dbname='lwp_roots')`

then simply call `splitter.run(n)` to split and record `n` polynomials.

**IMPORTANT** Currently only supports one instance of Splitter writing to the database at a time.
