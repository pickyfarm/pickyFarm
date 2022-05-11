class AbstractPurchaseException(Exception):
    def __init__(self, msg, type):
        self.msg = msg
        self.type = type

        self.log()
        super().__init__(msg)

    def __str__(self):
        return self.msg

    def log(self):
        print(f"[EXCEPTION] {self.msg}")


class StockLackException(AbstractPurchaseException):
    """결제오류(재고부족)"""

    def __init__(self, product):
        super().__init__(f"{product.title}의 재고가 부족합니다", "error_stock")


class PriceMatchException(AbstractPurchaseException):
    """결제오류(총가격 불일치)"""

    def __init__(self):
        super().__init__("클라이언트 요청 금액과 DB에 저장된 금액이 일치하지 않습니다.", "error_price_match")


class ServerErrorException(AbstractPurchaseException):
    """결제오류(서버)"""

    def __init__(self):
        super().__init__("서버에 오류가 있었습니다. 다시 시도해주세요", "error_server")


class ValidErrorException(AbstractPurchaseException):
    """결제오류(검증)"""

    def __init__(self):
        super().__init__("결제 검증에 오류가 있습니다. 다시 시도해주세요", "error_valid")
