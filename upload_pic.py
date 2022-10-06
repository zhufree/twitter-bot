import httpx
from config import headers

upload_url = 'https://upload.twitter.com/i/media/upload.json'
imageheaders = {
    "User-Agent": "Mozilla/5.0",
    "accept": "*/*",
    "accept-encoding": "gzip, deflate, br",
    "origin": "https://twitter.com",
    "authority": "upload.twitter.com",
    "referer": "https://twitter.com/",
}

def upload_img(img_url):
    # download img file
    print(f'Downloading {img_url}')
    image = httpx.get(img_url).content
    print(f'image size = {len(image)}')
    headers.update(imageheaders)
    img_type = 'gif' if img_url.endswith('gif') else 'jpeg'
    img_category = 'gif' if img_url.endswith('gif') else 'image' 
    with httpx.Client(headers=headers) as client:
        # get image id
        imageid_res = client.post(
            upload_url +
            f'?command=INIT&total_bytes={len(image)}&media_type=image%2F{img_type}&media_category=tweet_{img_category}'
        )
        # print(imageid_res.content)
        imageid_json = imageid_res.json()
        if 'media_id' in imageid_json.keys():
            image_id = imageid_json['media_id']
            files = {'media': image}
            # upload image
            append_res = client.post(upload_url +
                        f'?command=APPEND&media_id={image_id}&segment_index=0',
                        files=files)
            # print(append_res.content)
            finish_upload_res = client.post(
                upload_url + f'?command=FINALIZE&media_id={image_id}')
            print(finish_upload_res.content)
            if img_type == 'gif':
                status_res = client.get(upload_url + f'?command=STATUS&media_id={image_id}')
                print(status_res.content)
            return image_id
        else:
            return False

if __name__ == '__main__':
	upload_img('https://wx1.sinaimg.cn/orj1080/007cLxrLly1h6pxt3ruunj30hs2f5q7c.jpg')