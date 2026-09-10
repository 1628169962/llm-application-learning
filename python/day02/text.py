import  json
def load_models(name):
    with open(name,"r",encoding="utf-8") as f:
        data = json.load(f)
    return data

def filter_models(models):
    selected = []
    # 在这里筛选
    for model in models:
        if model["score"] >=0.9:
            selected.append(model)
    # 在这里排序
    selected = sorted(selected,key=lambda x:x["score"],reverse=True)
    return selected


def save_models(models, filename):
    with open(filename,"w",encoding="utf-8") as f:
        json.dump(models,f,ensure_ascii=False,indent=2)
models = load_models("models.json")
print(models)
selected = filter_models(models)
print(selected)
save_models(selected, "selected_models.json")


