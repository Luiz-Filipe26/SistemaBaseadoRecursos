#!/usr/bin/env python
# encoding: utf-8
import json
from flask import Flask, request, jsonify, make_response

app = Flask(__name__)

@app.route('/', methods=['GET'])
def query_records():
    name = request.args.get('name')
    with open('data.txt', 'r') as f:
        data = f.read()
        records = json.loads(data)
        for record in records:
            if record['name'] == str(name):
                return jsonify(record)
        return jsonify({'error': 'data not found'})

@app.route('/', methods=['POST'])
def create_record():
    record = json.loads(request.data)
    with open('data.txt', 'r') as f:
        data = f.read()
    if not data:
        records = [record]
    else:
        records = json.loads(data)
        records.append(record)
    with open('data.txt', 'w') as f:
        f.write(json.dumps(records, indent=2))
    return jsonify(record)

@app.route('/', methods=['PUT'])
def update_record():
    record = json.loads(request.data)
    new_records = []
    with open('data.txt', 'r') as f:
        data = f.read()
        records = json.loads(data)
    for r in records:
        if r['name'] == record['name']:
            r['email'] = record['email']
        new_records.append(r)
    with open('data.txt', 'w') as f:
        f.write(json.dumps(new_records, indent=2))
    return jsonify(record)

@app.route('/', methods=['DELETE'])
def delte_record():
    record = json.loads(request.data)
    new_records = []
    with open('data.txt', 'r') as f:
        data = f.read()
        records = json.loads(data)
        for r in records:
            if r['name'] == record['name']:
                continue
            new_records.append(r)
    with open('data.txt', 'w') as f:
        f.write(json.dumps(new_records, indent=2))
    return jsonify(record)

@app.route('/', methods=['PATCH'])
def patch_record():
    name = request.args.get('name')  # Obter o nome da URL
    updates = json.loads(request.data)  # Dados a serem atualizados
    new_records = []
    record_found = False

    with open('data.txt', 'r') as f:
        data = f.read()
        records = json.loads(data)

    for record in records:
        if record['name'] == name:
            record_found = True
            # Atualiza apenas os campos fornecidos em 'updates'
            for key, value in updates.items():
                record[key] = value
        new_records.append(record)

    if not record_found:
        return jsonify({'error': 'data not found'}), 404

    with open('data.txt', 'w') as f:
        f.write(json.dumps(new_records, indent=2))

    return jsonify({'message': 'record updated', 'record': record})


@app.route('/', methods=['OPTIONS'])
def options():
    response = make_response()

    # Adiciona os cabeçalhos necessários para CORS
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, PATCH, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    response.headers['Access-Control-Max-Age'] = '3600'  # Cache da resposta OPTIONS (em segundos)

    return response


app.run(debug=True)
