import discord
import youtube_dl
import asyncio

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class ytdlSrc(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, playNow = None, toQueue = None, volume=0.5):
        super().__init__(source, volume)
        self.data = data

        if not playNow:
            self.title = data.get('title')
        else:
            self.title = playNow.get('title')
        self.toQueue = toQueue
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, bot, guild, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        q = None
        if 'entries' in data:
            if len(data['entries']) > 1:
                playlistLength = len(data['entries'])
                q = data['entries'][1:playlistLength]
            p = data['entries'][0]
        else:
            p = data

        filename = p['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data, playNow=p, toQueue=q)