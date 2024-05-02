from flask import Flask,render_template,request
import pickle
import numpy as np

popular=pickle.load(open('popular.pkl','rb'))
pt=pickle.load(open('pt.pkl','rb'))
similarity_scores=pickle.load(open('similarity_scores.pkl','rb'))
final_ratings=pickle.load(open('final_ratings.pkl','rb'))

app=Flask(__name__)

@app.route('/')
def index():
   return render_template('index.html',
                        book_name=list(popular['Book-Title'].values),
                        author=list(popular['Book-Author'].values),
                        image=list(popular['Image-URL-M'].values),
                        votes=list(popular['num_ratings'].values),
                        rating=list(popular['avg_rating'].values))

@app.route('/recommender')
def recommenders():
    return render_template('recommender.html', book_name=list(final_ratings.drop_duplicates('Book-Title')['Book-Title'].values))

@app.route('/recommend',methods=['post'])
def recommend_books():
    user_input=request.form.get('user_input')
    if(user_input not in pt.index):
        return ("Error 404 : Write valid Book Name")
    index=np.where(pt.index==user_input)[0][0]
    similar_items = sorted(list(enumerate(similarity_scores[index])),key=lambda x:x[1],reverse=True)[1:6]
    data=[]
    for i in similar_items:
        #print(pt.index[i[0]])
        temp=[]
        temp_df=final_ratings[final_ratings['Book-Title']==pt.index[i[0]]]
        temp_df.drop_duplicates('Book-Title',inplace=True)
        temp.extend(temp_df['Book-Title'])
        temp.extend(temp_df['Book-Author'])
        temp.extend(temp_df['Image-URL-M'])
        temp.extend(temp_df['num_rating'])
        temp.extend(temp_df['votes'])
        data.append(temp)
    #print(data)
    return render_template('recommender.html',data=data)
    #return str(user_input)

if __name__=='__main__':
    app.run(debug=True)

