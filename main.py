from DrissionPage import ChromiumPage, ChromiumOptions
import json
from tqdm import tqdm
# import pandas as pd

stat_headers = ["HP", "攻撃", "防御", "素早さ", "賢さ", "運"]
# rating_headers = ["攻略評価","探索評価","レイド評価","PvP評価"]

def export_csv(data):
    delimiter = "\t"
    print("Export data to csv")
    header = ["unit", "attribute", "range", "vignette"] + stat_headers + ["Total"]
    with open("clean.csv", "w+", encoding='UTF-8') as f:
        f.write(delimiter.join(header)+"\n")
        for d in tqdm(data):
            row = []
            row.append(f'=HYPERLINK(\"{d["url"]}\", \"{d["name"]}\")')
            row += [d["attr"], d["range"], d["vignette"]]
            stat_total = 0
            for stat_h in stat_headers:
                stat = int(d["stat"][stat_h])
                stat_total += stat
                row.append(str(stat))
            row.append(str(stat_total))
            f.write(delimiter.join(row)+"\n")

        

def clean(data):
    print("Cleaning data")
    for i in tqdm(range(len(data))):
        data[i]["range"] = data[i]["range"].split('_')[-1]

    with open("clean.json", "w+", encoding='UTF-8') as f:
        f.write(json.dumps(data, indent=2))

def save_json(data):
    with open("data.json", "w+") as f:
        f.write(json.dumps(data, indent=2))

def load_json():
    try:
        with open("data.json", "r") as f:
            return json.load(f)
    except:
        return []



def main():
    force_update = False
    data = load_json()
    page = ChromiumPage()

    if not data:
        units_url = 'https://appmedia.jp/pando-land/77945405'
        page.get(units_url)
        unit_trs = page.eles("css:tr.single_data")
        # units_td_lookup = ["name", "attribute", "range", "vignette"]
        for tr in unit_trs:
            tds = tr.eles("css:td")
            d = {}
            d["url"] = tds[0].ele("tag:a").link
            d["name"] = tds[0].text
            d["attr"] = tds[1].ele("tag:img").attr("alt")
            d["range"] = tds[2].ele("tag:img").attr("alt")
            _vignette = tds[3].ele("tag:img").attr("alt")
            d["vignette"] = _vignette[_vignette.index('編成数')+3]
            d["stat"] = {}
            data.append(d)
        print(data)
        save_json(data)

    si = save_interval = 1
    for i in tqdm(range(len(data))):
        if force_update or not data[i]["stat"] or len(data[i]["stat"])!=6:
            page.get(data[i]["url"])
            # stat_tds = page.eles("css:.post-content table:nth-of-type(3) tr:nth-child(even) td")
            # stath_tds = page.eles("css:.post-content table:nth-of-type(3) tr:nth-child(odd) th")
            stat_tds = page.eles('css:.post-content h3+table tr:nth-child(even) td')
            stath_tds = page.eles('css:.post-content h3+table tr:nth-child(odd) th')
            data[i]["stat"] = dict([(x[0].text, x[1].text) for x in zip(stath_tds, stat_tds) if x[0].text in stat_headers])
            print(data[i])
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