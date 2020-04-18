import musify_server

if __name__ == '__main__':
    print(">> Musify Server gRPC executing...")
    print(">> Waiting for requests...")
    musify_server.MusifyServer().start(8888)
