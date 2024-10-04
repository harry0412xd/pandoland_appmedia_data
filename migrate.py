if __name__ == '__main__':
    import json
    data = {}
    with open("data.json", "r") as f:
        for unit in json.load(f):
            name = unit["name"]
            del unit["name"]
            data[name] = unit
    with open("data.json", "w") as f:
        f.write(json.dumps(data, indent=2))