import requests

# روابط مصادر القنوات (قائمة عالمية مفتوحة)
M3U_URL = "https://iptv-org.github.io/iptv/index.m3u"

def fetch_channels():
    try:
        response = requests.get(M3U_URL, timeout=15)
        lines = response.text.split('\n')
        
        # الكلمات المفتاحية التي نبحث عنها
        targets = ["Yemen", "Egypt", "beIN", "Sport"]
        found_html = ""

        current_name = ""
        for line in lines:
            if line.startswith("#EXTINF:"):
                # استخراج اسم القناة
                current_name = line.split(",")[-1].strip()
            elif line.startswith("http") and any(t.lower() in current_name.lower() for t in targets):
                # إذا كانت القناة ضمن اهتمامنا، ننشئ كود HTML لها
                found_html += f'<div class="channel-card" onclick="playChan(\'{line.strip()}\')">{current_name}</div>\n'
        
        return found_html
    except Exception as e:
        return f""

# تحديث ملف index.html
def update_index(html_content):
    with open("index.html", "r", encoding="utf-8") as f:
        index_content = f.read()

    start_tag = ""
    end_tag = ""
    
    # استبدال المحتوى بين العلامات
    new_content = index_content.split(start_tag)[0] + start_tag + "\n" + html_content + "\n" + end_tag + index_content.split(end_tag)[1]

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(new_content)

if __name__ == "__main__":
    channels_html = fetch_channels()
    if channels_html:
        update_index(channels_html)
        print("Done updating channels!")
