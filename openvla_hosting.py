from flask import Flask, request, jsonify
from PIL import Image
import io
import torch 
from transformers import AutoModelForVision2Seq, AutoProcessor

app = Flask(__name__)
vla = vla = AutoModelForVision2Seq.from_pretrained(
    #"Sombit/gradual_dino_siglip", 
    "openvla/openvla-7b",
    attn_implementation="flash_attention_2",  # [Optional] Requires `flash_attn`
    torch_dtype=torch.bfloat16, 
    low_cpu_mem_usage=True, 
    trust_remote_code=True
).to("cuda:0") 
processor = AutoProcessor.from_pretrained("openvla/openvla-7b", trust_remote_code=True)

@app.route('/api/process', methods=['POST'])
def process_image_and_text():
    # Check if both 'instruction' and 'image' are in the request
    if 'instruction' not in request.form or 'image' not in request.files:
        return jsonify({"error": "Both 'instruction' and 'image' are required"}), 400

    # Get the text instruction
    instruction = request.form['instruction'] 
    unnorm_key = request.form['data_key']

    # Get the image file from the request
    image_file = request.files['image']
    try:
        # Open the image using PIL
        image = Image.open(io.BytesIO(image_file.read()))
        # You can process the image here, e.g., resizing, converting to grayscale, etc.
        # For demonstration, let's just return the image's format and size.
        image_info = {
            "format": image.format,
            "size": image.size,
            "mode": image.mode
        }
        inputs = processor(instruction, image).to("cuda:0", dtype=torch.bfloat16)
        action = vla.predict_action(**inputs, unnorm_key=unnorm_key, do_sample=False)
        print(action)
        action = action.tolist()
        return jsonify({
            "action": action
        })
    except Exception as e:
        return jsonify({"error": f"Failed to process the image: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
