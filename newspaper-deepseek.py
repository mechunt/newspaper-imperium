#Schem of making newspapers
#Made for IMPERIUM and powered by ChatGPT

from openai import OpenAI
import requests
import json
from PIL import Image, ImageDraw, ImageFont
import textwrap
import re

response = str()

economic = Image.open("economic.png")
eco_im = ImageDraw.Draw(economic)

def send(message):
    global response
    response = requests.post(
      url="https://openrouter.ai/api/v1/chat/completions",
      headers={
        "Authorization": "Bearer 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",
        "Content-Type": "application/json"
      },
      data=json.dumps({
        "model": "deepseek/deepseek-r1:free",
        "messages": [
          {
            "role": "user",
            "content": message
          }
        ],

})
)

send("""Привет. Представь будто ты публицист 20-го века. Напиши пожалуйста заметку про новый фотоаппарат IS 100 компании Parker с такой логической цепочкой (наши фотоаппараты уступают Kodak -> мы нашли проблему в пленки -> мы начали делать ее нитроцеллюлозы -> Зерна стало меньше -> общее качество фотографии улучшилось -> наши фотоаппараты начали покупать). <Пример заметки:

Заголовок

Текст


Пример заметки с содержанием:

Развитие парков в Монте-Кристо

Многим известна история города Монте-Кристо, которая кочует с его графом Кириллом Герценом. Монте-Кристо стал новой силой для экоактивистов. Город который славился только руинами старой церкви, теперь известен как город парковый комплекс. С приходом Герцена появились белокаменные каналы, появились новые леса, а также мелкий остров, который казался бы уже зарос сорняками, и весь стал желтым из-за одуванчиков. Остров был заросшим крапивой, и на него было трудно пройти.

Теперь там пестрит песчанная стена, а над этой береговой линией стоит оранжевый дворец, и березовая аллея. В общем новые люди, привлекли новые инвестиции, а вот уже эти деньги пошли на облагораживание города. Теперь Монте-Кристо называют Гаитским (Доминиканским) Петергофом, а Герцена прославляют как Монте-Кристского Шереметьева.

Также помимо благоустройства островов, появление новых островов из-за каналов, местные власти пытаются сделать из Монте-Кристо Санкт-Петербург. Действительно Кирилл Герцен не мог не перевезти Питерский дух из своей малой Родины, и вот это сказывается на городе. Но слава Богу только в лучшую сторону.

Там где было болото, вырыт канал, в ряд посажены березы, а на другом берегу канала посажены ели. Несмотря на тропический климат, они очень хорошо приспособились к климату. Сосновые боры уже прекрывают вид на старую церковь.

Кстати о ней. Церковь была благоухожена, теперь это достопримечательность. Как вы знаете испанские завоеватели начинали колонизацию с церквей. Да и эта церковь прямиком из 15 века. Если ее, казалось бы, совсем забросили где-то еще в 18-м, и все начали переезжать в более перспективный Порт-о-Пренс, то сейчас уже из Порт-о-Пренса начинают сюда приезжать отдыхать.>

Не пиши пожалуйста заголовок, а также "редакция АБВГД", "1955 год" и другие примечания-предисловия. Не форматируй текст, так как ** ** не работают итд.""")
#decoded_response = response_text.decode('utf-8').strip()

resp_clr = response.json()["choices"][0]["message"]["content"]


font = ImageFont.truetype('a.ttf', size=47)

margin = 280
offset = 1140

z = 24
y = ''
gl = ["а","о","у","ы","э","я","ё","е","и", "ю"]
gl2 = ["а","о","у","ы","э","я","ё","е","и", "ю", " ", ",", ".","!", "?"]
xz = 0

def split_text_by_syllables(word, max_length):
    vowels = "аеёиоуыэюяАЕЁИОУЫЭЮЯ"
    consonants = "бвгджзйклмнпрстфхцчшщБВГДЖЗЙКЛМНПРСТФХЦЧШЩ"
    
    if '-' in word:
        parts = word.split('-')
        result = []
        current_part = parts[0]
        for part in parts[1:]:
            if len(current_part) + 1 + len(part) <= max_length:
                current_part += '-' + part
            else:
                result.append(current_part + '-')
                current_part = part
        result.append(current_part)
        return result if len(result) > 1 else [word]
    
    if len(word) <= max_length:
        return [word]
    
    best_split_pos = -1
    for split_pos in range(min(max_length, len(word)-1), 1, -1):
        prev_char = word[split_pos-1]
        next_char = word[split_pos]
        
        if prev_char == next_char and prev_char in consonants:
            continue
            
        if prev_char in vowels and next_char in consonants:
            best_split_pos = split_pos
            break
            
        if (prev_char in consonants and next_char in consonants and 
            split_pos > 1 and word[split_pos-2] in vowels):
            best_split_pos = split_pos
            break
    
    if best_split_pos != -1:
        return [word[:best_split_pos] + '-', word[best_split_pos:]]
    
    split_pos = max_length
    while split_pos > 1:
        if word[split_pos-1] not in consonants or word[split_pos] != word[split_pos-1]:
            return [word[:split_pos] + '-', word[split_pos:]]
        split_pos -= 1
    
    return [word[:max_length] + '-', word[max_length:]]

def wrap_text_to_lines(text, line_length):
    words = re.findall(r'\S+|\n', text)
    lines = []
    current_line = []
    current_length = 0
    
    for word in words:
        if word == '\n':
            if current_line:
                lines.append(' '.join(current_line))
                current_line = []
                current_length = 0
            lines.append('')
            continue
        
        word_length = len(word)
        space = 1 if current_line else 0
        total_length = current_length + space + word_length
        
        if total_length <= line_length:
            current_line.append(word)
            current_length = total_length
            continue
        
        remaining_space = line_length - current_length - space
        if remaining_space >= 2:
            parts = split_text_by_syllables(word, remaining_space)
            if len(parts) > 1:
                current_line.append(parts[0])
                lines.append(' '.join(current_line))
                
                remaining_word = parts[1]
                while len(remaining_word) > line_length:
                    parts = split_text_by_syllables(remaining_word, line_length - 1)
                    lines.append(parts[0])
                    remaining_word = parts[1]
                
                current_line = [remaining_word] if remaining_word else []
                current_length = len(remaining_word)
                continue
        
        if current_line:
            lines.append(' '.join(current_line))
        current_line = [word]
        current_length = len(word)
    
    if current_line:
        lines.append(' '.join(current_line))
    
    return lines

# Пример использования
text = resp_clr
line_length = 30
lines = wrap_text_to_lines(text, line_length)

    
for line in lines:
    eco_im.text((margin, offset), line, font=font, fill="Black")
    offset += font.getbbox(line)[3]
    if offset >= 3150:
        offset = 1140
        margin = 1330
        
    
'''eco_im.text(
    (280, 1140),
    resp_clr,
    fill="Black",
    font=font)'''


economic.show()
economic.save("example.png")


