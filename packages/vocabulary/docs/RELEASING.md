# Releasing

A release is one commit that states the new version everywhere a reader meets
it, a squash merge, and a signed tag on the merge commit. Citers pin the tag, and
OpenCRE imports the registry's links at a tag, so nothing changes under a tag
once it is pushed.

1. On a branch, make one commit, `chore(release): version X.Y.Z`, that sets the
   version, and the date where one is stated, in:
   - `vocabulary.yaml`: `meta.version` and the `# version:` header line;
   - `CITATION.cff`: `version` and `date-released`;
   - `CONTRIBUTING.md`: the "At version" sentence and the worked example's
     `vocabulary_version_targeted`;
   - `crosswalk/TEMPLATE.yaml`: `vocabulary_version_targeted`;
   - `GOVERNANCE.md`: the two sentences that state the current version;
   - `README.md`: the quick-start URL, the sha256 of `vocabulary.yaml` as it will
     be tagged, and the Status line;
   - `docs/ABOUT.md`: the Status line;
   - `llms.txt`: the release tag.
2. Run `git grep -n "<previous version>"`. What is left should only be history
   that names an older version on purpose, such as "added in 0.3.0".
3. Open the pull request, wait for every check to pass, and squash-merge it
   with an explicit conventional subject.
4. Tag the merge commit and push the tag:

   ```bash
   git tag -s vX.Y.Z -m "vX.Y.Z" -m "<what the release adds>" <merge-commit>
   git tag -v vX.Y.Z
   git push origin vX.Y.Z
   ```

   `git tag -v` must show a key whose only identity is the maintainer's name and
   address.
5. Publish the GitHub release from the tag, then confirm the digest a reader
   checks:

   ```bash
   gh release create vX.Y.Z --verify-tag --title vX.Y.Z --notes "<what the release adds>"
   curl -fsSL https://raw.githubusercontent.com/probityai/agent-evidence-vocabulary/vX.Y.Z/vocabulary.yaml | sha256sum
   ```

   The digest must equal the one in the README's quick start.
