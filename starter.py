from pyrogram import Client
from pyrogram.errors import FloodWait
from pyrogram.types import Message
import os
import time

# Replace these values with your actual API ID, API hash and chat ID
api_id = 123456780
api_hash = "19de0410407fde42a6c9750a18b65f01"
chat_id = -1001111111111

# Path to your session file
session_file = "my_session.session"

# Initialize the Pyrogram Client with the existing session file
app = Client(
    session_file,
    api_id=api_id,
    api_hash=api_hash,
)



# Ensure the download directory exists
download_dir = "downloads"
os.makedirs(download_dir, exist_ok=True)

async def extract_media():
    async with app:
        try:
            async for message in app.get_chat_history(chat_id):
                # Process media if message contains any
                if message.media_group_id:
                    # Handle albums (grouped media)
                    media_group = await app.get_media_group(chat_id, message.id)
                    for media_message in media_group:
                        await download_media(media_message)
                else:
                    await download_media(message)
        except FloodWait as e:
            print(f"FloodWait error: Need to wait for {e.x} seconds")
            time.sleep(e.x)
            await extract_media()  # Retry after waiting

async def download_media(message: Message):
    try:
        if message.photo:
            # Download photo
            file_name = f"photo_{message.id}.jpg"
            file_path = os.path.join(download_dir, file_name)
            await message.download(file_path)
            print(f"Downloaded: {file_name}")

        elif message.video:
            # Download video
            file_name = f"video_{message.id}.mp4"
            file_path = os.path.join(download_dir, file_name)
            await message.download(file_path)
            print(f"Downloaded: {file_name}")

        elif message.document:
            # Download document
            file_name = f"document_{message.id}_{message.document.file_name}"
            file_path = os.path.join(download_dir, file_name)
            await message.download(file_path)
            print(f"Downloaded: {file_name}")

        elif message.animation:
            # Download animation (GIF)
            file_name = f"animation_{message.id}.gif"
            file_path = os.path.join(download_dir, file_name)
            await message.download(file_path)
            print(f"Downloaded: {file_name}")

        # Add more conditions as needed for other media types
        else:
            # Handle messages without media (optional)
            print(f"Message {message.id} does not contain media.")
    except FloodWait as e:
        print(f"FloodWait error: Need to wait for {e.x} seconds")
        time.sleep(e.x)
        await download_media(message)  # Retry after waiting

if __name__ == "__main__":
    app.run(extract_media())
