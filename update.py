import requests
import re

def main():
    sources = [
        "https://iptv-org.github.io/iptv/index.m3u",
        "https://raw.githubusercontent.com/iptv-org/iptv/master/streams/ar.m3u"
    ]
    
    cards = ""
    seen = set()

    for src in sources:
        try:
            r = requests.get(src, timeout=20)
            lines = r.text.split('\n')
            name = ""
            for line in lines:
                if line.startswith("#EXTINF:"):
                    name = line.split(",")[-1].strip()
                elif line.startswith("http") and line not in seen:
                    url = line.strip()
                    low = name.lower()
                    cat = ""
                    icon = "📺"

                    # الفلاتر الذكية
                    if any(x in low for x in ["quran", "sunnah", "islam", "قرآن", "سنة"]): cat, icon = "islam", "🌙"
                    elif any(x in low for x in ["yemen", "shabab", "mahr", "masirah", "aden", "hadramout", "يمن"]): cat, icon = "yemen", "🇾🇪"
                    elif any(x in low for x in ["bein", "sport", "alkass", "ssc", "كاس", "رياضة"]): cat, icon = "sport", "⚽"
                    elif any(x in low for x in ["national", "doc", "وثائقية", "wild"]): cat, icon = "doc", "🐾"
                    elif any(x in low for x in ["wwe", "fight", "slap", "مصارعة"]): cat, icon = "fight", "🥊"
                    elif any(x in low for x in ["movie", "cinema", "أفلام", "مسرح", "play"]): cat, icon = "movie", "🎬"

                    if cat:
                        cards += f'<div class="card" data-cat="{cat}" onclick="play(\'{url}\')"><i>{icon}</i><span>{name}</span></div>\n'
                        seen.add(url)
        except: continue

    with open("index.html", "r", encoding="utf-8") as f:
        content = f.read()

    new_content = re.sub(r".*?", 
                         f"\n{cards}\n", 
                         content, flags=re.DOTALL)

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(new_content)

if __name__ == "__main__":
    main()
