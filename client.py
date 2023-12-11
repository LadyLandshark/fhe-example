import sys
import glob
sys.path.append('gen-py')
sys.path.insert(0, glob.glob('../../lib/py/build/lib*')[0])

from pathlib import Path

from fhe import FHE_Server
from fhe.ttypes import File, FHE_Server
from Pyfhel import Pyfhel, PyCtxt

from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol


def load_context(data):
    dataname = data.path
    HE_client = Pyfhel()
    with Path(dataname).open('wb') as f:
        data.data = f.read()
    with Path(dataname + '.ctx').open('wb') as f:
        data.ctx = HE_client.from_bytes_context(f.read())
    with Path(dataname + '.pub').open('wb') as f:
        data.pub_key = HE_client.from_bytes_public_key(f.read())
    with Path(dataname + '.relin').open('wb') as f:
        data.relin_key = HE_client.from_bytes_relin_key(f.read())
    with Path(dataname + '.rotate').open('wb') as f:
        data.rotate_key = HE_client.from_bytes_rotate_key(f.read())

def dump(filename, val):
    with Path(filename).open('wb') as f:
        f.write(val)


def dump_context(data):
    root = Path(data.path).root
    fname = Path(data.path.
    
    dump(
    

def add(client, data, column, val):
    load_context(data)
	# Find column  in binary

	# Columns are after every n commas minus the first row
	client.add()	
    

def download(client, path):
	file = client.download(path)

	# Decrypt




def upload(client, path):
    # Initialize encryption context
    HE_client = Pyfhel(context_params={'scheme':'ckks', 'n':2**13, 'scale':2**30, 'qi_sizes':[30]*5})
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


	with path.open('rb') as f:
        float_buf = np.frombuffer(f.read(), dtype='<f4')
    cx = HE_client.encrypt(float_buf)
	data.data = cx.to_bytes()
	
    dump_context(data)

	err = client.upload(data)
	if err != 0:
		print(f"Error uploading file {path}")


def main():
    # Make socket
    transport = TSocket.TSocket('localhost', 9090)

    # Buffering is critical. Raw sockets are very slow
    transport = TTransport.TBufferedTransport(transport)

    # Wrap in a protocol
    protocol = TBinaryProtocol.TBinaryProtocol(transport)

    # Create a client to use the protocol encoder
    client = FHE_Server.Client(protocol)

    # Connect!
    transport.open()

	prompt = "fhe"

	cmd = input(f"{prompt}> ")
	while(cmd not in ['bye', 'exit', 'quit']):
		cmd = input(f"{prompt}> ")
		if cmd == 'upload':
			continue
		if cmd == 'download':
			continue
		if cmd == 'add':
			continue	
		

    transport.close()

    sum_ = client.add(1, 1)
    print('1+1=%d' % sum_)

    work = Work()

    work.op = Operation.DIVIDE
    work.num1 = 1
    work.num2 = 0

    try:
        quotient = client.calculate(1, work)
        print('Whoa? You know how to divide by zero?')
        print('FYI the answer is %d' % quotient)
    except InvalidOperation as e:
        print('InvalidOperation: %r' % e)

    work.op = Operation.SUBTRACT
    work.num1 = 15
    work.num2 = 10

    diff = client.calculate(1, work)
    print('15-10=%d' % diff)

    log = client.getStruct(1)
    print('Check log: %s' % log.value)

    # Close!
