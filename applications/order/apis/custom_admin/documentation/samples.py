order_id = "3fa85f64-5717-4562-b3fc-2c963f66afa6"
order_items = [
    {
        "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "quantity": 4,
        "price": "5000.0",
        "discount": "100",
        "order": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "product": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    }
]
single_order = {
    "id": order_id,
    "order_items": order_items,
    "status": "pending",
    "total": "19900",
    "total_wait_time": 10,
    "payment_status": "pending",
    "order_number": "dbhvfgv387",
    "order_note": "dbhvfgv387",
    "tax": "0.00",
    "user": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "device": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "table": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
}

all_orders = [single_order]

update_payload = {
    "status": "pending",
    "payment_status": "pending",
}

tag_name = "Admin Orders"
