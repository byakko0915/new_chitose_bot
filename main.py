import discord
from discord import app_commands
import os
import datetime

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

@client.event
async def on_ready():
    print('Logged in as New Chitose Bot')
    await tree.sync()

@tree.command(name="test",description="Test command for anayalize jokes")
async def test_command(interaction: discord.Interaction, up_to: int):
    channel = client.get_channel(1071907616395100233)
    today = datetime.datetime.now()
    first_day = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    # 今月1日からのメッセージをすべて取得
    messages = [message async for message in channel.history(after=first_day)]

    # ユーザー名, 本文, いいね数をリストに出力
    authors = [message.author.mention for message in messages]
    contents = [message.content for message in messages]

    # リスト内包表記で何もなかった場合の記述ができるのか不明だったため一般的なループでの処理
    # なんとかなったらいいな
    thumbsup_counts = []

    for message in messages:
        for reaction in message.reactions:
            if reaction.emoji == "\N{Thumbs Up Sign}":
                thumbsup_counts.append(reaction.normal_count)
                break
        else:
            thumbsup_counts.append(0)
    
    # このコードは上のコードに代替されました
    # thumbsup_counts = [reaction.normal_count for message in messages for reaction in message.reactions if reaction.emoji == "\N{Thumbs Up Sign}"]
    
    # このコードは1つ上のコメントのコードを展開したものだったはずです
    # for message in messages:
    #   for reaction in message.reactions
    #     if reaction.emoji == ':thumbsup:':
    #       thumbsup.append(reaction.normal_count)

    # いいね数順にソート
    zipped_lists = zip(thumbsup_counts, authors, contents)
    zipped_sorted_lists = sorted(zipped_lists, reverse=True)
    sorted_thumbsup_counts, sorted_authors, sorted_contents = zip(*zipped_sorted_lists)

    await interaction.response.send_message('Aggregation currently in process')

    count = 0

    # ユーザー名, 本文, いいね数を1つのメッセージにまとめて送信
    for (author, content, thumbsup_count) in zip(sorted_authors, sorted_contents, sorted_thumbsup_counts):
        print(count)
        # 指定した順位まで出力したらBreak
        # でもこれ同列があったとき意図しない動作するような...?
        if count == up_to:
            break
        # いいね数1以上の嘘のみ出力
        if thumbsup_count >= 1:
            await interaction.followup.send(f'ユーザー: {author}\n> {content}\n \N{Thumbs Up Sign}: {thumbsup_count}',ephemeral=True)
            count += 1

client.run(os.environ['TOKEN'])