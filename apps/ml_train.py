import pickle

import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

from sklearn.ensemble import ExtraTreesClassifier


# Importando a database
df = pd.read_csv('database/dataset_2021-5-26-10-14.csv', sep='\t', encoding = 'utf-8')

# Escolhendo as features que considero importantes
X = df[['default_3months', 'ioi_36months', 'ioi_3months', 'valor_por_vencer',
       'valor_vencido', 'valor_quitado', 'quant_protestos', 'valor_protestos',
       'quant_acao_judicial', 'acao_judicial_valor', 'dividas_vencidas_valor',
       'dividas_vencidas_qtd', 'falencia_concordata_qtd', 'tipo_sociedade',
       'opcao_tributaria', 'valor_total_pedido']]

# Transformando features string em features binárias
X = pd.get_dummies(X)
y = df["default"]

# Separando o dataset entre treino e validação
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1)

# Classificadores a serem utilizados nos testes
names = ["Decision Tree"]

classifiers = [
    DecisionTreeClassifier(max_depth=8, max_features=16),
    ]

# Treinar cada um dos classificadores e analisar a performance
trained_models = {}
for name, classifier in zip(names, classifiers):
    classifier.fit(X_train, y_train)
    trained_models[name] = classifier
    print(f'Score classificador {name}: {classifier.score(X_test, y_test):.2f}')


# Melhor classificador foi o decision tree, vamos usar ele. 
# Agora para analisar as features realmente importantes, vamos utiizar uma técnica chamada de feature importance, 
# que analisa a importância relativa de cada uma das features no modelo
feat_importances = pd.Series(trained_models['Decision Tree'].feature_importances_, index=X.columns)
feat_importances.nlargest(13).plot(kind='barh')
plt.suptitle('Features mais importantes')
plt.show()

most_imp_keys = feat_importances.nlargest(13).keys()

# Escolhendo finalmente as features mais importantes
X_f = pd.get_dummies(df)[most_imp_keys]

y_f = df["default"]

# Separando o dataset entre treino e validação
X_train_f, X_test_f, y_train_f, y_test_f = train_test_split(X_f, y_f, test_size=0.2, random_state=1)

classifier_f = DecisionTreeClassifier(max_depth=8, max_features=13)
classifier_f.fit(X_train_f, y_train_f)
print(f'Score final do classificador: {classifier_f.score(X_test_f, y_test_f):.2f}')

features = list(feat_importances.nlargest(13).keys())

print(features)

save_dict = {'model': classifier_f, 'features': features, 'columns_structure': X.columns}
pickle.dump(save_dict, open('apps/models/ml_regression', 'wb'))

