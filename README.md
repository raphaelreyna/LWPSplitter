# LWPSplitter
Splits an arbitrary amount of Littlewood Polynomials and stores the result in a database.

## Usage
Move into the root directory of the project and run `sudo docker-compose up`.
Once the containers have started, you can access the database on port 5432 with username 'littlewood' and password 'JohnEdenson'. 
A RESTful API is available on port 5002 for splitting and getting the state.

### Example
Split the next 30 polynomials: `curl http://127.0.0.1:5002/split/30`

Get the current state: `curl http://127.0.0.1:5002/state`
