import requests
import re

def main():
    source = "https://iptv-org.github.io/iptv/index.m3u"
    try:
        # محاولة جلب القنوات مع وقت انتظار أطول
        r = requests.get(source, timeout=40)
        r.raise_for_status() # التأكد من عدم وجود خطأ في الطلب
        lines = r.text.split('\n')
        
        cards_html = ""
        name = ""
        for line in lines:
            if line.startswith("#EXTINF:"):
                name = line.split(",")[-1].strip()
            elif line.startswith("http"):
                url = line.strip()
                low_name = name.lower()
                # البحث عن beIN واليمن الإضافية
                if any(k in low_name for k in ["bein", "sport", "saeedah", "hadramout"]):
                    cards_html += f'''
                    <div class="channel-card" onclick="playChan('{url}')">
                        <span>{name}</span>
                    </div>\n'''

        with open("index.html", "r", encoding="utf-8") as f:
            content = f.read()

        # استبدال القنوات الديناميكية فقط
        new_content = re.sub(r".*?", 
                             f"\n{cards_html}\n", 
                             content, flags=re.DOTALL)

        with open("index.html", "w", encoding="utf-8") as f:
            f.write(new_content)
        print("Success: New channels added.")
    except Exception as e:
        # في حال الفشل، لا يفعل شيئاً ويترك القنوات الثابتة تعمل
        print(f"Update failed, keeping static channels. Error: {e}")

if __name__ == "__main__":
    main()
