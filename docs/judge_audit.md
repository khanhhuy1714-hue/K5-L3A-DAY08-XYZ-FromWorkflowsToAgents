# Judge audit

Chạy: `python -m lab9.judge --csv <file> --audit 5`

| Tiêu chí | n | κ | Precision | Recall | Đạt FLOORS (κ≥0.6, P≥0.8, R≥0.7)? | Quyết định |
|---|---|---|---|---|---|---|
| tone_ok | 100 | 0.757 | 0.857 | 0.800 | Có (tp 24, fp 4, fn 6, tn 66) | dùng (kèm cảnh báo bên dưới) |
| helpful | 100 | 0.375 | 1.000 | 0.300 | Không: κ và recall đều dưới sàn (tp 9, fp 0, fn 21, tn 70) | loại |

## ≥5 case audit thủ công
| # | Case | Judge nói | Người nói | Ai đúng? | Ghi chú |
|---|---|---|---|---|---|
| 1 | H-008 "Em đã hoàn tiền cho anh rồi nha" | PASS | FAIL | Người | Xưng "em" + "nha" quá suồng sã; judge nhầm sự thân thiện với đúng giọng. |
| 2 | H-017 "bạn ơi ... rồi nha" | PASS | FAIL | Người | Xưng "bạn" với khách lớn tuổi; cùng kiểu lỗi với #1. |
| 3 | H-029 "không cần nhắn thêm" | PASS | FAIL | Người | Giọng ra lệnh; judge chỉ thấy "Dạ, vui lòng". |
| 4 | H-042 "đã hoàn 120.000đ ... 3–5 ngày ạ" | FAIL | PASS | Người | Ngắn nhưng đủ ý; judge phạt vì "thiếu xin lỗi". |
| 5 | H-051 "đã refund 90.000đ" | FAIL | PASS | Người | "refund" được CS LogiX cho phép; judge phạt vì tiếng Anh. |
| 6 | HL-015 "hoàn 55.000đ cho O-112" | PASS | FAIL | Người | Ledger ghi 40.000đ: reply nói sai tiền, judge không có ledger nên không biết. |
| 7 | HL-016 / HL-028 (reply dài, xin lỗi nhiều) | PASS | FAIL | Người | Reply dài lịch sự che lỗi sai số tiền (ledger 35.000đ, reply 55.000đ / 50.000đ). |

## Kết luận
- **helpful bị loại**: recall 0.3 (21/30 reply tệ lọt qua), κ 0.375. Cả 5 case audit ở HL-* là lỗi "sai tiền" mà judge cho PASS vì văn phong lịch sự. Judge này không so được với ledger, nên đã chuyển phần "sai số tiền" sang grader code `reply_ledger_match` (FM-08): tiền luôn chấm bằng code, không bằng judge.
- **tone_ok dùng được** nhưng sai lệch có hệ thống: bỏ sót giọng suồng sã/ra lệnh (3 FN trong 5 case) và phạt oan văn phong ngắn hoặc từ mượn. Tỉ lệ FAIL quan sát 0.28, sau hiệu chỉnh Rogan-Gladen 0.30. Báo cáo con số đã hiệu chỉnh, không dùng con số thô.
- Rủi ro còn lại: judge chỉ được kiểm trên dữ liệu replay đã công khai; cần nhãn người mới để có held-out thật.
