# Delerious Discord Bot

<a href="https://github.com/Skylier07/discord-bot">
  <img alt="GitHub last commit (branch)"
       src="https://img.shields.io/github/last-commit/Skylier07/discord-bot/main">
</a>

<a href="https://github.com/Skylier07/discord-bot/blob/main/LICENSE">
  <img alt="GitHub License"
       src="https://img.shields.io/github/license/Skylier07/discord-bot">
</a>

A comprehensive Discord bot for managing Hypixel SkyBlock guild operations, carrier applications, and user verification for the Delerious community.

## 🎯 Features

- **User Verification**: Link Discord accounts to Minecraft/Hypixel accounts
- **Carrier Applications**: Automated application system for dungeon and slayer carriers with requirement checking
- **Guild Applications**: Streamlined guild application process with automatic approval
- **Scammer Detection**: Integration with SBZ (SkyBlockZ) scammer database for security
- **Guild Synchronization**: Automatic role synchronization based on guild membership
- **Admin Commands**: Bot management commands for syncing and restarting

## 📋 Prerequisites

- Python 3.8 or higher
- Discord Bot Token
- Hypixel API Key
- MongoDB Database (MongoDB Atlas or local instance)
- SBZ/Jerry API Key (for scammer checking)

## 🚀 Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/Skylier07/skyblock-bot.git
   cd delerious-bot
   ```

2. **Install dependencies**

   ```bash
   pip install discord.py Flask pymongo requests
   ```

3. **Configure your environment**

   Copy `keys.example.py` to `keys.py` (ignored by git) and fill in your credentials:

   ```python
   BOT_TOKEN = "your-discord-bot-token"
   MONGO_URI = "your-mongodb-connection-string"
   API_KEY = "your-hypixel-api-key"
   JERRY_API_KEY = "your-jerry-api-key"
   ```

4. **Update bot configuration**

   Edit `bot.py` and replace:

   - Bot token (line 220)
   - MongoDB URI (line 22)
   - Guild ID (replace `732620946300600331` with your guild ID)
   - Channel IDs as needed

## ⚙️ Configuration

### Required Discord Intents

The bot requires the following Discord intents:

- `messages`
- `message_content`
- `guilds`
- `members`

Enable these in your [Discord Developer Portal](https://discord.com/developers/applications).

### Database Setup

The bot uses MongoDB to store user verification data. Ensure your MongoDB database has a collection named `users` in a database named `Delerious`.

### Role Setup

The bot expects the following roles in your Discord server:

- `Verified`
- `Carry Team`
- `F1 Carrier` through `F6 Carrier`
- `Revenant Carrier`, `Tarantula Carrier`, `Sven Carrier`
- `Spruce Guild`
- `Guild Member`
- `Application Blacklisted`
- `Owner` (for admin commands)

## 📖 Usage

### Starting the Bot

```bash
python bot.py
```

### Commands

#### User Commands

- `/verify <username>` - Link your Discord account to your Minecraft account
- `/apply_dungeon_carrier <floor> [evidence]` - Apply to become a dungeon carrier
- `/apply_slayer_carrier <slayer>` - Apply to become a slayer carrier
- `/apply_guild <guild>` - Apply to join a Delerious guild

#### Admin Commands

- `/sync` - Sync bot to latest git branch (Owner only)
- `/restart` - Restart the bot (Owner only)
- `/carrier_embed` - Post carrier application embed (Owner only)
- `/guild_embed` - Post guild application embed (Owner only)

### Application Requirements

#### Dungeon Carriers

- **Floor 6**: Cata XP ≥ 13.26M
- **Floor 5**: Cata XP ≥ 3.08M
- **Floor 4**: Cata XP ≥ 1.24M
- **Floor 3**: Cata XP ≥ 488.6k
- **Floor 2**: Cata XP ≥ 188.1k
- **Floor 1**: Cata XP ≥ 97.6k

#### Slayer Carriers

- **All Slayers**: Slayer XP ≥ 20,000

#### Guild Requirements

- **Spruce Guild**: No entry requirement (automatic approval)

## 🏗️ Project Structure

```
delerious-bot/
├── bot.py              # Main bot file with commands and event handlers
├── hypixel_api.py      # Hypixel API integration for player data
├── verification.py     # User verification utilities
├── scammer.py          # Scammer database checking
├── skycrypt.py         # SkyCrypt API integration (legacy)
├── keys.example.py     # Sample credentials file (copy to keys.py)
├── keys.py             # Local credentials (git-ignored)
└── README.md           # This file
```

## 🔧 Key Components

### Verification System

- Links Discord accounts to Minecraft accounts via Hypixel social media links
- Stores verification data in MongoDB
- Required before applying for carrier or guild positions

### Application System

- Automated requirement checking using Hypixel API
- Manual review system for applications that don't meet bypass requirements
- Scammer database integration for security
- Automatic role assignment upon approval

### Guild Synchronization

- Runs every 12 hours (43200 seconds)
- Syncs Discord roles with actual guild membership
- Removes roles from members who left the guild
- Adds roles to new guild members

## 🔒 Security Notes

⚠️ **Important**: Before deploying, ensure you:

- Never commit `keys.py` or any files containing API keys/tokens
- Use environment variables or secure secret management in production
- Add `keys.py` to `.gitignore`
- Rotate any exposed credentials immediately

## 📝 License

This project is private and proprietary. All rights reserved.

## 🤝 Contributing

This is a private project for the Delerious community. For issues or suggestions, please contact the project maintainers.

## 📞 Support

For support, open a ticket in the Delerious Discord server or contact me through Discord `a.weeb`

---

**Note**: This bot is specifically designed for the Delerious Discord server and may require modifications for use in other servers.
