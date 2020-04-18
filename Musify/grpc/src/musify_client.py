import grpc, os
import musify_service_pb2 as MusifyService, musify_service_pb2_grpc as MusifyServiceGRPC
import lib, json

class MusifyClient:
    def __init__(self, address):
        channel = grpc.insecure_channel(address)
        self.stub = MusifyServiceGRPC.MusifyServiceStub(channel)

    def upload(self, filepath, filename):
        chunks_generator = lib.getFileChunks(filepath, filename)
        response = self.stub.upload(chunks_generator)
        status = "success" if response.length == os.path.getsize(filepath) else "failure"
        print(json.dumps({"status": status, "name": response.name}))

    def download(self, songFilename, songQuality):
        # response = self.stub.download(MusifyService.SongRequest(name=songFilename, quality=songQuality))
        # lib.saveChunksToFile(response, destinationPath)
        return self.stub.download(MusifyService.SongRequest(name=songFilename, quality=songQuality))