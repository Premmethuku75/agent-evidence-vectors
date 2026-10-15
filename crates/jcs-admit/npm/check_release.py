#!/usr/bin/env python3
"""Verify the tested tarball and exact source inputs before npm publication."""
import argparse
import base64
import hashlib
import json
from pathlib import Path
import tarfile
from artifact import artifact_population, copied_files, member_path, published_manifest_bytes, source_identity

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('receipts', type=Path)
    parser.add_argument('--commit', required=True)
    args = parser.parse_args()
    report = json.loads((args.receipts/'RESULT.json').read_text())
    if report['nativeExit'] != 0 or not report.get('browser') or not report.get('typescript'):
        raise SystemExit('Packed consumer qualification is incomplete.')
    if not report.get('node') or any(step['nativeExit'] != 0 for step in report['steps']):
        raise SystemExit('A packed consumer step did not pass.')
    package = report['tarball']
    name = package['filename']
    if Path(name).name != name:
        raise SystemExit('Unexpected packed filename.')
    artifact = args.receipts/name
    data = artifact.read_bytes()
    integrity = 'sha512-' + base64.b64encode(hashlib.sha512(data).digest()).decode()
    if len(data) != package['bytes'] or hashlib.sha256(data).hexdigest() != package['sha256'] or integrity != package['integrity']:
        raise SystemExit('Qualified tarball digest differs.')
    files = {}
    with tarfile.open(artifact) as archive:
        for member in archive:
            if not member.isreg():
                raise SystemExit('Unexpected packed member.')
            try:
                name = member_path(member.name)
            except ValueError as error:
                raise SystemExit(str(error)) from error
            if name in files:
                raise SystemExit('Duplicate packed member.')
            files[name] = archive.extractfile(member).read()
    build = json.loads(files['BUILD.json'])
    if build['source_commit'] != args.commit or build['source_dirty'] is not False:
        raise SystemExit('Release source identity is not a clean exact commit.')
    population = artifact_population(ROOT)
    if set(files) != population | {'BUILD.json'} or set(build['artifact_files']) != population:
        raise SystemExit('Packed file set differs from the build manifest.')
    for name, expected in build['artifact_files'].items():
        if hashlib.sha256(files[name]).hexdigest() != expected:
            raise SystemExit('Packed file differs: '+name)
    source_files,source_sha256 = source_identity(ROOT)
    if build['source_files'] != source_files or build['source_sha256'] != source_sha256:
        raise SystemExit('Source input population or identity differs.')
    for name,path in copied_files(ROOT).items():
        if files[name] != path.read_bytes():
            raise SystemExit('Copied source file differs: '+name)
    manifest = json.loads(files['package.json'])
    if files['package.json'] != published_manifest_bytes(ROOT) or manifest.get('scripts') or manifest.get('dependencies'):
        raise SystemExit('Release manifest differs from the exact source transform.')
    print(json.dumps({'tarball':str(artifact),'sha256':package['sha256'],'integrity':integrity,'source_commit':args.commit,'source_sha256':build['source_sha256'],'native_exit':0}))


if __name__ == '__main__':
    main()
