# FHE-Example

Example FHE Server and Client for a Data Privacy Class

Uses [Pyfhel](https://github.com/ibarrond/Pyfhel/tree/master) to provide fully homomorphic encrytion on data stored server side and [Apache Thrift](https://thrift.apache.org/) for the server-client framework.

Assumes client still has a record/copy of the data.

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
   python fhe_server.py
   ```
4. Start up the client:
   ```
   python fhe_client.py
   ```

The client currently accepts three commands:
- `upload <filename>`
- `download <filename>`
- `add <filename> <column> <value>`
