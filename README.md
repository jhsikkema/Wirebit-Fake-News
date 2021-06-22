# Bywire Fake News Detection, Truth Indicator, Real-Time Disinformation warning system.

In response to the Sentiment &amp; Opinion Mining Expert.ai and Devpost hackathon opportunity, the Bywire team decided to take the opportunity to complete a pet project which is often under prioritised. This hackathon provides a unique opportunity to use the api of Expert.ai and develop a fake news detection capability. With the help and incentives provided by Expert.ai, this project has today, become a reality.

It is currently running live on the [Bywire.news](https://bywire.news) website, where every single article is now analysed in real-time against the Expert.ai API and a set of custom, Bywire algorithms to combine these Neuro-Linguistic Programming (NLP) capabilities into a trustability score.

Trust, trust and accountability are in great demand, yet there are no objective bearers of truth that people will trust. Partisanship is a central problem to this ambition. With the use of artificial intelligence, Bywire hopes to regain objectivity, impartiality, and most importantly, hopes that Readers will be able to make better informed judgements with a broader set of dispassionate tools at their disposal.

Bywire hopes that this technology will become the new internet standard for online content verification, trust, and creator accountability. In the future, if Readers do not see the Bywire green tick, they will know to be cautious about what they are reading/watching.

There are many additional use cases for this technology. In particular, education could be totally transformed. Trust will allow teachers to educate pupils to be more aware of the mechanisms used to spread fake news and disinformation.

The sheer present of this AI tools will ensure that writers are warned right there in their CMS if the content they are about to publish has been previously flagged as fake.

The project uses NLP, in particular the fantastic Expert.ai tools and API, to turn an article into a feature vector. This feature vector is then transformed and uniformly scaled, by looking for statistical anomalies (e.g., an article provokes more fear than usual). These features are then combined using an Heuristic model and the Bywire Artificial Neural Network (BANN). Both models will increase our understanding over time of fake news. For the neural network to be trained properly we will need manually flagged, human inputted data, which at the moment is limited available, but we are generating this as we speak by allowing users to flag if they disagree with the results of the algorithm.

Using this technique we can build up large volumes of training data over time and improve the model. Since Bywire.news stores all articles on the IPFS, as part of our commitment to decentralisation, and timestamps them on the blockchain in order to allow independent verification of the veracity, we integrated the server and web frontend to allow retrieving directly the article associated with an IPFS document. One can go to the [wirebittoken eos account](https://www.bloks.io/account/wirebittoken)) and copy the article that is part of wirebittoken-publish into the web page and obtain a trust score.


## Technology
The core of the algorithms has been written in Python. We used python-flask to create a rest-api to interface with the algorithm and integrate it with the Bywire.news platform. Machine learning was performed in Keras together with TensorFlow. For the NLP we used Expert.ai, nltk and nrclex. Access to Expert.ai was done using the standard python bindings. As a database we employed Mongodb. Trained ANNs were flushed to the disk using json, and the hd5 formats. For the web frontend we used HTML5, JavaScript, jQuery, Bootstrap 5, Chart.js and PHP. For integration with the Bywire.news platform we used Angular, JavaScript and PHP. Integration with the IPFS was handled using an in house developed IPFS adapter, together with the go-ipfs server. Finally, the algorithms were developed using ubuntu 20.04. In theory they are programmed OS agnostic, but this has not yet been fully tested. Since it was not critical for the prototype user management was excluded. It is however extremely easy to add user management with JWT authentication via flask. The whitepaper is typeset using Latex.

## Expert AI

Expert.AI is an NLP library that improves significantly over standard Python libraries like nltk. Due to the need to parse more than 150k articles currently published at Bywire.news, with an average length of around 1930 characters, we developed a switch to allow processing of the bulk of the articles without Expert.ai until the algorithm is developed into a more mature stage. However, Expert.AI already forms an essential part of the algorithms used. At the moment we are using the sentiment as calculated by Expert.AI, in particular to construct the Euphoria indicator which points to extremely positive or negative sentiment and helps us detect when different NLP libraries give widely different results. We suspect the latter anomaly is a strong indication there is something suspect with the sentiment of an article. Furthermore, Expert.AI is used to detect the lexical complexity of an article. The use of Expert.AI is only limited by the severe lack of time, but the possible uses are limitless as any statistical anomalies that one can detect is worth investigating and using within our censuses. Apart from the measures already used we expect especial benefit in the short-term future from the person/entity/concept densities (i.e., nr persons, nr relevant persons divided by article length).

## Algorithm

To describe the algorithm in the briefest of terms: we use a relatively standard machine learning setup. First, we turn the text of an article, together with its context (where was it published, who was the author) into a feature vector. This is scaled to a uniform range. This benefits the gradient descent methods used in the learning algorithms for ANNs to have eigen values of similar magnitude. Then it is fed into a neural network. At the same time, we constructed a heuristic model to allow us to both display results for a wider range of articles, while we are gathering data from users to learn characteristics of which articles are falsified. It also allows us a better understanding of the role and characteristics of ANNs in fake news detections by investigating the cases where both models have given us significantly different predictions.

The Keras and Tensorflow already automatizes a lot of complexity with learning, overfitting and parameter instability away. So in short for the modelling process:

Text -\&gt; NLP Indicators -\&gt; Features -\&gt; Scaled Features -\&gt; Scores -\&gt; Trust.

We plan to next model using a Convoluted Neural Network (CNN) so we can determine intermediate scores using the machine learning algorithm. Since understanding why something is fake news is probably more important than knowing if something is fake news. The features that are of interest were determined by domain knowledge. Sentiment, both extremely positive and negative, is especially important to us, as fake news needs to trigger an emotional reaction in order to spread further, faster, and convince the maximum number of people. We have enhanced this with NRC sentiment to identify the top angry/fearful articles, since theory dictates that anger, fear and joy are emotions that spread better online, while sadness and trust are emotions that are far less effective at spreading online.

In short, we are looking for articles that were engineered to go viral online.

Further we look at lexical complexity: we expect that fake news is easier to read as it does not make sense to make an article that is hard to be read by the target demographic. Overly complex analysis would trigger thinking using the critical thinking system as defined by Daniel Kahnemann.

Additionally, we look for anomalies in the layout of the article: is it shorter than expected or uses shorter sentences to be more comprehensible.

For more details on how the algorithm was implemented and why, we are developing a whitepaper (included in this GitHub repository) that describes the finer details of the theory behind fake news detections.


### Features

At the moment we use NLP to turn the text into the following features.

They are described in more detail in the [draft whitepaper](https://github.com/Bywire-News-Official/bywire-online-fake-news-ai-ann/blob/main/whitepaper/whitepaper_trust.pdf) and it&#39;s references. The whitepaper explains some fundamental concepts necessary for understanding the theory why the prototype works. However, it definitely needs more development before launching globally, and is under active development.

Please note that this is a proof of concept and some shortcuts where invariably taken to get a working prototype on time. Any statements made are therefore hypotheses, and we not making any claims to their veracity, accuracy or legitimacy. They do offer, however, the Reader an opportunity to understand why a feature may be worth further investigation. Please remember that many features will be refined as we continue our agile development. (e.g., mapping synonyms).

- Sentiment
  - sentiment1. This is the anger minus sadness score from the nrc sentiment as calculated by nrclex, normalized by the spread (10% - 90% confidence interval). The idea that the aim of fake news is to spread virally. On the internet, anger and joy spread while sadness inhibits virality ([as described in one of the first interviews from trendfollowing](https://www.trendfollowing.com/podcast/)). Additionally, anger has the benefit that it induces actions/engagements: [a better explanation can be found here](https://www.smithsonianmag.com/science-nature/what-emotion-goes-viral-fastest-180950182/)
  - sentiment2. This is a more elaborate version of sentiment1 by using anger + fear - sadness - trust scores.
  - Euphoria. This is the maximum of positive euphoria and negative euphoria (depression). These are the positive and negative sentiment scores as calculated by Expert.ai normalized to 1 for the top 10% (90% confidence interval) and a linear increase from the top 50% (median) to the top 10%.
- Complexity
  - word\_length. This is the ratio of length of the clean text (removing punctuation, html and stop words) to the number of words. It was calculated using the nltk library. We suspect that having longer words might make a text harder to read and therefor harder to spread.
  - complexity. This is the ratio between the clean text and the length of stemmed words. It was calculated using the nltk library. When stemmed words are significantly shorter the text is likely to be more complex to read and therefore harder to spread.
  - duplication. This is the ratio between the number of tokens and the number of stemmed tokens. Indicating that certain terms were overly repeated, often enhancing the chances that people remember the message. It was calculated using the nltk library.
- Layout
  - text\_length. The raw number of characters. The idea is that longer text has a harder time to reach a large audience. This is calculated using standard python.
  - punctuation. This is the ratio between the raw text and the clean text. The idea is that it is a rough measure for the length of individual phrases. Longer phrase length makes an article harder to read and therefore harder to spread.

In the calibration step confidence intervals were calculated using the database of Bywire (150k articles from various professional new services) including for each feature only those articles where valid data was available.

These confidence intervals are then used to construct a mapping to map all features to the interval [0, 1] and to have a non-zero slope in the areas of interest. These confidence intervals are calculated for each platform and for all data. This was done as some features are highly platform dependent (e.g. a median of 1900 characters per article makes no sense for twitter), the total data values are a fallback when no or little data is available for a platform. The advantage is that in this way we don&#39;t need to recalculate the features when more data becomes available, and we can change the mapping without changing the underlying features.

## Endpoints

The server is implemented as a rest-api. However, since analysis might take a while and in order to allow asynchronous processing of text we introduced endpoints to post an article, and an endpoint to query whether the article was processed when the results are ready. Additionally, for convenience of the developers, there are endpoints to recalibrate parameters, models and to recalculate scores. Due to the complexity of the project and time constraints, no pacing restrictions were implemented, but it would be high on our priorities list to not allow querying the results or submitting too many requests too often.

However, there is code in place to submit a request only once and if a text or IPFS hash was already submitted its results are retrieved from the database instead of being recalculated again.

- /analyze/text - Submits an article to the server
  - input: {&quot;content&quot;: &quot;Text Goes Here&quot;, &quot;title&quot;: &quot;Title of the article&quot;, &quot;author&quot;: &quot;Author of the article&quot;, &quot;publisher&quot;: &quot;Publisher of the article&quot; &quot;platform&quot;: &quot;Platform that published the article&quot;}
  - output: {&quot;id&quot;: &quot;id to identify request&quot;, &quot;new&quot;: true}
- /analyze/ipfs - Submits an ipfs hash to the server. The corresponding document is retrieved.
  - input: {&quot;ipfs-hash&quot;: &quot;IPFS hash&quot;} \*output: {&quot;id&quot;: &quot;id to identify request&quot;, &quot;new&quot;: true}
- /analyze/flag - Flags an article as fake news
  - input: {&quot;id&quot;: &quot;id identifying the article&quot;, &quot;is\_expert&quot;: &quot;identifies if the user flagging the article was a regular reader or an expert&quot;, &quot;strength&quot;: &quot;flags how fake the news is: 100 is super fake, -100 is very real&quot;}
  - output {&quot;status&quot;: &quot;Status of request&quot;, &quot;done&quot;: true if done}
- /analyze/query - Queries the status of a request using it&#39;s id.
  - input: {&quot;id&quot;: &quot;id identifying the article&quot;}
  - ouptut: {&quot;id&quot;: &quot;id to identify request&quot;, &quot;status&quot;: &quot;Status of processing the request&quot;, &quot;done&quot;: &quot;Whether the reuqest was parsed.&quot;, &quot;data&quot;: json object containing the trust scores, &quot;text&quot;: &quot;if the request was from ipfs the ipfs text is returned&quot;}

The following are very much for development purposes.

- /parameters/calibrate - Calculates the scaling factors and trains the bann.
  - input: {}
- /parameters/clean - Removes old models and scores from the database
  - input: {}
- /parameters/recalculate - Recalculates the feature set.
  - input: {}
- /brew/coffee - Makes it rfc2324 compliant.


The following are very much for development purposes.
* /parameters/calibrate - Calculates the scaling factors and trains the ann.
  * input: {}
* /parameters/clean - Removes old models and scores from the database
  * input: {}
* /parameters/recalculate - Recalculates the feature set.
  * input: {}
* /brew/coffee - Makes it rfc2324 compliant

## Output

{&quot;trust\_score&quot;: 99, &quot;sentiment\_score&quot;: 80, &quot;layout\_score&quot;: 100, &quot;complexity\_score&quot;: 100, &quot;divergence\_score&quot;: 100, &quot;platform\_score&quot;: 100, &quot;author\_score&quot;: 100, &quot;reasons&quot;: [&quot;Provokes Anger&quot;]}


## Team
Jetze Sikkema (Implementation, Algorithm Development &amp; Programming) Michael O&#39;Sullivan (Concept, Product Manager, Algorithm Development (conceptual) Frontend and Psychology)

Examples

Here are some examples of fake news stories and real news stories. The IPFS hashes you can use to load the stories into the Bywire Disinformation Detector are added. The fake news stories were the first ones to appear on a google search for fake news. The real news stories were the first stories that appeared in the Guardian and BBC on the 18th of June 2021. However, we expect the algorithm to not always work this good as these were our first trials.

- Fake News
  - &quot;Pope Franciscus endorses Donald trump&quot;. \*\*Bywire Trust 1 - ipfs: \*\*. A discussion of this article can be found [here](https://www.buzzfeednews.com/article/craigsilverman/the-strangest-fake-news-empire) and  [here](https://www.snopes.com/fact-check/pope-francis-donald-trump-endorsement/)
  - &quot;Biden Calls Trump and Supporters &quot;Dregs of Society&quot;&quot;. \*\*Bywire Trust: 22 - ipfs: . The aricle can be found [here](https://twincitiesbusinessradio.com/content/all/biden-calls-trump-and-supporters-dregs-of-society)
  - &quot;Nancy Pelosi&#39;s Son Was Exec At Gas Company That Did Business In Ukraine&quot;. \*\*Bywire Trust: 14 - ipfs: \*\*
- Real News
  - Juneteenth: After decades, Opal Lee finally gets her day off. \*\*Bywire Trust: 76 - ipfs: \*\*. The article can be found [here](https://www.bbc.com/news/world-us-canada-57536944)
  - HSBC offers sub-1% mortgage as interest rate war intensifies. \*\*Bywire Trust: 86 - ipfs: \*\*. The article can be found [here](https://www.theguardian.com/money/2021/jun/18/hsbc-mortgage-interest-rate-banks-building-societies-house-prices)
  - Praise and condemnation for Iran&#39;s new hardline president. \*\*Bywire Trust: 61 - ipfs \*\*. The article can be found [here](https://www.reuters.com/world/middle-east/praise-disdain-irans-new-hardline-president-2021-06-19/)

Scores may have changed slightly due to better tuning of our algorithm, but the conclusions stay the same.

## HOW IT WORKS

[This](bywire.online) is a demo site as a prototype for fake news detection using expert ai.

An article can be uploaded through this site is converted into a Feature vector using well established criteria [1] for fake news.

1) Usareza Zafrani Xinyi Zhou. &quot;A Survey of Fake News:Fundamental Theories, Detection Methods, and Opportunities&quot;. In: Arxiv 1911.00643 (2020). url: [https://arxiv.org/abs/1812.00315](https://arxiv.org/abs/1812.00315).

