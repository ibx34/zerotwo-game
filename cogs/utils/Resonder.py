"""
You can add responses to any of the lists, note that unless you use the following tags the bot will not use variables.

── Tags ────────────────────────────

== User tags ==
{user} user#user_tag       | Example: wumpus#0000
{user_name} username       | Example: wumpus
{user_id} userid           | Example: 366649052357591044

== Channel Tags ==
{channel} #channel         | Example: #general
{channel_name} channel     | Example: general
{channel_id} channelid     | Example: 772677756861022209

== Card Tags ==
{rarity} card_rarity       | Example: Mystic
{name} card_name           | Example: ZeroTwo
{series} card_series       | Example: Darling in the FranxX
{damage} card_stats_damage | Example: -_---
{health} card_stats_health | Examole: -_---_---
{cost} card_stats_cost     | Example: -_---_---_---
"""



def respond(message:str,user=None,channel=None,card=None):

    formatted = message.format(**{"user": user, "user_name": user.name, "user_id": user.id, "channel": channel.mention, "channel_name": channel.name, "channel_id": channel.id, "rarity": card.type.value, "name": card.name, "series": card.series, "health": card.stats.health, "damage": card.stats.damage, "price": card.stats.price})
    return formatted

responses = {
    "claim": {
        "success": [
            "**{user_name}**, be gentle with your new **{rarity} {name}**... ",
            "**{user_name}**, OwO congwats you caught a **{rarity} {name}** ~!",
            "**{user_name}**, gg you caught a **{rarity} {name}**!",
            "OwO senpai **{user_name}**, you caught  a **{rarity} {name}**! :pleading_face: am I still your favorite?",
        ]
    }
}