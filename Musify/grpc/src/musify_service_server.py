import musify_server, os, sys
APP_ROOT = os.path.dirname(os.path.abspath(__file__)) + "/../.."

if __name__ == '__main__':
    os.system(
        "javac -cp " + APP_ROOT + ":" + APP_ROOT + "/components/jave-1.0.2.jar:" + APP_ROOT + "/components " + APP_ROOT + "/components/*.java"
    )
    print(">> Musify Server gRPC executing...")
    print(">> Waiting for requests...")
    musify_server.MusifyServer().start(8888)
