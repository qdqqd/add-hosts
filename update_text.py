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
    # 在每一行前面加上 "127.0.0.1 "
    lines = [f"127.0.0.1 {line}" for line in lines]
    return lines  # 返回列表而非字符串，以方便后续合并

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

    # 新增处理 anti-ad 的逻辑
    anti_ad_text = fetch_text("https://raw.githubusercontent.com/privacy-protection-tools/anti-AD/refs/heads/master/anti-ad-domains.txt")
    processed_anti_ad_lines = process_anti_ad_text(anti_ad_text)

    # 合并 githosts 和 anti-ad 的规则
    combined_rules = processed_githosts_text.splitlines() + processed_anti_ad_lines
    combined_rules = list(set(combined_rules))  # 去重
    final_output = '\n'.join(combined_rules)

    save_to_file('githosts', final_output)

if __name__ == "__main__":
    main()
