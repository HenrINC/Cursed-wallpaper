import requests, random, ctypes, os, time

from xml.etree import cElementTree as ElementTree

from bs4 import BeautifulSoup

TOP = True

TIME = "year"

SUB = "hmmmm"

LOADBAR_LEN = 20

MAX_ENTRIES = 30



def get_imgs(url):
    soup = BeautifulSoup(requests.get(url, headers = {"User-Agent": "Mozilla/5.0"}).text, "html.parser")
    post = soup.select("[data-test-id=post-content]>*")
    if len(post) < 4: #Content is NSFW
        return []
    else:
        return post[3].find_all("a")



rss = requests.get(f"https://reddit.com/r/{SUB}{'/top' if TOP else ''}/.rss{f'?t={TIME}' if TOP else ''}", headers = {"User-Agent": "Mozilla/5.0"}).text

rss = ElementTree.XML(rss)

posts = []

print("Looking for images...")

entries = rss.findall("{http://www.w3.org/2005/Atom}entry")[:MAX_ENTRIES]

for i, entry in enumerate(entries):
    link = entry.find("{http://www.w3.org/2005/Atom}link").get("href")

    imgs = get_imgs(link)
    
    if len(imgs) == 1:
        link = imgs[0]["href"]
        posts.append(link)

    percent = int(LOADBAR_LEN*(i+1)/len(entries))
    print(f"[{'='*(percent+1)}>{'.'*(LOADBAR_LEN-percent)}]",end="\r")
print("\n")
img = random.choice(posts)

img = requests.get(img, headers = {"User-Agent": "Mozilla/5.0"})

with open("temp.jpg", "wb") as file: file.write(img.content)

time.sleep(1)
print(os.path.join(os.getcwd(),"temp.jpg"))
ctypes.windll.user32.SystemParametersInfoW(20, 0, os.path.join(os.getcwd(),"temp.jpg") , 0)
                      
os.system("start RUNDLL32.EXE user32.dll,UpdatePerUserSystemParameters")

time.sleep(1)

os.remove("temp.jpg")
