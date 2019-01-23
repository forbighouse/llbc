from p2p.server import *

def main():
    while True:
        regInfo = register()
        if regInfo:
            datastr = json.dumps(regInfo)
            # tcpCliSock.send(datastr.encode('utf-8'))
            tcpCliSock.send(datastr.encode())
            break
    my_input_data = InputData()
    my_get_data = GetData()
    my_input_data.start()
    my_get_data.start()
    my_input_data.join()
    my_get_data.join()


if __name__ == "__main__":
    main()
