import yt_dlp
info_dict = yt_dlp.YoutubeDL({'extract_flat': True, 'skip_download': True}).extract_info(str(input("Donnez le lien de la video/playlist: ")), download=False)
playlist_url = str(input("Donnez le lien de la video/playlist: "))
if "_type" not in info_dict: yt_dlp.YoutubeDL({'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best', 'outtmpl': '%(title)s.%(ext)s'}).extract_info(playlist_url, download=True)
else:
    if not info_dict['entries']: info_dict = yt_dlp.YoutubeDL({'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best', 'outtmpl': '%(title)s.%(ext)s'}).extract_info("https://www.youtube.com/playlist?"+(playlist_url.split("list=")[1]).split("&")[0], download=False)
    try:
        for i in [entry['url'] for entry in info_dict['entries']]: yt_dlp.YoutubeDL({'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best', 'outtmpl': '%(title)s.%(ext)s'}).extract_info(i, download=True)
    except: pass
