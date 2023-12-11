import sys
import os
sys.path.append('gen-py')
import json
import numpy as np
from Pyfhel import Pyfhel, PyCtxt
from fhe import FHE_Fileserver
from fhe.ttypes import File
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer

pdir = "server/" # directory for server-side files

class FHE_FileserverHandler:
    def upload_file(self, f):
        path = f.path
        # if subdirectory for file does not exist, make it
        if not os.path.exists(pdir+path):
            os.makedirs(pdir+path)
        HE = Pyfhel()
        HE.from_bytes_context(f.ctx)
        HE.from_bytes_public_key(f.pub_key)
        HE.from_bytes_relin_key(f.relin_key)
        HE.from_bytes_rotate_key(f.rotate_key)
        cdata = PyCtxt(pyfhel=HE, bytestring=f.data)

        # save context, keys, and data
        HE.save_context(pdir+path+"/context")
        HE.save_public_key(pdir+path+"/pub.key")
        HE.save_relin_key(pdir+path+"/relin.key")
        HE.save_rotate_key(pdir+path+"/rotate.key")
        cdata.save(pdir+path+"/data.ctxt")
        return 0

    def download_file(self, path):
        HE = Pyfhel()
        HE.load_context(pdir+path+"/context")
        HE.load_public_key(pdir+path+"/pub.key")
        HE.load_relin_key(pdir+path+"/relin.key")
        HE.load_rotate_key(pdir+path+"/rotate.key")
        ctxt = PyCtxt(pyfhel=HE, fileName=pdir+path+"/data.ctxt")

        # prepare file to be sent to client
        f = File()
        f.ctx = HE.to_bytes_context()
        f.pub_key = HE.to_bytes_public_key()
        f.relin_key = HE.to_bytes_relin_key()
        f.rotate_key = HE.to_bytes_rotate_key()
        f.data = ctxt.to_bytes()
        f.path = path
        return f

    def add_file(self, path, data):
        HE = Pyfhel()
        HE.load_context(pdir+path+"/context")
        HE.load_public_key(pdir+path+"/pub.key")
        HE.load_relin_key(pdir+path+"/relin.key")
        HE.load_rotate_key(pdir+path+"/rotate.key")
        ctxt = PyCtxt(pyfhel=HE, fileName=pdir+path+"/data.ctxt")
        operand = np.frombuffer(data, dtype=np.int64)
        #operand = PyCtxt(pyfhel=HE, bytestring=data)
        cdata = ctxt + operand
        cdata.save(pdir+path+"/data.ctxt")
        return 0
    
if __name__ == '__main__':
    handler = FHE_FileserverHandler()
    processor = FHE_Fileserver.Processor(handler)
    transport = TSocket.TServerSocket(host='127.0.0.1', port = 9090)
    tfactory = TTransport.TBufferedTransportFactory()
    pfactory = TBinaryProtocol.TBinaryProtocolFactory()

    server = TServer.TSimpleServer(processor, transport, tfactory, pfactory)

    print("starting server...")
    server.serve()
    print("done.")
