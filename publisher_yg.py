import random  # library untuk membuat random angka
import datetime # library untuk fungsi waktu 
from paho.mqtt import client as mqtt_client # library untuk membuat client mqtt 

# Detail MQTT broker
broker_url = "broker.emqx.io" # untuk menghubungkan ke broker, menggunakan broker ip/url public emqx
broker_port = 1883 # TCP port untuk menghubungkan ke broker, menggunakan port 1883

print("YG Entertaiment Concerts Publisher Menu\n") # menampilkan "YG Entertaiment Concerts Publisher Menu"
username = input("Enter username: ") # username untuk melakukan otentikasi
password = input("Enter password: ") # password untuk melakukan otentikasi

# Set the client ID
client_id = f'python-mqtt-{random.randint(0, 1000)}' # untuk membuat id client dari 0 hingga 1000 secara random

# Set the topic for the SMTOWN concerts
topic = "concerts/ygent" 
# Define a function to connect the publisher to the broker
def connect_mqtt(): # Function yang digunakan untuk melakukan connect ke mqtt
  # Define a callback function for handling successful connections
  def on_connect(client, userdata, flags, rc): 
    # client: objek client MQTT yang telah terhubung.
    # userdata: data yang diberikan oleh pengguna ketika membuat objek client MQTT.
    # flags: mengandung informasi tambahan tentang koneksi, misalnya apakah koneksi tersebut merupakan hasil dari pemulihan koneksi setelah terputus.
    # rc (return code): kode koneksi yang menyatakan apakah koneksi tersebut berhasil atau tidak. Nilai 0 menunjukkan koneksi berhasil, sementara nilai yang lain menunjukkan adanya kesalahan.
    if rc == 0: # di set 0 yang bisa di artikan sebagai connection successfull
      print("\nConnected to MQTT Broker!") # Jika berhasil terconnect maka akan mengoutputkan teks tersebut
    else:
      print("Failed to connect, return code %d\n", rc) # Jika tidak terconnect maka akan mengeluarkan output tersebut

  # Create the MQTT client and set the username and password for authentication
  client = mqtt_client.Client(client_id) # membuat client mqtt dengan client_id yang sudah di buat
  client.username_pw_set(username, password) # untuk melakukan otentikasi dengan username dan password yang sudah di buat
  client.on_connect = on_connect # untuk mengecek apakah client terhubung atau tidak

  # Connect to the broker
  client.connect(broker_url, broker_port) # client melakukan connect ke broker dengan broker_url dan broker_port yang sudah di buat

  return client # mereturn client yang telah terkonfigurasi dan terhubung dengan broker

# Define a function to allow the publisher to publish messages to the broker
def publish(client):
  # Start a loop to allow the publisher to continuously publish messages
  command = 1
  while (command != 0):
    # Print a menu of options
    print("\nCommands: \n1. Publish\n0. Exit") # mengoutputkan menu untuk publisher YGENT 
    command = input("Enter command: ") # meminta inputan berupa angka 1 atau 0 
    if command == str(1):
      # Get the message from the user
      message = input("\nEnter message\t: ") # meminta inputan berupa pesan
      # Get the artist name from the user
      artist = input("Artist name\t: ")  # meminta inputan berupa nama artis
      # Get the schedule for the concert from the user
      try: 
        schedule = datetime.datetime.strptime( # konversi string tanggal dan waktu ke dalam objek datetime
            input('Enter concert schedule in `YYYY/mm/dd - HH:MM` format: '), "%Y/%m/%d - %H:%M") # meminta inputan berupa jadwal konser
      except:
        print("Masukan format yang sesuai, ulangi!") # Jika format yang di inputkan tidak sesuai maka akan mengeluarkan output tersebut dan akan mengulangi inputan jadwal konser
        schedule = datetime.datetime.strptime(
        input('Enter concert schedule in `YYYY/mm/dd - HH:MM` format: '), "%Y/%m/%d - %H:%M")
      # Format the message with the schedule
      msg = f"Pesan\t: {message}\nArtis\t: {artist} \nTempat\t: Sky Dome, Seoul. \nTema\t: GirlBand \nJadwal\t: {schedule}"  # untuk menggabungkan pesan, artis, jadwal konser, dan tempat konser
      result = client.publish(topic, msg) # untuk melakukan publish pesan ke broker
      status = result[0] # untuk mengecek apakah pesan berhasil terpublish atau tidak, kalau 0 terkoneksi, sisanya tidak terkoneksi 
      if status == 0:  
        # Nilai yang dikembalikan oleh fungsi ini adalah None jika berhasil mengirimkan pesan, atau mengembalikan kode kesalahan jika terjadi kesalahan saat mengirimkan pesan.
        print(f"Sent `{msg}` to topic `{topic}`") # Jika berhasil terpublish maka akan mengeluarkan output tersebut
      else:
        print(f"Failed to send message to topic {topic}") # Jika gagal terpublish maka akan mengeluarkan output tersebut
      print ()
    if command == str(0): # Jika command yang di inputkan 0 maka akan keluar dari program
      exit()

# Mendefinisikan fungsi utama
def run():
  # Menghubungkan publisher ke broker
  client = connect_mqtt()
  # mengirim atau menerima pesan dari broker secara terus-menerus
  client.loop_start()
  # Allow the publisher to publish messages
  publish(client)

# Run the main function when the script is executed
if __name__ == '__main__':
  run()