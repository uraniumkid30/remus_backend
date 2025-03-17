product_id = "3fa85f64-5717-4562-b3fc-2c963f66afa6"
single_product = {
    "id": product_id,
    "sub_category": {
        "id": "4228c1ad-9087-43b1-87b9-7cfc89eaa085",
        "category": {
            "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "name": "Meals",
            "slug": "snack",
            "description": "all foods",
            "image": "images.jpeg",
        },
        "name": "Starters",
        "slug": "rice",
        "description": "meals you can start with",
        "image": None,
    },
    "chef": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "ingredients": [
        {"name": "basmatic rice", "short_name": "basmatic rice", "restaurant": None},
        {"name": "chicken", "short_name": "chicken", "restaurant": None},
        {"name": "plantain", "short_name": "plantain", "restaurant": None},
    ],
    "discount": None,
    "name": "Jollof rice",
    "slug": "jollof-rice",
    "description": "",
    "point": 0,
    "unit_price": "8500.00",
    "wait_time": 40,
    "image": "images_2.jpeg",
    "is_available": False,
    "quantity_available": None,
}

all_products = [single_product]


product_tag_name = "Customer Products"


category_id = "f6717d0e-f6b2-4548-a480-78d9b4f28d9c"
single_category = {
    "id": category_id,
    "name": "Meals",
    "slug": "snack",
    "description": "all foods",
    "image": "images.jpeg",
    "sub_categories": [
        {
            "id": "4228c1ad-9087-43b1-87b9-7cfc89eaa085",
            "name": "Starters",
            "slug": "rice",
            "description": "meals you can start with",
            "image": None,
            "products": [
                {
                    "id": "01452417-b07f-444c-adcd-981ad0cc72fd",
                    "sub_category": "4228c1ad-9087-43b1-87b9-7cfc89eaa085",
                    "chef": None,
                    "ingredients": [
                        {
                            "name": "basmatic rice",
                            "short_name": "basmatic rice",
                            "restaurant": None,
                        },
                        {
                            "name": "chicken",
                            "short_name": "chicken",
                            "restaurant": None,
                        },
                        {
                            "name": "plantain",
                            "short_name": "plantain",
                            "restaurant": None,
                        },
                    ],
                    "discount": None,
                    "name": "Jollof rice",
                    "slug": "jollof-rice",
                    "description": "",
                    "point": 0,
                    "unit_price": "8500.00",
                    "wait_time": 40,
                    "image": "images_2.jpeg",
                    "is_available": False,
                    "quantity_available": None,
                },
                {
                    "id": "39785a54-75a1-40d5-bcc4-07690a58b779",
                    "sub_category": "4228c1ad-9087-43b1-87b9-7cfc89eaa085",
                    "chef": None,
                    "ingredients": [
                        {"name": "carrot", "short_name": "carrot", "restaurant": None},
                        {
                            "name": "basmatic rice",
                            "short_name": "basmatic rice",
                            "restaurant": None,
                        },
                        {
                            "name": "chicken",
                            "short_name": "chicken",
                            "restaurant": None,
                        },
                        {
                            "name": "plantain",
                            "short_name": "plantain",
                            "restaurant": None,
                        },
                    ],
                    "discount": None,
                    "name": "fried rice",
                    "slug": "fried-rice",
                    "description": "",
                    "point": 23,
                    "unit_price": "200.00",
                    "wait_time": 40,
                    "image": "rice_fried-rice-060_1.jpeg",
                    "is_available": True,
                    "quantity_available": None,
                },
            ],
        },
        {
            "id": "eb04c6b0-a894-4e08-933f-fa36ec27fc15",
            "name": "Swallow",
            "slug": "swallow",
            "description": "you are welcome to use your hands",
            "image": None,
            "products": [
                {
                    "id": "8ba8e99a-6e9b-4111-adf6-bd00e22894ac",
                    "sub_category": "eb04c6b0-a894-4e08-933f-fa36ec27fc15",
                    "chef": None,
                    "ingredients": [
                        {
                            "name": "goat meat",
                            "short_name": "goat meat",
                            "restaurant": None,
                        }
                    ],
                    "discount": None,
                    "name": "afang soup",
                    "slug": "afang-soup",
                    "description": "",
                    "point": 0,
                    "unit_price": "15000.00",
                    "wait_time": 70,
                    "image": "images_3.jpeg",
                    "is_available": False,
                    "quantity_available": None,
                }
            ],
        },
    ],
}

all_categories = [single_category]

category_tag_name = "Customer Product Categories"
r_category_tag_name = "Customer Restuarant Product Categories"
