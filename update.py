import requests
import re

def main():
    sources = [
        "https://iptv-org.github.io/iptv/index.m3u",
        "https://raw.githubusercontent.com/iptv-org/iptv/master/streams/ar.m3u"
    ]
    
    all_cards = ""
    processed_urls = set()

    for source_url in sources:
        try:
            r = requests.get(source_url, timeout=30)
            lines = r.text.split('\n')
            name = ""
            for line in lines:
                if line.startswith("#EXTINF:"):
                    name = line.split(",")[-1].strip()
                elif line.startswith("http") and line.strip() not in processed_urls:
                    url = line.strip()
                    low_name = name.lower()
                    
                    # الفئات: إسلامي، يمني، وثائقي، مصارعة، أفلام، رياضة
                    cat = ""
                    if any(x in low_name for x in ["quran", "sunnah", "islam", "makkah", "madinah", "قرآن", "سنة", "إسلام"]): cat = "islam"
                    elif any(x in low_name for x in ["yemen", "shabab", "mahr", "saeedah", "hawyah", "masirah", "aden", "hadramout", "يمن"]): cat = "yemen"
                    elif any(x in low_name for x in ["national", "abu dhabi nat", "documentary", "وثائقية"]): cat = "doc"
                    elif any(x in low_name for x in ["wwe", "wrestling", "مصارعة", "slap"]): cat = "fight"
                    elif any(x in low_name for x in ["movie", "cinema", "أفلام", "روتانا"]): cat = "movie"
                    elif any(x in low_name for x in ["bein", "sport", "alkass", "ssc"]): cat = "sport"

                    if cat:
                        icons = {"islam": "🌙", "yemen": "🇾🇪", "doc": "🐾", "fight": "🥊", "movie": "🎬", "sport": "⚽"}
                        all_cards += f'''
                        <div class="card" data-category="{cat}" onclick="play('{url}')">
                            <div class="badge">{cat.upper()}</div>
                            <div style="font-size:20px; margin-bottom:5px;">{icons.get(cat, "📺")}</div>
                            <span>{name}</span>
                        </div>\n'''
                        processed_urls.add(url)
        except: continue

    with open("index.html", "r", encoding="utf-8") as f:
        content = f.read()
    new_content = re.sub(r".*?", f"\n{all_cards}\n", content, flags=re.DOTALL)
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(new_content)
    print("Update Done!")

if __name__ == "__main__":
    main()
