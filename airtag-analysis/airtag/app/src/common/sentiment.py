from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from textblob import TextBlob
from app.src.common.config import AZURE_KEY, AZURE_ENDPOINT


# Authenticate the client using your key and endpoint
def authenticate_client():
    ta_credential = AzureKeyCredential(AZURE_KEY)
    text_analytics_client = TextAnalyticsClient(
        endpoint=AZURE_ENDPOINT, credential=ta_credential
    )
    return text_analytics_client


def azure_sentiment(
    sentence: list = ["Airtags are extremely useful and I love the design"],
):
    client = authenticate_client()
    response = client.analyze_sentiment(documents=sentence)[0]

    print(
        "Overall scores: Positive={0:.2f}; Neutral={1:.2f}; Negative={2:.2f} \n".format(
            response.confidence_scores.positive,
            response.confidence_scores.neutral,
            response.confidence_scores.negative,
        )
    )

    score = TextBlob(sentence[0]).sentiment.polarity

    if score < 0:
        sentiment = "Negative"
    elif score == 0:
        sentiment = "Neutral"
    elif score > 0:
        sentiment = "Positive"

    print("Sentence Sentiment: {}".format(sentiment))
    print("Scores: {0:.2f}".format(score))

    return score


def vader_sentiment_analysis(
    sentence: list = ["Airtags are extremely useful and I love the design"],
):
    vd = SentimentIntensityAnalyzer()
    vader_result = vd.polarity_scores(sentence[0])
    print(
        "Overall scores: Compound={0:.2f}; Negative={1:.2f}; Neutral={2:.2f}; Positive={3:.2f} \n".format(
            vader_result["compound"],
            vader_result["neg"],
            vader_result["neu"],
            vader_result["pos"],
        )
    )

    return vader_result


def getSubjectivity(text: str):
    return TextBlob(text).sentiment.subjectivity


def getPolarity(text: str):
    return TextBlob(text).sentiment.polarity


def getPolarityAnalysis(score: float):
    if score < 0:
        return "Negative"
    elif score == 0:
        return "Neutral"
    elif score > 0:
        return "Positive"


def getSubjectivityAnalysis(score: float):
    if score < 0.50:
        return "Objective"
    elif score == 0.50:
        return "Neutral"
    elif score > 0.50:
        return "Subjective"


def assignQuadrant(pol, subj):
    return pol + " and " + subj
