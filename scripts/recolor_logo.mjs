import assert from 'node:assert/strict';
import path from 'node:path';
import sharp from 'sharp';

const root = path.resolve(process.argv[2] || '.');
const source = path.join(root, 'assets/branding/venue-radar-source.png');
const destination = path.join(root, 'assets/venue-radar.png');
const {data, info} = await sharp(source).ensureAlpha().raw().toBuffer({resolveWithObject: true});
const {width, height} = info;
const palette = {
  border: [38, 50, 56],
  blue: [56, 166, 176],
  red: [200, 92, 98],
  white: [255, 255, 255],
};

function foregroundColor(r, g, b) {
  return r > g + 20 && r > b + 35 ? palette.red
    : g > r + 25 && b > r + 25 ? palette.blue : palette.border;
}

const left = new Int32Array(height).fill(width);
const right = new Int32Array(height).fill(-1);
let bodyTop = height;
for (let y = 0; y < height; y++) {
  for (let x = 0; x < width; x++) {
    const i = (y * width + x) * 4;
    if (data[i + 3] >= 128 && foregroundColor(...data.subarray(i, i + 3)) === palette.border) {
      left[y] = Math.min(left[y], x);
      right[y] = Math.max(right[y], x);
      if (x === Math.floor(width / 2)) bodyTop = Math.min(bodyTop, y);
    }
  }
}
assert(bodyTop < height / 3, 'The central calendar border must identify its top');

// Fill only between the existing calendar sides, not the space above its binding tabs.
const output = Buffer.from(data);
let filled = 0;
for (let pixel = 0; pixel < width * height; pixel++) {
  const i = pixel * 4;
  const [r, g, b, a] = data.subarray(i, i + 4);
  if (a === 0) {
    const x = pixel % width;
    const y = Math.floor(pixel / width);
    if (y >= bodyTop && x >= left[y] && x <= right[y]) {
      output.set([...palette.white, 255], i);
      filled++;
    } else {
      output.set([0, 0, 0, 0], i);
    }
    continue;
  }
  output.set(foregroundColor(r, g, b), i);
  assert.equal(output[i + 3], a, 'Original foreground alpha must stay unchanged');
}

for (const [x, y] of [[Math.round(width * .4), Math.round(height * .38)], [Math.round(width * .44), Math.round(height * .295)]]) {
  const i = (y * width + x) * 4;
  assert.deepEqual([...output.subarray(i, i + 4)], [...palette.white, 255], 'Calendar interior and header must be opaque white');
}
assert(filled > width * height / 5, 'Calendar interior must be filled');
const colors = new Set();
for (let pixel = 0; pixel < width * height; pixel++) {
  const i = pixel * 4;
  if (output[i + 3]) colors.add([...output.subarray(i, i + 3)].join(','));
  if (data[i + 3]) {
    assert.equal(output[i + 3], data[i + 3], 'All original foreground edge coverage must be preserved');
    assert.notDeepEqual([...output.subarray(i, i + 3)], palette.white);
  }
}
assert.deepEqual([...colors].sort(), Object.values(palette).map(color => color.join(',')).sort(), 'Artwork must use exactly four RGB colors');
await sharp(output, {raw: {width, height, channels: 4}}).png({compressionLevel: 9}).toFile(destination);
console.log(JSON.stringify({source, destination, width, height, filled, palette, preservedForeground: true, baseColors: colors.size}));
