import requests
import re

def main():
    try:
        # مصادر قوية للقنوات
        source = "https://iptv-org.github.io/iptv/index.m3u"
        r = requests.get(source, timeout=30)
        lines = r.text.split('\n')
        
        cards = ""
        name = ""
        for line in lines:
            if line.startswith("#EXTINF:"):
                name = line.split(",")[-1].strip()
            elif line.startswith("http"):
                url = line.strip()
                # جلب beIN و Alkass والسعيدة فقط لعدم إثقال الصفحة
                if any(x in name.lower() for x in ["bein", "alkass", "ssc", "saeedah", "hawyah"]):
                    cards += f'<div class="card" onclick="play(\'{url}\')"><div class="badge">Auto</div><span>{name}</span></div>\n'

        if not cards: return # إذا لم يجد شيئاً لا يغير الصفحة

        with open("index.html", "r", encoding="utf-8") as f:
            content = f.read()

        # حقن البطاقات في المكان المخصص
        new_content = re.sub(r".*?", 
                             f"\n{cards}\n", 
                             content, flags=re.DOTALL)

        with open("index.html", "w", encoding="utf-8") as f:
            f.write(new_content)
        print("Success!")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
