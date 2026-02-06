import requests

def main():
    # مصدر ضخم للقنوات
    url = "https://iptv-org.github.io/iptv/index.m3u"
    try:
        r = requests.get(url, timeout=20)
        lines = r.text.split('\n')
        
        added_channels = ""
        # الكلمات المفتاحية التي طلبتها
        keywords = {
            "sport": ["beIN", "Alkass"],
            "yemen": ["Saeedah", "Hadramout", "Hawyah", "Yemen", "Aden"]
        }

        current_name = ""
        for line in lines:
            if line.startswith("#EXTINF:"):
                current_name = line.split(",")[-1].strip()
            elif line.startswith("http"):
                url_link = line.strip()
                category = ""
                
                if any(k.lower() in current_name.lower() for k in keywords["sport"]):
                    category = "sport"
                elif any(k.lower() in current_name.lower() for k in keywords["yemen"]):
                    category = "yemen"
                
                if category:
                    added_channels += f'<div class="channel" data-category="{category}" onclick="playChan(\'{url_link}\')"><span>{current_name}</span></div>\n'

        with open("index.html", "r", encoding="utf-8") as f:
            content = f.read()

        import re
        content = re.sub(r".*?", 
                         f"\n{added_channels}\n", 
                         content, flags=re.DOTALL)

        with open("index.html", "w", encoding="utf-8") as f:
            f.write(content)
        print("Done!")
    except:
        print("Error")

if __name__ == "__main__":
    main()
