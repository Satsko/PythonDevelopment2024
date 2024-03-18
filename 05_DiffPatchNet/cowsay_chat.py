import asyncio
import cowsay

clients = {}
cowlst = cowsay.list_cows()

async def chat(reader, writer):
    reg=False
    me = ""
    queue = asyncio.Queue()
    send = asyncio.create_task(reader.readline())
    receive = asyncio.create_task(queue.get())
    while not reader.at_eof():
        done, pending = await asyncio.wait([send, receive], return_when=asyncio.FIRST_COMPLETED)
        for q in done:
            if q is send:
                send = asyncio.create_task(reader.readline())
                message = q.result().decode().split()
                if len(message < 1):
                  continue
                elif message[0] == "login":
                  if reg:
                    writer.write(("Registration as:" + me + "\n").encode())
                  elif (message[1] in cowlst) and not reg:
                    me = message[1]
                    clients[me] = asyncio.Queue()
                    cowlst.remove(message[1])
                    reg = True
                    writer.write("Successfully registration:\n".encode())
                    await writer.drain()
                    receive.cancel()
                    receive = asyncio.create_task(clients[me].get())
                  else:
                    writer.write("Name is invalid\n".encode())
                    await writer.drain()
                elif message[0] == "quit":
                  send.cancel()
                  receive.cancel()
                  if reg:
                    del clients[me]
                    cowlst.append(me)
                  writer.close()
                  await writer.wait_closed()
                  return
                elif (message[0] == 'cows'):
                    writer.write(f"Available usernames (cows): {', '.join(cows_list)}\n".encode())
                    await writer.drain()
                elif (message[0] == 'who'):
                    writer.write(f"Registered users: {', '.join(clients.keys())}\n".encode())
                    await writer.drain()
                else:
                  writer.write("Wrong command!\n".encode())
                  await writer.drain()
            elif q is receive:
                receive = asyncio.create_task(clients[me].get())
                writer.write(f"{q.result()}\n".encode())
                await writer.drain()
    send.cancel()
    receive.cancel()
    print(me, "DONE")
    del clients[me]
    writer.close()
    await writer.wait_closed()

async def main():
    server = await asyncio.start_server(chat, '0.0.0.0', 1337)
    async with server:
        await server.serve_forever()

asyncio.run(main())
