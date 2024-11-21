import http.client
import urllib
import json
import time
from my_class import User,Comment
from misc import *
from data import urls

# urls = [
#     # 'https://vt.tiktok.com/ZSjm7uh7U/',
#     # 'https://vt.tiktok.com/ZSjm7Qj7E/',
#     # 'https://vt.tiktok.com/ZSjm7AFjP/',
#     # 'https://vt.tiktok.com/ZSjm7kYpW/',
#     # 'https://vt.tiktok.com/ZSjm7D3LN/',
#     'https://www.tiktok.com/@sofl.tiengtrung/video/6937970214248238338?_r=1&_t=8rU7xnnpime'
# ]

conn = http.client.HTTPSConnection("tiktok-scraper7.p.rapidapi.com")
headers = {
    'x-rapidapi-key': "e7be0e5833mshaa3ab2a8d482ac2p135767jsn38209b78bb91",
    'x-rapidapi-host': "tiktok-scraper7.p.rapidapi.com"
}

def makeRequest(url:str, count=50, cursor=0)->str:
    decoded_url = urllib.parse.unquote(url)
    conn.request("GET", 
             f"/comment/list?url={decoded_url}&count={count}&cursor={cursor*count}", 
             headers=headers)

    res = conn.getresponse()
    data = res.read()
    ret = data.decode("utf-8")
    return ret if ret is not None else ''

if __name__ == '__main__':

    for i_url, url in enumerate(urls,42):
        print(f'--#URL {i_url}--')
        
        total_time = 0
        total_lines = 0
        
        for i in range(1,120,1):
            start_time = time.time()
            
            json_str = makeRequest(url=url,cursor=i)
            data = json.loads(json_str)
            if data == '': continue
            
            comments_data = data['data']['comments']

            # Convert to a list of Comment objects
            comments = []
            for comment_data in comments_data:
                user_data = comment_data['user']
                user = User(
                    id=user_data['id'],
                    region=user_data['region'],
                    sec_uid=user_data['sec_uid'],
                    unique_id=user_data['unique_id'],
                    nickname=user_data['nickname'],
                    signature=user_data['signature'],
                    avatar=user_data['avatar'],
                    verified=user_data['verified'],
                    secret=user_data['secret']
                )
                comment = Comment(
                    id=comment_data['id'],
                    video_id=comment_data['video_id'],
                    text=comment_data['text'],
                    create_time=comment_data['create_time'],
                    digg_count=comment_data['digg_count'],
                    reply_total=comment_data['reply_total'],
                    user=user,
                    status=comment_data['status']
                )
                comments.append(comment)

            # with open('comments.json', 'a', encoding='utf-8') as f:
            #     # Serialize the list of dictionaries (converted from Comment objects) to a JSON file
            #     json.dump([comment.to_dict() for comment in comments], f, ensure_ascii=False, indent=4)
            appendComments(comments=comments,
                        filename=f'{url2Filename(url)}.json')
            
            duration = time.time() - start_time
            total_time += duration
            l = len(comments)
            total_lines += l
            
            print(f'batch {i}: #cmt{l} {duration}s')
            
            if l == 0:
                break
            

        print(f'total time: {total_time}s')
        print(f'total lines: {total_lines}')