import json
import string
import re


class Data:
    def __init__(self, script, synonyms, mirror):
        self.script = script
        self.synonyms = synonyms
        self.mirror = mirror


class Exchange:
    def __init__(self, text, decomposition, delimiters, responses, key, index):
        self.text = text
        self.decomposition = decomposition
        self.delimiters = delimiters
        self.responses = responses
        self.key = key
        self.index = index


class Memory:
    def __init__(self, memory):
        self.contents = memory


class Lizzy:
    def __init__(self):
        self.data = Data({}, {}, {})
        self.memory = Memory([])
        self.decomposition = []


    def load(self):

        with open('script.json') as json_file:
            script = json.load(json_file)

        with open('synonyms.json') as json_file:
            synonyms = json.load(json_file)

        with open('mirror.json') as json_file:
            mirror = json.load(json_file)

        self.data = Data(script, synonyms, mirror)

        return self.data


    def load_synon_tags(self, text):
        text_arr = text.split()
        for i in range(len(text_arr)):
            if text_arr[i] in self.data.synonyms:
                text_arr[i] = self.data.synonyms[text_arr[i]]
        text = ' '.join(text_arr)
        return text


    def rank_script(self, text):
        text_arr = self.clean_input(text).split()
        max_rank = -1
        keys = []
        for i in range(len(text_arr)):
            if text_arr[i] in self.data.script:
                if self.data.script[text_arr[i]]['rank'] > max_rank:

                    max_rank = self.data.script[text_arr[i]]['rank']
                    keys.append(text_arr[i])

        return keys.pop()


    def get_exchange(self, text, key):
        desired_exchange = {}
        for i in range(0, len(self.data.script[key]['exchanges'])):

            valid = True
            decomposition = re.split('[ ](?=0)|(?<=0)[ ]', self.data.script[key]['exchanges'][i]['decomposition'])
            trimmed_text = text

            tag = re.search("{.*?}", trimmed_text).group(0) if re.search("{.*?}", trimmed_text) else None
            emote = re.search("(?<=\{).*?(?=\:)", trimmed_text).group(0) if re.search("(?<=\{).*?(?=\:)", trimmed_text) else None
            if tag and emote:
                trimmed_text = trimmed_text.replace(tag, emote)

            for j in range(0, len(decomposition)):
                if decomposition[j] != '0' and trimmed_text and decomposition[j] in trimmed_text:
                    trimmed_text = re.search("(?<=" + decomposition[j] + " ).*", trimmed_text).group(0) if re.search("(?<=" + decomposition[j] + " ).*", trimmed_text) else None
                elif decomposition[j] != '0' and (not trimmed_text or decomposition[j] not in trimmed_text):
                    valid = False

            if valid:
                desired_exchange = Exchange(text, decomposition, [], self.data.script[key]['exchanges'][i], key, i)
                break

        return desired_exchange


    def update_exchange_delimiters(self, exchange):
        for i in range(0, len(exchange.decomposition)):
            if exchange.decomposition[i] != '0':
                exchange.delimiters.append(exchange.decomposition[i])
        return exchange


    def update_exchange_text(self, exchange):

        first_tag = True
        while re.search("{.*?: .*?}", exchange.text):
            tag = re.search("{.*?: .*?}", exchange.text).group(0) if re.search("{.*?: .*?}", exchange.text) else None
            for i in range(0, len(exchange.decomposition)):

                if first_tag and tag and exchange.decomposition[i] != '0':

                    emote = re.search("(?<=\{).*?(?=\:)", tag).group(0) if re.search("(?<=\{).*?(?=\:)", tag) else None
                    emote_synon = re.search("(?<=\: ).*?(?=\})", tag).group(0) if re.search("(?<=\: ).*?(?=\})", tag) else None

                    exchange.text = exchange.text.replace(tag, emote_synon)
                    exchange.decomposition[i] = exchange.decomposition[i].replace(emote, emote_synon)

                elif not first_tag and tag:

                    emote_synon = re.search("(?<=\: ).*?(?=\})", tag).group(0) if re.search("(?<=\: ).*?(?=\})",
                                                                                            tag) else None
                    exchange.text = exchange.text.replace(tag, emote_synon)

                elif exchange.decomposition[i] != '0':
                    exchange.decomposition[i] = exchange.decomposition[i].replace(emote, emote_synon)

            if first_tag and tag:
                first_tag = False

        return exchange


    def select_response(self, exchange):

        delimiters = '|'.join(exchange.delimiters)
        templated_text = re.split(
            str('(^' + delimiters + '\s?|(?<=\s)' + delimiters + '(?=\s)|\s?' + delimiters + '$)'), exchange.text)

        response = self.data.script[exchange.key]['exchanges'][exchange.index]['responses'].pop(0)
        self.data.script[exchange.key]['exchanges'][exchange.index]['responses'].append(response)

        index = re.search("(?<=\[)[123456789](?=\])", response).group(0) if re.search("(?<=\[)[123456789](?=\])", response) else None
        if index:
            index = index[0]

        if index and templated_text[int(index)] and templated_text[int(index)] != '':

            response = re.split('\[[123456789]\]', response)
            separated_inset = re.split(' ', templated_text[int(index)])

            for i in range(0, len(separated_inset)):
                separated_inset[i] = self.data.mirror[separated_inset[i]] if separated_inset[i] in self.data.mirror else separated_inset[i]

            inset = ' '.join(separated_inset).strip()
            response = str(inset).join(response)

        elif index and templated_text[int(index)] == '':
            response = self.get_default_response()

        return response


    def get_default_response(self):

        if self.memory.contents != []:
            text = self.memory.contents.pop(0)
            exchange = Exchange(text, ['0', 'my', '0'], [], self.data.script['my']['exchanges'][0]['responses'], 'my', 0)
            updated_exchange = self.update_exchange_text(exchange)
            updated_exchange = self.update_exchange_delimiters(updated_exchange)
            response = self.select_response(updated_exchange)
        else:
            response = self.data.script['n/a']['exchanges'][0]['responses'].pop(0)
            self.data.script['n/a']['exchanges'][0]['responses'].append(response)

        return response


    def clean_input(self, text):

        return text.translate(str.maketrans('', '', string.punctuation)).lower()


    def run(self):

        print("How do you do. Please tell me your problem.")

        while True:
            try:
                text = input('> ')

                text = self.clean_input(text)

                if text.lower() == 'quit' or text.lower() == 'goodbye' or text.lower() == 'bye':
                    break

                text = self.load_synon_tags(text)

                top_ranked_key = self.rank_script(text)

                if top_ranked_key == 'my':
                    self.memory.contents.append(text)

                exchange = self.get_exchange(text, top_ranked_key)

                updated_exchange = self.update_exchange_text(exchange)

                updated_exchange = self.update_exchange_delimiters(updated_exchange)

                response = self.select_response(updated_exchange)

                print(response)

            except:
                print(self.get_default_response())

        print("Goodbye. Thank you for talking to me.")
