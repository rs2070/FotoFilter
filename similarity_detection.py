import os
from PIL import Image
import imagehash

def find_duplicates(directory, hash_size=7, cutoff=5):
    hashes = {}
    duplicates = {}

    for filename in os.listdir(directory): #all files listed
        if filename.endswith(('.jpg', '.jpeg', '.png')) and '_detected' not in filename:
            file_path = os.path.join(directory, filename)
            try:
                with Image.open(file_path) as img:
                    temp_hash = imagehash.average_hash(img, hash_size) #find hash, store in dict.
                    for h, existing_filename in hashes.items(): #compare hashes, find images that look the same
                        if abs(temp_hash - h) < cutoff:  #difference using abs()
                            if existing_filename not in duplicates:
                                duplicates[existing_filename] = [filename]
                            else:
                                duplicates[existing_filename].append(filename)
                            break
                    else:
                        hashes[temp_hash] = filename #add image + hash if no dupes detected
            except Exception as e:
                print(f"Error processing {filename}: {e}")

    return duplicates