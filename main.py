import discord
import os
import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

client = discord.Client(intents=intents)

async def analyze():
    joke_channel = client.get_channel(891948673095852052)
    analyze_channel = client.get_channel(1284589236200276128)
    
    today = datetime.datetime.now() - datetime.timedelta(days=1)
    first_day = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    # 今月1日からのメッセージをすべて取得
    messages = [message async for message in joke_channel.history(after=first_day)]

    # 表示名, 本文, いいね数をリストに出力
    authors = [message.author.global_name for message in messages]
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

    up_to = 5 #一時的に数値をハードコードしています, 後で外部から変更可能にするかもしれません
    count = 0

    await analyze_channel.send(f'嘘をつくチャンネル いいね数上位{up_to}件 {first_day.month}月分')

    # ユーザー名, 本文, いいね数を1つのメッセージにまとめて送信
    for (author, content, thumbsup_count) in zip(sorted_authors, sorted_contents, sorted_thumbsup_counts):
        # 指定した順位まで出力したらBreak
        # でもこれ同列があったとき意図しない動作するような...?
        if count == up_to:
            break
        # いいね数1以上の嘘のみ出力
        if thumbsup_count >= 1:
            await analyze_channel.send(f'ユーザー: {author}\n> {content}\n \N{Thumbs Up Sign}: {thumbsup_count}')
            count += 1

@client.event
async def on_ready():
    print('Logged in as New Chitose Bot')
    jst = datetime.timezone(datetime.timedelta(hours=9))
    scheduler = AsyncIOScheduler()
    scheduler.configure(timezone=jst)
    scheduler.add_job(analyze, 'cron', day=1)
    scheduler.start()

client.run(os.environ['TOKEN'])