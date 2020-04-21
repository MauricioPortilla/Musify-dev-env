from concurrent import futures
import grpc, time, lib, os, hashlib, datetime, random, subprocess, threading, sys
import musify_service_pb2 as MusifyService, musify_service_pb2_grpc as MusifyServiceGRPC

class MusifyServer(MusifyServiceGRPC.MusifyServiceServicer):

    def __init__(self):
        class Servicer(MusifyServiceGRPC.MusifyServiceServicer):
            def __init__(self):
                self.songsLocations = {
                    "highQuality": "/home/vagrant/Musify/storage/songs/highquality",
                    "mediumQuality": "/home/vagrant/Musify/storage/songs/mediumquality",
                    "lowQuality": "/home/vagrant/Musify/storage/songs/lowquality"
                };

            def convertSongThread(self, hashedName):
                result = subprocess.Popen(
                    "java -cp /home/vagrant/Musify/components:/home/vagrant/Musify/components/jave-1.0.2.jar Musify.components.SongQualityMain " + 
                    self.songsLocations["highQuality"] + "/" + hashedName,
                    shell=True,
                    stdout=subprocess.PIPE
                )
                message = result.stdout.read().decode("utf-8")
                if message:
                    print(message)
            
            def upload(self, request_iterator, context):
                hashedName = hashlib.sha1(
                    (str(random.randint(1, 10000)) + str(datetime.datetime.now().timestamp())).encode()
                ).hexdigest() + ".mp3"
                lib.saveChunksToFile(request_iterator, self.songsLocations["highQuality"] + "/" + hashedName)
                threading.Thread(target=self.convertSongThread, args=(hashedName,)).start()
                return MusifyService.SongStored(name=hashedName, length=os.path.getsize(self.songsLocations["highQuality"] + "/" + hashedName))

            def download(self, request, context):
                if request.name and request.quality:
                    return lib.getFileChunks(self.songsLocations[request.quality] + "/" + request.name, request.name)
            
        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
        MusifyServiceGRPC.add_MusifyServiceServicer_to_server(Servicer(), self.server)

    def start(self, port):
        if not os.path.exists("/home/vagrant/Musify/storage"):
            os.mkdir("/home/vagrant/Musify/storage")
        if not os.path.exists("/home/vagrant/Musify/storage/songs"):
            os.mkdir("/home/vagrant/Musify/storage/songs")
            os.mkdir("/home/vagrant/Musify/storage/songs/highquality")
            os.mkdir("/home/vagrant/Musify/storage/songs/mediumquality")
            os.mkdir("/home/vagrant/Musify/storage/songs/lowquality")

        self.server.add_insecure_port(f'[::]:{port}')
        self.server.start()

        try:
            while True:
                time.sleep(60*60*24)
        except KeyboardInterrupt:
            self.server.stop(0)
