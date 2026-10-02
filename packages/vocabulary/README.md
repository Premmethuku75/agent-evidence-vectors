# agent-evidence-vocabulary

A closed, versioned vocabulary for claims about an agent's execution: what it attempted, what the
system beneath it observed or refused, how directly and from what vantage the claim was obtained,
and how much of a population the claim covers.

It's for anyone who writes a predicate, a verifier or an evidence format for agents and needs each
term to mean one thing across vendors, including teams who want to map their own fields onto it.

## Quick start

Pin the registry at a release and check its digest:

```bash
curl -fsSLO https://raw.githubusercontent.com/probityai/agent-evidence-vocabulary/v0.3.0/vocabulary.yaml
echo "b21bbff810e86b59ceec9b9569a5cf44409affb8d61acd412f1af87474fd3f4c  vocabulary.yaml" | sha256sum -c
```

Then read a term:

```bash
pip install PyYAML==6.0.3
python3 -c 'import yaml; v = yaml.safe_load(open("vocabulary.yaml")); print(v["evidence_dimensions"]["observation_vantage"]["values"])'
```

It prints `['substrate', 'artifact']`. Every term carries a definition, its allowed values and a
lifecycle status.

To map your own system's fields onto the vocabulary, copy
[`crosswalk/TEMPLATE.yaml`](https://github.com/probityai/agent-evidence-vocabulary/blob/main/crosswalk/TEMPLATE.yaml)
and run `python3 scripts/validate_crosswalks.py` before opening a pull request.

## Status

Release v0.3.0, tagged September 25, 2026. The registry file is CC0-1.0, and the rest of the
repository is Apache-2.0. Every term starts as proposed and is promoted only when an independent
system emits it; the rules are in
[GOVERNANCE.md](https://github.com/probityai/agent-evidence-vocabulary/blob/main/GOVERNANCE.md).
The first crosswalk came from aee-e2, an independent implementation of the Adversarial Execution
Evidence predicate, in
[pull request 2](https://github.com/probityai/agent-evidence-vocabulary/pull/2).

## Documentation

| page | read it for |
| --- | --- |
| <a name="why-this-exists"></a><a name="files"></a><a name="companion-project"></a>[About the vocabulary](https://github.com/probityai/agent-evidence-vocabulary/blob/main/docs/ABOUT.md) | why it exists, what each file is for, and how the term set was chosen |
| [vocabulary.yaml](https://github.com/probityai/agent-evidence-vocabulary/blob/main/vocabulary.yaml) | the registry itself |
| [Proposed OpenCRE links](https://github.com/probityai/agent-evidence-vocabulary/blob/main/docs/OPENCRE.md) | three relying-party checks with pinned accepting and rejecting examples |
| [GOVERNANCE.md](https://github.com/probityai/agent-evidence-vocabulary/blob/main/GOVERNANCE.md) and [CONTRIBUTING.md](https://github.com/probityai/agent-evidence-vocabulary/blob/main/CONTRIBUTING.md) | the promotion rules, and how to file a crosswalk |
| [agent-evidence-vectors](https://github.com/probityai/agent-evidence-vectors) | the predicate specification and conformance vectors this vocabulary describes |
