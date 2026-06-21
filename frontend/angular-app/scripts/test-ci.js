const child = require('child_process');
(async ()=>{
  try{
    const m = await import('puppeteer');
    const puppeteer = m.default || m;
    const chrome = (typeof puppeteer.executablePath === 'function') ? puppeteer.executablePath() : undefined;
    if (chrome) {
      process.env.CHROME_BIN = chrome;
      console.log('Using Chromium from Puppeteer:', chrome);
    } else {
      console.warn('Puppeteer installed but executablePath not available');
    }
  } catch(e){
    console.error('Puppeteer not installed or failed to load:', e.message);
  }
  const res = child.spawnSync('ng',['test','--watch=false'],{stdio:'inherit'});
  process.exit(res.status);
})();
