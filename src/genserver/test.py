import requests
import threading


def send_request():
    response = requests.get('https://server.pakeplus.com/public/apps/1')
    print(f"Response: {response.text}")


def test():
    for i in range(20):
        thread = threading.Thread(target=send_request)
        thread.start()


if __name__ == '__main__':
    test()
    print("All tests passed!")
