import json
import os
import hashlib
import secrets
# è·åå½åæä»¶æå¨çç®å½
current_dir = os.path.dirname(os.path.realpath(__file__))
# è¯»åéç½®æä»¶
with open(os.path.join(current_dir, 'uu.json'), 'r') as f:
    config = json.load(f)
