from flask import Flask, request, jsonify
import joblib
import pandas as pd
import os

app = Flask(__name__)

model = joblib.load('modelo.pkl')
features = joblib.load('features.pkl')

def mapear_para_features(payload):
    temperatura = float(payload.get('temperatura', 25))
    umidade = float(payload.get('umidade', 60))
    vento = float(payload.get('vento', 15))
    chuva = float(payload.get('chuva', 0))
    co2 = float(payload.get('co2', 400))
    fumaca = float(payload.get('fumaca', 0))

    # Mapeamento das features IoT para features do modelo Algerian
    # FFMC: quanto mais seco e quente, maior. Fumaca aumenta
    ffmc = min(92.5, max(28.6,
        40 + (temperatura - 22) * 1.5
        - (umidade - 21) * 0.4
        + fumaca * 0.3
    ))

    # DMC: acumulo de seca. CO2 alto indica mais materia organica queimando
    dmc = min(65.9, max(1.1,
        5 + (temperatura - 22) * 0.8
        + (co2 - 400) * 0.01
        - chuva * 2
    ))

    # DC: seca profunda
    dc = min(220.4, max(7,
        30 + (temperatura - 22) * 3
        - umidade * 0.3
        - chuva * 5
    ))

    return {
        'Temperature': temperatura,
        'RH': umidade,
        'Ws': vento,
        'Rain': chuva,
        'FFMC': round(ffmc, 1),
        'DMC': round(dmc, 1),
        'DC': round(dc, 1)
    }

def calcular_score(prob_fire, mapped):
    base = prob_fire * 100

    if mapped['Temperature'] > 40: base += 5
    if mapped['RH'] < 20: base += 5
    if mapped['Rain'] == 0 and mapped['FFMC'] > 80: base += 5

    return min(100.0, round(base, 2))

@app.route('/predict', methods=['POST'])
def predict():
    try:
        payload = request.get_json()
        if not payload:
            return jsonify({'error': 'Payload vazio'}), 400

        mapped = mapear_para_features(payload)
        df_input = pd.DataFrame([mapped])[features]

        pred = model.predict(df_input)[0]
        prob = model.predict_proba(df_input)[0]
        prob_fire = float(prob[1])

        score = calcular_score(prob_fire, mapped)

        if score >= 70:
            nivel = 'ALTO'
        elif score >= 40:
            nivel = 'MEDIO'
        else:
            nivel = 'BAIXO'

        return jsonify({
            'prediction': 'fire' if pred == 1 else 'not fire',
            'score': score,
            'nivel': nivel,
            'prob_fire': round(prob_fire * 100, 2),
            'features_usadas': mapped
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok', 'model': 'Algerian Forest Fires RF'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8001))
    app.run(host='0.0.0.0', port=port)