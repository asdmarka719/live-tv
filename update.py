import requests
import re

def main():
    url = "https://iptv-org.github.io/iptv/index.m3u"
    try:
        r = requests.get(url, timeout=25)
        lines = r.text.split('\n')
        
        output_html = ""
        name = ""
        for line in lines:
            if line.startswith("#EXTINF:"):
                name = line.split(",")[-1].strip()
            elif line.startswith("http"):
                url_link = line.strip()
                category = "other"
                
                # فلاتر البحث الذكية
                low_name = name.lower()
                if any(s in low_name for s in ["bein", "sport", "alkass", "ssc"]): category = "sport"
                elif any(y in low_name for y in ["yemen", "shabab", "mahr", "masirah", "saeedah", "hawyah", "hadramout"]): category = "yemen"
                elif any(n in low_name for n in ["news", "aj", "arabia", "hadath", "sky"]): category = "news"

                # إذا كانت القناة تهمنا، أضفها بالتنسيق الجديد
                if category != "other":
                    output_html += f'''
                    <div class="channel-item" data-category="{category}" onclick="playChan('{url_link}')">
                        <div class="live-label">LIVE</div>
                        <span>📺</span>
                        <span>{name}</span>
                    </div>\n'''

        with open("index.html", "r", encoding="utf-8") as f:
            content = f.read()

        # استبدال المنطقة المخصصة للقنوات
        content = re.sub(r".*?", 
                         f"\n{output_html}\n", 
                         content, flags=re.DOTALL)

        with open("index.html", "w", encoding="utf-8") as f:
            f.write(content)
        print("تم التحديث بنجاح يا بطل!")
    except Exception as e:
        print(f"حدث خطأ: {e}")

if __name__ == "__main__":
    main()
