from discord_webhook import DiscordWebhook

from config_reader import get_config

config = get_config()


def send_message(msg: str):
    webhook = DiscordWebhook(
        url=config["Discord"]["WebhookUrl"],
        content=msg,
    )

    response = webhook.execute()


def send_embed(title: str, msg: str, filename: str):
    webhook = DiscordWebhook(url=config["Discord"]["WebhookUrl"])
    embed = DiscordEmbed(title=title, description=msg, color="03b2f8")
    with open(filename, "rb") as f:
        webhook.add_file(file=f.read(), filename=filename)
    embed.set_image(url=f"attachment://{filename}")
    webhook.add_embed(embed)
    response = webhook.execute()


def send_image(filename: str):
    webhook = DiscordWebhook(url=config["Discord"]["WebhookUrl"])

    with open(filename, "rb") as f:
        webhook.add_file(file=f.read(), filename=filename)

    response = webhook.execute()


if __name__ == "__main__":
    send_message("Hello, ~~World~~Discord!")
