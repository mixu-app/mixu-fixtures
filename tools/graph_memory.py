# SPDX-License-Identifier: Apache-2.0
"""Validate and deterministically export the independently annotated graph-memory corpus."""
from __future__ import annotations
import argparse
import copy
import hashlib
import json
from pathlib import Path
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / 'fixtures' / 'benchmarks' / 'graph-memory'

def encoded(value):
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + '\n').encode()

def horizons(facts, size):
    return [dict(ordinal=i, required_fact_ids=[f['fact_id'] for f in facts if f['valid_from_ordinal'] <= i], forbidden_fact_ids=[f['fact_id'] for f in facts if f['valid_from_ordinal'] > i]) for i in range(1, size + 1)]

def validate_pair(inp, gold):
    for name, obj in [('input', inp), ('gold', gold)]:
        schema = json.loads((ROOT / 'schema' / f'graph-memory-{name}.schema.json').read_text())
        Draft202012Validator(schema).validate(obj)
    assert inp['case_id'] == gold['case_id'], 'case mismatch'
    segments = {s['segment_id']: s for s in inp['segments']}
    assert len(segments) == len(inp['segments']), 'duplicate segment'
    assert [s['ordinal'] for s in inp['segments']] == list(range(1, len(segments) + 1)), 'segment order'
    facts = {f['fact_id']: f for f in gold['facts']}
    assert len(facts) == len(gold['facts']), 'duplicate fact'
    def span(p, quote_key='quote'):
        s = segments[p['segment_id']]
        assert p['ordinal'] == s['ordinal'], 'span ordinal mismatch'
        assert 0 <= p['start'] < p['end'] <= len(s['text']), 'invalid codepoint span'
        assert s['text'][p['start']:p['end']] == p[quote_key], 'quote mismatch'
    for f in facts.values():
        assert 1 <= f['valid_from_ordinal'] <= len(segments), 'invalid reveal'
        for p in f['provenance']:
            span(p)
            assert p['ordinal'] <= f['valid_from_ordinal'], 'future evidence'
        assert max(p['ordinal'] for p in f['provenance']) == f['valid_from_ordinal'], 'unjustified reveal'
    assert gold['horizons'] == horizons(gold['facts'], len(segments)), 'horizon leak or incomplete prefix'
    entities = {e['entity_id'] for e in gold['entities']}
    assert len(entities) == len(gold['entities']), 'duplicate entity'
    for entity in gold['entities']:
        for p in entity['mentions']: span(p, 'text')
    for c in gold['identity_constraints']:
        assert c['left'] in entities and c['right'] in entities and c['left'] != c['right'], 'invalid identity pair'
        for p in c['provenance']: span(p)
        assert max(p['ordinal'] for p in c['provenance']) == c['valid_from_ordinal'], 'identity horizon'
    for t in gold['transitions']:
        claim = facts[t['claim_fact_id']]
        assert claim['epistemic_status'] == 'CLAIMED', 'transition is not a claim'
        assert claim['valid_from_ordinal'] < t['ordinal'] <= len(segments), 'transition horizon'
        assert t['from_status'] == 'CLAIMED', 'invalid transition origin'
        assert t['target'] == {k:claim[k] for k in ('subject','relation','object','layer')}, 'transition target mismatch'
        for fid in t['evidence_fact_ids']:
            assert facts[fid]['valid_from_ordinal'] <= t['ordinal'], 'transition uses future evidence'
    return True

def load_cases(source=SOURCE):
    result = []
    for path in sorted((source / 'inputs').glob('*.json')):
        inp = json.loads(path.read_text())
        gold = json.loads((source / 'gold' / path.name).read_text())
        validate_pair(inp, gold)
        result.append((inp, gold))
    assert result, 'empty benchmark'
    assert {p.name for p in (source/'gold').glob('*.json')} == {p.name for p in (source/'inputs').glob('*.json')}, 'orphan gold'
    return result

def expand(inp, gold, size, distractors):
    assert size >= len(inp['segments']) and distractors >= 1, 'invalid stress parameters'
    inp, gold = copy.deepcopy(inp), copy.deepcopy(gold)
    base = inp['case_id']
    cid = f'{base}-n{size:03d}-d{distractors:03d}'
    inp['case_id'] = gold['case_id'] = cid
    mapping = {i: 1 + (i - 1) * (size - 1) // (len(inp['segments']) - 1) for i in range(1,len(inp['segments'])+1)}
    for f in gold['facts']:
        f['valid_from_ordinal'] = mapping[f['valid_from_ordinal']]
    for collection in [gold['facts'], gold['identity_constraints']]:
        for item in collection:
            if 'valid_from_ordinal' in item and collection is gold['identity_constraints']:
                item['valid_from_ordinal'] = mapping[item['valid_from_ordinal']]
            for p in item['provenance']:
                p['ordinal'] = mapping[p['ordinal']]
                p['segment_id'] = f"s{p['ordinal']:03d}"
    for e in gold['entities']:
        for p in e['mentions']:
            p['ordinal'] = mapping[p['ordinal']]
            p['segment_id'] = f"s{p['ordinal']:03d}"
    for t in gold['transitions']: t['ordinal'] = mapping[t['ordinal']]
    targets = {}
    for s in inp['segments']:
        s['ordinal'] = mapping[s['ordinal']]
        s['segment_id'] = f"s{s['ordinal']:03d}"
        targets[s['ordinal']] = s
    segments=[]
    for i in range(1,size+1):
        if i in targets:
            segments.append(targets[i]); continue
        texts=[]; start=0
        subject = f'T{max((n for n in range(1,i) if n not in targets), default=0):03d}'
        obj = f'T{i:03d}'
        text = {'en': f'The supplementary case ledger links trace station {subject} to trace station {obj}.', 'zh-Hans': f'案件补充记录确认线索站{subject}连接线索站{obj}。', 'ja': f'事件の補足記録は手掛かり地点{subject}と地点{obj}の接続を確認した。'}[inp['language']]
        texts.append(text)
        gold['facts'].append(dict(fact_id=f't{i:03d}',kind='assertion',subject=subject,relation='links_to',object=obj,layer='OUTER',epistemic_status='OBSERVED',valid_from_ordinal=i,qualifier={},critical=False,cross_segment=True,distractor=False,provenance=[dict(segment_id=f's{i:03d}',ordinal=i,start=0,end=len(text),quote=text)]))
        start = len(text)+1
        for j in range(1,distractors+1):
            subject=f'R{i:03d}-{j:03d}'
            obj=f'C{i:03d}-{j:03d}'
            text = {'en': f'Spare brush {subject} is stored in cabinet {obj}.', 'zh-Hans': f'备用刷子{subject}存放在{obj}柜。', 'ja': f'予備のブラシ{subject}は棚{obj}に保管されている。'}[inp['language']]
            texts.append(text)
            gold['facts'].append(dict(fact_id=f'd{i:03d}_{j:03d}',kind='distractor',subject=subject,relation='stored_in',object=obj,layer='OUTER',epistemic_status='OBSERVED',valid_from_ordinal=i,qualifier={},critical=False,cross_segment=False,distractor=True,provenance=[dict(segment_id=f's{i:03d}',ordinal=i,start=start,end=start+len(text),quote=text)]))
            start += len(text)+1
        segments.append(dict(segment_id=f's{i:03d}',ordinal=i,text=' '.join(texts)))
    inp['segments']=segments
    # Generated endpoint identities are explicit slots, not inferred graph nodes.
    stress_entities = {}
    for fact in gold['facts']:
        if fact['fact_id'].startswith(('t', 'd')):
            p = fact['provenance'][0]
            text = segments[p['ordinal']-1]['text']
            for label in (fact['subject'], fact['object']):
                entity = stress_entities.setdefault(label, dict(entity_id='stress_'+label, name=label, aliases=[], layer='OUTER', mentions=[]))
                start = text.index(label, p['start'], p['end'])
                mention = dict(segment_id=p['segment_id'],ordinal=p['ordinal'],start=start,end=start+len(label),text=label)
                if mention not in entity['mentions']: entity['mentions'].append(mention)
    gold['entities'].extend(stress_entities[key] for key in sorted(stress_entities))
    gold['horizons']=horizons(gold['facts'],size)
    validate_pair(inp,gold)
    return inp,gold,dict(base_case_id=base,source_ordinals={str(k):v for k,v in mapping.items()},distractors_per_filler_segment=distractors,relevant_facts_per_filler_segment=1,target_clue_distance_segments=mapping[6]-mapping[1])

def export(output, sizes=(24,48), distractors=1, source=SOURCE):
    cases=load_cases(source)
    entries=[]
    for inp,gold in cases:
        variants=[(inp,gold,dict(base_case_id=inp['case_id'],source_ordinals={str(i):i for i in range(1,len(inp['segments'])+1)},distractors_per_filler_segment=0,relevant_facts_per_filler_segment=0,target_clue_distance_segments=len(inp['segments'])-1))]
        variants += [expand(inp,gold,size,distractors) for size in sizes]
        for visible,answers,meta in variants:
            entry=dict(case_id=visible['case_id'],language=visible['language'],segment_count=len(visible['segments']),**meta)
            for name,value in [('input',visible),('gold',answers)]:
                rel=f"{name}s/{visible['case_id']}.json" if name=='input' else f"gold/{visible['case_id']}.json"
                path=output/rel;path.parent.mkdir(parents=True,exist_ok=True);data=encoded(value);path.write_bytes(data)
                entry[name+'_path']=rel;entry[name+'_sha256']=hashlib.sha256(data).hexdigest()
            entries.append(entry)
    manifest=dict(schema_version=1,license='CC0-1.0',span_unit='UNICODE_CODEPOINT',span_interval='HALF_OPEN',text_normalization='NONE',cases=entries)
    if source != SOURCE:
        manifest['source_sha256'] = hashlib.sha256(encoded(cases)).hexdigest()
        manifest['cohort'] = 'heldout-v1'
    (output/'manifest.json').write_bytes(encoded(manifest))
    return manifest

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action',choices=['validate','export'])
    parser.add_argument('--source',type=Path,default=SOURCE)
    parser.add_argument('--output',type=Path)
    parser.add_argument('--stress-segments',default='24,48')
    parser.add_argument('--distractors',type=int,default=1)
    args=parser.parse_args()
    if args.action=='validate':
        print(f'Validated {len(load_cases(args.source))} graph-memory cases')
    else:
        if args.output is None:parser.error('--output is required')
        sizes=tuple(int(s) for s in args.stress_segments.split(',') if s)
        assert len(set(sizes))==len(sizes), 'duplicate stress size'
        manifest=export(args.output,sizes,args.distractors,args.source)
        print(f"Exported {len(manifest['cases'])} cases; model inputs and gold are separate")
if __name__=='__main__':main()
