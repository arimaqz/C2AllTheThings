import xmlrpc.server
class MyRPCServer:
    def __init__(self):
        pass
    def command(self):
        cmd = input("enter a command: ")
        return cmd

    def response(self, response):
        print("received: ", response)
        return "received"
def run_server():
    server = xmlrpc.server.SimpleXMLRPCServer(("localhost", 8000))
    server.register_instance(MyRPCServer())  
    print("Server is running on http://localhost:8000")
    server.serve_forever()

if __name__ == "__main__":
    run_server()
