import requests

# مصادر قنوات متنوعة
SOURCES = {
    "sports": "https://raw.githubusercontent.com/mohammadreza-erd/IPTV/main/beIN.m3u",
    "yemen": "https://iptv-org.github.io/iptv/countries/ye.m3u",
    "egypt": "https://iptv-org.github.io/iptv/countries/eg.m3u",
    "general": "https://iptv-org.github.io/iptv/index.m3u"
}

def fetch_data(url):
    try:
        r = requests.get(url, timeout=20)
        return r.text if r.status_code == 200 else ""
    except:
        return ""

def generate_html(data):
    html = ""
    lines = data.split('\n')
    current_name = ""
    for line in lines:
        if line.startswith("#EXTINF:"):
            current_name = line.split(",")[-1].strip()
        elif line.startswith("http"):
            url = line.strip()
            if current_name:
                html += f'<div class="card" onclick="playChan(\'{url}\')"><span>{current_name}</span></div>\n'
                current_name = ""
    return html

def main():
    # جلب وفرز الرياضة
    sports_html = generate_html(fetch_data(SOURCES["sports"]))
    
    # جلب وفرز نايل سات (يمن + مصر)
    nile_html = generate_html(fetch_data(SOURCES["yemen"])) + generate_html(fetch_data(SOURCES["egypt"]))

    with open("index.html", "r", encoding="utf-8") as f:
        content = f.read()

    # تحديث الأقسام باستخدام العلامات (Tags)
    if sports_html:
        s_start, s_end = "", ""
        content = content.split(s_start)[0] + s_start + "\n" + sports_html + "\n" + s_end + content.split(s_end)[1]
    
    if nile_html:
        n_start, n_end = "", ""
        content = content.split(n_start)[0] + n_start + "\n" + nile_html + "\n" + n_end + content.split(n_end)[1]

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(content)

if __name__ == "__main__":
    main()
