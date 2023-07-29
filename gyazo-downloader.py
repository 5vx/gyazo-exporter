import base64
import filedate
import json
import os
import requests

session = requests.Session()

cookie = input("enter gyazo session cookie: ")

images = []

page = 1
while True:
    print(f"[{page}] fetching images...", flush=True, end="")
    
    request = session.get(
        f"https://gyazo.com/api/internal/images?page={page}&per=100",
        cookies={"Gyazo_session": cookie}
    )
    
    print(f" done!", flush=True)

    if request.text == "[]":
        break

    images += request.json()

    page += 1

if not os.path.exists("downloads"):
    os.makedirs("downloads")

count = 1
for image in images:
    print(f"downloading image {count} of {len(images)}...", flush=True, end="")

    jwt = image['alias_id']
    url = image['non_cropped_thumb']['url']
    metadata = image['metadata']

    payload = json.loads(base64.b64decode(jwt.split('.')[1] + "=="))
    id = payload['img']
    ext = url[-7:-4]

    if "app" in metadata:
        filename = f"downloads/{image['metadata']['app']}{id}.{ext}"
    elif "title" in metadata:
        filename = f"downloads/{image['metadata']['title']}{id}.{ext}"
    else:
        filename = f"downloads/{id}.{ext}"

    if not os.path.exists(filename):
        request = session.get(f"https://thumb.gyazo.com/thumb/8192/{id}.{ext}")

        with open(filename, "wb") as file:
            file.write(request.content)

        timestamp = image['created_at']

        filedate.File(filename).set(
            created = timestamp,
            modified = timestamp
        ) 

    print(" done!", flush=True)

    count += 1