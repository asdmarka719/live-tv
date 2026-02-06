import requests
import re

def main():
    try:
        # مصدر القنوات (سنستخدم مصدرين لضمان النجاح)
        sources = ["https://iptv-org.github.io/iptv/index.m3u", "https://raw.githubusercontent.com/iptv-org/iptv/master/streams/ar.m3u"]
        all_cards = ""
        
        for s in sources:
            try:
                r = requests.get(s, timeout=20)
                lines = r.text.split('\n')
                name = ""
                for line in lines:
                    if line.startswith("#EXTINF:"):
                        name = line.split(",")[-1].strip()
                    elif line.startswith("http"):
                        url = line.strip()
                        # فلتر القنوات الرياضية والبديلة
                        if any(x in name.lower() for x in ["bein", "sport", "alkass", "ssc", "saeedah"]):
                            all_cards += f'<div class="card" onclick="play(\'{url}\')"><div class="badge">Live</div><span>{name}</span></div>\n'
            except: continue

        if not all_cards: raise Exception("No channels found")

        # التحديث الآمن
        with open("index.html", "r", encoding="utf-8") as f:
            html = f.read()
        
        new_html = re.sub(r".*?", 
                          f"\n{all_cards}\n", 
                          html, flags=re.DOTALL)
        
        with open("index.html", "w", encoding="utf-8") as f:
            f.write(new_html)
        print("Updated successfully!")

    except Exception as e:
        print(f"Failed: {e}")

if __name__ == "__main__":
    main()
