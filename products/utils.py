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
                product_title[product.pk],
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


product_title = {
    19: "농가를 돕는 가치소비! [못난이 사과] 간식용 홍로 소과 3kg (14~18개) - 산지 직거래 / 산지 직송 / 흠과 비규격과 소과 가정용 선물용 사과",
    39: "농가를 돕는 가치소비! [못난이 사과] 든든한 듬직이 부사 사과 (21~23과) - 산지 직거래 산지 직송 사과 흠과 비규격과 가정용",
    40: "농가를 돕는 가치소비! [못난이 사과] 든든한 듬직이 부사 사과 (42~48과) - 산지 직거래 산지 직송 사과 흠과 비규격과 가정용",
    43: "농가를 돕는 가치소비! [못난이, 정상 혼합] 간식용 귀요미 부사 사과 (10~15과) - 산지 직거래 / 산지 직송 / [흠과 비규격과 혼합] 사과 소과 ",
    42: "농가를 돕는 가치소비! [못난이 사과] 아침햇살 한손이 부사 사과 (48~52과) - 산지 직거래 / 산지 직송 / 흠과 비규격과 가정용  ",
    41: "농가를 돕는 가치소비! [못난이 사과] 아침햇살 한손이 부사 사과 (24~26과) - 산지 직거래 / 산지 직송 / 흠과 비규격과 가정용  ",
    22: "흑목이 버섯 600g - 산지 직거래 산지 직송 농장 직거래 잡채 버섯",
    23: "건목이 버섯 90g - 산지 직거래 산지 직송 농장 직거래 잡채 버섯",
    24: "반값에 즐기는 건표고 버섯 200g - 산지 직거래 / 산지 직송 / 농장 직거래",
    25: "반값에 즐기는 건표고 버섯 400g - 산지 직거래 / 산지 직송 / 농장 직거래",
    26: "반값에 즐기는 건흰목이 버섯 60g - 산지 직거래 / 산지 직송 / 농장 직거래 잡채 버섯",
    27: "반값에 즐기고 농가를 돕는 가치소비! 못난이 흰목이 버섯 300g",
    29: "농가를 돕는 가치소비! [못난이 고구마] 강화 속노랑 고구마 3kg - 가정용 고구마 / 꿀 고구마 / 황금 고구마",
    30: "농가를 돕는 가치소비! [못난이 고구마] 강화 속노랑 고구마 5kg - 가정용 고구마 / 꿀 고구마 / 황금 고구마",
    31: "농가를 돕는 가치소비! [못난이 고구마] 강화 속노랑 고구마 3kg - 가정용 고구마 / 꿀 고구마 / 황금 고구마",
    33: "농가를 돕는 가치소비! [못난이 고구마] 강화 속노랑 고구마 3kg - 가정용 고구마 / 꿀 고구마 / 황금 고구마",
    34: "농가를 돕는 가치소비! [못난이 고구마] 강화 속노랑 고구마 5kg - 가정용 고구마 / 꿀 고구마 / 황금 고구마",
    35: "추운 겨울 강추 간식 고구마 강화 속노랑 고구마 3kg - 꿀 고구마 / 황금 고구마",
    36: "추운 겨울 강추 간식 고구마 강화 속노랑 고구마 5kg - 꿀 고구마 / 황금 고구마",
    44: "반값에 즐기고 농가를 돕는 가치소비! 잡채용 버섯 패키지 세트 - 산지 직거래 / 산지 직송",
}
