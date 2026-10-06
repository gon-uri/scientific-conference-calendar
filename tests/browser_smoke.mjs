import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
import path from 'node:path';
import {pathToFileURL} from 'node:url';
import {chromium} from 'playwright';

const url = process.argv[2] || pathToFileURL(path.resolve('docs/index.html')).href;
const launch = {headless: true};
if (process.env.CHROME_BIN) launch.executablePath = process.env.CHROME_BIN;
const browser = await chromium.launch(launch);
const page = await browser.newPage({viewport: {width: 1440, height: 1000}});
const errors = [];
page.on('pageerror', error => errors.push(error.message));
await page.addInitScript(() => { Date.now = () => Date.parse('2026-10-06T12:00:00Z'); });
// Local checks do not authenticate, create Discussions, or exercise Giscus.
await page.route('https://giscus.app/**', route => route.abort());

try {
  await page.goto(url);
  assert.equal(await page.title(), 'Venue Radar | Scientific Conference Calendar');
  assert.deepEqual(await page.locator('[data-filter-group="size"]').evaluateAll(inputs => inputs.map(i => i.value)), ['s', 'm', 'l', 'xl', 'xxl']);
  assert.equal(await page.locator('#deadlines-table .row-calendar-button').count(), 0);
  const toggle = page.locator('[data-deadline-group]:visible .deadline-toggle').first();
  await toggle.click();
  assert.equal(await toggle.getAttribute('aria-expanded'), 'true');
  await toggle.click();
  await page.locator('#open-only').check();
  const opportunities = await page.locator('[data-deadline-group]:visible').evaluateAll(rows => rows.map(r => r.dataset.edition));
  assert(!opportunities.includes('acc-2027'));
  assert(opportunities.includes('ieee-cdc-2027'));
  assert(opportunities.includes('netsci-2027'));

  await page.locator('#tab-conferences').click();
  assert(!(await page.locator('#open-only').isVisible()));
  assert.equal(await page.locator('#map-count').innerText(), '51 confirmed editions in 43 cities');
  assert.equal(await page.locator('.city-marker').count(), 43);
  assert.equal(await page.locator('#panel-conferences [data-submission-status]').count(), 0);
  await page.locator('#conference-map').scrollIntoViewIfNeeded();
  const montreal = page.locator('.city-marker[title^="Montreal"]');
  await montreal.focus();
  await page.keyboard.press('Enter');
  assert.match(await page.locator('.city-popup').innerText(), /AISTATS 2027/);
  await page.locator('.leaflet-popup-close-button').click();
  await page.locator('.map-city-link').filter({hasText: 'Montreal'}).click();
  await page.locator('.leaflet-popup-close-button').click();
  await montreal.hover();
  assert.match(await page.locator('.city-popup').innerText(), /COSYNE 2027/);

  await page.locator('#clear-filters').click();
  const familySummary = page.locator('.topic-family summary').first();
  await familySummary.focus();
  await page.keyboard.press('Enter');
  await page.locator('[data-topic-family="ml-ai"]').first().check();
  assert(await page.locator('[data-family-toggle="ml-ai"]').evaluate(input => input.indeterminate));
  await page.locator('#clear-filters').click();
  await familySummary.focus();
  await page.keyboard.press('Enter');
  await page.locator('[data-family-toggle="dynamics-control"]').check();
  await page.locator('[data-family-toggle="ml-ai"]').check();
  await page.locator('#topic-match').selectOption('all');
  const intersection = await page.locator('#upcoming-conferences-body [data-conference-row]:visible').evaluateAll(rows => rows.map(r => r.dataset.edition));
  assert(intersection.includes('l4dc-2027'));
  assert(!intersection.includes('netsci-2027'));
  await page.locator('#clear-filters').click();
  await page.locator('#search').fill('no-such-conference-xyz');
  assert.equal(await page.locator('.city-marker').count(), 0);
  assert(await page.locator('#map-empty').isVisible());
  await page.locator('#clear-filters').click();

  const output = process.env.SCREENSHOT_DIR;
  if (output) await fs.mkdir(output, {recursive: true});
  await page.getByRole('button', {name: 'Reset world view'}).click();
  for (const width of [1440, 768, 390, 320]) {
    await page.setViewportSize({width, height: width > 760 ? 1000 : 844});
    await page.waitForFunction(() => conferenceMap.getSize().x === document.querySelector('#conference-map').clientWidth);
    await page.waitForFunction(() => conferenceMap.getBounds().getEast() - conferenceMap.getBounds().getWest() > 330);
    assert(!(await page.evaluate(() => document.documentElement.scrollWidth > innerWidth)), `Map overflow at ${width}px`);
    assert(await page.locator('.leaflet-overlay-pane svg path').count() > 0);
    if (output) {
      await page.locator('#conference-map').scrollIntoViewIfNeeded();
      await page.screenshot({path: path.join(output, `map-${width}.png`)});
    }
    await page.locator('#tab-deadlines').click();
    assert(!(await page.evaluate(() => document.documentElement.scrollWidth > innerWidth)), `Deadline overflow at ${width}px`);
    if (output) {
      await page.evaluate(() => scrollTo(0, 0));
      await page.screenshot({path: path.join(output, `deadlines-${width}.png`)});
    }
    if (width <= 760) {
      await page.locator('#filter-details > summary').click();
      assert(!(await page.evaluate(() => document.documentElement.scrollWidth > innerWidth)), `Expanded filter overflow at ${width}px`);
      await page.locator('#filter-details > summary').click();
    }
    await page.locator('#tab-conferences').click();
  }
  assert.deepEqual(errors, []);
  console.log(`Browser smoke passed: ${opportunities.length} opportunities, ${intersection.length} cross-family matches; 1440/768/390/320px.`);
} finally {
  await browser.close();
}
