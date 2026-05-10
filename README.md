# 🕊️ Chaparino

**Chaparino** is a lightweight, modular messaging microservice designed to bridge the gap between your application and various communication gateways. It currently provides out-of-the-box support for **[SMS.ir](http://SMS.ir)** and the **Bale** messaging platform.

Built with **FastAPI**, Chaparino focuses on high-performance dispatch, dynamic templating, and seamless bulk messaging orchestration.

**[CHAPARINO.IR](https://chaparino.ir/)**

---

## ✨ Key Features

* **Multi-Provider Support**: Unified interface for [SMS.ir](http://SMS.ir) (SMS gateway) and Bale (Messaging API).
* **Dynamic Templating**: Centralized template management using Python-based string formatting for variables like `{name}`, `{code}`, or `{time}`.
* **Intelligent Phone Normalization**: Automatically formats phone numbers for different providers (e.g., converting `0912...` to international `98912...` for Bale).
* **Bulk Dispatch**: High-efficiency batch processing for **CSV** and **Excel** files.
* **Developer Friendly**: Auto-generated interactive API documentation via Swagger UI.
* **Docker Ready**: Streamlined deployment using containerization.


---

## 🛠 Project Structure

```text
.
├── app
│   ├── main.py          # FastAPI entry point & API routing
│   ├── core.py          # Core logic, provider integration & normalization
│   ├── templates.py     # Message template definitions & logic
│   └── utils.py         # File processing utilities (CSV/Excel)
├── data                 # Optional directory for bulk data files
├── .env                 # Environment variables (excluded from Git)
└── Dockerfile           # Docker image configuration
```


---

## 🚀 Getting Started

### 1. Environment Configuration

Create a `.env` file in the root directory and populate it with your credentials:

```env

BALE_ACCESS_KEY=your_access_key

BALE_BOT_ID=your_bot_id

SMS_IR_KEY=your_api_key

SMS_IR_LINE=your_line_number
```

### 2. Run with Docker (Recommended)

```bash

docker build -t chaparino .
docker run -p 8000:8000 --env-file .env chaparino
```

### 3. Local Installation

```bash

pip install -r requirements.txt

uvicorn app.main:app --reload
```


---

## 📖 API Documentation

Once the service is running, access the interactive docs at `http://localhost:8000/docs`.

### Single Dispatch

**Endpoint:** `POST /send/single`

| Parameter | Type | Description |
|----|----|----|
| `provider` | string | `sms` or `bale` |
| `template` | string | Template name (e.g., `otp`, `welcome`) |
| `phone` | string | Recipient phone number |
| `params` | JSON string | Template variables: `{"name": "Hesam"}` |

### Bulk Dispatch

**Endpoint:** `POST /send/bulk` Upload a CSV or Excel file. The system expects a `phone` column; all other columns are automatically mapped to template variables.


---

## 📝 Managing Templates

Templates are managed in `app/templates.py`. You can combine static strings with dynamic placeholders:

```python
# Example Template Definition
"welcome": "Hello {name}, welcome to {company_name}!"
```

### Usage Examples (cURL)

**Single Send:**

```bash

curl -X 'POST' \
  'http://localhost:8000/send/single' \
  -H 'Content-Type: multipart/form-data' \
  -F 'provider=bale' \
  -F 'template=otp' \
  -F 'phone=0912XXXXXXX' \
  -F 'params={"code": "2829", "company_name": "Chaparino"}'
```

**Bulk Send via CSV:**

```bash

curl -X 'POST' \
  'http://localhost:8000/send/bulk' \
  -H 'Content-Type: multipart/form-data' \
  -F 'provider=sms' \
  -F 'template=announcement' \
  -F 'file=@/path/to/users.csv'
```


---

## 📂 Bulk File Samples

The system intelligently restores missing leading zeros often removed by Excel formatting.

**Sample 1 (Announcement):**

| phone | name | time |
|----|----|----|
| 09121111111 | Ali Alavi | 10:30 |

**Sample 2 (OTP - Missing Zeros):**

| phone | code |
|----|----|
| 912XXXXXXX | 8713 |


---

## 🤝 Contributing

Contributions are welcome! If you'd like to add support for new providers (Telegram, WhatsApp, etc.), please submit a Pull Request or open an issue.


---

## 📄 License

**MIT No Attribution**

Copyright 2026 Amirhesamshahab ([hesamshahab.com](https://hesamshahab.com))

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so.