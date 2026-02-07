import requests
import re

def main():
    # سنستخدم قائمة مصادر لضمان الحصول على أكبر عدد من القنوات
    sources = [
        "https://iptv-org.github.io/iptv/index.m3u",
        "https://raw.githubusercontent.com/iptv-org/iptv/master/streams/ar.m3u"
    ]
    
    all_cards = ""
    processed_urls = set() # لمنع التكرار

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
                    
                    # الفلتر الذكي والشامل:
                    # يبحث عن: بين، كاس، يمن، سعيدة، هوية، طفال، كرتون، اخبار، ام بي سي
                    targets = ["bein", "sport", "alkass", "ssc", "yemen", "saeedah", "hawyah", "shabab", "mahr", "kids", "cartoon", "mbc", "news"]
                    
                    if any(t in low_name for t in targets):
                        # تحديد أيقونة مناسبة لكل نوع
                        icon = "📺"
                        if "sport" in low_name or "bein" in low_name: icon = "⚽"
                        elif "yemen" in low_name: icon = "🇾🇪"
                        elif "kids" in low_name or "cartoon" in low_name: icon = "🎈"
                        
                        all_cards += f'''
                        <div class="card" onclick="play('{url}')">
                            <div class="badge">LIVE</div>
                            <div style="font-size:20px; margin-bottom:5px;">{icon}</div>
                            <span>{name}</span>
                        </div>\n'''
                        processed_urls.add(url)
        except:
            continue

    if all_cards:
        with open("index.html", "r", encoding="utf-8") as f:
            content = f.read()

        # استبدال المحتوى بين العلامات المخصصة
        new_content = re.sub(r".*?", 
                             f"\n{all_cards}\n", 
                             content, flags=re.DOTALL)

        with open("index.html", "w", encoding="utf-8") as f:
            f.write(new_content)
        print("Success! Multi-source update completed.")

if __name__ == "__main__":
    main()
