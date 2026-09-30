// LRU缓存实现
class LRUCache {
  constructor(capacity) {
    this.capacity = capacity;
    this.cache = new Map();
  }

  get(key) {
    if (!this.cache.has(key)) {
      return null;
    }
    const value = this.cache.get(key);
    this.cache.delete(key);
    this.cache.set(key, value);
    return value;
  }

  set(key, value) {
    if (this.cache.has(key)) {
      this.cache.delete(key);
    } else if (this.cache.size >= this.capacity) {
      const oldestKey = this.cache.keys().next().value;
      this.cache.delete(oldestKey);
    }
    this.cache.set(key, value);
  }

  has(key) {
    return this.cache.has(key);
  }

  clear() {
    this.cache.clear();
  }

  size() {
    return this.cache.size;
  }

  keys() {
    return Array.from(this.cache.keys());
  }

  values() {
    return Array.from(this.cache.values());
  }

  entries() {
    return Array.from(this.cache.entries());
  }
}

// 缓存管理器
class CacheManager {
  constructor() {
    this.caches = new Map();
  }

  createCache(name, capacity = 100) {
    if (this.caches.has(name)) {
      throw new Error(`Cache '${name}' already exists`);
    }
    const cache = new LRUCache(capacity);
    this.caches.set(name, cache);
    return cache;
  }

  getCache(name) {
    if (!this.caches.has(name)) {
      throw new Error(`Cache '${name}' not found`);
    }
    return this.caches.get(name);
  }

  hasCache(name) {
    return this.caches.has(name);
  }

  deleteCache(name) {
    if (!this.caches.has(name)) {
      throw new Error(`Cache '${name}' not found`);
    }
    this.caches.delete(name);
  }

  clearAll() {
    this.caches.clear();
  }

  size() {
    return this.caches.size;
  }
}

// 创建全局缓存管理器
const cacheManager = new CacheManager();

// 创建常用缓存
const commentCache = cacheManager.createCache('commentAnalysis', 100);
const emotionCache = cacheManager.createCache('emotionAnalysis', 50);
const trendCache = cacheManager.createCache('trendAnalysis', 20);

export { LRUCache, CacheManager, cacheManager, commentCache, emotionCache, trendCache };