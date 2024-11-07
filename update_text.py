import requests
import re
from datetime import datetime
import pytz

all_urls = [
    'https://raw.githubusercontent.com/lingeringsound/10007_auto/master/all',
    'https://pgl.yoyo.org/adservers/serverlist.php?hostformat=hosts&showintro=0&mimetype=plaintext',
    'https://gitlab.com/ineo6/hosts/-/raw/master/next-hosts',
    'https://raw.hellogithub.com/hosts',
    'https://raw.githubusercontent.com/maxiaof/github-hosts/master/hosts'
]

githosts_urls = [
    'https://gitlab.com/ineo6/hosts/-/raw/master/next-hosts',
    'https://raw.hellogithub.com/hosts',
    'https://raw.githubusercontent.com/maxiaof/github-hosts/master/hosts'
]

tracker_urls = [
    'https://cdn.jsdelivr.net/gh/ngosang/trackerslist/trackers_all.txt',
    'https://trackerslist.com/all.txt',
    'https://cdn.jsdelivr.net/gh/DeSireFire/animeTrackerList/AT_all.txt',
    'https://newtrackon.com/api/all',
    'https://cf.trackerslist.com/all.txt',
    'https://raw.githubusercontent.com/adysec/tracker/refs/heads/main/trackers_best.txt',
    'https://trackers.run/s/rw_ws_up_hp_hs_v4_v6.txt',
    
]

custom_tracker_urls = [
    'http://open.acgtracker.com:1096/announce',
    'http://another.tracker.url:8080/announce'
    # 可以在此处添加更多自定义链接
]

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

def process_anti_ad_text(text):
    lines = text.splitlines()
    lines = [f"127.0.0.1 {line}" for line in lines]
    return lines

def process_tracker_text(text):
    lines = text.splitlines()
    lines = [line.strip() for line in lines if line.strip()]  # 去掉空行
    lines = list(set(lines))  # 去重
    return '\n'.join(lines)

def save_to_file(filename, content):
    with open(filename, 'w') as f:
        f.write(content)

def main():
    all_text = ''
    for url in all_urls:
        all_text += fetch_text(url) + '\n'
        
    processed_text = process_text(all_text)
    save_to_file('addhosts', processed_text)

    githosts_text = ''
    for url in githosts_urls:
        githosts_text += fetch_text(url) + '\n'
    
    processed_githosts_text = process_text(githosts_text)

    anti_ad_text = fetch_text("https://raw.githubusercontent.com/privacy-protection-tools/anti-AD/refs/heads/master/anti-ad-domains.txt")
    processed_anti_ad_lines = process_anti_ad_text(anti_ad_text)

    combined_rules = processed_githosts_text.splitlines() + processed_anti_ad_lines
    combined_rules = list(set(combined_rules))
    final_output = '\n'.join(combined_rules)

    save_to_file('githosts', final_output)

    # 处理 Trackers 的内容
    trackers_text = ''
    for url in tracker_urls:
        trackers_text += fetch_text(url) + '\n'
    
    processed_trackers_text = process_tracker_text(trackers_text)

    # 在 processed_trackers_text 底部加上自定义的链接
    processed_trackers_text += '\n' + '\n'.join(custom_tracker_urls) + '\n'

    save_to_file('Trackers.txt', processed_trackers_text)

if __name__ == "__main__":
    main()
