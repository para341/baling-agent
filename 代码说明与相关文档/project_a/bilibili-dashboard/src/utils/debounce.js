// 防抖函数实现
function debounce(func, wait, immediate) {
  let timeout;
  return function executedFunction(...args) {
    const context = this;
    const later = () => {
      timeout = null;
      if (!immediate) func.apply(context, args);
    };
    const callNow = immediate && !timeout;
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
    if (callNow) func.apply(context, args);
  };
}

// 节流函数实现
function throttle(func, limit) {
  let inThrottle;
  return function() {
    const args = arguments;
    const context = this;
    if (!inThrottle) {
      func.apply(context, args);
      inThrottle = true;
      setTimeout(() => inThrottle = false, limit);
    }
  };
}

// 高级节流函数实现
function throttleAdvanced(func, limit, options) {
  options = options || {};
  let inThrottle;
  let lastFunc;
  let lastRan;
  return function() {
    const args = arguments;
    const context = this;
    if (!inThrottle) {
      func.apply(context, args);
      lastRan = Date.now();
      inThrottle = true;
    } else {
      clearTimeout(lastFunc);
      lastFunc = setTimeout(() => {
        if (Date.now() - lastRan >= limit) {
          func.apply(context, args);
          lastRan = Date.now();
        }
      }, limit - (Date.now() - lastRan));
    }
  };
}

// 自定义防抖函数
function debounceCustom(func, wait, options) {
  options = options || {};
  let timeout;
  let lastArgs;
  let lastThis;
  let result;
  let lastCallTime;
  let lastInvokeTime = 0;
  const leading = options.leading || false;
  const trailing = options.trailing !== false;
  const maxWait = options.maxWait;
  let timerId;
  let maxTimeoutId;

  const shouldInvoke = (time) => {
    const timeSinceLastCall = time - lastCallTime;
    const timeSinceLastInvoke = time - lastInvokeTime;
    return (lastCallTime === undefined || (timeSinceLastCall >= wait) ||
            (timeSinceLastCall < 0) || (maxWait !== undefined && timeSinceLastInvoke >= maxWait));
  };

  const invokeFunc = (time) => {
    const args = lastArgs;
    const thisArg = lastThis;
    lastArgs = lastThis = undefined;
    lastInvokeTime = time;
    result = func.apply(thisArg, args);
    return result;
  };

  const leadingEdge = (time) => {
    lastInvokeTime = time;
    timerId = setTimeout(timerExpired, wait);
    return leading ? invokeFunc(time) : result;
  };

  const remainingWait = (time) => {
    const timeSinceLastCall = time - lastCallTime;
    const timeSinceLastInvoke = time - lastInvokeTime;
    const timeWaiting = wait - timeSinceLastCall;
    return maxWait === undefined ? timeWaiting : Math.min(timeWaiting, maxWait - timeSinceLastInvoke);
  };

  const shouldInvokeLeading = (time) => {
    const timeSinceLastInvoke = time - lastInvokeTime;
    return (lastCallTime === undefined || (timeSinceLastCall >= wait) ||
            (timeSinceLastCall < 0) || (maxWait !== undefined && timeSinceLastInvoke >= maxWait));
  };

  const timerExpired = () => {
    const time = Date.now();
    if (shouldInvoke(time)) {
      return trailingEdge(time);
    }
    timerId = setTimeout(timerExpired, remainingWait(time));
  };

  const trailingEdge = (time) => {
    timerId = undefined;
    if (trailing && lastArgs) {
      return invokeFunc(time);
    }
    lastArgs = lastThis = undefined;
    return result;
  };

  const cancel = () => {
    if (timerId) clearTimeout(timerId);
    if (maxTimeoutId) clearTimeout(maxTimeoutId);
    lastInvokeTime = 0;
    lastArgs = lastCallTime = lastThis = timerId = maxTimeoutId = undefined;
  };

  const flush = () => {
    return timerId === undefined ? result : trailingEdge(Date.now());
  };

  return function debounced(...args) {
    const time = Date.now();
    const isInvoking = shouldInvoke(time);
    lastArgs = args;
    lastThis = this;
    lastCallTime = time;

    if (isInvoking) {
      if (timerId === undefined) {
        return leadingEdge(lastCallTime);
      }
      if (maxWait !== undefined) {
        maxTimeoutId = setTimeout(timerExpired, maxWait);
        return invokeFunc(lastCallTime);
      }
    }
    if (timerId === undefined) {
      timerId = setTimeout(timerExpired, wait);
    }
    return result;
  };
}

export { debounce, throttle, throttleAdvanced, debounceCustom };