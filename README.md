# jumo_interview
Coding Problem (Data Engineer role) - Juan Maree

## Functional Requirement
Every two months we are given a text file from our accounting department detailing all the loans given out on our networks. This needs to be a validated against our internal systems by the tuple of (Network, Product, Month).

## Nonfunctional Requirement
* Handle two months worth of loan data
* Scalable
* Readable

## Prerequisites
Python 3 or higher

## Usage
The main application is a console program
It can be execute by running /dist/main.exe
```
C:\loan_aggregator\dist\main.exe
```

or

Running source from /src/main.py
```
python main.py
```

By default the program will look for 'Loans.csv' within data directory. If a different file needs to be processes this file can be replaced.
The application will also ask for the path of the CSV file, which can be entered. Will default to /data/Loans.csv if no input provided

It will then ask where it should output the resulting CSV. By default this is the same directory as executed, file name 'Output.csv', if no input provided.

## Assumptions
* It is assumed that the input file follows the ordered header MSISDN, Network, Date, Product, Amount
** Provision for other headers can be made in the LoanRecord class
* Assumption is made for proof of concept that program is terminal based. 
** Provision has been made for other input methods
* The aggregation expected is by the tuple of (Network, Product, Month) only
** By changing data structure from namedtuple to dict this can be made dynamic, at the cost of memory
* Assuming the input file could be large

## Technologies
Python was chosen as the langauge provides the ability to rapidly develop solutions and ease of use. It reduces time to market. 
Python is known to be rubust and less error prone.
It is flexible through its use of packages and offers scalability.
Python has a well optimised, easy use CSV handler
Python is also very good at analytics and data science through its use of pandas, numpy, scipy etc.

Within python, the following packages were used:
* **csv** - For handling of CSV files
* **collections** - For namedtuple data structure and Counter data structure
* **datetime** - For string to date conversions
* **decimal** - To ensure decimal precision for Currency values

* **unittest** - Used for unit testing
* **pyinstaller** - Used for packaging


Possible alternative if performance needed to be increased would be R, as it also contains built-in functions for CSV handling.

## Performance
As the loan file is received every two months, the file could potentially be very large. Depending on the throughput of the business.

* Generators are used to ensure only required rows are loaded into memory in a lazy approach. 
* **namedtuple** used as data structure to store loans as provides faster access, and lower memory demand than even a hash table. Loans can also be immutable

## Scalability
A seperation of concerns has been applied in which the aggregation algorithms and the file manipulations have been separated.

### Aggregator
Has been implemented through a template to allow for headers to be added or removed
Requires only an iterable, therefore there is a loose dependency to input method
Prepared for scalling process accross multiple workers by providing metadata to indicate processing positions
Also allow for multiple files to be submitted to the Aggregations

### File Reader
Strategy pattern has been applied to the file reader to provide abiliy to add in different sources for CSV

## Improvements
Given more time I would like to implement python Multiprocessing within the Aggregation function. Since hardware read is a limitation of reading from CSV, and rows are only read on demand, multiprocesses would not make much difference here. By adding multiple processes to the Aggregation, each process could iterate the Generator to receive a row to parse, and return the result to the shared data set without competing.

I would have also liked to add more Concrete methods of uploading a CSV file such as an API. To provide a way using the application as a micro service. For this I would use Flask as a framework.

With more time complete unit testing would have been a must! I unit tested the aggregator as this was the most involved code piece.

## Authors
* **Juan Maree**
