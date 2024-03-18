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
                    writer.write("Successfull registration:\n".encode())
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
                    writer.write(f"Available usernames (cows): {', '.join(cowlst)}\n".encode())
                    await writer.drain()
                elif (message[0] == 'who'):
                    writer.write(f"Registered users: {', '.join(clients.keys())}\n".encode())
                    await writer.drain()
                elif (message[0] == "say"):
                    if not reg:
                        writer.write("You need register to send messages\n".encode())
                        await writer.drain()
                        continue
                    if (message[1] in clients.keys()):
                        await clients[message[1]].put(f"Message from {me}:\n {cowsay.cowsay((' '.join(message[2:])).strip(), cow=me)}")
                        writer.write("Message is sent\n".encode())
                        await writer.drain()
                  else:
                    writer.write("There no user with this name\n".encode())
                    await writer.drain()
                elif (message[0] == 'yield'):
                  if not reg:
                    writer.write("You need register to send messages\n".encode())
                    await writer.drain()
                    continue
                  for dst in clients.values():
                    if dst is not clients[me]:
                      await dst.put(f"Message from {me}:\n {cowsay(' '.join(message[1:]).strip(), cow=me)}")
                  writer.write("Message is sent \n".encode())
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
