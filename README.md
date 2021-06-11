# Wirebit-Fake-News
This is our server to analyze and detect fake news
## Algorithm
Several features are build based on domain knowledge.
* Sentiment, top 10% angry likely fake.
* Lexical complexity.
* Capitalization.
* Certain words
These are fed to an deep learning ann. 

## Input
/analyze
{"text": "Text Goes Here"}

## Output
{"trust": 99, "distrust-vectors": {"sentiment": 99, "complexity": 80}}
{"trust": 99, "distrust-vectors": [{"type": "sentiment",  "score": 99},
	      			   {"type": "complexity", "score": 70}]
}

## Requirements

## Installation

To install Wirebits-EOS-API run sudo install.sh


## Running the API
./start.sh

To test if the API is setup and working correctly
pytest -v

## Structure
* src/wirebit Contains the c++ source and compiled contract of the wirebit token. To compile it one needs the cleos.cdt and run ./make.sh

* src/Source Contains the source of the rest api to interface with both cleos and rcp interfaces.

