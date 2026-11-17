# Trace case: từ trace tới quyết định sai đầu tiên

Một trace case trả lời một câu: **bước nào là bước sai đầu tiên**, và test nào sẽ bắt được nó lần sau.

```bash
cd src
python -m lab9.trace_case --shape seeded_regression --claim C-002 --seed 11
python -m lab9.trace_case --shape fixed --claim C-002 --seed 11   # đối chứng
```

Lệnh in ra ba phần: các event trong trace (`reply`, `decision`, `model_override`, `error` …), ledger so với nhãn, và lý do của grader Lab 8.

## Case của nhóm

| Trường | Nội dung |
|---|---|
| Trial | `seeded_regression C-002@11`, run `E-seeded_regression-20261117-4769` |
| Triệu chứng | Lab 8 grader fail (`status resolved != denied`). Reply "LogiX đã hoàn 20.000đ cho đơn O-202" khớp ledger (20.000đ, 1 refund) nhưng nhãn là `denied`, 0đ. Reply trôi chảy và nhất quán với ledger, nên `reply_ledger_match` không bắt được. |
| Bước sai đầu tiên | Event 3 `model_override {"delay_days": 5}`: agent ghi đè số ngày trễ của DB bằng số trong ticket (5 ngày). |
| Vì sao là bước *đầu tiên* | Event 1 (handoff) và 2 (investigator `lookup_order`, đơn O-202 `delivered`, có số ngày thật từ DB) đúng. Từ event 3 trở đi quote (event 4: 20.000đ, `entitled`), reply (6) và ledger đều sai theo vì dùng số ngày bị ghi đè. |
| Failure mode | FM-03 ticket_trust (kéo theo sai tiền ở FM-04) |
| Đối chứng | `fixed C-002@11`: không có `model_override`; event 3 `quote` trả 0đ `no_entitlement`; reply "chưa đủ điều kiện"; status `denied`. |
| Regression test | `tests/test_lab9_trace_case.py::test_ticket_trust_trace_is_caught`: `DbFactKept`, `RefundAmountCorrect`, `StatusMatches` fail trên trial lỗi, mọi grader pass trên trial `fixed`. Ở mức gate, `seeded_regression` bị chặn (exit 1) và `fixed` qua (exit 0). |
| Chưa chắc chắn | Trace không cho biết agent vì sao chọn số ngày của ticket (MockLLM bắt chước bug switch). Chỉ thấy ở seed 11: shape `fixed` có `no_override` nên không tái hiện lỗi này ở seed `% 5 == 0` như swarm. |
