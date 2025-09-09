# Overview

This is a Discord bot designed to format Roblox server configurations for the RoleplayM system. The bot uses AI-powered text processing through Groq's API to automatically correct and standardize server configuration formats. Users can submit raw configuration text via Discord commands, and the bot returns properly formatted RoleplayM-compatible configuration tables with enforced standards and validation.

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Bot Framework
- **Discord.py**: Uses the `commands.Bot` class for handling Discord interactions
- **Command System**: Prefix-based commands (using "." as prefix) for user interactions
- **Intent Configuration**: Enables message content, guild, and member intents for full functionality

## AI Integration
- **Groq API**: Asynchronous client for AI-powered text processing and formatting
- **Prompt Engineering**: Custom prompts designed to enforce RoleplayM configuration standards
- **Text Processing**: Converts raw user input into standardized Lua table format

## Configuration Management
- **Base Constants**: Predefined `TABLE_VALUES` dictionary containing default RoleplayM configuration values
- **Validation**: AI system enforces required fields, data types, and formatting standards
- **Standardization**: Ensures consistent capitalization, field placement, and value constraints

## Security & Permissions
- **Role-based Access**: Uses `MOD_ROLE_ID` for command permission control
- **Environment Variables**: Secure storage of Discord token and Groq API key
- **Input Sanitization**: AI processing includes validation of user-submitted configuration data

## Data Flow
1. User submits raw configuration text via Discord command
2. Bot validates user permissions against moderator role
3. Raw text is processed through Groq AI with formatting prompts
4. AI returns standardized RoleplayM configuration format
5. Formatted result is sent back to Discord channel

# External Dependencies

## APIs and Services
- **Discord API**: Primary platform for bot interactions and user interface
- **Groq API**: AI language model service for intelligent text formatting and validation

## Environment Configuration
- **DISCORD_TOKEN**: Bot authentication token for Discord API access
- **GROQ_API_KEY**: Authentication key for Groq AI service access

## Python Packages
- **discord.py**: Discord bot framework and API wrapper
- **groq**: Asynchronous client library for Groq AI API integration
- **os**: Built-in module for environment variable access

## External Integrations
- **Roblox Platform**: Target platform for generated server configurations
- **RoleplayM System**: Specific Roblox server management system with defined configuration format requirements