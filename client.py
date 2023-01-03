import time #library waktu
from paho.mqtt import client as mqtt_client # library untuk membuat client mqtt 

# Detail MQTT broker
broker_url = "broker.emqx.io" # untuk menghubungkan ke broker, menggunakan broker ip/url public emqx
broker_port = 1883 # TCP port untuk menghubungkan ke broker, menggunakan port 1883

username = input("Enter username: ") # username untuk melakukan otentikasi
password = input("Enter password: ") # password untuk melakukan otentikasi

client = mqtt_client.Client() # membuat objek client menggunakan kelas Client dari mqtt_client

### CONNECT SUBSCRIBER TO BROKER ###
def on_connect(client, userdata, flags, rc):
  # client: objek client MQTT yang telah terhubung.
  # userdata: data yang diberikan oleh pengguna ketika membuat objek client MQTT.
  # flags: mengandung informasi tambahan tentang koneksi, misalnya apakah koneksi tersebut merupakan hasil dari pemulihan koneksi setelah terputus.
  # rc (return code): kode koneksi yang menyatakan apakah koneksi tersebut berhasil atau tidak.
    if rc == 0: # di set 0 yang bisa di artikan sebagai connection successfull
        print("\nBerhasil terkoneksi ke MQTT Broker!") # Jika berhasil terconnect maka akan mengoutputkan teks tersebut
    else:
        print("Failed to connect, return code %d\n", rc) # Jika tidak terconnect maka akan mengeluarkan output tersebut

client.username_pw_set(username, password) # untuk melakukan otentikasi dengan username dan password yang sudah di buat
client.on_connect = on_connect # untuk mengecek apakah client terhubung atau tidak
client.connect(broker_url, broker_port) # client melakukan connect ke broker dengan broker_url dan broker_port yang sudah di buat

client.loop_start() # mengirim atau menerima pesan dari broker secara terus-menerus

# Callback function ini akan dipanggil ketika client menerima pesan dari broker.
def on_message(client, userdata, msg): # client: objek client MQTT yang telah terhubung. userdata: data yang diberikan oleh pengguna ketika membuat objek client MQTT. msg: objek pesan yang berisi topik dan payload.
  print(f"\nTopik\t: {msg.topic}\n{msg.payload.decode()}") # untuk menampilkan topik dan payload yang diterima

client.on_message = on_message # untuk mengecek apakah client menerima pesan dari broker atau tidak

# Topik yang akan di subscribe atau unsubscribe
SM = "concerts/smtown"
YG = "concerts/ygent"
subs = [] # daftar topik yang di subscribe lewat list

# Fungsi untuk subscribe atau unsubscribe topik
def subscribe_menu():
  print(f"\nSubscribe/unsubscribe:\n1. {SM}\n2. {YG}") # untuk menampilkan topik yang bisa di subscribe atau unsubscribe
  command = input("\nEnter command: ") # untuk memasukkan command yang akan di lakukan
  if command == str(1):
    # If currently subscribed to SM, unsubscribe. Otherwise, subscribe.
    if SM in subs: 
      subs.pop(subs.index(SM)) # untuk menghapus topik yang di subscribe dari list
      client.unsubscribe(SM) # untuk unsubscribe topik yang di subscribe
    else:
      subs.append(SM) # untuk menambahkan topik yang di subscribe ke list
      client.subscribe(SM) # untuk subscribe topik yang di subscribe
  elif command == str(2):
    # If currently subscribed to YG, unsubscribe. Otherwise, subscribe.
    if YG in subs:
      subs.pop(subs.index(YG)) # untuk menghapus topik yang di subscribe dari list
      client.unsubscribe(YG) # untuk unsubscribe topik yang di subscribe
    else:
      subs.append(YG) # untuk menambahkan topik yang di subscribe ke list
      client.subscribe(YG) # untuk subscribe topik yang di subscribe
  print(f"Currently subscribed to: {subs}") # untuk menampilkan topik yang di subscribe
 
while True: # untuk membuat perulangan yang terus menerus untuk interaksi dengan client
  inputs = input("\nType `menu` to subscribe/unsubscribe\nType anything else to exit\n") # untuk memasukkan command yang akan di lakukan
  if (inputs == "menu"): # jika mengetik "menu" maka akan di jalankan fungsi subscribe_menu()
    subscribe_menu()
  else:
    client.loop_stop() # untuk menghentikan perulangan yang terus menerus
    break;
  time.sleep(1)
  # Jeda ini berguna untuk memberikan waktu kepada client untuk terhubung dengan broker. Jika client belum terhubung dengan broker, maka loop akan terus dijalankan setiap 1 detik hingga client terhubung.

