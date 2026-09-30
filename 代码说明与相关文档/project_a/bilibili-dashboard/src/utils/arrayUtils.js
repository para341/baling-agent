// 数组处理工具类
class ArrayUtils {
  // 判断数组是否为空
  static isEmpty(array) {
    if (!Array.isArray(array)) {
      throw new TypeError('array must be an array');
    }
    return array.length === 0;
  }

  // 判断数组是否包含指定元素
  static contains(array, element) {
    if (!Array.isArray(array)) {
      throw new TypeError('array must be an array');
    }
    return array.includes(element);
  }

  // 判断数组是否包含所有指定元素
  static containsAll(array, elements) {
    if (!Array.isArray(array) || !Array.isArray(elements)) {
      throw new TypeError('array and elements must be arrays');
    }
    return elements.every(element => array.includes(element));
  }

  // 判断数组是否包含任何一个指定元素
  static containsAny(array, elements) {
    if (!Array.isArray(array) || !Array.isArray(elements)) {
      throw new TypeError('array and elements must be arrays');
    }
    return elements.some(element => array.includes(element));
  }

  // 获取数组的长度
  static length(array) {
    if (!Array.isArray(array)) {
      throw new TypeError('array must be an array');
    }
    return array.length;
  }

  // 获取数组的第一个元素
  static first(array) {
    if (!Array.isArray(array)) {
      throw new TypeError('array must be an array');
    }
    if (array.length === 0) {
      return undefined;
    }
    return array[0];
  }

  // 获取数组的最后一个元素
  static last(array) {
    if (!Array.isArray(array)) {
      throw new TypeError('array must be an array');
    }
    if (array.length === 0) {
      return undefined;
    }
    return array[array.length - 1];
  }

  // 获取数组的指定位置元素
  static get(array, index) {
    if (!Array.isArray(array) || typeof index !== 'number') {
      throw new TypeError('array must be an array and index must be a number');
    }
    if (index < 0 || index >= array.length) {
      return undefined;
    }
    return array[index];
  }

  // 设置数组的指定位置元素
  static set(array, index, element) {
    if (!Array.isArray(array) || typeof index !== 'number') {
      throw new TypeError('array must be an array and index must be a number');
    }
    if (index < 0 || index >= array.length) {
      throw new RangeError('index out of bounds');
    }
    array[index] = element;
    return array;
  }

  // 向数组末尾添加元素
  static push(array, element) {
    if (!Array.isArray(array)) {
      throw new TypeError('array must be an array');
    }
    array.push(element);
    return array;
  }

  // 向数组开头添加元素
  static unshift(array, element) {
    if (!Array.isArray(array)) {
      throw new TypeError('array must be an array');
    }
    array.unshift(element);
    return array;
  }

  // 从数组末尾移除元素
  static pop(array) {
    if (!Array.isArray(array)) {
      throw new TypeError('array must be an array');
    }
    return array.pop();
  }

  // 从数组开头移除元素
  static shift(array) {
    if (!Array.isArray(array)) {
      throw new TypeError('array must be an array');
    }
    return array.shift();
  }

  // 移除数组的指定位置元素
  static remove(array, index) {
    if (!Array.isArray(array) || typeof index !== 'number') {
      throw new TypeError('array must be an array and index must be a number');
    }
    if (index < 0 || index >= array.length) {
      throw new RangeError('index out of bounds');
    }
    return array.splice(index, 1)[0];
  }

  // 移除数组的指定元素
  static removeElement(array, element) {
    if (!Array.isArray(array)) {
      throw new TypeError('array must be an array');
    }
    const index = array.indexOf(element);
    if (index === -1) {
      return undefined;
    }
    return array.splice(index, 1)[0];
  }

  // 移除数组的所有指定元素
  static removeAllElements(array, element) {
    if (!Array.isArray(array)) {
      throw new TypeError('array must be an array');
    }
    const removedElements = [];
    for (let i = array.length - 1; i >= 0; i--) {
      if (array[i] === element) {
        removedElements.push(array.splice(i, 1)[0]);
      }
    }
    return removedElements;
  }

  // 清空数组
  static clear(array) {
    if (!Array.isArray(array)) {
      throw new TypeError('array must be an array');
    }
    array.length = 0;
    return array;
  }

  // 复制数组
  static copy(array) {
    if (!Array.isArray(array)) {
      throw new TypeError('array must be an array');
    }
    return [...array];
  }

  // 浅复制数组
  static shallowCopy(array) {
    if (!Array.isArray(array)) {
      throw new TypeError('array must be an array');
    }
    return array.slice();
  }

  // 深复制数组
  static deepCopy(array) {
    if (!Array.isArray(array)) {
      throw new TypeError('array must be an array');
    }
    return JSON.parse(JSON.stringify(array));
  }

  // 合并数组
  static merge(array1, array2) {
    if (!Array.isArray(array1) || !Array.isArray(array2)) {
      throw new TypeError('array1 and array2 must be arrays');
    }
    return [...array1, ...array2];
  }

  // 合并多个数组
  static mergeAll(...arrays) {
    for (const array of arrays) {
      if (!Array.isArray(array)) {
        throw new TypeError('all arguments must be arrays');
      }
    }
    return arrays.reduce((merged, array) => [...merged, ...array], []);
  }

  // 拼接数组
  static concat(array1, array2) {
    if (!Array.isArray(array1) || !Array.isArray(array2)) {
      throw new TypeError('array1 and array2 must be arrays');
    }
    return array1.concat(array2);
  }

  // 拼接多个数组
  static concatAll(...arrays) {
    for (const array of arrays) {
      if (!Array.isArray(array)) {
        throw new TypeError('all arguments must be arrays');
      }
    }
    return arrays.reduce((concatenated, array) => concatenated.concat(array), []);
  }

  // 截取数组
  static slice(array, start, end) {
    if (!Array.isArray(array) || typeof start !== 'number' || typeof end !== 'number') {
      throw new TypeError('array must be an array and start and end must be numbers');
    }
    if (start < 0 || start >= array.length || end < 0 || end > array.length || start >= end) {
      throw new RangeError('start and end must be within the bounds of the array and start must be less than end');
    }
    return array.slice(start, end);
  }

  // 截取数组的前n个元素
  static take(array, n) {
    if (!Array.isArray(array) || typeof n !== 'number') {
      throw new TypeError('array must be an array and n must be a number');
    }
    if (n < 0 || n > array.length) {
      throw new RangeError('n must be within the bounds of the array');
    }
    return array.slice(0, n);
  }

  // 截取数组的后n个元素
  static takeRight(array, n) {
    if (!Array.isArray(array) || typeof n !== 'number') {
      throw new TypeError('array must be an array and n must be a number');
    }
    if (n < 0 || n > array.length) {
      throw new RangeError('n must be within the bounds of the array');
    }
    return array.slice(array.length - n);
  }

  // 跳过数组的前n个元素
  static skip(array, n) {
    if (!Array.isArray(array) || typeof n !== 'number') {
      throw new TypeError('array must be an array and n must be a number');
    }
    if (n < 0 || n > array.length) {
      throw new RangeError('n must be within the bounds of the array');
    }
    return array.slice(n);
  }

  // 跳过数组的后n个元素
  static skipRight(array, n) {
    if (!Array.isArray(array) || typeof n !== 'number') {
      throw new TypeError('array must be an array and n must be a number');
    }
    if (n < 0 || n > array.length) {
      throw new RangeError('n must be within the bounds of the array');
    }
    return array.slice(0, array.length - n);
  }

  // 反转数组
  static reverse(array) {
    if (!Array.isArray(array)) {
      throw new TypeError('array must be an array');
    }
    return array.reverse();
  }

  // 排序数组
  static sort(array, comparator) {
    if (!Array.isArray(array)) {
      throw new TypeError('array must be an array');
    }
    if (comparator && typeof comparator !== 'function') {
      throw new TypeError('comparator must be a function');
    }
    return array.sort(comparator);
  }

  // 随机打乱数组
  static shuffle(array) {
    if (!Array.isArray(array)) {
      throw new TypeError('array must be an array');
    }
    const shuffledArray = [...array];
    for (let i = shuffledArray.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [shuffledArray[i], shuffledArray[j]] = [shuffledArray[j], shuffledArray[i]];
    }
    return shuffledArray;
  }

  // 去重数组
  static unique(array) {
    if (!Array.isArray(array)) {
      throw new TypeError('array must be an array');
    }
    return [...new Set(array)];
  }

  // 去重数组（根据指定属性）
  static uniqueBy(array, property) {
    if (!Array.isArray(array) || typeof property !== 'string') {
      throw new TypeError('array must be an array and property must be a string');
    }
    const seen = new Set();
    return array.filter(item => {
      const value = item[property];
      if (seen.has(value)) {
        return false;
      }
      seen.add(value);
      return true;
    });
  }

  // 去重数组（根据指定函数）
  static uniqueByFunction(array, func) {
    if (!Array.isArray(array) || typeof func !== 'function') {
      throw new TypeError('array must be an array and func must be a function');
    }
    const seen = new Set();
    return array.filter(item => {
      const value = func(item);
      if (seen.has(value)) {
        return false;
      }
      seen.add(value);
      return true;
    });
  }

  // 过滤数组
  static filter(array, predicate) {
    if (!Array.isArray(array) || typeof predicate !== 'function') {
      throw new TypeError('array must be an array and predicate must be a function');
    }
    return array.filter(predicate);
  }

  // 映射数组
  static map(array, mapper) {
    if (!Array.isArray(array) || typeof mapper !== 'function') {
      throw new TypeError('array must be an array and mapper must be a function');
    }
    return array.map(mapper);
  }

  // 归约数组
  static reduce(array, reducer, initialValue) {
    if (!Array.isArray(array) || typeof reducer !== 'function') {
      throw new TypeError('array must be an array and reducer must be a function');
    }
    return array.reduce(reducer, initialValue);
  }

  // 遍历数组
  static forEach(array, iterator) {
    if (!Array.isArray(array) || typeof iterator !== 'function') {
      throw new TypeError('array must be an array and iterator must be a function');
    }
    array.forEach(iterator);
    return array;
  }

  // 查找数组的第一个匹配元素
  static find(array, predicate) {
    if (!Array.isArray(array) || typeof predicate !== 'function') {
      throw new TypeError('array must be an array and predicate must be a function');
    }
    return array.find(predicate);
  }

  // 查找数组的第一个匹配元素的索引
  static findIndex(array, predicate) {
    if (!Array.isArray(array) || typeof predicate !== 'function') {
      throw new TypeError('array must be an array and predicate must be a function');
    }
    return array.findIndex(predicate);
  }

  // 查找数组的最后一个匹配元素
  static findLast(array, predicate) {
    if (!Array.isArray(array) || typeof predicate !== 'function') {
      throw new TypeError('array must be an array and predicate must be a function');
    }
    for (let i = array.length - 1; i >= 0; i--) {
      if (predicate(array[i], i, array)) {
        return array[i];
      }
    }
    return undefined;
  }

  // 查找数组的最后一个匹配元素的索引
  static findLastIndex(array, predicate) {
    if (!Array.isArray(array) || typeof predicate !== 'function') {
      throw new TypeError('array must be an array and predicate must be a function');
    }
    for (let i = array.length - 1; i >= 0; i--) {
      if (predicate(array[i], i, array)) {
        return i;
      }
    }
    return -1;
  }

  // 检查数组的所有元素是否匹配指定条件
  static every(array, predicate) {
    if (!Array.isArray(array) || typeof predicate !== 'function') {
      throw new TypeError('array must be an array and predicate must be a function');
    }
    return array.every(predicate);
  }

  // 检查数组的任何元素是否匹配指定条件
  static some(array, predicate) {
    if (!Array.isArray(array) || typeof predicate !== 'function') {
      throw new TypeError('array must be an array and predicate must be a function');
    }
    return array.some(predicate);
  }

  // 统计数组的元素个数
  static count(array, predicate) {
    if (!Array.isArray(array) || typeof predicate !== 'function') {
      throw new TypeError('array must be an array and predicate must be a function');
    }
    return array.filter(predicate).length;
  }

  // 统计数组的元素个数（根据指定值）
  static countByValue(array, value) {
    if (!Array.isArray(array)) {
      throw new TypeError('array must be an array');
    }
    return array.filter(item => item === value).length;
  }

  // 统计数组的元素个数（根据指定属性）
  static countByProperty(array, property, value) {
    if (!Array.isArray(array) || typeof property !== 'string') {
      throw new TypeError('array must be an array and property must be a string');
    }
    return array.filter(item => item[property] === value).length;
  }

  // 统计数组的元素个数（根据指定函数）
  static countByFunction(array, func) {
    if (!Array.isArray(array) || typeof func !== 'function') {
      throw new TypeError('array must be an array and func must be a function');
    }
    return array.filter(func).length;
  }

  // 分组数组（根据指定属性）
  static groupBy(array, property) {
    if (!Array.isArray(array) || typeof property !== 'string') {
      throw new TypeError('array must be an array and property must be a string');
    }
    return array.reduce((groups, item) => {
      const key = item[property];
      if (!groups[key]) {
        groups[key] = [];
      }
      groups[key].push(item);
      return groups;
    }, {});
  }

  // 分组数组（根据指定函数）
  static groupByFunction(array, func) {
    if (!Array.isArray(array) || typeof func !== 'function') {
      throw new TypeError('array must be an array and func must be a function');
    }
    return array.reduce((groups, item) => {
      const key = func(item);
      if (!groups[key]) {
        groups[key] = [];
      }
      groups[key].push(item);
      return groups;
    }, {});
  }

  // 分区数组（根据指定条件）
  static partition(array, predicate) {
    if (!Array.isArray(array) || typeof predicate !== 'function') {
      throw new TypeError('array must be an array and predicate must be a function');
    }
    return array.reduce((partitions, item) => {
      if (predicate(item)) {
        partitions[0].push(item);
      } else {
        partitions[1].push(item);
      }
      return partitions;
    }, [[], []]);
  }

  // 扁平化数组
  static flatten(array) {
    if (!Array.isArray(array)) {
      throw new TypeError('array must be an array');
    }
    return array.flat();
  }

  // 深度扁平化数组
  static flattenDeep(array) {
    if (!Array.isArray(array)) {
      throw new TypeError('array must be an array');
    }
    return array.flat(Infinity);
  }

  // 扁平化数组（指定深度）
  static flattenDepth(array, depth) {
    if (!Array.isArray(array) || typeof depth !== 'number') {
      throw new TypeError('array must be an array and depth must be a number');
    }
    return array.flat(depth);
  }

  // 转换数组为对象
  static toObject(array, keyProperty, valueProperty) {
    if (!Array.isArray(array) || typeof keyProperty !== 'string' || typeof valueProperty !== 'string') {
      throw new TypeError('array must be an array and keyProperty and valueProperty must be strings');
    }
    return array.reduce((object, item) => {
      const key = item[keyProperty];
      const value = item[valueProperty];
      object[key] = value;
      return object;
    }, {});
  }

  // 转换数组为Map
  static toMap(array, keyProperty, valueProperty) {
    if (!Array.isArray(array) || typeof keyProperty !== 'string' || typeof valueProperty !== 'string') {
      throw new TypeError('array must be an array and keyProperty and valueProperty must be strings');
    }
    return array.reduce((map, item) => {
      const key = item[keyProperty];
      const value = item[valueProperty];
      map.set(key, value);
      return map;
    }, new Map());
  }

  // 转换数组为Set
  static toSet(array) {
    if (!Array.isArray(array)) {
      throw new TypeError('array must be an array');
    }
    return new Set(array);
  }

  // 转换数组为字符串
  static toString(array, separator) {
    if (!Array.isArray(array) || typeof separator !== 'string') {
      throw new TypeError('array must be an array and separator must be a string');
    }
    return array.join(separator);
  }

  // 转换数组为JSON字符串
  static toJson(array) {
    if (!Array.isArray(array)) {
      throw new TypeError('array must be an array');
    }
    return JSON.stringify(array);
  }

  // 转换数组为CSV字符串
  static toCsv(array, separator) {
    if (!Array.isArray(array) || typeof separator !== 'string') {
      throw new TypeError('array must be an array and separator must be a string');
    }
    return array.map(item => item.join(separator)).join('\n');
  }

  // 转换数组为TSV字符串
  static toTsv(array) {
    if (!Array.isArray(array)) {
      throw new TypeError('array must be an array');
    }
    return array.map(item => item.join('\t')).join('\n');
  }

  // 转换数组为XML字符串
  static toXml(array, rootElement, itemElement) {
    if (!Array.isArray(array) || typeof rootElement !== 'string' || typeof itemElement !== 'string') {
      throw new TypeError('array must be an array and rootElement and itemElement must be strings');
    }
    const xmlItems = array.map(item => `<${itemElement}>${item}</${itemElement}>`).join('\n');
    return `<${rootElement}>\n${xmlItems}\n</${rootElement}>`;
  }

  // 转换数组为HTML列表
  static toHtmlList(array, listType) {
    if (!Array.isArray(array) || typeof listType !== 'string') {
      throw new TypeError('array must be an array and listType must be a string');
    }
    if (listType !== 'ul' && listType !== 'ol') {
      throw new Error('listType must be either "ul" or "ol"');
    }
    const listItems = array.map(item => `<li>${item}</li>`).join('\n');
    return `<${listType}>\n${listItems}\n</${listType}>`;
  }

  // 转换数组为HTML表格
  static toHtmlTable(array) {
    if (!Array.isArray(array)) {
      throw new TypeError('array must be an array');
    }
    const tableRows = array.map(row => `<tr>${row.map(cell => `<td>${cell}</td>`).join('')}</tr>`).join('\n');
    return `<table>\n${tableRows}\n</table>`;
  }

  // 转换数组为Markdown列表
  static toMarkdownList(array, ordered) {
    if (!Array.isArray(array) || typeof ordered !== 'boolean') {
      throw new TypeError('array must be an array and ordered must be a boolean');
    }
    if (ordered) {
      return array.map((item, index) => `${index + 1}. ${item}`).join('\n');
    } else {
      return array.map(item => `- ${item}`).join('\n');
    }
  }

  // 转换数组为Markdown表格
  static toMarkdownTable(array) {
    if (!Array.isArray(array)) {
      throw new TypeError('array must be an array');
    }
    if (array.length === 0) {
      return '';
    }
    const header = array[0].map(cell => `| ${cell} `).join('') + '|';
    const separator = array[0].map(() => '| --- ').join('') + '|';
    const rows = array.slice(1).map(row => row.map(cell => `| ${cell} `).join('') + '|').join('\n');
    return `${header}\n${separator}\n${rows}`;
  }

  // 转换数组为YAML
  static toYaml(array) {
    if (!Array.isArray(array)) {
      throw new TypeError('array must be an array');
    }
    return array.map(item => `- ${item}`).join('\n');
  }

  // 转换数组为INI
  static toIni(array, section) {
    if (!Array.isArray(array) || typeof section !== 'string') {
      throw new TypeError('array must be an array and section must be a string');
    }
    const iniItems = array.map(item => `${item.key}=${item.value}`).join('\n');
    return `[${section}]\n${iniItems}`;
  }

  // 转换数组为JSON Lines
  static toJsonLines(array) {
    if (!Array.isArray(array)) {
      throw new TypeError('array must be an array');
    }
    return array.map(item => JSON.stringify(item)).join('\n');
  }

  // 转换数组为XML Lines
  static toXmlLines(array, itemElement) {
    if (!Array.isArray(array) || typeof itemElement !== 'string') {
      throw new TypeError('array must be an array and itemElement must be a string');
    }
    return array.map(item => `<${itemElement}>${item}</${itemElement}>`).join('\n');
  }

  // 转换数组为HTML Lines
  static toHtmlLines(array, element) {
    if (!Array.isArray(array) || typeof element !== 'string') {
      throw new TypeError('array must be an array and element must be a string');
    }
    return array.map(item => `<${element}>${item}</${element}>`).join('\n');
  }

  // 转换数组为Markdown Lines
  static toMarkdownLines(array, element) {
    if (!Array.isArray(array) || typeof element !== 'string') {
      throw new TypeError('array must be an array and element must be a string');
    }
    return array.map(item => `${element} ${item}`).join('\n');
  }

  // 转换数组为YAML Lines
  static toYamlLines(array) {
    if (!Array.isArray(array)) {
      throw new TypeError('array must be an array');
    }
    return array.map(item => `- ${item}`).join('\n');
  }

  // 转换数组为INI Lines
  static toIniLines(array) {
    if (!Array.isArray(array)) {
      throw new TypeError('array must be an array');
    }
    return array.map(item => `${item.key}=${item.value}`).join('\n');
  }

  // 转换数组为CSV Lines
  static toCsvLines(array, separator) {
    if (!Array.isArray(array) || typeof separator !== 'string') {
      throw new TypeError('array must be an array and separator must be a string');
    }
    return array.map(item => item.join(separator)).join('\n');
  }

  // 转换数组为TSV Lines
  static toTsvLines(array) {
    if (!Array.isArray(array)) {
      throw new TypeError('array must be an array');
    }
    return array.map(item => item.join('\t')).join('\n');
  }
}

export default ArrayUtils;