// 性能监控工具实现
class PerformanceMonitor {
  constructor() {
    this.metrics = new Map();
    this.startTimes = new Map();
    this.endTimes = new Map();
    this.durations = new Map();
  }

  startMetric(name) {
    if (this.startTimes.has(name)) {
      console.warn(`Metric '${name}' is already running`);
      return;
    }
    this.startTimes.set(name, performance.now());
  }

  endMetric(name) {
    if (!this.startTimes.has(name)) {
      console.warn(`Metric '${name}' is not running`);
      return;
    }
    const startTime = this.startTimes.get(name);
    const endTime = performance.now();
    const duration = endTime - startTime;
    this.startTimes.delete(name);
    this.endTimes.set(name, endTime);
    this.durations.set(name, duration);
    return duration;
  }

  getMetric(name) {
    if (!this.durations.has(name)) {
      return null;
    }
    return {
      endTime: this.endTimes.get(name),
      duration: this.durations.get(name)
    };
  }

  getAllMetrics() {
    const metrics = [];
    this.durations.forEach((duration, name) => {
      metrics.push({
        name,
        endTime: this.endTimes.get(name),
        duration
      });
    });
    return metrics;
  }

  clearMetrics() {
    this.metrics.clear();
    this.startTimes.clear();
    this.endTimes.clear();
    this.durations.clear();
  }

  size() {
    return this.durations.size;
  }

  getAverageDuration() {
    if (this.durations.size === 0) {
      return 0;
    }
    const total = Array.from(this.durations.values()).reduce((sum, duration) => sum + duration, 0);
    return total / this.durations.size;
  }

  getMaxDuration() {
    if (this.durations.size === 0) {
      return 0;
    }
    return Math.max(...this.durations.values());
  }

  getMinDuration() {
    if (this.durations.size === 0) {
      return 0;
    }
    return Math.min(...this.durations.values());
  }

  logMetrics() {
    console.log('Performance Metrics:');
    this.durations.forEach((duration, name) => {
      console.log(`  ${name}: ${duration.toFixed(2)}ms`);
    });
  }
}

// 性能分析工具
class PerformanceAnalyzer {
  constructor() {
    this.monitor = new PerformanceMonitor();
    this.analysisResults = new Map();
  }

  analyzeFunction(func, name) {
    return function(...args) {
      this.monitor.startMetric(name);
      const result = func.apply(this, args);
      this.monitor.endMetric(name);
      return result;
    };
  }

  async analyzeAsyncFunction(func, name) {
    return async function(...args) {
      this.monitor.startMetric(name);
      const result = await func.apply(this, args);
      this.monitor.endMetric(name);
      return result;
    };
  }

  analyzePerformance() {
    const metrics = this.monitor.getAllMetrics();
    const analysis = {
      totalMetrics: metrics.length,
      averageDuration: this.monitor.getAverageDuration(),
      maxDuration: this.monitor.getMaxDuration(),
      minDuration: this.monitor.getMinDuration(),
      metrics
    };
    this.analysisResults.set(`analysis-${Date.now()}`, analysis);
    return analysis;
  }

  getAnalysisResults() {
    return Array.from(this.analysisResults.values());
  }

  clearAnalysisResults() {
    this.analysisResults.clear();
  }
}

// 性能监控装饰器
function performanceDecorator(name) {
  return function(target, propertyKey, descriptor) {
    const originalMethod = descriptor.value;
    const monitor = new PerformanceMonitor();

    descriptor.value = async function(...args) {
      monitor.startMetric(name);
      const result = await originalMethod.apply(this, args);
      monitor.endMetric(name);
      const duration = monitor.getMetric(name).duration;
      console.log(`${name} executed in ${duration.toFixed(2)}ms`);
      return result;
    };

    return descriptor;
  };
}

// 性能监控函数
function monitorPerformance(func, name) {
  return function(...args) {
    const startTime = performance.now();
    const result = func.apply(this, args);
    const endTime = performance.now();
    const duration = endTime - startTime;
    console.log(`${name} executed in ${duration.toFixed(2)}ms`);
    return result;
  };
}

// 异步性能监控函数
function monitorAsyncPerformance(func, name) {
  return async function(...args) {
    const startTime = performance.now();
    const result = await func.apply(this, args);
    const endTime = performance.now();
    const duration = endTime - startTime;
    console.log(`${name} executed in ${duration.toFixed(2)}ms`);
    return result;
  };
}

// 性能报告生成器
function generatePerformanceReport(metrics) {
  const report = {
    generatedAt: new Date().toISOString(),
    totalMetrics: metrics.length,
    averageDuration: metrics.reduce((sum, metric) => sum + metric.duration, 0) / metrics.length,
    maxDuration: Math.max(...metrics.map(metric => metric.duration)),
    minDuration: Math.min(...metrics.map(metric => metric.duration)),
    metrics
  };
  return report;
}

export { PerformanceMonitor, PerformanceAnalyzer, performanceDecorator, monitorPerformance, monitorAsyncPerformance, generatePerformanceReport };