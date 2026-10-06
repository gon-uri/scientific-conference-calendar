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
  const filterSummary = page.locator('#filter-details > summary');
  assert(!(await page.locator('#filter-details').evaluate(details => details.open)));
  assert(!(await page.locator('#clear-filters').isVisible()));
  assert.equal(await filterSummary.innerText(), 'Filters & search');
  assert(Number.parseFloat(await filterSummary.evaluate(summary => getComputedStyle(summary).fontSize)) >= 17);
  assert.equal(await page.locator('input:not(#open-only), select, #clear-filters').evaluateAll(controls => controls.filter(control => !control.closest('#filter-details')).length), 0);
  assert(await page.getByLabel('Show only submission opportunities', {exact: true}).isVisible());
  assert(await page.locator('#open-only').evaluate(input => !input.closest('#filter-details') && !!input.closest('.tab-toolbar')));
  const tabsBox = await page.locator('.table-tabs').boundingBox();
  const opportunitiesBox = await page.locator('.open-toggle').boundingBox();
  assert(opportunitiesBox.x > tabsBox.x + tabsBox.width && Math.abs(opportunitiesBox.y + opportunitiesBox.height / 2 - tabsBox.y - tabsBox.height / 2) < 1);
  await filterSummary.click();
  assert.equal(await page.getByRole('link', {name: 'ICORE Rank', exact: true}).getAttribute('href'), 'https://portal.core.edu.au/conf-ranks/');
  const ccfPage = 'https://www.ccf.org.cn/Academic_Evaluation/By_category/2026-03-31/870181.shtml';
  assert.equal(await page.getByRole('link', {name: 'CCF Rank', exact: true}).getAttribute('href'), ccfPage);
  assert(await page.locator('.rank-link-ccf').evaluateAll(links => links.every(link => link.href === 'https://www.ccf.org.cn/Academic_Evaluation/By_category/2026-03-31/870181.shtml')));
  assert.equal(await page.locator('.calendar-caption').innerText(), 'Download calendar');
  assert(await page.locator('header').evaluate(header => header.querySelector('.calendar-action').getBoundingClientRect().right > header.querySelector('.brand-line').getBoundingClientRect().right));
  assert.equal(await page.locator('.brand-mark').evaluate(image => image.clientWidth), 76);
  assert.notEqual(await page.locator('#tab-deadlines').evaluate(tab => getComputedStyle(tab).backgroundColor), await page.locator('#tab-conferences').evaluate(tab => getComputedStyle(tab).backgroundColor));
  assert((await page.locator('.topic-filter').boundingBox()).width <= 360);
  assert.equal(await page.locator('.topic-filter > legend').innerText(), 'Topics & Subtopics');
  assert(await page.locator('.topic-family > summary').evaluateAll(summaries => summaries.every(summary => getComputedStyle(summary).display === 'list-item' && summary.title === 'Expand or collapse subtopics')));
  const searchLabel = await page.locator('.search-control .control-label').boundingBox();
  const acceptanceLabel = await page.locator('.filter-group').filter({has: page.locator('[data-filter-group="acceptance"]')}).locator('legend').boundingBox();
  assert(searchLabel.x > acceptanceLabel.x + acceptanceLabel.width);
  assert(Math.abs(searchLabel.y - acceptanceLabel.y) < 1, 'Search and filter headings must align vertically');
  assert.deepEqual(await page.locator('[data-filter-group="size"]').evaluateAll(inputs => inputs.map(i => i.value)), ['s', 'm', 'l', 'xl', 'xxl']);
  assert.equal(await page.locator('#panel-deadlines .row-calendar-button').count(), 0);
  const toggle = page.locator('[data-deadline-group]:visible .deadline-toggle').first();
  await toggle.click();
  assert.equal(await toggle.getAttribute('aria-expanded'), 'true');
  await toggle.click();
  await filterSummary.click();
  await page.locator('#open-only').check();
  const opportunities = await page.locator('[data-deadline-group]:visible').evaluateAll(rows => rows.map(r => r.dataset.edition));
  assert(!opportunities.includes('acc-2027'));
  assert(opportunities.includes('ieee-cdc-2027'));
  assert(opportunities.includes('netsci-2027'));
  await filterSummary.click();

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

  await page.locator('[data-filter-group="ccf"][value="B"]').check();
  const ccfMatches = page.locator('#upcoming-conferences-body [data-conference-row]:visible');
  assert(await ccfMatches.evaluateAll(rows => rows.length > 0 && rows.every(row => row.dataset.ccf === 'B')));
  assert((await page.locator('.city-marker').count()) > 0 && (await page.locator('.city-marker').count()) < 43);
  await page.locator('[data-filter-group="icore"][value="Unranked"]').check();
  assert(await ccfMatches.evaluateAll(rows => rows.length > 0 && rows.every(row => row.dataset.ccf === 'B' && row.dataset.icore === 'Unranked')));
  assert(await ccfMatches.evaluateAll(rows => rows.some(row => row.dataset.edition === 'icassp-2027')));
  await page.locator('#tab-deadlines').click();
  assert(await page.locator('[data-deadline-group]:visible').evaluateAll(rows => rows.length > 0 && rows.every(row => row.dataset.ccf === 'B' && row.dataset.icore === 'Unranked')));
  await page.locator('#clear-filters').click();
  await page.locator('[data-filter-group="ccf"][value="Unranked"]').check();
  assert(await page.locator('[data-deadline-group]:visible').evaluateAll(rows => rows.length > 0 && rows.every(row => row.dataset.ccf === 'Unranked')));
  await page.locator('#clear-filters').click();
  await page.locator('#tab-conferences').click();
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
  await filterSummary.click();
  const widths = [1440, 1051, 1050, 768, 390, 320];
  for (const width of widths) {
    await page.setViewportSize({width, height: width > 760 ? 1000 : 844});
    await page.waitForFunction(() => conferenceMap.getSize().x === document.querySelector('#conference-map').clientWidth);
    await page.waitForFunction(() => conferenceMap.getBounds().getEast() - conferenceMap.getBounds().getWest() > 330);
    assert(!(await page.evaluate(() => document.documentElement.scrollWidth > innerWidth)), `Map overflow at ${width}px`);
    assert(await page.locator('.leaflet-overlay-pane svg path').count() > 0);
    if (width > 760) {
      assert(await page.locator('th:visible').evaluateAll(headings => headings.every(heading => {
        const range = document.createRange();
        range.selectNodeContents(heading);
        const text = range.getBoundingClientRect();
        const cell = heading.getBoundingClientRect();
        return text.left >= cell.left - 1 && text.right <= cell.right + 1;
      })), `Conference header overlap at ${width}px`);
    }
    if (output) {
      await page.locator('#conference-map').scrollIntoViewIfNeeded();
      await page.screenshot({path: path.join(output, `map-${width}.png`)});
    }
    await page.locator('#tab-deadlines').click();
    assert(!(await page.evaluate(() => document.documentElement.scrollWidth > innerWidth)), `Deadline overflow at ${width}px`);
    if (width > 760) {
      assert(await page.locator('th:visible').evaluateAll(headings => headings.every(heading => {
        const range = document.createRange();
        range.selectNodeContents(heading);
        const text = range.getBoundingClientRect();
        const cell = heading.getBoundingClientRect();
        return text.left >= cell.left - 1 && text.right <= cell.right + 1;
      })), `Deadline header overlap at ${width}px`);
    }
    if (output) {
      await page.evaluate(() => scrollTo(0, 0));
      await page.screenshot({path: path.join(output, `deadlines-${width}.png`)});
    }
    assert(!(await page.locator('#filter-details').evaluate(details => details.open)));
    assert(await page.locator('#open-only').isVisible());
    await filterSummary.click();
    assert(await page.locator('#clear-filters').isVisible());
    assert(!(await page.evaluate(() => document.documentElement.scrollWidth > innerWidth)), `Expanded filter overflow at ${width}px`);
    if (width > 760) {
      const searchBox = await page.locator('.search-control .control-label').boundingBox();
      const rateBox = await page.locator('.filter-group').filter({has: page.locator('[data-filter-group="acceptance"]')}).locator('legend').boundingBox();
      assert(searchBox.x > rateBox.x + rateBox.width && Math.abs(searchBox.y - rateBox.y) < 1, `Search alignment at ${width}px`);
    }
    if (output) await page.screenshot({path: path.join(output, `filters-${width}.png`)});
    await filterSummary.click();
    await page.locator('#tab-conferences').click();
  }
  assert.deepEqual(errors, []);
  console.log(`Browser smoke passed: ${opportunities.length} opportunities, ${intersection.length} cross-family matches; ${widths.join('/')}px.`);
} finally {
  await browser.close();
}
