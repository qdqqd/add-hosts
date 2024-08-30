import requests
import re
from datetime import datetime
import pytz

# 网址列表
all_urls = [
    'https://raw.githubusercontent.com/lingeringsound/10007_auto/master/reward',
    'https://raw.githubusercontent.com/rentianyu/Ad-set-hosts/master/hosts',
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
    """从给定的 URL 获取文本内容"""
    response = requests.get(url)
    response.raise_for_status()  # 如果请求失败则抛出异常
    return response.text

def process_text(text):
    """处理文本内容"""
    lines = text.splitlines()
    # 删除以 # 开头的行
    lines = [line for line in lines if not line.strip().startswith('#')]
    # 使用正则表达式替换多个空格为一个空格
    lines = [re.sub(r'\s+', ' ', line) for line in lines]
    # 删除包含 'reward' 的域名
    lines = [line for line in lines if 'reward' not in line.lower()]
    # 删除重复行
    lines = list(set(lines))
    # 添加更新时间
    tz = pytz.timezone('Asia/Shanghai')
    now_local = datetime.now(tz)
    formatted_now = now_local.strftime('%Y-%m-%d %H:%M:%S')  # 格式化为北京时间
    lines.insert(0, f'# 作者：by柯乐\n# 主页：https://www.qdqqd.com/\n# githosts文件：github访问下载加速\n# addhosts文件：去除广告以及内置github加速\n# Updated on: {formatted_now}\n\n')
    return '\n'.join(lines)

def save_to_file(filename, content):
    """将内容保存到指定的文件"""
    with open(filename, 'w') as f:
        f.write(content)

def main():
    """主函数，获取和处理所有网址的文本内容"""
    # 更新 addhosts 文件
    all_text = ''
    for url in all_urls:
        all_text += fetch_text(url) + '\n'
    processed_text = process_text(all_text)
    save_to_file('addhosts', processed_text)
    
    # 更新 githosts 文件
    githosts_text = ''
    for url in githosts_urls:
        githosts_text += fetch_text(url) + '\n'
    processed_githosts_text = process_text(githosts_text)
    save_to_file('githosts', processed_githosts_text)

if __name__ == "__main__":
    main()
