# TravelBuddy — Kết Quả Test Cases
**Ngày chạy:** 2026-04-07
**Model:** gpt-4o-mini
**Framework:** LangGraph + LangChain

---

## Tổng kết
Xem chi tiết test case tại test.py
| Test | Tên | Input | Tool calls (kỳ vọng → thực tế) | Kết quả |
|:---:|---|---|:---:|:---:|
| 1 | Direct Answer | Xin chào, chưa biết đi đâu | 0 → 0 | ✅ PASS |
| 2 | Single Tool Call | Tìm vé Hà Nội → Đà Nẵng | 1 → 1 | ✅ PASS |
| 3 | Multi-Step Chaining | Phú Quốc 2 đêm, budget 5 triệu | 3 → 3 | ✅ PASS |
| 4 | Missing Info | Muốn đặt khách sạn | 0 → 0 | ✅ PASS |
| 5 | Guardrail | Bài tập linked list | 0 → 0 | ✅ PASS |
| 6 | Reverse Flight | Đà Nẵng → Hà Nội | 1 → 1 | ✅ PASS |
| 7 | Non-existent Route | Hà Nội → Hội An | 1 → 0 | ⚠️ NOTE |
| 8 | Hotel No Result | Phú Quốc dưới 100k/đêm | 1 → 1 | ✅ PASS |
| 9 | Budget Exceeded | Phú Quốc 2 đêm, budget 2 triệu | 3 → 3 | ✅ PASS |
| 10 | Multi-destination | So sánh Đà Nẵng vs Phú Quốc | 2 → 2 | ✅ PASS |

**Kết quả: 9/10 PASS**

---

## Chi tiết từng test

---

### Test 1 — Direct Answer ✅ PASS
> Agent chào hỏi và hỏi thêm thông tin mà không gọi tool.

**Input:** `Xin chào! Tôi đang muốn đi du lịch nhưng chưa biết đi đâu.`
**Kỳ vọng:** Không gọi tool, hỏi thêm sở thích / ngân sách / thời gian.
**Tool calls:** 0 → 0

**Agent Logs:**
Trả lời trực tiếp

**Agent Answer:**
> Chào bạn! Thật tuyệt khi bạn muốn đi du lịch! Bạn đã có ý tưởng nào về điểm đến chưa? Nếu chưa, mình có thể gợi ý cho bạn một số nơi thú vị ở Việt Nam như
Đà Nẵng, Phú Quốc, hay Hà Nội... Bạn có thể cho mình biết bạn thích đi đâu hay thời gian dự kiến đi không? Cũng như ngân sách của bạn nữa nhé!

---

### Test 2 — Single Tool Call ✅ PASS
> Agent gọi đúng 1 tool với đúng tham số, liệt kê đủ 4 chuyến bay.

**Input:** `Tìm giúp tôi chuyến bay từ Hà Nội đi Đà Nẵng`
**Kỳ vọng:** Gọi `search_flights('Hà Nội', 'Đà Nẵng')`, liệt kê 4 chuyến bay.
**Tool calls:** 1 → 1

**Agent Logs:**
Gọi tool: search_flights({'origin': 'Hà Nội', 'destination': 'Đà Nẵng'})
Trả lời trực tiếp

**Agent Answer:**
> Đây là các chuyến bay từ Hà Nội đi Đà Nẵng:
> 1. **Vietnam Airlines** | 06:00 → 07:20 | economy | 1.450.000đ
> 2. **Vietnam Airlines** | 14:00 → 15:20 | business | 2.800.000đ
> 3. **VietJet Air** | 08:30 → 09:50 | economy | 890.000đ
> 4. **Bamboo Airways** | 11:00 → 12:20 | economy | 1.200.000đ

---

### Test 3 — Multi-Step Tool Chaining ✅ PASS
> Agent tự chuỗi 3 tools theo đúng thứ tự: flights → hotels → budget.

**Input:** `Tôi ở Hà Nội, muốn đi Phú Quốc 2 đêm, budget 5 triệu. Tư vấn giúp!`
**Kỳ vọng:** Gọi đủ 3 tools theo thứ tự, tổng hợp kế hoạch hoàn chỉnh.
**Tool calls:** 3 → 3

**Agent Logs:**
Gọi tool: search_flights({'origin': 'Hà Nội', 'destination': 'Phú Quốc'})
Gọi tool: search_hotels({'city': 'Phú Quốc'})
Gọi tool: calculate_budget({'total_budget': 5000000, 'expenses': 'vé_máy_bay:1350000,khách_sạn:400000'})
Trả lời trực tiếp

**Agent Answer:**
> ✈️ **Chuyến bay:** VietJet Air | 10:00 → 12:15 | economy | 1.350.000đ
> 🏨 **Khách sạn:** 9Station Hostel | 2 Sao | Dương Đông | 200.000đ/đêm
> 💰 **Tổng chi:** 1.750.000đ — Còn lại: 3.250.000đ
> 💡 **Gợi ý:** Dư ngân sách cho tour đảo, hải sản, thể thao nước.

---

### Test 4 — Missing Info / Clarification ✅ PASS
> Agent hỏi lại đúng thông tin còn thiếu, không gọi tool vội.

**Input:** `Tôi muốn đặt khách sạn`
**Kỳ vọng:** Hỏi lại thành phố và ngân sách. Không gọi tool.
**Tool calls:** 0 → 0

**Agent Logs:**
Trả lời trực tiếp

**Agent Answer:**
> Bạn có thể cho mình biết bạn đang tìm khách sạn ở thành phố nào và ngân sách tối đa mỗi đêm của bạn là bao nhiêu không?

---

### Test 5 — Guardrail / Refusal ✅ PASS
> Agent từ chối lịch sự yêu cầu ngoài phạm vi du lịch.

**Input:** `Giải giúp tôi bài tập lập trình Python về linked list`
**Kỳ vọng:** Từ chối, nói chỉ hỗ trợ du lịch.
**Tool calls:** 0 → 0

**Agent Logs:**
Trả lời trực tiếp

**Agent Answer:**
> Xin lỗi, mình không thể giúp bạn về lập trình hay bài tập liên quan đến Python. Nhưng nếu bạn cần tư vấn về du lịch, đặt phòng hoặc vé máy bay, mình rất sẵn
lòng giúp đỡ!

---

### Test 6 — Reverse Flight ✅ PASS
> Logic chiều ngược trong `search_flights` hoạt động đúng, có cảnh báo rõ ràng.

**Input:** `Tìm chuyến bay từ Đà Nẵng về Hà Nội`
**Kỳ vọng:** Gọi `search_flights('Đà Nẵng', 'Hà Nội')`, trả về kết quả chiều ngược kèm cảnh báo.
**Tool calls:** 1 → 1

**Agent Logs:**
Gọi tool: search_flights({'origin': 'Đà Nẵng', 'destination': 'Hà Nội'})
Trả lời trực tiếp

**Agent Answer:**
> Mình không tìm thấy chuyến bay từ Đà Nẵng về Hà Nội, nhưng có thông tin về các chuyến bay từ Hà Nội đến Đà Nẵng gồm 4 chuyến của Vietnam Airlines, VietJet
Air và Bamboo Airways.

---

### Test 7 — Non-existent Route ⚠️ NOTE
> Agent dùng domain knowledge thay vì gọi tool — hành vi thông minh nhưng lệch metric.

**Input:** `Có chuyến bay từ Hà Nội đi Hội An không?`
**Kỳ vọng:** Gọi `search_flights`, trả về không tìm thấy.
**Tool calls:** 1 → 0

**Agent Logs:**
Trả lời trực tiếp

**Agent Answer:**
> Hội An không có sân bay riêng, nên bạn sẽ phải bay tới sân bay Đà Nẵng rồi di chuyển từ Đà Nẵng tới Hội An. Bạn có muốn mình tìm chuyến bay từ Hà Nội tới Đà
Nẵng không?

**Nhận xét:** Agent không gọi tool vì tự nhận biết Hội An không có sân bay — đây là hành vi đúng về mặt nghiệp vụ. Metric "số tool calls" không phản ánh được
chất lượng câu trả lời trong trường hợp này.

---

### Test 8 — Hotel No Result ✅ PASS
> Tool `search_hotels` lọc đúng và trả về thông báo gợi ý tăng ngân sách.

**Input:** `Tìm khách sạn ở Phú Quốc dưới 100.000đ một đêm`
**Kỳ vọng:** Gọi `search_hotels('Phú Quốc', max_price=100000)`, báo không có kết quả.
**Tool calls:** 1 → 1

**Agent Logs:**
Gọi tool: search_hotels({'city': 'Phú Quốc', 'max_price_per_night': 100000})
Trả lời trực tiếp

**Agent Answer:**
> Mình không tìm thấy khách sạn nào ở Phú Quốc với giá dưới 100.000đ một đêm. Bạn có muốn tăng ngân sách lên để tìm kiếm thêm lựa chọn không?

---

### Test 9 — Budget Exceeded ✅ PASS
> Agent chuỗi 3 tools và `calculate_budget` cảnh báo vượt ngân sách đúng.

**Input:** `Tôi có 2 triệu, muốn đi Hà Nội đến Phú Quốc 2 đêm. Tư vấn giúp!`
**Kỳ vọng:** Chuỗi 3 tools, `calculate_budget` báo vượt hoặc sát ngân sách.
**Tool calls:** 3 → 3

**Agent Logs:**
Gọi tool: search_flights({'origin': 'Hà Nội', 'destination': 'Phú Quốc'})
Gọi tool: search_hotels({'city': 'Phú Quốc'})
Gọi tool: calculate_budget({'total_budget': 2000000, 'expenses': 'vé_máy_bay:1100000,khách_sạn:400000'})
Trả lời trực tiếp

**Agent Answer:**
> ✈️ **Chuyến bay:** VietJet Air | 16:00 → 18:15 | economy | 1.100.000đ
> 🏨 **Khách sạn:** 9Station Hostel | 2 Sao | 200.000đ/đêm × 2 = 400.000đ
> 💰 **Tổng chi:** 1.500.000đ — Còn lại: 500.000đ
> 💡 Phương án tiết kiệm nhất trong tầm ngân sách 2 triệu.

---

### Test 10 — Multi-destination ✅ PASS
> Agent tự gọi cùng 1 tool 2 lần với tham số khác nhau, so sánh rõ ràng.

**Input:** `So sánh giá vé từ Hà Nội đi Đà Nẵng và Hà Nội đi Phú Quốc`
**Kỳ vọng:** Gọi `search_flights` 2 lần, liệt kê và so sánh cả hai tuyến.
**Tool calls:** 2 → 2

**Agent Logs:**
Gọi tool: search_flights({'origin': 'Hà Nội', 'destination': 'Đà Nẵng'})
Gọi tool: search_flights({'origin': 'Hà Nội', 'destination': 'Phú Quốc'})
Trả lời trực tiếp

**Agent Answer:**
> **Hà Nội → Đà Nẵng:** rẻ nhất 890.000đ (VietJet Air), đắt nhất 2.800.000đ (VN Airlines Business)
> **Hà Nội → Phú Quốc:** rẻ nhất 1.100.000đ (VietJet Air), đắt nhất 2.100.000đ (VN Airlines)
> → Đà Nẵng rẻ hơn Phú Quốc ~210.000đ ở phân khúc economy.