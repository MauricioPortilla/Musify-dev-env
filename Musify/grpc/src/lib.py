import musify_service_pb2 as MusifyService, musify_service_pb2_grpc as MusifyServiceGRPC

CHUNK_SIZE = 1024 * 1024

def getFileChunks(path, filename):
    with open(path, 'rb') as file:
        piece = file.read(CHUNK_SIZE);
        while piece:
            yield MusifyService.SongChunk(buffer=piece, name=filename)
            piece = file.read(CHUNK_SIZE);

def saveChunksToFile(chunks, filename):
    with open(filename, 'wb') as file:
        for chunk in chunks:
            file.write(chunk.buffer)
