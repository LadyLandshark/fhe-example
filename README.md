# FHE-Example

Example FHE Server and Client for a Data Privacy Class

Uses [Pyfhel](https://github.com/ibarrond/Pyfhel/tree/master) to provide fully homomorphic encrytion on data stored server side and [Apache Thrift](https://thrift.apache.org/) for the server-client framework.

Assumes client still has a record/copy of the data.

This only works for CSV files where all data values are integers.

## Instructions

1. Install dependencies (you may want to install Python dependencies into a virtual environment):  
   ```
   sudo apt install thrift-compiler
   pip install numpy Pyfhel
   ```
2. Generate the thrift code:
   ```
   thrift --gen py fhe.thrift
   ```
3. Start up the server (either do so in the background or in another terminal):
   ```
   python3 fhe_server.py
   ```
4. Start up the client:
   ```
   python3 fhe_client.py
   ```

The client currently accepts three commands:
- `upload <filename>`
- `download <filename>`
- `add <filename> <column> <value>` (assumes 1-indexed columns)
