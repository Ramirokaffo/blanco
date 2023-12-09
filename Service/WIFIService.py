import subprocess
import socket


# meta_data = subprocess.check_output(["netsh", "wlan", "show", "profiles"])
# meta_data = subprocess.check_output(["ipconfig"])
# print(meta_data)
# data = meta_data.decode("utf-8", errors="backslashreplace")
#
# data = data.split("\n")

# print(data)

class WIFIService:

    @staticmethod
    def get_local_ip():
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(("192.255.255.255", 1))
            IP = s.getsockname()[0]
        except:
            IP = "127.0.0.1"
        finally:
            s.close()
        return IP

