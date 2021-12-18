import streamlit as st


def app():
    st.title("PBG Airtag analysis")
    st.subheader("Python Biella Group Airtag Sentiment and Text Analysis")

    st.markdown(
        """
                
                This is a simple dashboard designed with the new version of streamlit that aim to analyze the sentiment and the text of tweets regarding Apple Airtag.
                
                """
    )

    st.image(
        "./app/static/images/airtag.png",
        width=800,
    )

    st.markdown(
        """
                ***What is sentiment analysis?***
                
                **What is Sentiment Analysis**

                Sentiment Analysis, or Opinion Mining, is a sub-field of
                Natural Language Processing (NLP) that tries to identify and
                extract opinions within a given text

                The aim of sentiment analysis is to gauge sentiments,
                evaluations, attitudes and emotions of a speaker/writer
                based on the computational treatment of subjectivity in a
                text

                **Why perform sentiment analysis?**

                *   Manage critical posts on social media
                *   Improve the Customer Experience
                *   Assess the impact of sponsorships and CSR activities
                *   Discover new market trends
                *   Maintain the quality of the service on a national,international and global scale

                **Why is so important?**

                Sentiment Analysis enables companies to make sense out of
                data. Thus they are able to elicit vital insights from a vast
                unstructured dataset without having to manually indulge
                with it

                **Challenges**
                * Understanding emotions through text are not always easy.
                Sometimes even humans can get misled
                * A text may contain multiple sentiments all at once
                * Heavy use of emoticons and slangs with sentiment values in
                social media texts like that of Twitter and Facebook also
                makes text analysis difficult

                * A sentence containing positive or negative words could be
                neutral, that is not to express any opinion. In the questions
                or in the conditional sentences:
                – “Can you tell me which Sony camera is good?”
                – “If I can find a good camera in the shop, I will buy it”
                * The use of sarcasm is difficult to grasp:
                – “What a great car! It stopped working in two days.”
                * Some phrases do not have sentiment words but indicate
                anyway an implicit opinion:
                – “After two days of normal usage, the screen became black on the
                bottom”
                
                """
    )
    st.image("./app/static/images/pipeline.png", width=800)
