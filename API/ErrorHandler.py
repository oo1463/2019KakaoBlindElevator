class ErrorHandler:
    @staticmethod
    def error_404(e):
        print(f'404 error 발생\n {e}')

    @staticmethod
    def error_500(e):
        print(f'500 server error\n {e}')

    @staticmethod
    def error_json(e):
        print(f'json error\n {e}')
