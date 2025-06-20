import pandas as pd
from rapidfuzz import process, fuzz
import re

def compare_prices(data_jaymart, data_advice):

    def clean_name_advice(text):
        pattern = r"(.+?)\((\d+)\+(\d+)(GB|TB)"
        match = re.search(pattern, text)
        if match:
            name_part = match.group(1).strip()
            spec_part = f"{match.group(2)}/{match.group(3)}{match.group(4)}"
            return f"{name_part} ({spec_part})"
        else:
            return text.strip()
        
    def clean_name_jaymart(text):

        text = re.sub(r"(?i)^pre-order\s*", "", text)
        spec_match = re.search(r"(\d+/\d+(GB|TB))", text)
        text = re.sub(r"\(.*?\)", "", text).strip()
        text = re.sub(r"\b\d+/\d+(GB|TB)\b", "", text).strip()
        text = re.sub(r'\s{2,}', ' ', text)

        if spec_match:
            spec = spec_match.group(1)
            return f"{text} ({spec})"
        else:
            return text.strip()

    data_advice['name'] = data_advice['name'].apply(clean_name_advice).str.upper()
    data_jaymart['name'] = data_jaymart['name'].apply(clean_name_jaymart).str.upper()

    data_advice = data_advice.drop_duplicates(subset=['name']).reset_index(drop=True)
    data_jaymart = data_jaymart.drop_duplicates(subset=['name']).reset_index(drop=True)


    matched_names = []
    similarities = []
    matched_prices = []

    for index, row in data_jaymart.iterrows():
        name_to_match = row['name']
        prefix_to_match = ' '.join(name_to_match.strip().split()[:2]).lower()

        filtered_data_advice = data_advice[data_advice['name'].apply(lambda x: ' '.join(x.strip().split()[:2]).lower() == prefix_to_match)]

        if not filtered_data_advice.empty:

            match, score, match_index = process.extractOne(name_to_match, filtered_data_advice['name'], scorer=fuzz.token_set_ratio)

            matched_row = filtered_data_advice.loc[match_index]

            matched_names.append(match)
            similarities.append(score)
            matched_prices.append(matched_row['online_price'])
        else:
            matched_names.append(None)
            similarities.append(0)
            matched_prices.append(None)

    data_jaymart['matched_name'] = matched_names
    data_jaymart['similarity'] = similarities
    data_jaymart['matched_price'] = matched_prices
    matched_df = data_jaymart[data_jaymart['similarity'] > 97].reset_index(drop=True)
    matched_df['price_diff'] = matched_df['online_price'] - matched_df['matched_price']
    data_jaymart_not_matched = data_jaymart[data_jaymart['matched_name'].isnull()].copy()
    data_jaymart_not_matched[['matched_price', 'price_diff']] = '-'
    final_df = pd.concat([matched_df, data_jaymart_not_matched], ignore_index=True)
    final_df = final_df.drop(columns=['link','similarity'])
    final_df = final_df.fillna('-')
    final_df = final_df.sort_values(by='name').reset_index(drop=True)
    final_df.columns = ['brand', 'jaymart_name', 'jaymart_price', 'advice_name', 'advice_price', 'price_diff']
    
    return final_df
