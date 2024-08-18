const fs = require('fs');
const axios = require('axios');

// 定义要获取的链接
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

    // 处理数据
    let processedData = processTextData(allData);

    // 添加更新时间和作者信息
    const now = new Date();
    const header = `# Updated on: ${now.toISOString()}\n# Author: by 柯乐\n# Homepage: https://www.qdqqd.com\n# https://raw.githubusercontent.com/qdqqd/add-hosts/main/addhosts\n# 用于去除各种广告\n\n`;
    processedData = header + processedData;

    // 写入处理后的数据
    fs.writeFileSync(filePath, processedData);
    console.log(`Updated ${filePath} successfully.`);
  } catch (error) {
    console.error(`Error updating ${filePath}:`, error);
  }
}

// 函数来处理文本数据
function processTextData(text) {
  // 删除以 # 开头的行
  let lines = text.split('\n').filter(line => !line.trim().startsWith('#'));

  // 将所有的长空格替换成一个空格
  lines = lines.map(line => line.replace(/\s+/g, ' '));

  // 删除重复的文本行
  let uniqueLines = Array.from(new Set(lines));

  return uniqueLines.join('\n');
}

fetchAndUpdateFile(addhostsUrls, 'addhosts');
