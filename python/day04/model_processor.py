
import csv
import time
def clean_model(model):
    model["model"] = model["model"].strip()
    model["score"] = float(model["score"])
    model["latency"] = float(model["latency"])
    return model
def filter_models(models):
    for model in models:
        if model["score"] >= 0.9:
            yield model
def load_models(file_path):
    models = []
    with open(file_path,"r",encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            clean_model(row)
            models.append(row)
    return models
def timer(func):
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        temp = func(*args,**kwargs)
        end = time.perf_counter()
        ans = end - start
        print(f"耗时：{ans}秒")
        return temp
    return wrapper
@timer
def process_models(file_path):
    models = load_models(file_path)
    for model in filter_models(models):
        print(model)

# process_models("models.csv")
