package corpora

import "regexp"

func init() { register(connectorScope()) }

var csPHI = []*regexp.Regexp{
	regexp.MustCompile(`\b\d{3}-\d{2}-\d{4}\b`),
	regexp.MustCompile(`(?i)\bmrn[:=]?\s*\d{5,}`),
	regexp.MustCompile(`(?i)\bdob[:=]`),
	regexp.MustCompile(`\b(19|20)\d{2}-\d{2}-\d{2}\b.*(?i:born)`),
}

func csIn(r any, kind string) bool {
	scope := rcMap(rcGet(r, "connector.declared_scope"))
	return rcStringSet(scope[kind])[rcStr(rcGet(r, "action.resource"))]
}

func csPermitted(r any) bool {
	kind := rcStr(rcGet(r, "action.kind"))
	return (kind == "read" || kind == "change") && csIn(r, kind)
}

func csPerformed(r any) bool { return rcGet(r, "outcome.result") == "performed" }

// connectorScope judges vectors-connector-scope/: one action against the scope a
// health-system connector was granted. The rules and their order are those of
// packaging/agent_evidence_vectors/connectorscope.py.
func connectorScope() ruleCorpus {
	return ruleCorpus{suite: "connector-scope-record/v1", accept: "scope_respected", rules: []rcRule{
		{"scope_declaration_missing", func(r any) bool {
			scope := rcMap(rcGet(r, "connector.declared_scope"))
			_, read := scope["read"]
			_, change := scope["change"]
			return scope == nil || !read || !change
		}},
		{"grant_digest_mismatch", func(r any) bool {
			return rcStr(rcGet(r, "connector.grant_digest")) != rcDigest(rcGet(r, "connector.declared_scope"))
		}},
		{"fixture_not_phi_free", func(r any) bool {
			text, err := pythonCompactJSON(r)
			if err != nil {
				return true
			}
			for _, p := range csPHI {
				if p.Match(text) {
					return true
				}
			}
			return !rcTrue(rcGet(r, "fixture.phi_free"))
		}},
		{"change_performed_under_read_grant", func(r any) bool {
			return rcGet(r, "action.kind") == "change" && csPerformed(r) && !csIn(r, "change") && csIn(r, "read")
		}},
		{"out_of_scope_action_performed", func(r any) bool { return csPerformed(r) && !csPermitted(r) }},
		{"in_scope_action_refused_as_out_of_scope", func(r any) bool {
			return rcGet(r, "outcome.result") == "refused" && csPermitted(r) && rcGet(r, "outcome.reason") == "out_of_scope"
		}},
		{"refusal_not_recorded", func(r any) bool {
			return rcGet(r, "outcome.result") == "refused" && !csPermitted(r) &&
				!(rcStr(rcGet(r, "outcome.reason")) != "" && rcStr(rcGet(r, "outcome.refusal_recorded_by")) != "")
		}},
		{"action_digest_mismatch", func(r any) bool {
			return rcStr(rcGet(r, "record.action_digest")) != rcDigest(rcGet(r, "action"))
		}},
	}}
}
