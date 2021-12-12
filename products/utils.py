import pandas as pd
from .models import Product, Product_Image, Category


def get_product_db():
    products = Product.objects.filter(open=True, status="sale")
    db_columns = [
        "id",
        "title",
        "price_pc",
        "link",
        "image_link",
        "add_image_link",
        "category_name2",
        "category_name1",
        "naver_category",
        "review_count",
        "shipping",
        "search_tag",
        "origin",
    ]

    product_data = []

    for product in products:
        cat = product.category
        images = product.product_images.all()
        image_url = "|".join([image.image.url for image in images])
        product_data.append(
            [
                product.pk,
                product.title,
                product.sell_price,
                f"https://www.pickyfarm.com/product/detail/{product.pk}",
                product.main_image.url,
                image_url,
                cat.name,
                cat.parent.name,
                get_product_naver_category_code(cat.name),
                product.product_comments.all().count(),
                product.default_delivery_fee,
                cat.name,
                "국산",
            ]
        )

    df = pd.DataFrame(data=product_data, columns=db_columns)
    filename = "pickyfarm_EP.txt"
    df.to_csv(filename, index=False, sep="\t", encoding="utf-8")


def get_product_naver_category_code(category):
    if category == "사과":
        return "50002160"
    elif category == "고구마":
        return "50002214"
    elif category == "버섯":
        return "500022051"
    elif category == "샐러드":
        return "50002211"
