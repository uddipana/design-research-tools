import pandas as pd
from pprint import pprint

def process(input_file, output_file, cards_for_analysis):
    df = pd.read_excel(input_file)
    agg = aggregate_and_modify(df, cards_for_analysis)
    agg.to_excel(output_file)
    print(f'{output_file} has been written.')

def print_list_of_available_card_labels(input_file):
    df = pd.read_excel(input_file)
    print('List of available card labels for `cards_for_analysis`:')
    pprint(list(df['card label'].value_counts().index))


def aggregate_and_modify(df, cards_for_analysis):
    agg = df.groupby(['participant', 'category label'], as_index=False).agg(cards=pd.NamedAgg(column="card label", aggfunc=lambda x: list(x)))

    def get_finding_percentage(cards):
        common = len([c for c in cards if c in cards_for_analysis])
        return round(common / len(cards_for_analysis) * 100, 2)

    def get_participant_sort_percentage(cards):
        common = len([c for c in cards if c in cards_for_analysis])
        return round(common / len(cards) * 100, 2)
    
    agg['finding_percentage'] = agg['cards'].apply(get_finding_percentage)
    agg['participant_sort_percentage'] = agg['cards'].apply(get_participant_sort_percentage)
    return agg