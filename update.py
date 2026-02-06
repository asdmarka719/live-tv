import requests
import re

def main():
    url = "https://iptv-org.github.io/iptv/index.m3u"
    try:
        r = requests.get(url, timeout=20)
        lines = r.text.split('\n')
        
        html_cards = ""
        # القنوات التي تهمنا
        targets = ["beIN", "Alkass", "Yemen", "Saeedah", "Shabab", "Masirah", "Hawyah"]

        name = ""
        for line in lines:
            if line.startswith("#EXTINF:"):
                name = line.split(",")[-1].strip()
            elif line.startswith("http"):
                if any(t.lower() in name.lower() for t in targets):
                    # وضع القناة داخل تصميم المربع (Card)
                    html_cards += f'<div class="chan-card" onclick="playChan(\'{line.strip()}\')"><span>{name}</span></div>\n'

        with open("index.html", "r", encoding="utf-8") as f:
            content = f.read()

        # استبدال المحتوى بدقة بين العلامات
        pattern = r".*?"
        replacement = f"\n{html_cards}\n"
        new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)

        with open("index.html", "w", encoding="utf-8") as f:
            f.write(new_content)
        print("Success!")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
