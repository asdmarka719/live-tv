import requests
import re

def main():
    # مصادر شاملة (عالمية وعربية) لضمان تغطية نايل سات و beIN
    sources = [
        "https://iptv-org.github.io/iptv/index.m3u",
        "https://raw.githubusercontent.com/mohamed-attya/IPTV-Free-Arabic/master/Arabic.m3u",
        "https://raw.githubusercontent.com/iptv-org/iptv/master/streams/ar.m3u"
    ]
    
    all_cards = ""
    seen_urls = set()

    for url_src in sources:
        try:
            r = requests.get(url_src, timeout=30)
            if r.status_code != 200: continue
            
            lines = r.text.split('\n')
            name = ""
            for line in lines:
                if line.startswith("#EXTINF:"):
                    name = line.split(",")[-1].strip()
                elif line.startswith("http") and line.strip() not in seen_urls:
                    link = line.strip()
                    low_name = name.lower().replace(" ", "")
                    
                    cat = ""
                    # فلترة beIN 1-9 و MAX
                    if "bein" in low_name:
                        if any(num in low_name for num in ["1","2","3","4","5","6","7","8","9","max"]):
                            cat = "sport"
                    # فلترة قنوات نايل سات واليمن
                    elif any(x in low_name for x in ["yemen", "shabab", "mahr", "saeedah", "hawyah", "masirah", "aden", "mbc", "drama", "kids"]):
                        cat = "yemen" if "yemen" in low_name or "shabab" in low_name else "movie"
                    # وثائقي ومصارعة
                    elif any(x in low_name for x in ["national", "natgeo", "wwe", "wrestling", "fight"]):
                        cat = "doc" if "nat" in low_name else "fight"
                    # إسلامي
                    elif any(x in low_name for x in ["quran", "sunnah", "islam", "قرآن"]):
                        cat = "islam"

                    if cat:
                        icon = {"sport":"⚽", "yemen":"🇾🇪", "islam":"🌙", "doc":"🐾", "fight":"🥊", "movie":"📺"}.get(cat, "🎬")
                        all_cards += f'<div class="card" data-cat="{cat}" onclick="playHLS(\'{link}\')"><i>{icon}</i><span>{name}</span></div>\n'
                        seen_urls.add(link)
        except: continue

    if not all_cards:
        print("No channels found, skipping update to protect index.html")
        return

    # قراءة الملف وحقن البيانات بدقة لضمان عدم تلف التصميم
    with open("index.html", "r", encoding="utf-8") as f:
        content = f.read()

    new_content = re.sub(r".*?", 
                         f"\n{all_cards}\n", 
                         content, flags=re.DOTALL)

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(new_content)
    print("إمبراطورية القنوات جاهزة!")

if __name__ == "__main__":
    main()
