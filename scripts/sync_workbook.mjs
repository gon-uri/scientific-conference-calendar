// Run with the bundled artifact-tool dependency available. Serving the site
// never needs Node or this optional catalog-review workbook operation.
import fs from 'node:fs/promises';
import {FileBlob, SpreadsheetFile} from '@oai/artifact-tool';

const [workbookPath, payloadPath, previewDir] = process.argv.slice(2);
if (!workbookPath || !payloadPath || !previewDir) {
  throw Error('Usage: sync_workbook.mjs workbook.xlsx catalog.json preview-directory');
}
const wb = await SpreadsheetFile.importXlsx(await FileBlob.load(workbookPath));
const payload = JSON.parse(await fs.readFile(payloadPath, 'utf8'));
const catalog = wb.worksheets.getItem('Core Conferences');
const existing = catalog.getUsedRange().values;
const bySeries = new Map(payload.rows.map((row) => [row[0], row]));
const currentOrder = existing.slice(1).map((row) => row[0]).filter(Boolean);
if (currentOrder.some((series) => !bySeries.has(series))) throw Error('Workbook contains an unmapped series; review before removing it');
const ordered = currentOrder.map((series) => bySeries.get(series));
const additions = payload.rows.filter((row) => !currentOrder.includes(row[0]));
catalog.getRange(`A2:N${ordered.length + 1}`).values = ordered;
if (additions.length) {
  catalog.tables.items[0].rows.add(null, additions);
  for (let i = 0; i < additions.length; i++) {
    catalog.getRange(`A${ordered.length + 2 + i}:N${ordered.length + 2 + i}`)
      .copyFrom(catalog.getRange('A2:N2'), 'all');
  }
  catalog.getRange(`A${ordered.length + 2}:N${ordered.length + additions.length + 1}`).values = additions;
  catalog.getRange(`F${ordered.length + 2}:F${ordered.length + additions.length + 1}`).format.wrapText = true;
}
const total = ordered.length + additions.length;
catalog.getRange(`A2:N${total + 1}`).values = [...ordered, ...additions];
catalog.getRange(`K2:K${total + 1}`).setNumberFormat('0.0%');
catalog.getRange(`L2:L${total + 1}`).setNumberFormat('0');

const vocab = wb.worksheets.getItem('Tag Vocabulary');
const previous = vocab.getUsedRange().values.slice(1);
const definitions = new Map(previous.filter((row) => row[0]).map((row) => [row[0], String(row[1]).split(' Family: ')[0]]));
definitions.set('Fairness & Responsible AI', 'Fairness, accountability, discrimination, and equitable AI. Stable feed key; displayed as Fairness & accountability.');
const newDefinitions = {
  'Natural Language Processing & LLMs': 'Natural language processing, language models, computational linguistics, and LLM systems.',
  'Reinforcement Learning': 'Learning actions and policies from interaction, reward, and feedback.',
  'Federated & Distributed Learning': 'Distributed training, federated learning, and collaborative learning systems. Not automatically an ethics tag.',
  'Computer Vision & Pattern Recognition': 'Visual understanding, image analysis, recognition, and structured pattern learning.',
  'Nonlinear Dynamics & Chaos': 'Dynamical systems, bifurcations, chaos, synchronization, and nonlinear modeling.',
  'Complex Systems & Network Science': 'Complex adaptive systems, emergence, network structure, and dynamics on networks.',
  'Control & Robotics': 'Feedback control, automation, decision making, robotics, and learning-based control.',
  'System Identification & Data-driven Dynamics': 'Identifying dynamical models from data, state estimation, and data-driven dynamics.',
  'Ethics & Governance': 'AI ethics, social impacts, governance, regulation, and responsible research.',
  'Privacy-preserving ML': 'Privacy, differential privacy, confidential learning, and privacy-preserving computation.',
  'Robustness & Safety': 'Reliable and safe AI, adversarial robustness, distribution shift, and model assurance.',
  'Evolutionary Computation & Optimization': 'Evolutionary algorithms, genetic programming, neuroevolution, and population-based optimization.',
  'Cognitive Science & Computational Cognition': 'Computational models of cognition, learning, perception, language, and reasoning.',
  'ML Systems & Infrastructure': 'Systems for ML and ML for systems, including training, inference, compilers, hardware, and serving.',
};
const topicByName = new Map(payload.topics.map((topic) => [topic.tag, topic]));
const topicOrder = payload.topics.map((topic) => topic.tag);
const vocabulary = topicOrder.map((tag) => [tag, `${definitions.get(tag) || newDefinitions[tag]} Family: ${topicByName.get(tag).family}.`]);
vocab.getRange(`A2:B${previous.length + 1}`).values = vocabulary.slice(0, previous.length);
if (vocabulary.length > previous.length) {
  vocab.tables.items[0].rows.add(null, vocabulary.slice(previous.length));
  for (let row = previous.length + 2; row <= vocabulary.length + 1; row++) {
    vocab.getRange(`A${row}:B${row}`).copyFrom(vocab.getRange('A2:B2'), 'all');
  }
  vocab.getRange(`A${previous.length + 2}:B${vocabulary.length + 1}`).values = vocabulary.slice(previous.length);
}
vocab.getRange(`A2:B${vocabulary.length + 1}`).values = vocabulary;
catalog.getRange(`B2:B${total + 1}`).format.wrapText = true;
vocab.getRange(`B2:B${vocabulary.length + 1}`).format.wrapText = true;
vocab.getRange(`A2:B${vocabulary.length + 1}`).format.autofitRows();
catalog.getRange(`A2:F${total + 1}`).format.autofitRows();

let scopeSheet;
let scopeRows;
if (payload.scopes) {
  try {
    scopeSheet = wb.worksheets.getItem('Conference Scope');
  } catch {
    scopeSheet = wb.worksheets.add('Conference Scope');
  }
  scopeSheet.tables.items.forEach(table => table.delete());
  scopeSheet.getUsedRange()?.clear({applyTo: 'contents'});
  scopeRows = payload.scopes.map(row => [...row.slice(0, 5), Date.parse(`${row[5]}T00:00:00Z`) / 86400000 + 25569]);
  const last = scopeRows.length + 1;
  scopeSheet.getRange(`A1:F${last}`).values = [
    ['Series', 'Additional topics', 'Scope summary', 'Source edition', 'Scope sources', 'Scope reviewed'],
    ...scopeRows,
  ];
  const table = scopeSheet.tables.add(`A1:F${last}`, true, 'ConferenceScope');
  table.style = catalog.tables.items[0].style;
  scopeSheet.getRange(`A1:F${last}`).format.font = {name: 'Arial', size: 10};
  scopeSheet.getRange(`A1:F${last}`).format.verticalAlignment = 'top';
  scopeSheet.getRange(`A1:F${last}`).format.wrapText = true;
  for (const [column, width] of [['A',140],['B',300],['C',500],['D',100],['E',350],['F',110]]) {
    scopeSheet.getRange(`${column}1:${column}${last}`).format.columnWidthPx = width;
  }
  scopeSheet.getRange(`D2:D${last}`).setNumberFormat('0');
  scopeSheet.getRange(`F2:F${last}`).setNumberFormat('yyyy-mm-dd');
  scopeSheet.getRange(`A1:F${last}`).format.autofitRows();
  scopeSheet.getRange('A1:F1').format.verticalAlignment = 'center';
  scopeSheet.freezePanes.freezeRows(1);
  scopeSheet.freezePanes.freezeColumns(1);
  scopeSheet.showGridLines = false;
}
wb.recalculate();
const actual = catalog.getRange(`A2:N${total + 1}`).values;
if (JSON.stringify(actual) !== JSON.stringify([...ordered, ...additions])) throw Error('Catalog synchronization mismatch');
if (JSON.stringify(vocab.getRange(`A2:B${vocabulary.length + 1}`).values) !== JSON.stringify(vocabulary)) throw Error('Topic vocabulary synchronization mismatch');
if (scopeSheet && JSON.stringify(scopeSheet.getRange(`A2:F${scopeRows.length + 1}`).values) !== JSON.stringify(scopeRows)) throw Error('Scope synchronization mismatch');
console.log((await wb.inspect({kind:'match', searchTerm:'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A|#NUM!|#NULL!', options:{useRegex:true,maxResults:30}, summary:'Formula error check',maxChars:2500})).ndjson);
await fs.mkdir(previewDir, {recursive:true});
for (const [sheetName, range, name] of [
  ['Core Conferences', `A${Math.max(1,total - 7)}:F${total + 1}`, 'catalog'],
  ['Tag Vocabulary', `A${Math.max(2,vocabulary.length - 9)}:B${vocabulary.length + 1}`, 'topics'],
  ...(scopeSheet ? [['Conference Scope', 'A1:F5', 'scope']] : []),
]) {
  const preview = await wb.render({sheetName, range, scale:1.2, format:'png'});
  await fs.writeFile(`${previewDir}/${name}.png`, new Uint8Array(await preview.arrayBuffer()));
}
await (await SpreadsheetFile.exportXlsx(wb)).save(workbookPath);
console.log(`Synchronized ${total} conference series, ${vocabulary.length} subtopics, and ${scopeRows?.length || 0} scope profiles.`);
