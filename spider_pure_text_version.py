# https://www.discuss.com.hk/
import os.path
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
import utils_pure as utils
# from transformers import AutoTokenizer

if __name__ == "__main__":
    prefix_url = "https://www.discuss.com.hk/"
    root_url = 'https://www.discuss.com.hk/archiver/'

    visited_link_pool = set()
    on_look_link_pool = set()
    on_look_link_pool.add(root_url)
    # on_look_link_pool.add(candidate_url)
    tq = tqdm()
    sum_text_num = 0
    current_text_num = 0
    file_counter = 0
    max_one_save_file = 1e7
    save_path = "./pure_text_data"
    state_path = "./pure_checkpoint/"
    current_text_lst = []
    fail_num = 0
    save_state_step = 10
    sum_id = 0
    batch_size = 5000
    max_workers = 40


    # tokenizer = AutoTokenizer.from_pretrained("./tokenizer", trust_remote_code=True, use_fast=False)
    all_tokens = 0

    load_state_file_name = "state-2023-11-xxxx.pkl"
    state_full_name = os.path.join(state_path, load_state_file_name)
    if (os.path.exists(state_full_name)):
        print(f"加载{state_full_name}")
        sum_text_num, current_text_num, file_counter, on_look_link_pool, \
            fail_num, visited_link_pool, sum_id, current_text_lst, all_tokens = utils.load_state(state_full_name)

    while on_look_link_pool:
        if (sum_id % save_state_step == 0):
            if (os.path.exists(state_full_name)):
                sum_text_num, current_text_num, file_counter, on_look_link_pool, \
                    fail_num, visited_link_pool, sum_id, current_text_lst, all_tokens = utils.load_state(state_full_name)

        tq.update(1)
        tq.set_postfix(
            sum_char=sum_text_num,
            current_text=current_text_num,
            file_counter=file_counter,
            on_look_link_pool_size=len(on_look_link_pool),
            fail_num=fail_num,
            visited_link_pool_size=len(visited_link_pool),
            all_tokens = all_tokens
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
            soups = list(soups)

        for soup in soups:
            if (soup is None):
                fail_num += 1
                continue
            new_links = utils.get_links(prefix_url, soup, visited_link_pool)
            # print("链接数量：",len(new_links))
            [on_look_link_pool.add(link) for link in new_links]
            content, content_size = utils.get_content(soup)
            # print("content_size:",content_size)
            # -
            sum_text_num += content_size
            current_text_num += content_size

            # 处理非法字符
            content = content.encode('utf-8', errors="ignore")
            content = content.decode('utf-8', errors="ignore")
            # 统计token数量
            # all_tokens += len(tokenizer.encode(content))

            current_text_lst.append(content)
            # print(content)

            if (current_text_num > max_one_save_file):
                print("保存文件")
                try:
                    with open(f"{save_path}/{file_counter}.txt", "w", encoding="utf-8") as f:
                        f.write("\n".join(current_text_lst))
                except:
                    print(f"保存文件失败:{save_path}/{file_counter}.txt")

                current_text_lst = []
                current_text_num = 0
                file_counter += 1

        if (sum_id % save_state_step == 0):
            print("保存状态")
            state = [sum_text_num, current_text_num, file_counter, on_look_link_pool,
                     fail_num, visited_link_pool, sum_id, current_text_lst,all_tokens]
            state_full_name = utils.save_state(state, state_path)
        sum_id += 1

    state = [sum_text_num, current_text_num, file_counter, on_look_link_pool,
             fail_num, visited_link_pool, sum_id, current_text_lst,all_tokens]
    state_full_name = utils.save_state(state, state_path)
    print("over!")
