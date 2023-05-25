import uuid

import cv2
import numpy as np

from articles.models import Change
from PIL import Image


def change(img, serializer):
    change_post = Change.objects.get(id=serializer['id'])
    now = uuid.uuid4()

    net = cv2.dnn.readNetFromTorch('models/candy.t7')
    data = cv2.imread((f'.{img}'))

    # 인코딩 및 디코딩
    encoded_img = np.fromstring(data, dtype=np.uint8)
    img = cv2.imdecode(encoded_img, cv2.IMREAD_COLOR)

    h, w, c = data.shape
    img = cv2.resize(data, dsize=(500, int(h / w * 500)))
    MEAN_VALUE = [103.939, 116.779, 123.680]
    blob = cv2.dnn.blobFromImage(img, mean=MEAN_VALUE)

    net.setInput(blob)
    output = net.forward()
    output = output.squeeze().transpose((1, 2, 0))
    output += MEAN_VALUE

    # 크기에 맞게 자르고 type을 바꿔줌
    output = np.clip(output, 0, 255)
    output = output.astype('uint8')
    output = Image.fromarray(output)


    # 이미지 저장
    change_image = f"after_image/{change_post.user.nickname}_{now}.jpg"
    # cv2.imwrite(f"./media/after_image/{change_image}", output)
    output.save(f"./media/{change_image}", "JPEG")
    change_post.change_image = change_image
    change_post.save()