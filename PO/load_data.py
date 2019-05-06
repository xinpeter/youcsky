import yaml,os
base = os.path.dirname(os.path.dirname(__file__))

def load_data():
    print(base)
    with open("%s/data/data.yml" %base,"r",encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data

