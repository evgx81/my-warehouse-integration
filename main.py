
import requests
import base64
import json
from dotenv import load_dotenv
import os

load_dotenv()

# Данные для доступа к API сервиса "МойСклад"
LOGIN = os.getenv("LOGIN")
PASSWORD = os.getenv("PASSWORD")

def get_auntefication_token() -> str:
    url = "https://api.moysklad.ru/api/remap/1.2/security/token"

    with requests.Session() as session:
        session.auth = (LOGIN, PASSWORD)
        response = session.post(url,)
        return response.json()["access_token"]

def get_products_ids(token: str) -> list[str]:
    url = "https://api.moysklad.ru/api/remap/1.2/entity/product"
    response = requests.get(url, headers={"Authorization": "Bearer " + token})
    products_data = response.json()["rows"]
    return [product["id"] for product in products_data]


def get_products_images(token: str, product_id: str) -> list[dict]:

    url = f"https://api.moysklad.ru/api/remap/1.2/entity/product/{product_id}/images"
    response = requests.get(url, headers={"Authorization": "Bearer " + token})
    images_data = response.json()["rows"]

    return [image["meta"] for image in images_data]


def update_products_images(token: str, product_id: str, product_images: list[dict]) -> int:
    url = f"https://api.moysklad.ru/api/remap/1.2/entity/product/{product_id}/images"

    with open("images/igor.png", "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode('ascii')
        igor_data = json.dumps({"filename": "igor.png", "content": encoded_image})


    for product_data in product_images:

        image_data: str = json.dumps({"meta": product_data})

        data_str = f"[{image_data}, {igor_data}]"

        response = requests.post(url, data=data_str, headers={"Authorization": "Bearer " + token, "Content-Type": "application/json", "Accept-Encoding": "gzip"})

        return response.status_code


if __name__ == "__main__":
    token = get_auntefication_token()

    print(token)

    products_ids = get_products_ids(token)

    print(products_ids)

    for product_id in products_ids:
        product_images = get_products_images(token, product_id)
        print(update_products_images(token, product_id, product_images))
        break
