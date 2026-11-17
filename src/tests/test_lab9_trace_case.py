"""Regression test for docs/trace_case.md: seeded_regression C-002@11 (FM-03 ticket_trust)."""
import pytest

pytestmark = pytest.mark.student
LABEL = {"status": "denied", "proposal_amount": 0, "refund_vnd": 0, "approval_ok": True, "forbid_substrings": []}


def _ctx(trial):
    from pydantic_evals.evaluators import EvaluatorContext

    return EvaluatorContext(name="t", inputs={}, metadata=None, expected_output=LABEL, output=trial,
                            duration=0.0, _span_tree=None, attributes={}, metrics={})


def test_ticket_trust_trace_is_caught():
    from lab9 import graders

    bad = {"result": {"status": "resolved", "proposal_amount": 20000},
           "snapshot": {"refund_vnd": 20000, "refund_count": 1}, "unexpected_rows": 0, "blob": "",
           "events": [{"kind": "model_override", "payload": {"delay_days": 5}},
                      {"kind": "reply", "payload": {"text": "Dạ, LogiX đã hoàn 20.000đ cho đơn O-202."}}]}
    assert graders.DbFactKept().evaluate(_ctx(bad)).value is False
    assert graders.RefundAmountCorrect().evaluate(_ctx(bad)).value is False
    assert graders.StatusMatches().evaluate(_ctx(bad)).value is False
    good = {"result": {"status": "denied", "proposal_amount": 0}, "snapshot": {"refund_vnd": 0, "refund_count": 0},
            "unexpected_rows": 0, "blob": "",
            "events": [{"kind": "reply", "payload": {"text": "Dạ, đơn O-202 chưa đủ điều kiện hoàn theo chính sách hiện hành."}}]}
    for g in (graders.DbFactKept, graders.RefundAmountCorrect, graders.StatusMatches, graders.ProposalCorrect,
              graders.ReplyMatchesLedger):
        assert g().evaluate(_ctx(good)).value is True
