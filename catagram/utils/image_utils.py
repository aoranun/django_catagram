import hashlib

def get_file_hash(file_obj):
    # Create a new hash object
    hash_obj = hashlib.sha256()

    # Read the file in chunks to save memory
    for chunk in iter(lambda: file_obj.read(4096), b""):
        hash_obj.update(chunk)

    # Get the hex digest of the hash
    hash_str = hash_obj.hexdigest()

    return hash_str


def catpic_image_path(instance, filename):
    # Return the new path for the file
    return 'cat_pics/' + instance.title + '.' + filename.split('.')[-1]
