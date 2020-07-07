from flask import request

languages = {
    "es": {
        "UNAUTHORIZED": "No autorizado.",
        "NON_EXISTENT_ACCOUNT_SONG": "Esta canción no existe.",
        "NO_FILES_SELECTED": "No hay archivos seleccionados.",
        "ACCOUNT_SONG_DELETED": "Canción eliminada.",
        "ACCOUNT_NOT_AN_ARTIST": "Esta cuenta no es un artista",
        "NON_EXISTENT_ALBUM": "Este álbum no existe.",
        "NO_INPUT_DATA_PROVIDED": "No se proporcionó información.",
        "NON_EXISTENT_ARTIST": "Este artista no existe.",
        "NO_TOKEN_AUTH_PROVIDED": "No se proporcionó un Token de Autorización.",
        "INVALID_TOKEN_PROVIDED": "Token inválido.",
        "NON_EXISTENT_ACCOUNT": "Esta cuenta no existe.",
        "EXISTENT_ACCOUNT": "Esta cuenta ya existe.",
        "EXISTENT_ARTIST": "Este artista ya existe.",
        "INVALID_REQUEST_PROVIDED": "Tipo de solicitud inválida.",
        "NON_EXISTENT_GENRE": "Este género no existe.",
        "NO_VALID_INPUT_DATA_PROVIDED": "No se proporcionó información válida.",
        "NON_EXISTENT_PLAYLIST": "Esta lista de reproducción no existe.",
        "PLAYLIST_DELETED": "Lista de reproducción eliminada.",
        "SONG_NOT_IN_PLAYLIST": "Esta lista de reproducción no tiene esta canción.",
        "SONG_ALREADY_IN_PLAYLIST": "Esta lista de reproducción ya tiene esta canción.",
        "SONG_DELETED_FROM_PLAYLIST": "Canción eliminada de la lista de reproducción.",
        "NO_RATE_SUBMITTED": "No se ha calificado esta canción.",
        "NON_EXISTENT_SONG": "Esta canción no existe.",
        "RATE_ALREADY_SUBMITTED": "Ya se ha calificado esta canción.",
        "SONG_RATE_DELETED": "Calificación eliminada.",
        "SONG_NOT_READY_YET": "Esta canción no está lista aún.",
        "NON_ACTIVE_SUBSCRIPTION": "Esta cuenta no tiene una suscripción activa.",
        "ALREADY_ACTIVE_SUBSCRIPTION": "Esta cuenta ya tiene una suscripción activa."
    },
    "en": {
        "UNAUTHORIZED": "Unauthorized.",
        "NON_EXISTENT_ACCOUNT_SONG": "This account song does not exist.",
        "NO_FILES_SELECTED": "No files selected.",
        "ACCOUNT_SONG_DELETED": "Account song deleted.",
        "ACCOUNT_NOT_AN_ARTIST": "This account is not an artist.",
        "NON_EXISTENT_ALBUM": "This album does not exist.",
        "NO_INPUT_DATA_PROVIDED": "No input data provided.",
        "NON_EXISTENT_ARTIST": "This artist does not exist.",
        "NO_TOKEN_AUTH_PROVIDED": "No token Authorization provided.",
        "INVALID_TOKEN_PROVIDED": "Invalid token provided.",
        "NON_EXISTENT_ACCOUNT": "Account does not exist.",
        "EXISTENT_ACCOUNT": "Account already exists.",
        "EXISTENT_ARTIST": "Artist already exists.",
        "INVALID_REQUEST_PROVIDED": "No valid request type provided.",
        "NON_EXISTENT_GENRE": "This genre does not exist.",
        "NO_VALID_INPUT_DATA_PROVIDED": "No valid input data provided.",
        "NON_EXISTENT_PLAYLIST": "This playlist does not exist.",
        "PLAYLIST_DELETED": "Playlist deleted.",
        "SONG_NOT_IN_PLAYLIST": "This playlist does not have this song.",
        "SONG_ALREADY_IN_PLAYLIST": "This playlist already has this song.",
        "SONG_DELETED_FROM_PLAYLIST": "Song deleted from playlist.",
        "NO_RATE_SUBMITTED": "No rate submitted to this song.",
        "NON_EXISTENT_SONG": "This song does not exist.",
        "RATE_ALREADY_SUBMITTED": "A rate was already submitted.",
        "SONG_RATE_DELETED": "Song rate deleted.",
        "SONG_NOT_READY_YET": "This song is not ready yet.",
        "NON_ACTIVE_SUBSCRIPTION": "This account does not have an active subscription.",
        "ALREADY_ACTIVE_SUBSCRIPTION": "This account already have an active subscription."
    }
}

def get_request_message(request, message):
    language = request.headers.get("Accept-Language")
    if language and (language in languages):
        if (message in languages[language]):
            return languages[language][message]
        else:
            return "Invalid message"
    elif message in languages["en"]:
        return languages["en"][message]
    else:
        return "Unsupported language for this message"
