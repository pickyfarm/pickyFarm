class HttpBodyDataError(Exception):
    def __init__(self):
        super().__init__("전송된 data의 값에 오류가 있습니다")
