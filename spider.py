# https://www.discuss.com.hk/
import os.path
import pickle
import queue
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Pool

from tqdm import tqdm
import utils

if __name__ == "__main__":
    root_url = 'https://www.discuss.com.hk/'

    visited_link_pool = set()
    on_look_link_pool = set()
    on_look_link_pool.add(root_url)
    tq = tqdm()
    sum_text_num = 0
    current_text_num = 0
    file_counter = 0
    max_one_save_file = 1e6
    save_path = "./data"
    state_path = "./data/state.pkl"
    current_text_lst = []
    fail_num = 0
    save_state_step = 1
    sum_id = 0
    batch_size = 5
    max_workers = 3

    while on_look_link_pool:
        if (sum_id % save_state_step == 0):
            if (os.path.exists(state_path)):
                with open(state_path, "rb") as f:
                    sum_text_num, current_text_num, file_counter, on_look_link_pool, \
                        fail_num, visited_link_pool, sum_id, current_text_lst = pickle.load(f)

        tq.update(1)
        tq.set_postfix(
            sum_char=sum_text_num,
            current_text=current_text_num,
            file_counter=file_counter,
            on_look_link_pool_size=len(on_look_link_pool),
            fail_num=fail_num,
            visited_link_pool_size=len(visited_link_pool),
        )
        # -
        url_batch = []
        try:
            for i in range(batch_size):
                url = on_look_link_pool.pop()
                url_batch.append(url)
                visited_link_pool.add(url)
        except:
            pass

        # print(f"访问{url}")
        # 创建线程池
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # 使用线程池的map方法进行多线程
            soups = executor.map(utils.get_one_page, url_batch)


        for soup in soups:
            if (soup is None):
                fail_num += 1
                continue
            new_links = utils.get_links(root_url, soup, visited_link_pool)
            # print("链接数量：",len(new_links))
            [on_look_link_pool.add(link) for link in new_links]
            content, content_size = utils.get_content(soup)
            # print("content_size:",content_size)
            # -
            sum_text_num += content_size
            current_text_num += content_size
            current_text_lst.append(content)
            print(content)

            if (current_text_num > max_one_save_file):
                print("保存文件")
                with open(f"{save_path}/{file_counter}.txt", "w", encoding="utf-8") as f:
                    f.write("\n".join(current_text_lst))
                current_text_lst = []
                current_text_num = 0
                file_counter += 1

        sum_id += 1
        if (sum_id % save_state_step == 0):
            print("保存状态")
            with open(state_path, "wb") as f:
                state = [sum_text_num, current_text_num, file_counter, on_look_link_pool,
                         fail_num, visited_link_pool, sum_id, current_text_lst]
                pickle.dump(state, f)

    with open(state_path, "wb") as f:
        state = [sum_text_num, current_text_num, file_counter, on_look_link_pool,
                 fail_num, visited_link_pool, sum_id, current_text_lst]
        pickle.dump(state, f)
    print("over!")
