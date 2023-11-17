import queue

import requests
from bs4 import BeautifulSoup
from html.parser import HTMLParser

def get_one_page(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',

        'Cookie': 'nwtc=6552195b243bd5.17667496; AB_18=B; AB_28=B; AB_29=A; AB_34=B; AB_61=B; AB_62=A; _sharedID=058c527d-0555-4b3d-b958-810a107c0828; _sharedID_cst=zix7LPQsHA%3D%3D; _lr_env_src_ats=false; _cc_id=49ce091c93f39dd5929ad05c0c512221; _ga=GA1.3.1362542073.1699879271; cdb_panoid=1a49855f90f24e68b91815f23cada9fb927aaf00bcf72b3c313bc2a43521a838; trc_cookie_storage=taboola%2520global%253Auser-id%3D35f32bfa-c474-4eee-9468-c0154a33203a-tuct7410c26; _fbp=fb.2.1699879347548.988850939; _pubcid=3f1d457d-d98d-4f33-ae40-652679d98437; _pubcid_cst=zix7LPQsHA%3D%3D; cookieconsent_status=dismiss; cdb_nc_open_datetime=2023-11-16%2022%3A35%3A43; panoramaId=1a49855f90f24e68b91815f23cada9fb927aaf00bcf72b3c313bc2a43521a838; cdb_cookietime=2592000; cdb_auth=DtKH99khXLCIWAKyNhX8V4aBfuk1luvqkElLC1ELfmkSP9ca0CqIo9MOf1i5UTyhXJ2ace%2BgyylVzgJOR0HTX6Wh6Coy%2FRs4rbUUw85FUQjLjGE; mission_menu_popup_status=true; nwu=7323693; ui_uid_up=Q+eAI8jsH9ny7qc2zcqV5A==; mission_unread=0; _lr_geo_location_state=; _lr_geo_location=HK; _lr_sampling_rate=100; pbjs-unifiedid=%7B%22TDID%22%3A%22db58f4ba-9a3b-4d1e-b3d1-6a2edaafe3b9%22%2C%22TDID_LOOKUP%22%3A%22TRUE%22%2C%22TDID_CREATED_AT%22%3A%222023-10-16T14%3A39%3A05%22%7D; id5_storage=%7B%22signature%22%3A%22ID5_AlaFAaH9Y1yvZgqICbFIAWZHgyEf4lrkAnuUXICwg3wR6tUMAt8FFQWwv3NhRzO2UiZdyKhE90kjslZlRKRsAmHdnAkaSqhlAsttfiDXRop3ftp5gd0OdFWc%22%2C%22created_at%22%3A%222023-11-13T12%3A41%3A06.632Z%22%2C%22id5_consent%22%3Atrue%2C%22original_uid%22%3A%22ID5*r3PjbT5qqEPP1Whqwj0WKjSQjA8gTQ8q3sRoJ9h9kJJuiW7BxTJlP61u8B1Sp5H1bopuPA8pc9lWiUUNtYYWSw%22%2C%22universal_uid%22%3A%22ID5*mAY_bit12v4Vm7LUnjFgZ84r_aPZfbyQxPyb002SkrZuiTbfJHmq4L9p68HFK46abopBTxt9ZXSffRg21ReVPg%22%2C%22link_type%22%3A2%2C%22cascade_needed%22%3Afalse%2C%22privacy%22%3A%7B%22jurisdiction%22%3A%22other%22%2C%22id5_consent%22%3Atrue%7D%2C%22ext%22%3A%7B%22linkType%22%3A2%2C%22pba%22%3A%22lEAt4UirtMfcJXWh8AoblQ%3D%3D%22%7D%2C%22cache_control%22%3A%7B%22max_age_sec%22%3A7200%7D%7D; dfp_seg_ids=%5B%5D; lotame-audience-web=1700146046; panoramaIdType=panoDevice; connectId=%7B%22vmuid%22%3A%22TFVwzOcOWhwRc9c9toSWuhKNhRVfbT7UwnxmXhAn-5S58Te7hPNCVGeab0H4X_Em1TRUrUDR6eqzl5T39bk49Q%22%2C%22connectid%22%3A%22TFVwzOcOWhwRc9c9toSWuhKNhRVfbT7UwnxmXhAn-5S58Te7hPNCVGeab0H4X_Em1TRUrUDR6eqzl5T39bk49Q%22%2C%22connectId%22%3A%22TFVwzOcOWhwRc9c9toSWuhKNhRVfbT7UwnxmXhAn-5S58Te7hPNCVGeab0H4X_Em1TRUrUDR6eqzl5T39bk49Q%22%2C%22ttl%22%3A86400000%2C%22he%22%3A%229889ec291318f235a78835267e9a326bae3ce5b5da54a02ad2050253c2e11866%22%2C%22lastSynced%22%3A1700145509225%2C%22lastUsed%22%3A1700146056624%7D; mission_unread=2; uid2hash=a01695; __uid2_advertising_token=AgAABWYM5zlSkclnmEIlqZjVHbCHGos6OLX1rbLUzjC8PqgOSaIU+eXwhMOK43NOkiMUNtnOeByj0HvixfTME7IFP02hJA8UYeCdUp8Rfty7t61ka8srxd+vQxdUsjgdtS1sKRmjs7XcEtJMOGrUqY/q6qBvorfh9lgVu+/HLHO0vLPXHg%3D%3D; _lr_retry_request=true; _clck=kfv6oh%7C2%7Cfgs%7C0%7C1412; cdb_sid=SgOG7m; goowifq=1; screen_skin=true; up_c=1700224828; AB_full=18-B_28-B_29-A_34-B_61-B_62-A; cdb_oldtopics=D31363283D; cdb_visitedfid=437D1228D57D46D1230D23D175D54D679D40D106; cdb_urihistory=31363283-1%3B; cdb_urihistorycount=1; ttd-web=1700224832; nmc-web=1700224832; innity-web=1700224832; verizon-web=1700224832; __uid_2=%7B%22refresh_from%22%3A1700227321066%2C%22refresh_expires%22%3A1702815721066%2C%22identity_expires%22%3A1700310121066%2C%22advertising_token%22%3A%22AgAABWYM5zlSkclnmEIlqZjVHbCHGos6OLX1rbLUzjC8PqgOSaIU%2BeXwhMOK43NOkiMUNtnOeByj0HvixfTME7IFP02hJA8UYeCdUp8Rfty7t61ka8srxd%2BvQxdUsjgdtS1sKRmjs7XcEtJMOGrUqY%2Fq6qBvorfh9lgVu%2B%2FHLHO0vLPXHg%3D%3D%22%2C%22refresh_token%22%3A%22AAAABWdPgl75iJjsuoIymWq%2BrB9ZyYG4l48eBMtkhBrg6Lr0%2FflzIRzWuoojdvlc70dC83UrAikESDPMTeIjyYdakASAdGNFTsJDms1%2BFft3kbgTTY%2FzHZyjlV0hQW9tw7t44MYLz%2B4gWEbTaXiRf2ATNIZYmrE6TMQud2QVfkNF2WjX%2FmMGlo717A%2BjwgDIkEXqrONTPseFpRPM4wi581tRLoPd1OTj%2FLXfTaTTNIZpv8x1jlfJFiMlSeDMXhoKW22kztFCNFozyaW7lwMnyBfdMInSCU%2F290Bq4bXVR87F%2FtfXuuCiqqWHM%2FXaP%2B7m1eoGQGsIzaP7Oul4I8TxQtNfxQEG%2B6ZPRfminTCWON7Re%2F9ErfIiFxs4UsaAgVCnuiYH%22%2C%22refresh_response_key%22%3A%22dTn3CQDb4ZiN6OvHmBVLqnyOZjZXoUOL%2BUndeBCZi8o%3D%22%7D; _pbjs_userid_consent_data=3524755945110770; panoramaId_expiry=1700311233974; cdb_fb_referer=https%3A%2F%2Fwww.discuss.com.hk%2Fviewthread.php%3Ftid%3D31363283%26utm_source%3Dfestival_fid%26utm_medium%3D1228%26utm_campaign%3D804%26extra%3Dpage%253D1; nvg56367=13a19b25daf3433fc86f5a7c3810|0_322; cto_bundle=bAn5G19EMUNSWFYwak11YnFlSjROc3dENlF2aWtiNTVCQXl5YUxvWGVuOHpvSVBuYTR4UVVuZ3hVQjR5OFJZcnBQSXdNQWYlMkZGeEpNOVdTMUJvZmlEd3FRT3Nzd2dZd2JPZExTT00lMkZnMHpuMWwyTUslMkZrNHB2QnlwRncxWmZEZ1IlMkZacmlNYlFVUzVCSDNpc1lXakd1NFhrc2JXQjA1MTd0bEZsSUNZcTdiJTJGMnU3dlc0JTNE; cto_bidid=qfcESl8lMkZTZVBBS3d5MnN0UG1OdG1hbHZua3ZBMXVTS05xYmg5b3NtUzAxUURMdTFPT0NNV1VtYzElMkJzektHaGlUeVljNzl5VW9CZ0NqVEptcnhRTUZlbk5ab0t4MG5WS2xPN0RzUlFkeXY1UzAyZzR3Ym9ITFI4cUprJTJCZmpONVpiQmxHSg; FCNEC=%5B%5B%22AKsRol8SX6jstOLoHSVrp_P90b8_kDA3Spx_WlJkfnhVVCuw8WjTdFUXSA7MsamOP_0d-1HW4xfku_apkGQs_zSXVtZ74XLYDXevz0rETWFTzGdoOtt4D6DTSeaFqLKq01_FGRdZYyewVWjEljYDoKb1tPGcDoPd6w%3D%3D%22%5D%2Cnull%2C%5B%5D%5D; viewthread_history=31363283%7C31363283%7C31367742%7C31357434%7C31357434%7C31206713%7C31364858%7C31365370%7C31351574%7C31363107%7C31363768%7C31364189%7C31364327%7C31364327%7C31364327; cdb_lastrequest=XKsAO4PVra3nlAFbo%2B44d89M; _clsk=z2oob5%7C1700224916055%7C2%7C1%7Cy.clarity.ms%2Fcollect; __gads=ID=8716b30edb38dd5f:T=1699879338:RT=1700224929:S=ALNI_MYBsvLvnyEFj0tq0mlRiycixSdDNQ; __gpi=UID=00000c85aa4a2c6e:T=1699879338:RT=1700224929:S=ALNI_MZWZjrr_vMwOZ9A9_6XrLfTFmmzaw; _ga_8P52FKWN6G=GS1.3.1700223721.6.1.1700224938.0.0.0',
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
        if href and "php" in href :
            links.append(href)

    links = [link for link in links if link not in visited_link_pool]
    links = [root_url+"/"+link for link in links]
    links = [link.replace("//","/") for link in links]
    links = [link.replace("//","/") for link in links]
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