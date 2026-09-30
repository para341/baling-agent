// 字符串处理工具类
class StringUtils {
  // 去除字符串两端的空格
  static trim(str) {
    if (typeof str !== 'string') {
      throw new TypeError('str must be a string');
    }
    return str.trim();
  }

  // 去除字符串中的所有空格
  static removeAllSpaces(str) {
    if (typeof str !== 'string') {
      throw new TypeError('str must be a string');
    }
    return str.replace(/\s+/g, '');
  }

  // 去除字符串中的多余空格
  static removeExtraSpaces(str) {
    if (typeof str !== 'string') {
      throw new TypeError('str must be a string');
    }
    return str.replace(/\s+/g, ' ').trim();
  }

  // 将字符串转换为小写
  static toLowerCase(str) {
    if (typeof str !== 'string') {
      throw new TypeError('str must be a string');
    }
    return str.toLowerCase();
  }

  // 将字符串转换为大写
  static toUpperCase(str) {
    if (typeof str !== 'string') {
      throw new TypeError('str must be a string');
    }
    return str.toUpperCase();
  }

  // 将字符串的首字母转换为大写
  static capitalizeFirstLetter(str) {
    if (typeof str !== 'string') {
      throw new TypeError('str must be a string');
    }
    if (str.length === 0) {
      return str;
    }
    return str.charAt(0).toUpperCase() + str.slice(1);
  }

  // 将字符串的每个单词首字母转换为大写
  static capitalizeEachWord(str) {
    if (typeof str !== 'string') {
      throw new TypeError('str must be a string');
    }
    return str.replace(/\b\w/g, function(char) {
      return char.toUpperCase();
    });
  }

  // 反转字符串
  static reverse(str) {
    if (typeof str !== 'string') {
      throw new TypeError('str must be a string');
    }
    return str.split('').reverse().join('');
  }

  // 统计字符串中的字符数
  static countCharacters(str) {
    if (typeof str !== 'string') {
      throw new TypeError('str must be a string');
    }
    return str.length;
  }

  // 统计字符串中的单词数
  static countWords(str) {
    if (typeof str !== 'string') {
      throw new TypeError('str must be a string');
    }
    if (str.trim().length === 0) {
      return 0;
    }
    return str.trim().split(/\s+/).length;
  }

  // 统计字符串中的行数
  static countLines(str) {
    if (typeof str !== 'string') {
      throw new TypeError('str must be a string');
    }
    return str.split('\n').length;
  }

  // 判断字符串是否包含子字符串
  static contains(str, substring) {
    if (typeof str !== 'string' || typeof substring !== 'string') {
      throw new TypeError('str and substring must be strings');
    }
    return str.includes(substring);
  }

  // 判断字符串是否以子字符串开头
  static startsWith(str, substring) {
    if (typeof str !== 'string' || typeof substring !== 'string') {
      throw new TypeError('str and substring must be strings');
    }
    return str.startsWith(substring);
  }

  // 判断字符串是否以子字符串结尾
  static endsWith(str, substring) {
    if (typeof str !== 'string' || typeof substring !== 'string') {
      throw new TypeError('str and substring must be strings');
    }
    return str.endsWith(substring);
  }

  // 替换字符串中的子字符串
  static replace(str, oldSubstring, newSubstring) {
    if (typeof str !== 'string' || typeof oldSubstring !== 'string' || typeof newSubstring !== 'string') {
      throw new TypeError('str, oldSubstring, and newSubstring must be strings');
    }
    return str.replace(oldSubstring, newSubstring);
  }

  // 替换字符串中的所有子字符串
  static replaceAll(str, oldSubstring, newSubstring) {
    if (typeof str !== 'string' || typeof oldSubstring !== 'string' || typeof newSubstring !== 'string') {
      throw new TypeError('str, oldSubstring, and newSubstring must be strings');
    }
    return str.replace(new RegExp(oldSubstring, 'g'), newSubstring);
  }

  // 分割字符串
  static split(str, delimiter) {
    if (typeof str !== 'string' || typeof delimiter !== 'string') {
      throw new TypeError('str and delimiter must be strings');
    }
    return str.split(delimiter);
  }

  // 连接字符串
  static join(parts, delimiter) {
    if (!Array.isArray(parts) || typeof delimiter !== 'string') {
      throw new TypeError('parts must be an array and delimiter must be a string');
    }
    return parts.join(delimiter);
  }

  // 填充字符串左侧
  static padLeft(str, length, padCharacter) {
    if (typeof str !== 'string' || typeof length !== 'number' || typeof padCharacter !== 'string') {
      throw new TypeError('str must be a string, length must be a number, and padCharacter must be a string');
    }
    return str.padStart(length, padCharacter);
  }

  // 填充字符串右侧
  static padRight(str, length, padCharacter) {
    if (typeof str !== 'string' || typeof length !== 'number' || typeof padCharacter !== 'string') {
      throw new TypeError('str must be a string, length must be a number, and padCharacter must be a string');
    }
    return str.padEnd(length, padCharacter);
  }

  // 截断字符串
  static truncate(str, length, suffix) {
    if (typeof str !== 'string' || typeof length !== 'number' || typeof suffix !== 'string') {
      throw new TypeError('str must be a string, length must be a number, and suffix must be a string');
    }
    if (str.length <= length) {
      return str;
    }
    return str.substring(0, length) + suffix;
  }

  // 包裹字符串
  static wrap(str, wrapper) {
    if (typeof str !== 'string' || typeof wrapper !== 'string') {
      throw new TypeError('str and wrapper must be strings');
    }
    return wrapper + str + wrapper;
  }

  // 重复字符串
  static repeat(str, times) {
    if (typeof str !== 'string' || typeof times !== 'number') {
      throw new TypeError('str must be a string and times must be a number');
    }
    return str.repeat(times);
  }

  // 随机打乱字符串
  static shuffle(str) {
    if (typeof str !== 'string') {
      throw new TypeError('str must be a string');
    }
    const array = str.split('');
    for (let i = array.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [array[i], array[j]] = [array[j], array[i]];
    }
    return array.join('');
  }

  // 去除字符串中的HTML标签
  static removeHtmlTags(str) {
    if (typeof str !== 'string') {
      throw new TypeError('str must be a string');
    }
    return str.replace(/<[^>]*>/g, '');
  }

  // 去除字符串中的特殊字符
  static removeSpecialCharacters(str) {
    if (typeof str !== 'string') {
      throw new TypeError('str must be a string');
    }
    return str.replace(/[^\w\s]/gi, '');
  }

  // 去除字符串中的数字
  static removeNumbers(str) {
    if (typeof str !== 'string') {
      throw new TypeError('str must be a string');
    }
    return str.replace(/\d+/g, '');
  }

  // 去除字符串中的字母
  static removeLetters(str) {
    if (typeof str !== 'string') {
      throw new TypeError('str must be a string');
    }
    return str.replace(/[a-zA-Z]+/g, '');
  }

  // 去除字符串中的汉字
  static removeChineseCharacters(str) {
    if (typeof str !== 'string') {
      throw new TypeError('str must be a string');
    }
    return str.replace(/[\u4e00-\u9fa5]/g, '');
  }

  // 提取字符串中的数字
  static extractNumbers(str) {
    if (typeof str !== 'string') {
      throw new TypeError('str must be a string');
    }
    const matches = str.match(/\d+/g);
    return matches ? matches.join('') : '';
  }

  // 提取字符串中的字母
  static extractLetters(str) {
    if (typeof str !== 'string') {
      throw new TypeError('str must be a string');
    }
    const matches = str.match(/[a-zA-Z]+/g);
    return matches ? matches.join('') : '';
  }

  // 提取字符串中的汉字
  static extractChineseCharacters(str) {
    if (typeof str !== 'string') {
      throw new TypeError('str must be a string');
    }
    const matches = str.match(/[\u4e00-\u9fa5]+/g);
    return matches ? matches.join('') : '';
  }

  // 提取字符串中的邮箱地址
  static extractEmailAddresses(str) {
    if (typeof str !== 'string') {
      throw new TypeError('str must be a string');
    }
    const matches = str.match(/[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}/g);
    return matches ? matches : [];
  }

  // 提取字符串中的URL地址
  static extractUrls(str) {
    if (typeof str !== 'string') {
      throw new TypeError('str must be a string');
    }
    const matches = str.match(/https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)/g);
    return matches ? matches : [];
  }

  // 提取字符串中的手机号码
  static extractPhoneNumbers(str) {
    if (typeof str !== 'string') {
      throw new TypeError('str must be a string');
    }
    const matches = str.match(/1[3-9]\d{9}/g);
    return matches ? matches : [];
  }

  // 提取字符串中的身份证号码
  static extractIdCardNumbers(str) {
    if (typeof str !== 'string') {
      throw new TypeError('str must be a string');
    }
    const matches = str.match(/\d{17}([0-9]|X|x)/g);
    return matches ? matches : [];
  }

  // 判断字符串是否为邮箱地址
  static isEmail(str) {
    if (typeof str !== 'string') {
      throw new TypeError('str must be a string');
    }
    const emailRegex = /[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}/;
    return emailRegex.test(str);
  }

  // 判断字符串是否为URL地址
  static isUrl(str) {
    if (typeof str !== 'string') {
      throw new TypeError('str must be a string');
    }
    const urlRegex = /https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)/;
    return urlRegex.test(str);
  }

  // 判断字符串是否为手机号码
  static isPhoneNumber(str) {
    if (typeof str !== 'string') {
      throw new TypeError('str must be a string');
    }
    const phoneRegex = /1[3-9]\d{9}/;
    return phoneRegex.test(str);
  }

  // 判断字符串是否为身份证号码
  static isIdCardNumber(str) {
    if (typeof str !== 'string') {
      throw new TypeError('str must be a string');
    }
    const idCardRegex = /\d{17}([0-9]|X|x)/;
    return idCardRegex.test(str);
  }

  // 判断字符串是否为数字
  static isNumber(str) {
    if (typeof str !== 'string') {
      throw new TypeError('str must be a string');
    }
    const numberRegex = /^\d+$/;
    return numberRegex.test(str);
  }

  // 判断字符串是否为字母
  static isLetter(str) {
    if (typeof str !== 'string') {
      throw new TypeError('str must be a string');
    }
    const letterRegex = /^[a-zA-Z]+$/;
    return letterRegex.test(str);
  }

  // 判断字符串是否为汉字
  static isChineseCharacter(str) {
    if (typeof str !== 'string') {
      throw new TypeError('str must be a string');
    }
    const chineseRegex = /^[\u4e00-\u9fa5]+$/;
    return chineseRegex.test(str);
  }

  // 判断字符串是否为空
  static isEmpty(str) {
    if (typeof str !== 'string') {
      throw new TypeError('str must be a string');
    }
    return str.trim().length === 0;
  }

  // 判断字符串是否为空白
  static isBlank(str) {
    if (typeof str !== 'string') {
      throw new TypeError('str must be a string');
    }
    return str.length === 0;
  }

  // 判断字符串是否为JSON格式
  static isJson(str) {
    if (typeof str !== 'string') {
      throw new TypeError('str must be a string');
    }
    try {
      JSON.parse(str);
      return true;
    } catch (error) {
      return false;
    }
  }

  // 判断字符串是否为XML格式
  static isXml(str) {
    if (typeof str !== 'string') {
      throw new TypeError('str must be a string');
    }
    const xmlRegex = /^<[^>]+>/;
    return xmlRegex.test(str);
  }

  // 判断字符串是否为HTML格式
  static isHtml(str) {
    if (typeof str !== 'string') {
      throw new TypeError('str must be a string');
    }
    const htmlRegex = /<[^>]+>/;
    return htmlRegex.test(str);
  }

  // 判断字符串是否为Markdown格式
  static isMarkdown(str) {
    if (typeof str !== 'string') {
      throw new TypeError('str must be a string');
    }
    const markdownRegex = /(#|\*|\_|\[|\]|\(|\)|`|~)/;
    return markdownRegex.test(str);
  }

  // 判断字符串是否为YAML格式
  static isYaml(str) {
    if (typeof str !== 'string') {
      throw new TypeError('str must be a string');
    }
    const yamlRegex = /^\s*[a-zA-Z0-9_]+:/;
    return yamlRegex.test(str);
  }

  // 判断字符串是否为INI格式
  static isIni(str) {
    if (typeof str !== 'string') {
      throw new TypeError('str must be a string');
    }
    const iniRegex = /^\s*\[.*\]\s*$/;
    return iniRegex.test(str);
  }

  // 判断字符串是否为CSV格式
  static isCsv(str) {
    if (typeof str !== 'string') {
      throw new TypeError('str must be a string');
    }
    const csvRegex = /^([^,]+,)*[^,]+$/;
    return csvRegex.test(str);
  }

  // 判断字符串是否为TSV格式
  static isTsv(str) {
    if (typeof str !== 'string') {
      throw new TypeError('str must be a string');
    }
    const tsvRegex = /^([^\t]+\t)*[^\t]+$/;
    return tsvRegex.test(str);
  }

  // 判断字符串是否为JSON5格式
  static isJson5(str) {
    if (typeof str !== 'string') {
      throw new TypeError('str must be a string');
    }
    try {
      // JSON5 is a superset of JSON, so we can use JSON.parse
      JSON.parse(str);
      return true;
    } catch (error) {
      return false;
    }
  }

  // 判断字符串是否为JSON Lines格式
  static isJsonLines(str) {
    if (typeof str !== 'string') {
      throw new TypeError('str must be a string');
    }
    const lines = str.split('\n');
    for (const line of lines) {
      if (line.trim().length === 0) {
        continue;
      }
      try {
        JSON.parse(line);
      } catch (error) {
        return false;
      }
    }
    return true;
  }

  // 判断字符串是否为XML Lines格式
  static isXmlLines(str) {
    if (typeof str !== 'string') {
      throw new TypeError('str must be a string');
    }
    const lines = str.split('\n');
    for (const line of lines) {
      if (line.trim().length === 0) {
        continue;
      }
      const xmlRegex = /^<[^>]+>$/;
      if (!xmlRegex.test(line)) {
        return false;
      }
    }
    return true;
  }

  // 判断字符串是否为HTML Lines格式
  static isHtmlLines(str) {
    if (typeof str !== 'string') {
      throw new TypeError('str must be a string');
    }
    const lines = str.split('\n');
    for (const line of lines) {
      if (line.trim().length === 0) {
        continue;
      }
      const htmlRegex = /^<[^>]+>$/;
      if (!htmlRegex.test(line)) {
        return false;
      }
    }
    return true;
  }

  // 判断字符串是否为Markdown Lines格式
  static isMarkdownLines(str) {
    if (typeof str !== 'string') {
      throw new TypeError('str must be a string');
    }
    const lines = str.split('\n');
    for (const line of lines) {
      if (line.trim().length === 0) {
        continue;
      }
      const markdownRegex = /^(#|\*|\_|\[|\]|\(|\)|`|~)/;
      if (!markdownRegex.test(line)) {
        return false;
      }
    }
    return true;
  }

  // 判断字符串是否为YAML Lines格式
  static isYamlLines(str) {
    if (typeof str !== 'string') {
      throw new TypeError('str must be a string');
    }
    const lines = str.split('\n');
    for (const line of lines) {
      if (line.trim().length === 0) {
        continue;
      }
      const yamlRegex = /^\s*[a-zA-Z0-9_]+:/;
      if (!yamlRegex.test(line)) {
        return false;
      }
    }
    return true;
  }

  // 判断字符串是否为INI Lines格式
  static isIniLines(str) {
    if (typeof str !== 'string') {
      throw new TypeError('str must be a string');
    }
    const lines = str.split('\n');
    for (const line of lines) {
      if (line.trim().length === 0) {
        continue;
      }
      const iniRegex = /^\s*\[.*\]\s*$/;
      if (!iniRegex.test(line)) {
        return false;
      }
    }
    return true;
  }

  // 判断字符串是否为CSV Lines格式
  static isCsvLines(str) {
    if (typeof str !== 'string') {
      throw new TypeError('str must be a string');
    }
    const lines = str.split('\n');
    for (const line of lines) {
      if (line.trim().length === 0) {
        continue;
      }
      const csvRegex = /^([^,]+,)*[^,]+$/;
      if (!csvRegex.test(line)) {
        return false;
      }
    }
    return true;
  }

  // 判断字符串是否为TSV Lines格式
  static isTsvLines(str) {
    if (typeof str !== 'string') {
      throw new TypeError('str must be a string');
    }
    const lines = str.split('\n');
    for (const line of lines) {
      if (line.trim().length === 0) {
        continue;
      }
      const tsvRegex = /^([^\t]+\t)*[^\t]+$/;
      if (!tsvRegex.test(line)) {
        return false;
      }
    }
    return true;
  }
}

export default StringUtils;