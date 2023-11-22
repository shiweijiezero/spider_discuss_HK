import os
import pickle
import queue
import time

import requests
from bs4 import BeautifulSoup
from html.parser import HTMLParser




def get_one_page(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',

        'Cookie': 'nwtc=6552195b243bd5.17667496; AB_18=B; AB_28=B; AB_29=A; AB_34=B; AB_61=B; AB_62=A; _sharedID=058c527d-0555-4b3d-b958-810a107c0828; _sharedID_cst=zix7LPQsHA%3D%3D; _lr_env_src_ats=false; _cc_id=49ce091c93f39dd5929ad05c0c512221; _ga=GA1.3.1362542073.1699879271; cdb_panoid=1a49855f90f24e68b91815f23cada9fb927aaf00bcf72b3c313bc2a43521a838; trc_cookie_storage=taboola%2520global%253Auser-id%3D35f32bfa-c474-4eee-9468-c0154a33203a-tuct7410c26; _fbp=fb.2.1699879347548.988850939; _pubcid=3f1d457d-d98d-4f33-ae40-652679d98437; _pubcid_cst=zix7LPQsHA%3D%3D; cookieconsent_status=dismiss; cdb_cookietime=2592000; cdb_auth=DtKH99khXLCIWAKyNhX8V4aBfuk1luvqkElLC1ELfmkSP9ca0CqIo9MOf1i5UTyhXJ2ace%2BgyylVzgJOR0HTX6Wh6Coy%2FRs4rbUUw85FUQjLjGE; nwu=7323693; ui_uid_up=Q+eAI8jsH9ny7qc2zcqV5A==; mission_unread=0; pbjs-unifiedid=%7B%22TDID%22%3A%22db58f4ba-9a3b-4d1e-b3d1-6a2edaafe3b9%22%2C%22TDID_LOOKUP%22%3A%22TRUE%22%2C%22TDID_CREATED_AT%22%3A%222023-10-16T14%3A39%3A05%22%7D; id5_storage=%7B%22signature%22%3A%22ID5_AlaFAaH9Y1yvZgqICbFIAWZHgyEf4lrkAnuUXICwg3wR6tUMAt8FFQWwv3NhRzO2UiZdyKhE90kjslZlRKRsAmHdnAkaSqhlAsttfiDXRop3ftp5gd0OdFWc%22%2C%22created_at%22%3A%222023-11-13T12%3A41%3A06.632Z%22%2C%22id5_consent%22%3Atrue%2C%22original_uid%22%3A%22ID5*r3PjbT5qqEPP1Whqwj0WKjSQjA8gTQ8q3sRoJ9h9kJJuiW7BxTJlP61u8B1Sp5H1bopuPA8pc9lWiUUNtYYWSw%22%2C%22universal_uid%22%3A%22ID5*mAY_bit12v4Vm7LUnjFgZ84r_aPZfbyQxPyb002SkrZuiTbfJHmq4L9p68HFK46abopBTxt9ZXSffRg21ReVPg%22%2C%22link_type%22%3A2%2C%22cascade_needed%22%3Afalse%2C%22privacy%22%3A%7B%22jurisdiction%22%3A%22other%22%2C%22id5_consent%22%3Atrue%7D%2C%22ext%22%3A%7B%22linkType%22%3A2%2C%22pba%22%3A%22lEAt4UirtMfcJXWh8AoblQ%3D%3D%22%7D%2C%22cache_control%22%3A%7B%22max_age_sec%22%3A7200%7D%7D; uid2hash=a01695; _pbjs_userid_consent_data=3524755945110770; nvg56367=13a19b25daf3433fc86f5a7c3810|0_322; _clck=kfv6oh%7C2%7Cfgs%7C0%7C1412|2|fgs|0|1416; connectId=%7B%22vmuid%22%3A%22TFVwzOcOWhwRc9c9toSWuhKNhRVfbT7UwnxmXhAn-5S58Te7hPNCVGeab0H4X_Em1TRUrUDR6eqzl5T39bk49Q%22%2C%22connectid%22%3A%22TFVwzOcOWhwRc9c9toSWuhKNhRVfbT7UwnxmXhAn-5S58Te7hPNCVGeab0H4X_Em1TRUrUDR6eqzl5T39bk49Q%22%2C%22connectId%22%3A%22TFVwzOcOWhwRc9c9toSWuhKNhRVfbT7UwnxmXhAn-5S58Te7hPNCVGeab0H4X_Em1TRUrUDR6eqzl5T39bk49Q%22%2C%22ttl%22%3A86400000%2C%22he%22%3A%229889ec291318f235a78835267e9a326bae3ce5b5da54a02ad2050253c2e11866%22%2C%22lastSynced%22%3A1700145509225%2C%22lastUsed%22%3A1700225676963%7D; cdb_news_all=0; viewthread_history=31358885%7C31358885%7C31358885%7C31364416%7C31364416%7C31367839%7C31351574%7C31363283%7C31363283%7C31363283%7C31367742%7C31357434%7C31357434%7C31206713%7C31364858%7C31365370%7C31351574%7C31363107%7C31363768%7C31364189%7C31364327%7C31364327%7C31364327; FCNEC=%5B%5B%22AKsRol_-l3y9tJeo3am3XGU1FwFN4yddjZGoh7rOZ5bbo4KTRWxfA3ie-inOnsPinm8vrhdUUo7kzayuRgIJzKgCFTr3Lh0t8N5ySuLOufLlV1TFtPeja0CWx-bOeS3QTiqS4bGambNyPTFJmTG-uMhuaNwqyA7vxw%3D%3D%22%5D%2Cnull%2C%5B%5D%5D; cdb_visitedfid=1192D1230D316D54D59D679D437D1228D57D46D23; cdb_fb_referer=https%3A%2F%2Fwww.discuss.com.hk%2Fforumdisplay.php%3Ffid%3D1192%26filter%3Dtype%26orderby%3Dt.lastpost%26ascdesc%3DDESC%26typeid%3D1122; __gads=ID=8716b30edb38dd5f:T=1699879338:RT=1700227159:S=ALNI_MYBsvLvnyEFj0tq0mlRiycixSdDNQ; __gpi=UID=00000c85aa4a2c6e:T=1699879338:RT=1700227159:S=ALNI_MZWZjrr_vMwOZ9A9_6XrLfTFmmzaw; cto_bundle=Ugdkb19EMUNSWFYwak11YnFlSjROc3dENlFnUGRHUyUyQm9MdWhlS29NWUJzNkdBZE91VGJ0clNnNGk5cTBUNlhEZG1La0thMmZVMnRGdWdXYUVScCUyRjMzUENIZnZnOWUlMkYwSzJ1TWxDN01tWTdVRWNmeVA3UHo3b25sbyUyQjkwbE81S3pFd0RqaXBvem5NNmlucEVQa0g4ZEtHdldhdjVUbWZNc2F0ckprbk1XZFBmMmFwOCUzRA; cto_bidid=xu4A818lMkZTZVBBS3d5MnN0UG1OdG1hbHZua3ZBMXVTS05xYmg5b3NtUzAxUURMdTFPT0NNV1VtYzElMkJzektHaGlUeVljNzl5VW9CZ0NqVEptcnhRTUZlbk5ab0w1VWI3SVd3Um9HQUJWNDJYclF5Tmx2T3dpYktZdkVpTXYzbXN1UWRTVmM; cdb_sid=cnJVlU; mission_unread=1; goowifq=1; ttd-web=1700654144; nmc-web=1700654144; innity-web=1700654144; verizon-web=1700654144; _lr_retry_request=true; mission_menu_popup_status=true; AB_full=18-B_28-B_29-A_34-B_61-B_62-A; __uid2_advertising_token=AgAABW+D4fKP+EwJu5YkveZdH1hDRERB8x+I2aq9NBlqe9wMJcRWsKjJeX37Hrqk0SQB1Y+hvh4GYma+jRc9klVDZBrD3jZoVgIUvVyHB7ZmTyZQsskGmLr3VTjQUWSfVCsRHuYfubdZV/xPj8mlra+FsW8X7noXSi6Nwu4GRKWLOuOy/w%3D%3D; up_c=1700654148; panoramaId_expiry=1700740547727; panoramaId=1a49855f90f24e68b91815f23cada9fb927aaf00bcf72b3c313bc2a43521a838; _lr_geo_location_state=; _lr_geo_location=HK; __uid_2=%7B%22refresh_from%22%3A1700657747109%2C%22refresh_expires%22%3A1703246147109%2C%22identity_expires%22%3A1700740547109%2C%22advertising_token%22%3A%22AgAABW%2BD4fKP%2BEwJu5YkveZdH1hDRERB8x%2BI2aq9NBlqe9wMJcRWsKjJeX37Hrqk0SQB1Y%2Bhvh4GYma%2BjRc9klVDZBrD3jZoVgIUvVyHB7ZmTyZQsskGmLr3VTjQUWSfVCsRHuYfubdZV%2FxPj8mlra%2BFsW8X7noXSi6Nwu4GRKWLOuOy%2Fw%3D%3D%22%2C%22refresh_token%22%3A%22AAAABXCZ0wwf5KQjHVrBNLukX3VR0nUO41qr7H0fXq73phJDP8qtnl7vgh%2BHCGrGjgyUpdCGwbxkwYhc%2Be8opuv%2BdpWK4gCaGs49VMhjkQU6V1LzOB3AJIhyqJgrImGkT5STXwaiEjHvcuTg971yRhhfUpeQsVZZFxM3Ou%2Bo7FILsfhYKBD56Sj%2Fr7hlqT2xqLpKOMCBKHwQPUZpkUbpjbUUBD8AhpXDepmq0SgdHEi%2B8MpiXS7pN%2FjuAVW2C01pg9U65TDlUbo2epS8lCbiBAAFBRkwZANULoMWQZsuQG4KW80yaA9nVKO5vcLsqQ7jhadh%2BbOrWpTF9rru2PXHCSqOGWuC4e2uRMpWH%2BeO4xYWEAkAckm2C8nJ%2FcOJuhGJlo2y%22%2C%22refresh_response_key%22%3A%22p8h9CoiFRDqu5vamH7W6CQp384OY94wiJmIhtEUK%2F8k%3D%22%7D; _ga_8P52FKWN6G=GS1.3.1700654147.7.1.1700654333.0.0.0; cdb_lastrequest=C6BRbIPU9fjnlAFbp%2Bk4fc1K; _lr_sampling_rate=100',
    }

    i=0
    while i < 2:
        try:
            resp = requests.get(url,headers=headers, timeout=1)
            # if (resp.status_code!=200):
            #     print(f"resp：{resp.status_code}")
            break # 一定要break
        except:
            i+=1
    if(i>=2):
        print("超时2次")
        return None
    soup = BeautifulSoup(resp.text, 'html.parser')
    return soup

def get_links(prefix_url,soup,visited_link_pool):
    links = []
    for a in soup.find_all('a'):
        href = a.get('href')
        if href and href.startswith("archiver"):
            href = f"{prefix_url}{href}"
            links.append(href)

    links = [link for link in links if link not in visited_link_pool]
    return links

def get_content(soup):
    s = soup.get_text()
    s = s.replace(" ", "")
    s = s.replace("\n", "")
    s = s.replace("\t", "")
    return s,len(s)


def strip_tags(html):
    """
    Python中过滤HTML标签的函数
    """
    html = html.strip()
    html = html.strip("\n")

    result = []
    parser = HTMLParser()
    parser.handle_data = result.append
    parser.feed(html)
    parser.close()
    result = ''.join(result)
    result = result.replace("\n", "")
    return result

def load_state(state_path):
    with open(state_path, "rb") as f:
        return pickle.load(f)

def save_state(state,state_path):
    local_time = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())
    target_file = os.path.join(state_path,f"state-{local_time}.pkl")
    with open(target_file, "wb") as f:
        pickle.dump(state, f)
    return target_file