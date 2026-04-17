# LeetCode CLI - Refactored

## Cấu Trúc Thư Mục Mới

```
leetcode-cli/
├── leet.py                  # Entry point
├── config.json              # Cấu hình
├── cli/
│   ├── commands/            # Các lệnh CLI
│   │   ├── add_problem.py   # Thêm bài toán mới
│   │   ├── add_solution.py  # Thêm solution cho bài toán
│   │   └── manage_structures.py  # Quản lý data structures
│   └── utils/               # Tiện ích hỗ trợ
│       ├── config_manager.py
│       └── file_utils.py
└── tests/                   # Tests
```

## Lệnh CLI

### 1. Thêm bài toán mới
```bash
leet add
```
- Nhập số bài toán
- Nhập tên bài toán
- Chọn data structure có sẵn HOẶC thêm data structure mới
- Tạo file C++ template

### 2. Thêm solution mới
```bash
leet add-sol
```
- Chọn file bài toán từ danh sách
- Nhập phương pháp, độ phức tạp thời gian & không gian
- Paste code (kết thúc bằng `EOF`)

### 3. Quản lý Data Structures
```bash
leet manage-structures
```
- Liệt kê tất cả data structures
- Thêm data structure mới
- Xóa data structure

## Tính Năng Mới

✨ **Thêm Data Structure Tùy Chỉnh**
- Khi thêm bài toán, bạn có thể chọn từ danh sách sẵn có
- Hoặc chọn `[ADD NEW DATA STRUCTURE]` để tạo data structure mới ngay

✨ **Quản Lý Data Structures**
- Xem danh sách tất cả data structures
- Thêm data structure mới
- Xóa data structure không cần dùng

## Cấu Hình

File `config.json`:
```json
{
  "base_dir": "D:/leetcode",
  "data_structures": {
    "array": "array",
    "string": "string",
    "linked_list": "linked_list",
    "stack": "stack",
    "graph": "graph",
    "queue": "queue"
  }
}
```

Data structures sẽ tự động được thêm vào khi bạn sử dụng lệnh `leet add` hoặc `leet manage-structures`.
