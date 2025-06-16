import requests
import re
from datetime import datetime
import pytz

all_urls = [
    'https://raw.githubusercontent.com/lingeringsound/10007_auto/master/all',
  #  'https://gitlab.com/ineo6/hosts/-/raw/master/next-hosts',
 #   'https://raw.hellogithub.com/hosts',
#    'https://raw.githubusercontent.com/maxiaof/github-hosts/master/hosts'
]

tracker_urls = [
    'https://cdn.jsdelivr.net/gh/ngosang/trackerslist/trackers_all.txt',
    'https://cdn.jsdelivr.net/gh/DeSireFire/animeTrackerList/AT_all.txt',
    'https://newtrackon.com/api/all',
    'https://cf.trackerslist.com/all.txt',
    'https://raw.githubusercontent.com/adysec/tracker/refs/heads/main/trackers_best.txt',
    'https://trackers.run/s/rw_ws_up_hp_hs_v4_v6.txt',
]

custom_tracker_urls = [
    # 可以在此处添加更多自定义链接
]

anti_ad_url = 'https://anti-ad.net/domains.txt'

def fetch_text(url):
    response = requests.get(url)
    response.raise_for_status()  # 如果请求失败则抛出异常
    return response.text

def process_text(text):
    lines = text.splitlines()
    lines = [line for line in lines if not line.strip().startswith('#')]
    lines = [re.sub(r'\s+', ' ', line) for line in lines]
    lines = list(set(lines))
    tz = pytz.timezone('Asia/Shanghai')
    now_local = datetime.now(tz)
    formatted_now = now_local.strftime('%Y-%m-%d %H:%M:%S')
    lines.insert(0, f'# 作者：by柯乐\n# Updated on: {formatted_now}\n\n')
    return '\n'.join(lines)

def process_tracker_text(text):
    lines = text.splitlines()
    lines = [line.strip() for line in lines if line.strip() != '']  # 去掉只包含空白的行
    lines = list(set(lines))  # 去重
    return ','.join(lines)  # 用逗号连接所有的行

def process_anti_ad_text(text):
    lines = text.splitlines()
    # 移除注释行和空行
    lines = [line.strip() for line in lines if line.strip() and not line.startswith('#')]
    # 为每个域名添加 127.0.0.1 前缀
    lines = [f'127.0.0.1 {line}' for line in lines]
    return '\n'.join(lines)

def save_to_file(filename, content):
    with open(filename, 'w') as f:
        f.write(content)

def main():
    # 从所有 URL 获取内容并处理
    all_text = ''
    for url in all_urls:
        all_text += fetch_text(url) + '\n'
    
    # 处理 anti-ad 内容并添加到 all_text
    anti_ad_text = fetch_text(anti_ad_url)
    processed_anti_ad_text = process_anti_ad_text(anti_ad_text)
    all_text += '\n' + processed_anti_ad_text
    
    # 处理最终的 hosts 内容
    processed_text = process_text(all_text)
    # 替换所有 0.0.0.0 为 127.0.0.1
    processed_text = processed_text.replace('0.0.0.0', '127.0.0.1')
    save_to_file('addhosts.txt', processed_text)

    # 处理 Trackers 内容
    trackers_text = ''
    for url in tracker_urls:
        trackers_text += fetch_text(url) + '\n'
    
    processed_trackers_text = process_tracker_text(trackers_text)

    # 追加自定义的 Tracker 链接，并且也使用逗号分隔
    processed_trackers_text += ',' + ','.join(custom_tracker_urls) + ','  # 确保自定义的跟踪器也使用逗号分隔

    save_to_file('Trackers.txt', processed_trackers_text)

if __name__ == "__main__":
    main()
