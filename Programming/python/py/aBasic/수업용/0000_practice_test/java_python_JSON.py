import json, socket

if __name__ == '__main__':
    num = 10
    try:
        print('client - activated')
        Server_Addr = ('127.0.0.1',5000)

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
            client.connect(Server_Addr)
            print('server - connected')

            while True:
                input_temp = input('send data : ')
                data = {'name':'client','contents':input_temp,'num':num}
                print(f"send: name:{data['name']}, contents: {data['contents']}, num:{data['num']}")
                client.sendall(json.dumps(data).encode('UTF-8'))

                data = client.recv(4096)
                data = json.loads(data)

                print(f"receive : {data['name']}, contents : {data['contents']}, num : {data['num']} ")

                num = int(data['num']) + 1

    except Exception as e :
        print(e)
        input_temp = input('exit - press any button')


myjson = json.dumps(data)
# dict -> JSON


