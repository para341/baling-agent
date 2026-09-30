// 图片懒加载实现
function lazyLoadImages() {
  const images = document.querySelectorAll('img[data-src]');
  
  const imageObserver = new IntersectionObserver((entries, observer) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const img = entry.target;
        img.src = img.dataset.src;
        img.removeAttribute('data-src');
        observer.unobserve(img);
      }
    });
  }, {
    root: null,
    rootMargin: '0px',
    threshold: 0.1
  });
  
  images.forEach(img => imageObserver.observe(img));
}

// 组件懒加载实现
function lazyLoadComponent(selector, loadFunction) {
  const element = document.querySelector(selector);
  
  const componentObserver = new IntersectionObserver((entries, observer) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        loadFunction();
        observer.unobserve(entry.target);
      }
    });
  }, {
    root: null,
    rootMargin: '0px',
    threshold: 0.1
  });
  
  if (element) {
    componentObserver.observe(element);
  }
}

// 高级图片懒加载实现
function lazyLoadImagesAdvanced(options) {
  options = options || {};
  const root = options.root || null;
  const rootMargin = options.rootMargin || '0px';
  const threshold = options.threshold || 0.1;
  const loadFunction = options.loadFunction || defaultLoadFunction;
  
  const images = document.querySelectorAll(options.selector || 'img[data-src]');
  
  const imageObserver = new IntersectionObserver((entries, observer) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const img = entry.target;
        loadFunction(img);
        observer.unobserve(img);
      }
    });
  }, {
    root,
    rootMargin,
    threshold
  });
  
  images.forEach(img => imageObserver.observe(img));
}

// 默认加载函数
function defaultLoadFunction(img) {
  if (img.dataset.src) {
    img.src = img.dataset.src;
    img.removeAttribute('data-src');
  }
}

// 视频懒加载实现
function lazyLoadVideos() {
  const videos = document.querySelectorAll('video[data-src]');
  
  const videoObserver = new IntersectionObserver((entries, observer) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const video = entry.target;
        video.src = video.dataset.src;
        video.removeAttribute('data-src');
        video.load();
        observer.unobserve(video);
      }
    });
  }, {
    root: null,
    rootMargin: '0px',
    threshold: 0.1
  });
  
  videos.forEach(video => videoObserver.observe(video));
}

// 背景图懒加载实现
function lazyLoadBackgroundImages() {
  const elements = document.querySelectorAll('[data-bg-src]');
  
  const bgObserver = new IntersectionObserver((entries, observer) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const element = entry.target;
        element.style.backgroundImage = `url(${element.dataset.bgSrc})`;
        element.removeAttribute('data-bg-src');
        observer.unobserve(element);
      }
    });
  }, {
    root: null,
    rootMargin: '0px',
    threshold: 0.1
  });
  
  elements.forEach(element => bgObserver.observe(element));
}

// 通用懒加载函数
function lazyLoad(selector, loadFunction, options) {
  options = options || {};
  const root = options.root || null;
  const rootMargin = options.rootMargin || '0px';
  const threshold = options.threshold || 0.1;
  
  const elements = document.querySelectorAll(selector);
  
  const observer = new IntersectionObserver((entries, observer) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const element = entry.target;
        loadFunction(element);
        observer.unobserve(element);
      }
    });
  }, {
    root,
    rootMargin,
    threshold
  });
  
  elements.forEach(element => observer.observe(element));
}

export { lazyLoadImages, lazyLoadComponent, lazyLoadImagesAdvanced, lazyLoadVideos, lazyLoadBackgroundImages, lazyLoad };