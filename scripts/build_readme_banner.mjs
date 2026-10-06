import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
import path from 'node:path';
import {chromium} from 'playwright';

const root = path.resolve(process.argv[2] || '.');
const logo = (await fs.readFile(path.join(root, 'assets/venue-radar.png'))).toString('base64');
const font = (await fs.readFile(path.join(root, 'assets/vendor/audiowide-latin.woff2'))).toString('base64');
const output = path.join(root, 'assets/branding/venue-radar-banner.png');
const launch = {headless: true};
if (process.env.CHROME_BIN) launch.executablePath = process.env.CHROME_BIN;
const browser = await chromium.launch(launch);

try {
  const page = await browser.newPage({viewport: {width: 1400, height: 175}});
  await page.route('**/*', route => route.abort());
  await page.setContent(`<!doctype html>
    <html lang="en"><head><meta charset="utf-8"><style>
      @font-face {font-family: Audiowide; font-weight: 400; font-style: normal;
        src: url(data:font/woff2;base64,${font}) format('woff2');}
      body {margin: 0; background: #fff; color: #263238;}
      .brand {display: flex; align-items: center; gap: 19.5px; padding: 26px;
        width: 1400px; height: 175px; box-sizing: border-box;}
      img {width: 123px; height: 123px; object-fit: contain; flex: 0 0 auto;}
      h1 {margin: 0; font-family: Audiowide, sans-serif; font-size: 63px;
        font-weight: 400; font-synthesis: none; line-height: 1.15;
        letter-spacing: 0; transform: translateY(3px);}
    </style></head><body><div class="brand">
      <img src="data:image/png;base64,${logo}" alt="">
      <h1>Venue Radar</h1>
    </div></body></html>`);
  await page.evaluate(() => document.fonts.ready);
  assert(await page.evaluate(() => [...document.fonts].some(face => face.family === 'Audiowide' && face.status === 'loaded')));
  assert(await page.locator('img').evaluate(image => image.complete && image.naturalWidth === 256));
  assert(await page.locator('h1').evaluate(title => title.scrollWidth <= title.clientWidth));
  await fs.mkdir(path.dirname(output), {recursive: true});
  await page.screenshot({path: output});
  console.log(`Generated ${output}`);
} finally {
  await browser.close();
}
