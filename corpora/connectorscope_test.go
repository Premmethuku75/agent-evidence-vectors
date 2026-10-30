package corpora_test

import "testing"

func TestConnectorScopeCommittedCorpusIsClean(t *testing.T) {
	rcCommittedCorpusIsClean(t, "vectors-connector-scope", 4, 9)
}

func TestConnectorScopeReaderDerivesRatherThanEchoes(t *testing.T) {
	rcReaderDerivesRatherThanEchoes(t, "vectors-connector-scope")
}
