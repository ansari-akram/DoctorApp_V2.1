import sys
import urllib3
import json
import requests
import os
from Pathology.views import *

urllib3.disable_warnings()

# import sys
# print(sys.argv[1:])
# file_name = sys.argv[1]
# print(file_name)

# a =   Lab_Api.objects.all()

# POWER_AI_VISION_API_URL = "https://10.150.20.65/powerai-vision/api/dlapis/73ba9966-b631-4ea9-86e7-16a063a864a9"


def detect_image_label(file_name, url):
    rc11 = 0
    retry_count = 0
    label_value = ''
    confidence = 0
    result = ''
    while (rc11 != 200) and (retry_count < 5):
        if retry_count != 0:
            print("[INFO] Retrying Image uploading to SERVER...")

        try:
            with open(file_name, 'rb') as f:
                s = requests.Session()
                r = s.post(url, files={'files': (file_name, f), 'containHeatMap': 'true'}, verify=False, timeout=10)
            data = json.loads(r.text)
            result = data["result"]
            heatmap = data['heatmap']
            data_label = data["classified"]
            for label, val in data_label.items():
                confidence = float(val)
                confidence = confidence * 100
                label_value = label

            rc11 = r.status_code

            return result, label_value, confidence, heatmap

        except Exception as exc:
            rc1 = 0
            retry_count = retry_count + 1
            continue
