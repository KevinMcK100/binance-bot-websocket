from unicorn_binance_websocket_api.unicorn_binance_websocket_api_manager import BinanceWebSocketApiManager
import logging
import time
import threading
import os
import json
import requests
import zipfile

USER_CONFIG_PATH = '.config.json'
EXCHANGE_API_MANAGERS = {}
JSON_CONTENT_TYPE_HEADER = {"content-type": "application/json"}

# https://docs.python.org/3/library/logging.html#logging-levels
logging.basicConfig(level=logging.INFO,
                    filename='{}.log'.format(os.path.basename(__file__)),
                    format='{asctime} [{levelname:8}] {process} {thread} {module}: {message}',
                    style='{')


def load_config_from_file():
    if os.path.isfile(USER_CONFIG_PATH):
        print("Local config file exists.")
        with open(USER_CONFIG_PATH) as config_json:
            return json.load(config_json)
    else:
        print("Local config not found. Attempting to extract from zip")
        with zipfile.ZipFile(os.path.dirname(__file__)) as zip_file:
            with zip_file.open(USER_CONFIG_PATH) as config_json:
                return json.load(config_json)


def load_active_user_profiles(config: dict):
    user_config = list(config.get("USERS"))
    active_profiles = []
    for user in user_config:
        if user.get("WEBSOCKET_ACTIVE"):
            active_profiles.append(user)
    return active_profiles


def get_exchange_api_manager(user_profile):
    exchange = user_profile.get("EXCHANGE")
    if exchange not in EXCHANGE_API_MANAGERS:
        exchange_endpoint = user_profile.get("EXCHANGE_ENDPOINT")
        exchange_api_manager = BinanceWebSocketApiManager(exchange=exchange_endpoint)
        EXCHANGE_API_MANAGERS[exchange] = exchange_api_manager
        return exchange_api_manager
    else:
        return EXCHANGE_API_MANAGERS[exchange]


def send_order_update_event(request_body: dict, profile: dict, base_url):
    user_id = profile.get("USER_ID")
    service_url = '{}?userId={}'.format(base_url, user_id)
    response = requests.post(service_url, data=json.dumps(request_body), headers=JSON_CONTENT_TYPE_HEADER)
    print(response.json())


def check_stream_events(exchange_api_manager, stream_id: str, profile: dict, service_endpoint: str):
    while True:
        if exchange_api_manager.is_manager_stopping():
            exit(0)
        stream_data = exchange_api_manager.pop_stream_data_from_stream_buffer(stream_id)
        if stream_data is False:
            time.sleep(0.01)
        else:
            json_data = json.loads(stream_data)
            print("Order update event received: {}".format(json_data))
            event_type = json_data.get("e")
            order = dict(json_data.get("o", {}))
            order_status = order.get("X")
            if event_type == "ORDER_TRADE_UPDATE" and order_status == "FILLED":
                order_event_request = {
                    "auth": profile.get("BOT_API_KEY"),
                    "exchange": profile.get("EXCHANGE"),
                    "order": json_data
                }
                send_order_update_event(request_body=order_event_request, profile=profile, base_url=service_endpoint)


def init_websocket():

    config = load_config_from_file()
    active_user_profiles = load_active_user_profiles(config=config)

    for profile in active_user_profiles:
        profile = dict(profile)
        exchange_api_manager = get_exchange_api_manager(profile)
        api_key = profile.get("EXCHANGE_API_KEY")
        api_secret = profile.get("EXCHANGE_SECRET_KEY")
        user_id = profile.get("USER_ID")
        exchange = profile.get("EXCHANGE")
        stream_label = '{}-{}'.format(user_id, exchange)
        stream_id = exchange_api_manager.create_stream('arr', '!userData', stream_label=stream_label,
                                                       stream_buffer_name=True, api_key=api_key, api_secret=api_secret)

        # start a worker process to move the received stream_data from the stream_buffer to a print function
        service_endpoint = config.get("SERVICE_ENDPOINT")
        worker_thread = threading.Thread(target=check_stream_events,
                                         args=(exchange_api_manager, stream_id, profile, service_endpoint))
        worker_thread.start()

    # monitor the streams
    while True:
        for stream in EXCHANGE_API_MANAGERS.values():
            stream.print_summary()
            time.sleep(1)
        time.sleep(30)


def main():
    init_websocket()


if __name__ == "__main__":
    main()
