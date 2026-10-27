package corpora

// The optional sequence member (revision 01): a numbered series a producer
// issues, named by boundary, with a seq that starts at 1 and rises by one.

// arSequenceChecks names each sentence of the sequence rule so a test can drop
// one and see the member that tests it fail.
var arSequenceChecks = map[string]bool{"members": true, "positive": true}

// arRuleSequence: exactly boundary, a non-empty string, and seq, a positive
// integer (SQ1). Any other member (SQ2) or a seq below 1 (SQ3) is refused.
func arRuleSequence(s *arState) error {
	raw, present := s.pred["sequence"]
	if !present {
		return nil
	}
	sequence, ok := raw.(map[string]any)
	if !ok {
		return arRefuse("sequence-malformed")
	}
	if arSequenceChecks["members"] && len(sequence) != 2 {
		return arRefuse("sequence-malformed")
	}
	boundary, ok := sequence["boundary"].(string)
	if !ok || boundary == "" {
		return arRefuse("sequence-malformed")
	}
	seq, ok := arInt(sequence["seq"])
	if !ok || (arSequenceChecks["positive"] && seq < 1) {
		return arRefuse("sequence-malformed")
	}
	return nil
}
