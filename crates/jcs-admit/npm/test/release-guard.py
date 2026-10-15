#!/usr/bin/env python3
"""Synthetic mutation controls for release validation; no publication claim."""
import base64
import copy
import hashlib
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tarfile
import tempfile

NPM = Path(__file__).resolve().parents[1]
ROOT = NPM.parent


def main():
    receipts = Path(os.environ.get('JCS_TEST_RECEIPTS',NPM/'test-results'))/'release-guard'
    receipts.mkdir(parents=True,exist_ok=True)
    original = {str(p.relative_to(NPM/'dist')):p.read_bytes() for p in (NPM/'dist').rglob('*') if p.is_file()}
    commit = 'f'*40
    build = json.loads(original['BUILD.json'])
    # A synthetic clean identity lets these controls run independently of the
    # actual Node/browser qualification. It is never a release receipt.
    build.update(source_commit=commit,source_dirty=False)
    original['BUILD.json'] = json.dumps(build).encode()
    mutations = [
        ('positive',None,None),
        ('metadata-exports','metadata','Release manifest differs from the exact source transform.'),
        ('metadata-provenance','provenance','Release manifest differs from the exact source transform.'),
        ('metadata-boolean-type','boolean-type','Release manifest differs from the exact source transform.'),
        ('unexpected-member','member','Packed file set differs from the build manifest.'),
        ('dot-component','dot','Packed member name is not canonical.'),
        ('parent-component','parent','Packed member name is not canonical.'),
        ('duplicate-slash','slash','Packed member name is not canonical.'),
        ('backslash','backslash','Packed names must use the package/ POSIX prefix.'),
        ('source-subset','subset','Source input population or identity differs.'),
    ]
    outcomes=[]
    for label,mutation,message in mutations:
        files=copy.deepcopy(original)
        metadata=json.loads(files['package.json'])
        record=json.loads(files['BUILD.json'])
        if mutation=='metadata':
            metadata['exports']['.']['node']['default']='./lib/altered.mjs'
            files['package.json']=json.dumps(metadata).encode()
        elif mutation=='provenance':
            metadata['publishConfig']['provenance']=False
            files['package.json']=json.dumps(metadata).encode()
        elif mutation=='boolean-type':
            metadata['publishConfig']['provenance']=1
            files['package.json']=json.dumps(metadata).encode()
        elif mutation=='member':
            files['extra.mjs']=b'export const unexpected = true;\n'
        elif mutation=='subset':
            removed=sorted(record['source_files'])[0]
            del record['source_files'][removed]
            record['source_sha256']=hashlib.sha256(json.dumps(record['source_files'],sort_keys=True,separators=(',',':')).encode()).hexdigest()
        # Rehash altered package bytes and the outer report. A refusal must
        # establish source/population/metadata rules, not just notice old hashes.
        record['artifact_files']={name:hashlib.sha256(data).hexdigest() for name,data in files.items() if name!='BUILD.json'}
        files['BUILD.json']=json.dumps(record).encode()
        with tempfile.TemporaryDirectory(prefix='jcs-release-control-') as temporary:
            directory=Path(temporary)
            artifact=directory/'jcs-admit-0.1.0.tgz'
            with tarfile.open(artifact,'w:gz') as archive:
                for name,data in sorted(files.items()):
                    member='package/'+name
                    if name=='lib/api.mjs':
                        if mutation=='dot':member='package/./lib/api.mjs'
                        elif mutation=='parent':member='package/lib/../lib/api.mjs'
                        elif mutation=='slash':member='package//lib/api.mjs'
                        elif mutation=='backslash':member='package/lib\\api.mjs'
                    entry=tarfile.TarInfo(member)
                    entry.size=len(data)
                    archive.addfile(entry,io.BytesIO(data))
            data=artifact.read_bytes()
            report={'nativeExit':0,'node':[{'synthetic':True}],'browser':{'synthetic':True},'typescript':{'synthetic':True},'steps':[],
                    'tarball':{'filename':artifact.name,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'integrity':'sha512-'+base64.b64encode(hashlib.sha512(data).digest()).decode()}}
            (directory/'RESULT.json').write_text(json.dumps(report))
            p=subprocess.run([sys.executable,str(NPM/'check_release.py'),str(directory),'--commit',commit],cwd=ROOT,capture_output=True)
            (receipts/(label+'.stdout')).write_bytes(p.stdout)
            (receipts/(label+'.stderr')).write_bytes(p.stderr)
            expected=0 if mutation is None else 1
            passed=p.returncode==expected and (mutation is None or p.stderr.decode().strip()==message)
            outcomes.append({'control':label,'native_exit':p.returncode,'expected_exit':expected,'expected_guard':message,'passed':passed,'tarball_sha256':hashlib.sha256(data).hexdigest()})
    result={'scope':'Synthetic release-guard mutation controls only; not native/WASM consumer qualification, clean-source proof or publication.','controls':outcomes,'native_exit':0 if all(r['passed'] for r in outcomes) else 1}
    (receipts/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result))
    raise SystemExit(result['native_exit'])


if __name__=='__main__':
    main()
