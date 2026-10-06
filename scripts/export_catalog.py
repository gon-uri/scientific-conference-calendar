"""Export the latest edition of each series for workbook synchronization."""

import argparse
import json
from pathlib import Path
import yaml

from catalog_metadata import FAMILIES_PATH, load_mapping
from validate import (
    TOPICS_PATH, acceptance_band, load_acceptance_rates, load_ccf_rankings,
    load_conferences, load_icore_rankings,
)


def catalog_payload() -> dict:
    latest = {}
    for item in load_conferences():
        if item['series'] not in latest or item['year'] > latest[item['series']]['year']:
            latest[item['series']] = item
    icore = load_icore_rankings()['rankings']
    ccf_data = load_ccf_rankings()
    ccf = ccf_data['rankings']
    rates = load_acceptance_rates()['rates']
    rows = []
    for series, item in latest.items():
        i, c, rate = icore.get(series), ccf.get(series), rates.get(series)
        percent = rate.get('percent') if rate else None
        band = acceptance_band(percent) if percent is not None else rate['band'] + ' (estimated)' if rate else 'Unknown'
        rows.append([
            series, '; '.join(item['topics']), item['size'], band,
            i['rank'] if i else None, item['submission_type'], item['website'],
            f'https://portal.core.edu.au/conf-ranks/{i["portal_id"]}/' if i else None,
            c['rank'] if c else None,
            f'{ccf_data["source_url"]}#page={c["page"]}' if c else None,
            percent / 100 if percent is not None else None,
            rate['year'] if rate else None, rate['track'] if rate else None,
            rate['source_url'] if rate else None,
        ])
    families = load_mapping(FAMILIES_PATH)
    family_by_topic = {topic: family['label'] for family in families['families'] for topic in family['topics']}
    return {'rows': rows, 'topics': [
        {'tag': topic, 'family': family_by_topic[topic], 'label': families['labels'][topic]}
        for topic in yaml.safe_load(TOPICS_PATH.read_text(encoding='utf-8'))
    ]}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    args.output.write_text(json.dumps(catalog_payload(), indent=2) + '\n', encoding='utf-8')
    print(f'Exported {args.output}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
