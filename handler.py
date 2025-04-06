# handler.py
from ycmladapter import YandexCloudClineAdapter

adapter = YandexCloudClineAdapter(async_mode=False)

def process_cline_request(request_json):
    # Эта функция будет вызываться из Cline
    return adapter.cline_handler(request_json)