import os
import musify_client

if __name__ == '__main__':
    client = musify_client.MusifyClient('192.168.1.75:8888')

    client.upload('/home/vagrant/Musify/storage/songs/2.mp3', '2.mp3')
    # client.download('de4a98d41bf7b126063b3b631d261b54edd4cbef.mp3', 'mediumQuality', './')
