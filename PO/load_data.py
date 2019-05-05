import yaml,os

def load_data(tem_data):
    base = os.path.dirname(os.path.dirname(__file__))
    print(base)
    with open("%s/data/data.yml" %base,"r",encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data.get(tem_data)
