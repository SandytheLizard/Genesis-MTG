import random, json, time
from operator import itemgetter
def initialize():
    with open("cards.json", "r",encoding='UTF-8') as read_file:
        data = json.load(read_file)
    return data
def main(data):
    tags = ['gain life', 'lose life', 'graveyard', 'token', 'power', 'toughness', '+1/+1 counter', 'instant', 'sorcery', 'graveyard', 'mill', 'sacrifice', 'draw', 'discard', 'land', 'artifact', 'aura', 'flying', 'damage', 'enchantment', 'search', "can't", "doesn't", 'gets -']
    target_tags = ['you', 'each player', 'each opponent']
    def remove_illegal_cards():
        card_data = []
        for card in data:
            try:
                typeline = card["type_line"]
                if card["legalities"]["commander"] == "legal" and 'Token' not in typeline and 'Land' not in typeline and card["set_type"] != 'funny':
                    card_data.append(card)
            except:
                pass
        return card_data
    def generate_commander():
        LegendaryCreatures = []
        for card in data:
            try:
                card_type = card["type_line"]
            except:
                card_type = 'None'
            if 'Legendary Creature' in card_type:
                print(card["name"])
                LegendaryCreatures.append(card)
        commander = random.choice(LegendaryCreatures)
        print(commander["name"])
        return commander

    def get_commander_tags(Commander, tags):
        CommanderTags = []
        print(Commander["oracle_text"])
        for tag in tags:
            if tag in Commander["oracle_text"]:
                CommanderTags.append(tag)
                print(tag)
        return CommanderTags
    def restrict_data_by_color(Commander, card_data):
        on_color_cards = []
        try:
            color_identity = Commander["color_identity"]
            color_identity.append('C')
        except:
            color_identity = ['C']
        for card in card_data:
            try:
                card_color = card["color_identity"]
                card_color.append('C')
            except:
                card_color = ['C']
            on_color = True
            for color in card_color:
                if color not in color_identity:
                    on_color = False
            if on_color:
                on_color_cards.append(card)
                print(card["name"])
        return on_color_cards

    def determine_card_scores(CommanderTags, GenericTags, card_data):
        scored_cards = []
        debuff_tags = ['lose life', 'sacrifice', 'discard', "can't", "doesn't", 'gets -']
        for card in card_data:
            try:
                oracle = card["oracle_text"]
            except:
                oracle = ''
            print(card["name"])
            debuff_indicators = ['you', card["name"]]
            score = 0
            possible_debuffs = []
            debuff_detected = False
            for debuff_tag in debuff_tags:
                if debuff_tag in oracle:
                        possible_debuffs.append(debuff_tag)
            for tag in GenericTags:
                if tag in oracle:
                    if tag in CommanderTags:
                        score += 8
                    elif tag in debuff_tags:
                        for indicator in debuff_indicators:
                            if indicator in card['oracle_text']:
                                debuff_detected = True
                        if debuff_detected:
                            score -= 1
                    else:
                        score += 1
            try:
                score -= int(card["cmc"]) // 3
            except:
                pass
            try:
                stats = int(card["power"] - card["toughness"])
                if stats < 0:
                    stats *= -1
            except:
                stats = 0
            score += stats
            print(score)
            scored_cards.append([score, card])
        return scored_cards
    def generate_deck(cards):
        decklist = []
        cards.sort(reverse=True,key=lambda x: int(x[0]))
        used_names = []
        checks = 0
        confirmed = 0
        while confirmed <= 63:
            card = cards[checks][1]
            card_name = card["name"]
            while card_name in used_names:
                checks += 1
                card = cards[checks][1]
                card_name = card["name"]
            decklist.append(card)
            used_names.append(card_name)
            confirmed += 1

        for i in range(10):
            print(' ')
        for card in decklist:
            print(card['name'])
        print(Commander["name"])
    Commander = generate_commander()
    print('COMMANDER:', Commander["name"])
    card_data = remove_illegal_cards()
    card_data = restrict_data_by_color(Commander, card_data)
    CommanderTags = get_commander_tags(Commander, tags)
    card_scores = determine_card_scores(CommanderTags, tags, card_data)
    decklist = generate_deck(card_scores)
    
data = initialize()
main(data)