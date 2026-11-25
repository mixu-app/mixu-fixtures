# SPDX-License-Identifier: Apache-2.0
"""Independent invariant and negative-path checks for the segmented benchmark."""
import copy
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parent.parent
spec=importlib.util.spec_from_file_location('graph_memory',ROOT/'tools/graph_memory.py')
gm=importlib.util.module_from_spec(spec);spec.loader.exec_module(gm)

class GraphMemoryTest(unittest.TestCase):
    def test_authored_coverage_and_critical_evidence(self):
        cases=gm.load_cases()
        self.assertEqual(6,len(cases))
        self.assertEqual({'en':2,'ja':2,'zh-Hans':2},{lang:sum(i['language']==lang for i,g in cases) for lang in ('en','ja','zh-Hans')})
        self.assertEqual(6,len({g['scenario'] for i,g in cases}))
        for inp,gold in cases:
            self.assertEqual(6,len(inp['segments']))
            self.assertTrue(any(f['critical'] for f in gold['facts']))
            self.assertTrue(gold['horizons'][0]['forbidden_fact_ids'])
            self.assertFalse(gold['horizons'][-1]['forbidden_fact_ids'])

    def test_cli_rejects_actual_horizon_leak(self):
        with tempfile.TemporaryDirectory() as tmp:
            source=Path(tmp)/'corpus';shutil.copytree(gm.SOURCE,source)
            path=source/'gold/gm-en-01.json';gold=json.loads(path.read_text())
            gold['horizons'][0]['forbidden_fact_ids'].append('f1')
            path.write_text(json.dumps(gold))
            run=subprocess.run([sys.executable,str(ROOT/'tools/graph_memory.py'),'validate','--source',str(source)],capture_output=True,text=True)
            self.assertNotEqual(0,run.returncode)
            self.assertIn('horizon leak',run.stderr)

    def test_bad_quotes_future_transition_and_input_gold_are_rejected(self):
        inp,gold=next((i,g) for i,g in gm.load_cases() if i['case_id']=='gm-en-01')
        bad=copy.deepcopy(gold);bad['facts'][0]['provenance'][0]['end']-=1
        with self.assertRaises(AssertionError):gm.validate_pair(inp,bad)
        bad=copy.deepcopy(gold);bad['transitions'][0]['evidence_fact_ids']=['f7']
        with self.assertRaises(AssertionError):gm.validate_pair(inp,bad)
        bad_input=copy.deepcopy(inp);bad_input['gold']=gold
        with self.assertRaises(Exception):gm.validate_pair(bad_input,gold)

    def test_stress_adds_relevant_chain_and_explicit_distractors(self):
        for inp,gold in gm.load_cases():
            for size in (24,48):
                visible,answers,meta=gm.expand(inp,gold,size,2)
                self.assertEqual(size,len(visible['segments']))
                self.assertEqual(size-1,meta['target_clue_distance_segments'])
                added=[f for f in answers['facts'] if f['kind']=='distractor']
                self.assertEqual((size-6)*2,len(added))
                chain=[f for f in answers['facts'] if f['relation']=='links_to']
                self.assertEqual(size-6,len(chain))
                entity_labels={e.get('name') for e in answers['entities']}
                self.assertIn('T000',entity_labels)
                for f in chain+added:
                    self.assertIn(f['subject'],entity_labels)
                    self.assertIn(f['object'],entity_labels)
                if inp['language']=='en':self.assertTrue(all(f['provenance'][0]['quote'].startswith('Spare brush R') for f in added))
                for left,right in zip(chain,chain[1:]):self.assertEqual(left['object'],right['subject'])
                self.assertEqual([f['fact_id'] for f in gold['facts']],[f['fact_id'] for f in answers['facts'][:len(gold['facts'])]])
                self.assertTrue(all(set(s)=={'segment_id','ordinal','text'} for s in visible['segments']))

    def test_deterministic_export_hashes_isolate_model_inputs(self):
        import hashlib
        with tempfile.TemporaryDirectory() as a,tempfile.TemporaryDirectory() as b:
            ma=gm.export(Path(a),(24,48),2);mb=gm.export(Path(b),(24,48),2)
            self.assertEqual(ma,mb)
            self.assertEqual(18,len(ma['cases']))
            for case in ma['cases']:
                for kind in ('input','gold'):
                    data=(Path(a)/case[kind+'_path']).read_bytes()
                    self.assertEqual(data,(Path(b)/case[kind+'_path']).read_bytes())
                    self.assertEqual(case[kind+'_sha256'],hashlib.sha256(data).hexdigest())
                visible=json.loads((Path(a)/case['input_path']).read_text())
                self.assertEqual({'schema_version','case_id','language','segments'},set(visible))

    def test_nested_layer_and_claim_status_boundaries(self):
        cases={i['case_id']:(i,g) for i,g in gm.load_cases()}
        facts={f['fact_id']:f for f in cases['gm-en-02'][1]['facts']}
        self.assertEqual('INNER:loop1',facts['f2']['layer'])
        self.assertEqual('OUTER',facts['f3']['layer'])
        self.assertEqual('INNER:loop2',facts['f4']['layer'])
        claim=cases['gm-en-01'][1]
        self.assertEqual(['RETRACTED','CORROBORATED'],[t['to_status'] for t in claim['transitions']])
        self.assertEqual('CLAIMED',claim['facts'][0]['epistemic_status'])


    def test_heldout_has_multi_source_role_resolution_without_current_named_answer(self):
        source=ROOT/'fixtures/benchmarks/graph-memory-heldout'
        cases=gm.load_cases(source)
        self.assertEqual(3,len(cases))
        self.assertEqual({'en','ja','zh-Hans'},{i['language'] for i,g in cases})
        for inp,gold in cases:
            self.assertEqual(12,len(inp['segments']))
            cross=[f for f in gold['facts'] if len(f['provenance'])>1]
            self.assertGreaterEqual(len(cross),4)
            signatures=[(f['subject'],f['relation'],f['object'],f['layer'],f['epistemic_status'],json.dumps(f['qualifier'],sort_keys=True)) for f in gold['facts']]
            self.assertEqual(len(signatures),len(set(signatures)))
            confirmation=next(f for f in gold['facts'] if f['fact_id']=='f10')
            self.assertEqual('confirms',confirmation['relation'])
            self.assertTrue(confirmation['critical'])
            role_name=gold['entities'][0]['name']
            late=[f for f in cross if f['subject']==role_name and f['valid_from_ordinal']>=6]
            self.assertTrue(late)
            for fact in late:
                self.assertNotIn(role_name,inp['segments'][fact['valid_from_ordinal']-1]['text'])
                self.assertTrue(any(p['ordinal']<fact['valid_from_ordinal'] for p in fact['provenance']))
            revision=gold['transitions'][0]
            evidence=next(f for f in gold['facts'] if f['fact_id']==revision['evidence_fact_ids'][-1])
            self.assertTrue(any(p['ordinal']<revision['ordinal'] for p in evidence['provenance']))

    def test_heldout_export_is_separate_and_no_stress_is_implicitly_added(self):
        source=ROOT/'fixtures/benchmarks/graph-memory-heldout'
        with tempfile.TemporaryDirectory() as tmp:
            manifest=gm.export(Path(tmp),(),1,source)
            self.assertEqual('heldout-v1',manifest['cohort'])
            self.assertEqual(64,len(manifest['source_sha256']))
            self.assertEqual(3,len(manifest['cases']))
            self.assertEqual({12},{c['segment_count'] for c in manifest['cases']})

if __name__=='__main__':unittest.main()
