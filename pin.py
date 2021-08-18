import subprocess
import sys 
import json 
from copy import deepcopy  

img_path = sys.argv[1]
metadata_path = sys.argv[2]

print("img_path: ", img_path)

node_path = '/usr/bin/node'

# jwt_token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySW5mb3JtYXRpb24iOnsiaWQiOiJkZTZjMmE0MC05MGQzLTRkNDQtYmMzMS1mZDcxYjhiNDcwNGMiLCJlbWFpbCI6InJlYWxqb2hudHdhcmRAZ21haWwuY29tIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsInBpbl9wb2xpY3kiOnsicmVnaW9ucyI6W3siaWQiOiJOWUMxIiwiZGVzaXJlZFJlcGxpY2F0aW9uQ291bnQiOjF9XSwidmVyc2lvbiI6MX0sIm1mYV9lbmFibGVkIjpmYWxzZX0sImF1dGhlbnRpY2F0aW9uVHlwZSI6InNjb3BlZEtleSIsInNjb3BlZEtleUtleSI6IjAwOTUxODA5YjA3M2QwYTU1ZTlhIiwic2NvcGVkS2V5U2VjcmV0IjoiM2IxMDg5ZjlhNzdlMmY2Y2VlOTY3YWVhYjNiY2RhOGM5NDI3ZTUxOWIxMThmMDdiYmYyNzRhZTAwOTkzOTgzZiIsImlhdCI6MTYyNTg4MDM2NH0.q1EyAh57PH_sAqG7DEv5g8dtBmPwrOb3LHNRB5CI-Js'
base_metadata = json.load(open(metadata_path))
metadata_hashes = json.load(open('./metadata_hashes.json'))
metadata_hashes[img_path] = []

def pin_img_to_pinata(img_path):
    ipfs_hash = subprocess.check_output([f'{node_path}','./_pinImgToPinata.js', img_path])
    return ipfs_hash.decode().strip()

def pin_metadata_to_pinata(img_ipfs_hash, edition_index):
    metadata = deepcopy(base_metadata)
    metadata['image'] = base_metadata['image'] + img_ipfs_hash
    metadata['attributes'].append({'display_type': 'number', 'trait_type': 'Edition', 'max_value': 10, 'value': edition_index + 1})
    metadata_ipfs_hash = subprocess.check_output([node_path, './_pinMetadataToPinata.js', json.dumps(metadata), str(edition_index+1)])
    return metadata_ipfs_hash.decode().strip()

img_ipfs_hash = pin_img_to_pinata(img_path)

for i in range(0, base_metadata['total_editions']):
    metadata_hash = pin_metadata_to_pinata(img_ipfs_hash, i)
    metadata_hashes[img_path].append(metadata_hash)
    print(f'Edition: {i+1}; Metadata Hash: {metadata_hash}')

json.dump(metadata_hashes, open('./metadata_hashes.json', 'w'))
print("Done")
    