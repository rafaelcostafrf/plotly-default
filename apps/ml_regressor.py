import pickle
import pandas as pd

saved_dict = pickle.load(open('apps/models/default_classifier', 'rb'))

# Carregando o modelo, as features mais importantes, e o setup de colunas da database original
model = saved_dict['model']
features = saved_dict['features']
columns = saved_dict['columns']


def generate_data_dict(names, data):
    data_dict = {x: [y] for x, y in zip(names, data)}
    return data_dict


def default_prediction(data_dict):
    X = pd.DataFrame(data_dict, columns=columns)
    prediction = model.predict(X[features])
    prob = model.predict_proba(X[features])
    return prediction, prob

if __name__=='__main__':
    names = [
        'default_3months', 
        'valor_vencido', 
        'ioi_36months', 
        'opcao_tributaria_simples nacional', 
        'valor_quitado', 
        'valor_por_vencer', 
        'valor_total_pedido', 
        'ioi_3months', 
        'quant_protestos', 
        'valor_protestos']

    data = [3, 10000, 0, 1, 0, 0, 25000, 0, 5000, 0]

    data_dict = generate_data_dict(names=names, data=data)
    pred = default_prediction(data_dict)


