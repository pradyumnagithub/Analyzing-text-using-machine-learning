import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfVectorizer

class DetectSpam:
    def spam_analysis(self, text):
        # Loading the dataset
        data = pd.read_csv("C:/Users/prady/Desktop/Project/Dependencies/SpamCollection", sep="\t", names=["Status", "Message"])

        # Replacing spam with 1 and ham with 0
        answer = ["Not Spam", "Spam"]

        data.loc[data["Status"]=='spam', 'Status'] = 1
        data.loc[data["Status"]=='ham', 'Status'] = 0

        data_x = data["Message"]
        data_y = data["Status"]

        x_train, x_test, y_train, y_test = train_test_split(data_x, data_y, test_size=0.2)

        # Converting the message string data into representative numbers
        cv = TfidfVectorizer(min_df=1, stop_words='english')
        x_train_cv = cv.fit_transform(x_train)
        x_test_cv = cv.transform(x_test)

        # Creating the model and using that
        mnb = MultinomialNB()
        y_train = y_train.astype('int')

        mnb.fit(x_train_cv, y_train)

        # Huge data prediction
        # predictions = mnb.predict(x_test_cv)
        # print(predictions)
        # print(np.array(y_test))

        # One message prediction
        data = [text]
        data_cv = cv.transform(data)
        pred = mnb.predict(data_cv)
        
        return answer[pred[0]]

if __name__ == "__main__":
    s = DetectSpam()
    print(s.spam_analysis(open('C:/Users/prady/Desktop/Project/Dependencies/read.txt', encoding='utf-8').read()))

