const fs = require('fs');
const axios = require('axios');

// 定义要获取的链接
const githostsUrls = [
  'https://gitlab.com/ineo6/hosts/-/raw/master/next-hosts',
  'https://raw.githubusercontent.com/rentianyu/Ad-set-hosts/master/hosts',
  'https://pgl.yoyo.org/adservers/serverlist.php?hostformat=hosts&showintro=0&mimetype=plaintext'
];

const addhostsUrls = [
  'https://raw.githubusercontent.com/lingeringsound/10007_auto/master/all',
  'https://raw.githubusercontent.com/rentianyu/Ad-set-hosts/master/hosts',
  'https://pgl.yoyo.org/adservers/serverlist.php?hostformat=hosts&showintro=0&mimetype=plaintext',
  'https://gitlab.com/ineo6/hosts/-/raw/master/next-hosts',
  'https://raw.hellogithub.com/hosts',
  'https://raw.githubusercontent.com/maxiaof/github-hosts/master/hosts'
];

// 函数来获取数据并写入文件
async function fetchAndUpdateFile(urls, filePath) {
  try {
    let allData = '';
    for (const url of urls) {
      const response = await axios.get(url);
      allData += response.data + '\n'; // 将每个响应数据添加到最终数据中
    }
    fs.writeFileSync(filePath, allData); // 写入文件
    console.log(`Updated ${filePath} successfully.`);
  } catch (error) {
    console.error(`Error updating ${filePath}:`, error);
  }
}

// 更新 githosts 和 addhosts 文件
fetchAndUpdateFile(githostsUrls, 'githosts');
fetchAndUpdateFile(addhostsUrls, 'addhosts');

