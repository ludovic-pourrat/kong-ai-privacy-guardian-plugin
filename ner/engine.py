from flask import Flask, request, jsonify
import spacy

# Load the spaCy model for English
nlp = spacy.load("en_core_web_sm")

# Initialize the Flask application
app = Flask(__name__)


# Entity class definition (as provided above)
class Entity:
    def __init__(self, text, entity_type, start, end):
        self.text = text
        self.entity_type = entity_type
        self.start = start
        self.end = end

    def serialize(self):
        return {
            'entity': self.text,
            'type': self.entity_type,
            'start': self.start,
            'end': self.end
        }


# Define the /ner endpoint
@app.route('/ner', methods=['POST'])
def ner():
    # Get the JSON payload from the request
    data = request.get_json()

    # Extract the text and encoding from the payload
    text = data.get('text', '')
    encoding = data.get('encoding', 'utf-8')

    # Decode the text using the provided encoding
    try:
        decoded_text = text.encode().decode(encoding)
    except Exception as e:
        return jsonify({'error': f'Failed to decode text: {str(e)}'}), 400

    # Process the decoded text with spaCy
    doc = nlp(decoded_text)

    # Extract entities with their types and positions
    entities = []
    for ent in doc.ents:
        entity = Entity(ent.text, ent.label_, ent.start_char, ent.end_char)
        entities.append(entity.serialize())

    # Return the entities as JSON
    return jsonify({'entities': entities})


# Run the Flask application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
