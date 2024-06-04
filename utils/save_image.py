import os
import secrets

def generate_unique_filename(filename):
    base, extension = os.path.splitext(filename)
    random_string = secrets.token_hex(8)  # Adjust length as needed
    unique_filename = f"{random_string}{extension}"
    return unique_filename

def save_to_album_media(instance, filename):
    unique_filename = generate_unique_filename(filename)
    return os.path.join("album_images", unique_filename)

def save_to_user_media(instance, filename):
    unique_filename = generate_unique_filename(filename)
    return os.path.join("user_images", unique_filename)

def save_to_track_media(instance, filename):
    unique_filename = generate_unique_filename(filename)
    return os.path.join("track_images", unique_filename)

def save_to_playlist_media(instance, filename):
    unique_filename = generate_unique_filename(filename)
    return os.path.join("playlist_images", unique_filename)
