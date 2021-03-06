from flask import Flask,jsonify,request
import pandas as pd
import re
import pickle

app = Flask(__name__)

@app.route('/',methods=['GET','POST'])
def predict():
  transcription= request.args.get('transcription')
  if transcription != None:
    unseen_data = pd.DataFrame([(transcription)],columns=['Transcription'])
    unseen_data['Transcription'] = unseen_data['Transcription'].apply(lambda x: " ".join(x.lower() for x in x.split())) 
    unseen_data['Transcription'] = unseen_data['Transcription'].map(lambda x: re.sub(r'\W+', ' ', x)) 
    vectorizer_word_unigram = pickle.load(open('vectorizer_word_unigram.pkl', 'rb'))
    unseen_data = unseen_data['Transcription']
    transform_unseen_data = vectorizer_word_unigram.transform(unseen_data)
    transform_unseen_data = transform_unseen_data.todense()
    word_unigram_features = vectorizer_word_unigram.get_feature_names()
    unseen_data_features = pd.DataFrame(transform_unseen_data, columns = word_unigram_features)
    model = pickle.load(open('trained_model.pkl', 'rb'))
    model_predictions = model.predict(unseen_data_features)
    return jsonify( result = int(model_predictions[0]))
  else:
    return jsonify( result = transcription)


if __name__ == '__main__':
  app.run()
