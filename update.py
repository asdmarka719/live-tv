import requests
import re

def main():
    # مصدر القنوات العالمي
    source_url = "https://iptv-org.github.io/iptv/index.m3u"
    try:
        r = requests.get(source_url, timeout=25)
        lines = r.text.split('\n')
        
        final_html = ""
        # القنوات والرموز التعبيرية
        icons = {"sport": "⚽", "yemen": "🇾🇪", "news": "📰", "kids": "🎈", "other": "📺"}
        
        name = ""
        for line in lines:
            if line.startswith("#EXTINF:"):
                name = line.split(",")[-1].strip()
            elif line.startswith("http"):
                url = line.strip()
                cat = "other"
                
                # تصنيف ذكي للقنوات
                low_name = name.lower()
                if any(x in low_name for x in ["bein", "sport", "alkass", "ssc"]): cat = "sport"
                elif any(x in low_name for x in ["yemen", "shabab", "mahr", "masirah", "saeedah", "hawyah", "hadramout"]): cat = "yemen"
                elif any(x in low_name for x in ["news", "aj", "arabia", "hadath"]): cat = "news"
                elif any(x in low_name for x in ["kids", "cartoon", "spacetoon", "mbc3", "baraem"]): cat = "kids"

                # بناء بطاقة القناة
                if cat != "other" or "yemen" in low_name:
                    final_html += f'''
                    <div class="channel-card" data-category="{cat}" onclick="playChan('{url}')">
                        <div class="live-dot"></div>
                        <span class="icon">{icons.get(cat, "📺")}</span>
                        <span>{name}</span>
                    </div>\n'''

        # حقن القنوات في ملف index.html
        with open("index.html", "r", encoding="utf-8") as f:
            content = f.read()

        pattern = r".*?"
        new_content = re.sub(pattern, f"\n{final_html}\n", content, flags=re.DOTALL)

        with open("index.html", "w", encoding="utf-8") as f:
            f.write(new_content)
        print("Success! Channels Rebuilt.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
