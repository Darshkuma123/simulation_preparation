import socket

Host='127.0.0.1'
port=4840
from asyncua import Client
import asyncio

async def main():
    async with Client(url='opc.tcp://localhost:4840/freeopcua/server/') as client:
     while True:
        # Do something with client
         node = client.get_node('i=3')
         value = await node.read_value()


asyncio.run(main())