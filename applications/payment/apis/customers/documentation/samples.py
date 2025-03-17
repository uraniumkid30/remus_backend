payment_id = "3fa85f64-5717-4562-b3fc-2c963f66afa6"
receipt_data = [
    {
        "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "quantity": 4,
        "price": "5000.0",
        "discount": "100",
        "order": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "product": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    }
]
single_payment = {
    "id": payment_id,
    "order": {
        "id": "6edb971e-dd16-47da-95d9-7e55046b2031",
        "order_items": [
            {
                "id": "f79e32a1-31ec-4ead-ba5d-9583add733f6",
                "quantity": 2,
                "price": "200.00",
                "discount": "0.00",
                "order": "6edb971e-dd16-47da-95d9-7e55046b2031",
                "product": "39785a54-75a1-40d5-bcc4-07690a58b779",
            }
        ],
        "status": "pending",
        "total": "400.00",
        "total_wait_time": 1,
        "payment_status": "pending",
        "order_number": "FCC3D5D2-1",
        "order_note": None,
        "tax": "0.00",
        "customer": None,
        "device": None,
        "table": "d8dffe82-768c-4800-9bcd-27e88e9e2117",
    },
    "payment_id": "OP-207179",
    "payment_method": "card",
    "barcode": "9835385965145",
    "amount": "400.00",
    "amount_paid": "0.00",
    "status": "pending",
    "currency": "NGN",
}

all_payments = [single_payment]

make_payment_payload = {
    "payment_method": "card",
    "amount_paid": 800,
    "currency": "NGN",
    "payment_method_meta": {
        "number": "4084084084084081",
        "cvv": 408,
        "expiry_month": 12,
        "expiry_year": 25,
    },
}

tag_name = "Customer Payments"
