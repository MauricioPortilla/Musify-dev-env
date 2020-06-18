from concurrent import futures
import grpc, time, lib, os, hashlib, datetime, random, subprocess, threading, sys, uuid
import musify_service_pb2 as MusifyService, musify_service_pb2_grpc as MusifyServiceGRPC
from musify_service_server import APP_ROOT

class MusifyServer(MusifyServiceGRPC.MusifyServiceServicer):

    def __init__(self):
        class Servicer(MusifyServiceGRPC.MusifyServiceServicer):
            def __init__(self):
                self.songsLocations = {
                    "highquality": APP_ROOT + "/storage/songs/highquality",
                    "mediumquality": APP_ROOT + "/storage/songs/mediumquality",
                    "lowquality": APP_ROOT + "/storage/songs/lowquality"
                };

            def convertSong(self, hashedName):
                print("> Converting " + hashedName + "...")
                result = subprocess.Popen(
                    "java -cp " + APP_ROOT + "/..:" + APP_ROOT + "/components/jave-1.0.2.jar:" + APP_ROOT + "/components Musify.components.SongQualityMain " + 
                        self.songsLocations["highquality"] + "/" + hashedName,
                    shell=True,
                    stdout=subprocess.PIPE
                )
                message = result.stdout.read().decode("utf-8")
                if message:
                    print(message)
                return message
            
            def upload(self, request_iterator, context):
                hashedName = hashlib.sha1(
                    (str(uuid.uuid4()) + str(datetime.datetime.now().timestamp())).encode()
                ).hexdigest() + ".bin"
                lib.saveChunksToFile(request_iterator, self.songsLocations["highquality"] + "/" + hashedName)
                result = self.convertSong(hashedName)
                return MusifyService.SongStored(name=hashedName, length=os.path.getsize(self.songsLocations["highquality"] + "/" + hashedName))

            def download(self, request, context):
                if request.name and request.quality:
                    return lib.getFileChunks(self.songsLocations[request.quality] + "/" + request.name, request.name)
            
        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=4))
        MusifyServiceGRPC.add_MusifyServiceServicer_to_server(Servicer(), self.server)

    def start(self, port):
        if not os.path.exists(APP_ROOT + "/storage"):
            os.mkdir(APP_ROOT + "/storage")
        if not os.path.exists(APP_ROOT + "/storage/songs"):
            os.mkdir(APP_ROOT + "/storage/songs")
            os.mkdir(APP_ROOT + "/storage/songs/highquality")
            os.mkdir(APP_ROOT + "/storage/songs/mediumquality")
            os.mkdir(APP_ROOT + "/storage/songs/lowquality")

        self.server.add_insecure_port(f'[::]:{port}')
        self.server.start()

        try:
            while True:
                time.sleep(60 * 60 * 24)
        except KeyboardInterrupt:
            self.server.stop(0)
