import boto3
from os import getenv
import pickle

BUCKET_NAME = 'helpo-ml'


class RecommendationsManager(object):

    def __init__(self):
        self.S3 = boto3.client(
            's3', region_name='us-west-2', 
            aws_access_key_id=getenv('aws_access_key_id'),
            aws_secret_access_key=getenv('aws_secret_access_key')
        )
        self.model_evento = self.load_model('model_evento.pkl')

    def load_model(self, key):
        # Load model from S3 bucket
        response = self.S3.get_object(Bucket=BUCKET_NAME, Key=key)
        # Load pickle model
        print(response)
        model_str = response['Body'].read()     
        return pickle.loads(model_str)

    def predict_eventos_userbased(self, user_id, user_scores, eventos):
        predictions = {}
        wtd_sum = 0
        similarities, indices = self.find_k_similar_users(user_id, user_scores, 4) # similar users based on cosine similarity
        mean_rating = user_scores.mean() #to adjust for zero based indexing
        sum_wt = np.sum(similarities)-1
        for evento in eventos:
            for i in range(0, len(indices.flatten())):
                if indices.flatten()[i]+1 == user_id:
                    continue
                else: 
                    scores_diff = scores.iloc[indices.flatten()[i], evento-1]-np.mean(scores.iloc[indices.flatten()[i],:])
                    product = scores_diff * (similarities[i])
                    wtd_sum = wtd_sum + product
            prediction = int(round(mean_rating + (wtd_sum/sum_wt)))
            print ('\nPredicted rating for user {0} -> item {1}: {2}'.format(user_id, evento, prediction))
            predictions[str(evento)] = prediction
        return predictions

    def find_k_similar_users(self, user_id, user_scores, k):
        distances, indices = model_knn.kneighbors(user_scores.values.reshape(1, -1), n_neighbors = k+1)
        similarities = 1-distances.flatten()
        print ('{0} most similar users for User {1}:\n'.format(k, user_id))
        for i in range(0, len(indices.flatten())):
            if indices.flatten()[i]+1 == user_id:
                continue
            else:
                print ('{0}: User {1}, with similarity of {2}'.format(i, indices.flatten()[i]+1, similarities.flatten()[i]))
                
        return similarities, indices

        