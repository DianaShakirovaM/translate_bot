# Library Bot
## A Telegram bot for searching books using the Open Library API. The bot helps find information about books, authors, and publication years.
---
## Features
- Search books by title
- Book information: author, publication year, Open Library link
- User-friendly interface with buttons
- Open Library integration - access to millions of books

## Technologies
- Python 3.8+
- Aiogram 3.x
- Open Library API - book database

## Installation and Setup
1. Clone and setup
```bash
git clone https://github.com/DianaShakirovaM/seacher_bot
cd search_bot
```
2. Install dependencies
```bash
pip install -r requirements.txt
```
3. Configure environment variables
```env
TOKEN=your_bot_token_from_BotFather
```
4. Run the bot
```bash
python bot.py
```
## Bot commands:
- /start - start working with the bot
- /search_book - search book by title

## How it works:
1. Start the bot with /start command
2. Click "Search Book" button
3. Enter book title

Example Bot Response
```text
📚 The Great Gatsby
✍️ Author(s): F. Scott Fitzgerald
📅 First published: 1925

Powered by Open Library
```
