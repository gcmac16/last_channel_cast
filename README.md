# Last Cast in Channel By User

This script fetches the last cast from a specified user in a specified channel using the Neynar API. It uses environment variables for API keys and can read from a `.env` file if the environment variable is not set.

## Features

- Retrieves the user FID (Farcaster ID) by username.
- Retrieves the channel URL by channel name.
- Fetches and prints the last cast from the specified user in the specified channel.

## Requirements

- Python 3.x

## Setup

1. Install the required Python libraries:
    ```bash
    pip install -r requirements.txt
    ```

2. Create a `.env` file in the same directory as the script (if not using environment variables directly) with the following content:
    ```
    NEYNAR_API_KEY=your_api_key_here
    ```

## Usage

Run the script with the username and channel name as arguments:

```bash
python get_last_cast.py [fc_username] [channel_name]
```

Replace `[fc_username]` with the Farcaster username and `[channel_name]` with the name of the channel you want to query.

Example:
```bash
python get_last_cast.py dwr farcaster
```

This script fetches and prints the last cast from a specified user in a specified channel using the Neynar API. Ensure the API key is set as an environment variable or in a `.env` file.