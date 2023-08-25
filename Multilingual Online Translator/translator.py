import requests
from bs4 import BeautifulSoup
import argparse
import sys

languages = ['arabic', 'german', 'english', 'spanish', 'french', 'hebrew',
             'japanese', 'dutch', 'polish', 'portuguese', 'romanian',
             'russian', 'turkish', 'all']

args = sys.argv  # ['translator.py', 'source_language', 'target_language', 'word']
source_lang = args[1]
target_lang = args[2]
word = args[3]

base_url = 'https://context.reverso.net/translation/'
headers = {'User-Agent': 'Mozilla/5.0'}
send_req = requests.Session()

if source_lang not in languages:
    print(f"Sorry, the program doesn't support {source_lang}")
    sys.exit()

if target_lang not in languages:
    print(f"Sorry, the program doesn't support {target_lang}")
    sys.exit()


def find_translations(source, target, word_look):
    url = base_url + source.lower() + "-" + target.lower() + "/" + word_look
    page = send_req.get(url, headers=headers)
    if page.status_code == 404:
        print(f"Sorry, unable to find {word_look}")
        sys.exit()
    soup = BeautifulSoup(page.content, "html.parser")
    with open(f'{word}.txt', 'a', encoding='utf-8') as file:
        file.write("\n" + target.capitalize() + " Translations:" + "\n")
        words_transl = soup.find_all("span", {"class": "display-term"}, limit=5)
        list_words = [translation.text for translation in words_transl]
        for word_example in list_words:
            file.write(word_example + "\n")
            # print(word_example)
        file.write("\n")
        file.write("\n" + target.capitalize() + " Example:" + "\n")
        # 'trg ltr' is the class of the target language sentences
        translated_sentences = soup.find_all('div', {'class': ["trg ltr", "trg rtl arabic", "trg rtl"]}, limit=1)
        list_translated_sentences = [sentence.text.strip() for sentence in translated_sentences]
        # 'src ltr' is the class of the source language sentences
        source_sentences = soup.find_all("div", {"class": "src ltr"}, limit=1)
        list_source_sentences = [sentence.text.strip() for sentence in source_sentences]
        for i in range(1):
            file.write(list_source_sentences[i] + "\n")
            file.write(list_translated_sentences[i] + "\n")
        file.write("\n")


if target_lang == 'all':
    for lang in languages:
        if lang != source_lang and lang != 'all':
            find_translations(source_lang, lang, word)
else:
    find_translations(source_lang, target_lang, word)

read_file = open(f'{word}.txt', 'r', encoding='utf-8')
print(read_file.read())
read_file.close()
