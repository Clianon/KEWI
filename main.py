from flask import Flask, render_template, request, jsonify, Response, stream_with_context
import requests

purl = 'your url here'

app = Flask(__name__, static_folder='./static')
debugMode = True
@app.route('/')
def index():
    print("Kwei")
    return render_template('index.html')

@app.route('/models', methods=['GET'])
def get_models():
    return jsonify({
        "object": "list",
        "data":[
                {"id":"gpt-4","object":"model","created": 1677532384,"owned_by":"kwei","permission": []},
								{"id":"gpt-3.5 Turbo","object":"model","created": 1677532384,"owned_by":"kwei","permission": []},
								{"id":"gpt-3.5 Turbo-0301","object":"model","created": 1677532384,"owned_by":"kwei","permission": []}
            ]
    })


@app.route('/chat/completions', methods=['POST', 'GET'])
def chat_completions():
    if debugMode == True:
        print(f"request: {request}")
    if request.method == 'POST':
        print("[CHAT]: Received POST request /chat/completions")
        if request.is_json:
            print("[CHAT]: Request is JSON")
            url = f'{purl}'
            req_data = request.get_json()
            stream = req_data.get("stream", False)

            if stream:
                def generate():
                    with requests.post(url, json=req_data, stream=True) as response:
                        for chunk in response.iter_content(chunk_size=None):
                            yield chunk

                print("[CHAT]: Returning Response[stream=True]")
                return Response(stream_with_context(generate()), content_type='application/json')
            else:
                print("[CHAT]: Returning Response[stream=False]")
                response = requests.post(url, json=req_data)
                return jsonify(response.json())
        else:
            print("[CHAT]: Request is not JSON")
            return jsonify({"error": "request is not json"})
    else:
        print("[CHAT]: Received GET request /chat/completions")
        return jsonify({"error": "Cannot GET /chat/completions"})

@app.route('/text/completions', methods=['POST', 'GET'])
def text_completions():
    if debugMode == True:
        print(f"request: {request}")
    if request.method == 'POST':
        print("[TEXT]: Received POST request /text/completions")
        if request.is_json:
            print("[TEXT]: Request is JSON")
            url = f'{purl}'
            req_data = request.get_json()
            stream = req_data.get("stream", False)

            if stream:
                def generate():
                    with requests.post(url, json=req_data, stream=True) as response:
                        for chunk in response.iter_content(chunk_size=None):
                            yield chunk
                print("[TEXT]: Returning Response[stream=True]")
                return Response(stream_with_context(generate()), content_type='application/json')
            else:
                print("[TEXT]: Returning Response[stream=False]")
                response = requests.post(url, json=req_data)
                return jsonify(response.json())
        else:
            print("[TEXT]: Request is not JSON")
            return jsonify({"error": "request is not json"})
    else:
        print("[TEXT]: Received GET request /text/completions")
        return jsonify({"error": "Cannot GET /text/completions"})

    

if __name__ == '__main__':
    print("Starting Flask Server")

    app.run(debug=True, host='0.0.0.0', port=1489)
