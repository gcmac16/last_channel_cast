import argparse
import os
from urllib.parse import quote

import requests
from dotenv import load_dotenv


def get_request_headers():
    return {
        "accept": "application/json",
        "api_key": get_api_key(),
    }


def get_api_key():
    api_key = os.getenv("NEYNAR_API_KEY")
    if not api_key:
        load_dotenv()
        api_key = os.getenv("NEYNAR_API_KEY")
        if not api_key:
            raise ValueError(
                "NEYNAR_API_KEY environment variable not set and not found in .env file"
            )

    return api_key


def get_last_cast(fid, channel_url):
    encoded_channel_url = quote(channel_url)
    url = f"https://api.neynar.com/v1/farcaster/casts?fid={fid}&parent_url={encoded_channel_url}&limit=25"

    response = requests.get(url, headers=get_request_headers())

    if response.status_code == 200:
        cast = response.json()["result"]["casts"][0]["text"]
        print(cast)
    else:
        print(f"Failed to retrieve casts. HTTP Status Code: {response.status_code}")


def get_user_fid(username):
    url = f"https://api.neynar.com/v1/farcaster/user-by-username?username={username}"
    response = requests.get(url, headers=get_request_headers())

    if response.status_code == 200:
        try:
            return response.json()["result"]["user"]["fid"]
        except KeyError:
            raise ValueError(f"No user '{username}' exists")
    elif response.status_code == 404:
        raise ValueError(f"No user '{username}' exists")
    else:
        raise Exception(
            f"Failed to retrieve user FID. HTTP Status Code: {response.status_code}"
        )


def get_channel_url(channel_name):
    url = f"https://api.neynar.com/v2/farcaster/channel?id={channel_name}"
    response = requests.get(url, headers=get_request_headers())

    if response.status_code == 200:
        try:
            return response.json()["channel"]["parent_url"]
        except KeyError:
            raise ValueError(f"No channel '{channel_name}' exists")
    elif response.status_code == 404:
        raise ValueError(f"No channel '{channel_name}' exists")
    else:
        raise Exception(
            f"Failed to retrieve channel URL. HTTP Status Code: {response.status_code}"
        )


def main(username, channel_name):
    try:
        fid = get_user_fid(username)
        channel_url = get_channel_url(channel_name)
    except Exception as e:
        print(f"ERROR: {e}")

    try:
        get_last_cast(fid, channel_url)
    except IndexError:
        print(f"ERROR: {username} has never casted in /{channel_name}")
    except Exception as e:
        print(f"ERROR: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Get the last cast from a specified user in a specified channel using Neynar."
    )
    parser.add_argument("fc_username", type=str, help="The FC username of the user")
    parser.add_argument("channel_name", type=str, help="The name of the channel")

    args = parser.parse_args()
    main(args.fc_username, args.channel_name)
