from DrissionPage import ChromiumPage, ChromiumOptions
import json
from tqdm import tqdm
# import pandas as pd

stat_headers = ["HP", "攻撃", "防御", "素早さ", "賢さ", "運"]
# rating_headers = ["攻略評価","探索評価","レイド評価","PvP評価"]

def export_csv(data):
    delimiter = "\t"
    print("Export data to csv")
    header = ["unit", "rarity", "attribute", "range", "vignette"] + stat_headers + ["Total"]
    with open("clean.csv", "w+", encoding='UTF-8') as f:
        f.write(delimiter.join(header)+"\n")
        for name, d in tqdm(data.items()):
            row = []
            row.append(f'=HYPERLINK(\"{d["url"]}\", \"{name}\")')
            row += [d["rarity"], d["attr"], d["range"], d["vignette"]]
            stat_total = 0
            for stat_h in stat_headers:
                stat = int(d["stat"][stat_h])
                stat_total += stat
                row.append(str(stat))
            row.append(str(stat_total))
            f.write(delimiter.join(row)+"\n")

        

def clean(data):
    print("Cleaning data")
    for unit_name in tqdm(data.keys()):
        data[unit_name]["range"] = data[unit_name]["range"].split('_')[-1]

    with open("clean.json", "w+", encoding='UTF-8') as f:
        f.write(json.dumps(data, indent=2))

def save_json(data):
    with open("data.json", "w+", encoding='UTF-8') as f:
        f.write(json.dumps(data, indent=2))

def load_json():
    try:
        with open("data.json", "r", encoding='UTF-8') as f:
            return json.load(f)
    except:
        return {}



def main():
    force_update = 1
    data = load_json()
    page = ChromiumPage()

    if not data or force_update==1:
        units_url = 'https://appmedia.jp/pando-land/77945405'
        page.get(units_url)
        unit_trs = page.eles("css:tr.single_data")
        for tr in unit_trs:
            td = tr.ele("tag:td")
            unit_name = td.text
            # d = data.get(unit_name, {})
            d = data[unit_name]
            d["url"] = td.ele("tag:a").link
            d["attr"] = tr.attr("data-ele")
            d["range"] = tr.attr("data-type")
            d["rarity"] = tr.attr("data-rare")
            d["vignette"] = tr.attr("data-team_vig")
            data[unit_name] = d


        print(data)
        save_json(data)

    si = save_interval = 100
    for unit_name in tqdm(data.keys()):
        if force_update==2 or "stat" not in data[unit_name] or len(data[unit_name]["stat"])!=6:
            page.get(data[unit_name]["url"])
            stat_tds = page.eles('css:.post-content h3+table tr:nth-child(even) td')
            stath_tds = page.eles('css:.post-content h3+table tr:nth-child(odd) th')
            data[unit_name]["stat"] = dict([(x[0].text, x[1].text) for x in zip(stath_tds, stat_tds) if x[0].text in stat_headers])
            print(data[unit_name])
            si -= 1
            if si==0:
                si = save_interval
                save_json(data)
    if si!=save_interval:
        save_json(data)
    clean(data)
    export_csv(data)



if __name__ == '__main__':
    main()