#!/usr/bin/python3
"""Consume and process data from the JSONPlaceholder API."""
import csv
import requests

URL = "https://jsonplaceholder.typicode.com/posts"


def fetch_and_print_posts():
    """Fetch all posts, print the status code and the title of each post."""
    response = requests.get(URL)
    print("Status Code: {}".format(response.status_code))

    if response.status_code == 200:
        posts = response.json()
        for post in posts:
            print(post["title"])


def fetch_and_save_posts():
    """Fetch all posts and save id, title and body into posts.csv."""
    response = requests.get(URL)

    if response.status_code == 200:
        posts = response.json()
        data = [
            {"id": post["id"], "title": post["title"], "body": post["body"]}
            for post in posts
        ]

        with open("posts.csv", "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=["id", "title", "body"])
            writer.writeheader()
            writer.writerows(data)
