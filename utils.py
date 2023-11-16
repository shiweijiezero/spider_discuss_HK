import queue

import requests
from bs4 import BeautifulSoup
from html.parser import HTMLParser

def get_one_page(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',

        'Cookie': 'nwtc=6552195b243bd5.17667496; AB_18=B; AB_28=B; AB_29=A; AB_34=B; AB_61=B; AB_62=A; _sharedID=058c527d-0555-4b3d-b958-810a107c0828; _sharedID_cst=zix7LPQsHA%3D%3D; _lr_env_src_ats=false; _cc_id=49ce091c93f39dd5929ad05c0c512221; _ga=GA1.3.1362542073.1699879271; cdb_panoid=1a49855f90f24e68b91815f23cada9fb927aaf00bcf72b3c313bc2a43521a838; trc_cookie_storage=taboola%2520global%253Auser-id%3D35f32bfa-c474-4eee-9468-c0154a33203a-tuct7410c26; _fbp=fb.2.1699879347548.988850939; _pubcid=3f1d457d-d98d-4f33-ae40-652679d98437; _pubcid_cst=zix7LPQsHA%3D%3D; cookieconsent_status=dismiss; nvg56367=13a19b25daf3433fc86f5a7c3810|0_319; cdb_visitedfid=46D1230D437D23D175D54D679D40D106D110; viewthread_history=31357434%7C31357434%7C31206713%7C31364858%7C31365370%7C31351574%7C31363107%7C31363768%7C31364189%7C31364327%7C31364327%7C31364327; cto_bidid=9Hhlz18lMkZTZVBBS3d5MnN0UG1OdG1hbHZua3ZBMXVTS05xYmg5b3NtUzAxUURMdTFPT0NNV1VtYzElMkJzektHaGlUeVljNzl5VW9CZ0NqVEptcnhRTUZlbk5ab045Y1l0dWFISnJ5UDIySUxJZ0E5RjhsR2g2dW1sJTJGWlN4eDRadEw5UTlkRQ; cdb_sid=OdOZ4i; cdb_nc_open_datetime=2023-11-16%2022%3A35%3A43; ttd-web=1700145343; nmc-web=1700145343; innity-web=1700145343; verizon-web=1700145343; _lr_retry_request=true; panoramaId_expiry=1700231745013; panoramaId=1a49855f90f24e68b91815f23cada9fb927aaf00bcf72b3c313bc2a43521a838; AB_full=18-B_28-B_29-A_34-B_61-B_62-A; up_c=1700145349; _clck=kfv6oh|2|fgr|0|1412; cdb_cookietime=2592000; cdb_auth=DtKH99khXLCIWAKyNhX8V4aBfuk1luvqkElLC1ELfmkSP9ca0CqIo9MOf1i5UTyhXJ2ace%2BgyylVzgJOR0HTX6Wh6Coy%2FRs4rbUUw85FUQjLjGE; mission_menu_popup_status=true; nwu=7323693; ui_uid_up=Q+eAI8jsH9ny7qc2zcqV5A==; mission_unread=1; mission_unread=0; _lr_geo_location_state=; _lr_geo_location=HK; __gads=ID=8716b30edb38dd5f:T=1699879338:RT=1700145466:S=ALNI_MYBsvLvnyEFj0tq0mlRiycixSdDNQ; __gpi=UID=00000c85aa4a2c6e:T=1699879338:RT=1700145466:S=ALNI_MZWZjrr_vMwOZ9A9_6XrLfTFmmzaw; _lr_sampling_rate=100; cdb_lastrequest=C6BUO9eG9KnnlAFboOg5e85L; _ga_8P52FKWN6G=GS1.3.1700145345.4.1.1700145508.0.0.0; connectId=%7B%22vmuid%22%3A%22TFVwzOcOWhwRc9c9toSWuhKNhRVfbT7UwnxmXhAn-5S58Te7hPNCVGeab0H4X_Em1TRUrUDR6eqzl5T39bk49Q%22%2C%22connectid%22%3A%22TFVwzOcOWhwRc9c9toSWuhKNhRVfbT7UwnxmXhAn-5S58Te7hPNCVGeab0H4X_Em1TRUrUDR6eqzl5T39bk49Q%22%2C%22connectId%22%3A%22TFVwzOcOWhwRc9c9toSWuhKNhRVfbT7UwnxmXhAn-5S58Te7hPNCVGeab0H4X_Em1TRUrUDR6eqzl5T39bk49Q%22%2C%22ttl%22%3A86400000%2C%22he%22%3A%229889ec291318f235a78835267e9a326bae3ce5b5da54a02ad2050253c2e11866%22%2C%22lastSynced%22%3A1700145509225%2C%22lastUsed%22%3A1700145509225%7D; cto_bundle=aMbHv19EMUNSWFYwak11YnFlSjROc3dENlFuaUxnUTNoMEVqVjBVRXdBS0RFJTJGT2V3aUxqRiUyQkYzMk5VZW1PR1lBQlZCN2p1SkpZTDVtdEJBZjRFeU9ZU2FaR00wJTJCVUhwR29RU0xJZHJvUlhWWUJNUmRnbERXcVpPN29XMU5UVjdnUkhmc283eDBPV0VSNWZDWlklMkJ6bFdtZ2p3VEUlMkYlMkIzZTJlJTJGbW9wN2JNR1BJa29IdyUzRA; _clsk=rhqsve|1700145517547|4|1|r.clarity.ms/collect; FCNEC=%5B%5B%22AKsRol_JLnn0ABe3eYY8DBs2SPp4vC1tG8sOAv2T3FGIbXB3QtoyWyTzCmySNx3R9lPseRzr-2G5MmlHqUdpyReCsiEFzRxsbaOT80rueb66VDTIVU5dzwRqk0kFY7qLscYPE6pc6nBslA6m42pYLyNrtY3Xe292zQ%3D%3D%22%5D%2Cnull%2C%5B%5D%5D; _pbjs_userid_consent_data=6683316680106290; pbjs-unifiedid=%7B%22TDID%22%3A%22db58f4ba-9a3b-4d1e-b3d1-6a2edaafe3b9%22%2C%22TDID_LOOKUP%22%3A%22TRUE%22%2C%22TDID_CREATED_AT%22%3A%222023-10-16T14%3A39%3A05%22%7D; id5_storage=%7B%22signature%22%3A%22ID5_AlaFAaH9Y1yvZgqICbFIAWZHgyEf4lrkAnuUXICwg3wR6tUMAt8FFQWwv3NhRzO2UiZdyKhE90kjslZlRKRsAmHdnAkaSqhlAsttfiDXRop3ftp5gd0OdFWc%22%2C%22created_at%22%3A%222023-11-13T12%3A41%3A06.632Z%22%2C%22id5_consent%22%3Atrue%2C%22original_uid%22%3A%22ID5*r3PjbT5qqEPP1Whqwj0WKjSQjA8gTQ8q3sRoJ9h9kJJuiW7BxTJlP61u8B1Sp5H1bopuPA8pc9lWiUUNtYYWSw%22%2C%22universal_uid%22%3A%22ID5*mAY_bit12v4Vm7LUnjFgZ84r_aPZfbyQxPyb002SkrZuiTbfJHmq4L9p68HFK46abopBTxt9ZXSffRg21ReVPg%22%2C%22link_type%22%3A2%2C%22cascade_needed%22%3Afalse%2C%22privacy%22%3A%7B%22jurisdiction%22%3A%22other%22%2C%22id5_consent%22%3Atrue%7D%2C%22ext%22%3A%7B%22linkType%22%3A2%2C%22pba%22%3A%22lEAt4UirtMfcJXWh8AoblQ%3D%3D%22%7D%2C%22cache_control%22%3A%7B%22max_age_sec%22%3A7200%7D%7D',
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

def get_links(root_url,soup,visited_link_pool):
    links = []
    for a in soup.find_all('a'):
        href = a.get('href')
        if href and "php" in href:
            links.append(href)

    links = [link for link in links if link not in visited_link_pool]
    links = [root_url+"/"+link for link in links]
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