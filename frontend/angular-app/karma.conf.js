module.exports = function(config) {
  config.set({
    frameworks: ['jasmine'],
    files: [],
    preprocessors: {},
    reporters: ['progress'],
    port: 9876,
    colors: true,
    logLevel: config.LOG_INFO,
    autoWatch: false,
    singleRun: true,
    concurrency: Infinity,
    browsers: ['ChromeHeadlessPuppeteer'],
    customLaunchers: {
      ChromeHeadlessPuppeteer: {
        base: 'ChromeHeadless',
        flags: ['--no-sandbox', '--disable-setuid-sandbox', '--headless', '--disable-gpu', '--remote-debugging-port=9222']
      }
    }
  });
};
