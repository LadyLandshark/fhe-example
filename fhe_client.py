import sys
import glob
import csv
sys.path.append('gen-py')

from pathlib import Path
import numpy as np

from fhe import FHE_Fileserver
from fhe.ttypes import File
from Pyfhel import Pyfhel, PyCtxt

from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol



def dump_context(data):
    HE = Pyfhel()
    HE.from_bytes_context(data.ctx)
    HE.from_bytes_public_key(data.pub_key)
    HE.from_bytes_relin_key(data.relin_key)
    HE.from_bytes_rotate_key(data.rotate_key)
    path = Path(data.path)
    name = path.name
    HE.save_context(f".{name}.ctx")
    HE.save_public_key(f".{name}.pub")
    HE.save_relin_key(f".{name}.relin")
    HE.save_rotate_key(f".{name}.rotate")

def add(client, path, column, val):
    file_len = path.stat().st_size
    with Path(path).open('r') as f:
        reader = csv.reader(f)
        fields = next(reader)

    data_buf = np.loadtxt(str(path), delimiter=',', skiprows=1, dtype=np.int64).flatten()
    op_buf = np.zeros((len(data_buf)//len(fields), len(fields)), dtype=np.int64)
    op_buf[:, column-1] = val


    # Columns are after every n commas minus the first row
    client.add_file(str(path), op_buf.flatten().tobytes())    
    

def download(client, path):
    file_len = path.stat().st_size
    file = client.download_file(str(path))
    HE = Pyfhel()
    HE.from_bytes_context(file.ctx)
    HE.from_bytes_public_key(file.pub_key)
    HE.from_bytes_relin_key(file.relin_key)
    HE.from_bytes_rotate_key(file.rotate_key)
    ctxt = PyCtxt(pyfhel=HE, bytestring=file.data)
    HE.load_secret_key(f".{path}.secret")
    
    with Path(file.path).open('r') as f:
        reader = csv.reader(f)
        fields = next(reader)
        file_len -= len(','.join(fields))
    # Decrypt
    cdata = HE.decrypt(ctxt)
    reshaped = np.reshape(cdata[:file_len//2], (file_len//2//len(fields), len(fields)))
    np.savetxt(file.path, reshaped, delimiter=',', fmt="%d", header=','.join(fields), comments='')



def upload(client, path):
    file_len = path.stat().st_size
    # Initialize encryption context
    HE_client = Pyfhel(context_params={'scheme':'bgv', 'n':2**13, 't': 65537, 't_bits':20, 'sec':128})
    HE_client.keyGen()             # Generates both a public and a private key
    HE_client.relinKeyGen()
    HE_client.rotateKeyGen()
    # Read in file
    data = File()
    data.path = str(path)
    data.ctx = HE_client.to_bytes_context()
    data.pub_key = HE_client.to_bytes_public_key()
    data.relin_key = HE_client.to_bytes_relin_key()
    data.rotate_key = HE_client.to_bytes_rotate_key()

    with path.open('r') as f:
        reader = csv.reader(f)        
        fields = next(reader)

    data_buf = np.loadtxt(str(path), delimiter=',', skiprows=1, dtype=np.int64).flatten()
    cptxt = HE_client.encode(data_buf)
    cx = HE_client.encryptPtxt(cptxt)
    data.data = cx.to_bytes()
    
    err = client.upload_file(data)
    if err != 0:
        print(f"Error uploading file {path}")

    dump_context(data)
    HE_client.save_secret_key(f".{path}.secret")



def main():
    # Make socket
    transport = TSocket.TSocket('localhost', 9090)

    # Buffering is critical. Raw sockets are very slow
    transport = TTransport.TBufferedTransport(transport)

    # Wrap in a protocol
    protocol = TBinaryProtocol.TBinaryProtocol(transport)

    # Create a client to use the protocol encoder
    client = FHE_Fileserver.Client(protocol)

    # Connect!
    transport.open()

    prompt = "fhe"

    cmd = ''
    while(cmd not in ['bye', 'exit', 'quit']):
        cmd = input(f"{prompt}> ")
        parts = cmd.split()
        if parts[0] == 'upload':
            upload(client, Path(parts[1]))
            continue
        if parts[0] == 'download':
            download(client, Path(parts[1]))
            continue
        if parts[0] == 'add':
            add(client, Path(parts[1]), int(parts[2]), int(parts[3]))
            continue    

    transport.close()

if __name__ == '__main__':
   main() 
