import pandas as pd
from .models import Product, Product_Image, Category

# NAVER
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
    elif category == "한라봉":
        return "50002179"
    elif category == "레드향":
        return "50002178"  # 천혜향 코드
    elif category == "패키지":
        return "50002195"  # 혼합과일세트 코드
    elif category == "딸기":
        return "50002164"


product_title = {
    19: "농가를 돕는 가치소비! [못난이 사과] 간식용 홍로 소과 3kg (14~18개) - 산지 직거래 / 산지 직송 / 흠과 비규격과 소과 가정용 선물용 사과",
    39: "농가를 돕는 가치소비! [못난이 사과] 든든한 듬직이 부사 사과 (21~23과) - 산지 직거래 산지 직송 사과 흠과 비규격과 가정용",
    40: "농가를 돕는 가치소비! [못난이 사과] 든든한 듬직이 부사 사과 (42~48과) - 산지 직거래 산지 직송 사과 흠과 비규격과 가정용",
    43: "농가를 돕는 가치소비! [못난이, 정상 혼합] 간식용 귀요미 부사 사과 (10~15과) - 산지 직거래 / 산지 직송 / [흠과 비규격과 혼합] 사과 소과 ",
    42: "농가를 돕는 가치소비! [못난이 사과] 아침햇살 한손이 부사 사과 (48~52과) - 산지 직거래 / 산지 직송 / 흠과 비규격과 가정용  ",
    41: "농가를 돕는 가치소비! [못난이 사과] 아침햇살 한손이 부사 사과 (24~26과) - 산지 직거래 / 산지 직송 / 흠과 비규격과 가정용  ",
    45: "선물용 부사 사과 5Kg (18~20과) 농가 직거래",
    46: "선물용 부사 사과 10Kg (36~40과) 농가 직거래",
    22: "흑목이 버섯 600g - 산지 직거래 산지 직송 농장 직거래 잡채 버섯",
    23: "건목이 버섯 90g - 산지 직거래 산지 직송 농장 직거래 잡채 버섯",
    24: "반값에 즐기는 건표고 버섯 200g - 산지 직거래 / 산지 직송 / 농장 직거래",
    25: "반값에 즐기는 건표고 버섯 400g - 산지 직거래 / 산지 직송 / 농장 직거래",
    26: "반값에 즐기는 건흰목이 버섯 60g - 산지 직거래 / 산지 직송 / 농장 직거래 잡채 버섯",
    27: "반값에 즐기고 농가를 돕는 가치소비! 못난이 흰목이 버섯 300g",
    29: "농가를 돕는 가치소비! [못난이 고구마] 강화 속노랑 고구마 3kg - 가정용 고구마 / 꿀 고구마 / 황금 고구마",
    30: "농가를 돕는 가치소비! [못난이 고구마] 강화 속노랑 고구마 5kg - 가정용 고구마 / 꿀 고구마 / 황금 고구마",
    31: "농가를 돕는 가치소비! [못난이 고구마] 강화 속노랑 고구마 3kg - 가정용 고구마 / 꿀 고구마 / 황금 고구마",
    32: "농가를 돕는 가치소비! [못난이 고구마] 강화 속노랑 고구마 5kg - 가정용 고구마 / 꿀 고구마 / 황금 고구마",
    33: "농가를 돕는 가치소비! [못난이 고구마] 강화 속노랑 고구마 3kg - 가정용 고구마 / 꿀 고구마 / 황금 고구마",
    34: "농가를 돕는 가치소비! [못난이 고구마] 강화 속노랑 고구마 5kg - 가정용 고구마 / 꿀 고구마 / 황금 고구마",
    35: "추운 겨울 강추 간식 고구마 강화 속노랑 고구마 3kg - 꿀 고구마 / 황금 고구마",
    36: "추운 겨울 강추 간식 고구마 강화 속노랑 고구마 5kg - 꿀 고구마 / 황금 고구마",
    44: "반값에 즐기고 농가를 돕는 가치소비! 잡채용 버섯 패키지 세트 - 산지 직거래 / 산지 직송",
    52: "제주도 서귀포 명품 가정용 선물용 레드향 중향 3kg 농장 직거래 택배 제철 겨울과일",
    53: "제주도 서귀포 명품 가정용 선물용 레드향 대향 3kg 농장 직거래 택배 제철 겨울과일",
    54: "제주도 서귀포 명품 가정용 선물용 레드향 중향 5kg 농장 직거래 택배 제철 겨울과일",
    55: "제주도 서귀포 명품 가정용 선물용 레드향 대향 5kg 농장 직거래 택배 제철 겨울과일",
    56: "제주도 서귀포 명품 가정용 선물용 레드향 중향 10kg 농장 직거래 택배 제철 겨울과일",
    57: "제주도 서귀포 명품 가정용 선물용 레드향 대향 10kg 농장 직거래 택배 제철 겨울과일",
    58: "맛있는 제주 선물용 가정용 한라봉세트 3kg 농가 직거래 택배 제철 겨울과일",
    59: "맛있는 제주 선물용 가정용 한라봉세트 5kg 농가 직거래 택배 제철 겨울과일",
    60: "맛있는 제주 선물용 가정용 한라봉세트 10kg 농가 직거래 택배 제철 겨울과일",
    61: "산지직송 한라봉 레드향 반반 세트 3kg /  제주도 서귀포 직거래 / 선물용 가정용 만감류",
    62: "산지직송 한라봉 레드향 반반 세트 5kg / 제주도 서귀포 직거래 / 선물용 가정용 만감류",
    63: "산지직송 한라봉 레드향 반반 세트 10kg / 제주도 서귀포 직거래 / 선물용 가정용 만감류",
    64: "산지직송 꽃상추 청상추 패키지 1kg / 당일수확 당일배송 / 다이어트 샐러드 / 유기농 쌈채소 / 농산물직거래",
    65: "[당일수확 당일배송] 논산 설향딸기 35과 650g / 과학영농 / 산지직송 / 가정용 선물용",
    66: "[당일수확 당일배송] 논산 설향딸기 35과 800g / 과학영농 / 산지직송 / 가정용 선물용",
    67: "[당일수확 당일배송] 논산 설향딸기 中 30과 800g / 과학영농 / 산지직송 / 가정용 선물용",
    68: "[당일수확 당일배송] 논산 설향딸기 大 24과 800g / 과학영농 / 산지직송 / 가정용 선물용",
    69: "[당일수확 당일배송] 논산 설향딸기 특大 20과 800g / 과학영농 / 산지직송 / 가정용 선물용",
}


# DAUM
def get_product_db_daum():
    products = Product.objects.filter(open=True, status="sale")
    product_data = []

    for product in products:
        cat = product.category
        product_data.append(
            [
                "<<<begin>>>",
                f"<<<mapid>>>{product.pk}",
                f"<<<price>>>{product.sell_price}",
                f"<<<pname>>>{product_title_daum[product.pk]}",
                f"<<<pgurl>>>https://www.pickyfarm.com/product/detail/{product.pk}",
                f"<<<igurl>>>{product.main_image.url}",
                f"<<<cate1>>>{cat.parent.name}",
                f"<<<cate2>>>{cat.name}",
                f"<<<caid1>>>{get_product_naver_category_code(cat.name)}",
                f"<<<deliv>>>{product.default_delivery_fee}",
                "<<<ftend>>>",
            ]
        )

    df = pd.DataFrame(data=product_data)
    filename = "pickyfarm_daum_EP.txt"
    df.to_csv(filename, index=False, sep="\n", header=None, encoding="utf-8")


product_title_daum = {
    19: " ",
    39: " ",
    40: " ",
    43: " ",
    42: " ",
    41: " ",
    45: " ",
    46: " ",
    22: " ",
    23: " ",
    24: " ",
    25: " ",
    26: " ",
    27: " ",
    29: " ",
    30: " ",
    31: " ",
    32: " ",
    33: " ",
    34: " ",
    35: " ",
    36: " ",
    44: " ",
    52: " ",
    53: " ",
    54: " ",
    55: " ",
    56: " ",
    57: " ",
    58: " ",
    59: " ",
    60: " ",
    61: " ",
    62: " ",
    63: " ",
    64: " ",
    65: " ",
    66: " ",
    67: " ",
    68: " ",
    69: " ",
}
