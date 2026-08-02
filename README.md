# PayMobZ

### Unofficial Python SDK for the Paymob payment gateway.

---

## 🚀 Installation

`pip install paymobz`


---

## ⚡ Quick Start
```python
from paymobz import Paymob
from paymobz.models.payment_link import PaymentLinkRequest

paymob = Paymob(
	api_key="",
     secret_key="",
     public_key="",
)
payment_method = 1234567


link = PaymentLinkRequest(
    amount_cents=2000,
    currency="EGP",
    payment_methods=[payment_method],
    billing_data={
        "first_name": "Test",
        "last_name": "User",
        "email": "test@test.com",
        "phone_number": "+201000000000",
        "city": "Cairo",
        "country": "EG"
    }
)

data = paymob.payment_links.create(link)
print(data)
```
---

## 💳 Supported Features

- Unified Checkout
- Intention API
- Iframe Integration
- Webhook Handling

---

## 🧠 Notes

- Amount is in cents (e.g. 2000 = 20 EGP)
- Uses Paymob hosted checkout (secure)
- No card data is handled by this SDK

---

## ⚠️ Disclaimer

This is an unofficial SDK and is not affiliated with Paymob.

---

## 📌 Status

Early release 

More improvements, documentation, and features coming soon.

---

# Author
###  Ahmed Saoud