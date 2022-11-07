# Answers to the Machine Learning Engineer Assesment

Every month, there are thousands of events active on TicketSwap websites. These events range from music festivals to concerts to sporting events, stand up comedy shows and more. To help our users find the events they would like to attend, we try to extract the event lineup, as well as any additional information, from the event titles. 

## Part 1: Building a line up extracting model!

Leveraging the CamemBERT huggingface transformers model, a high precision NER model is built to extract entities from a given event title.
Various problematic cases have been identified and addressed during the development of the model to ensure high quality information extraction.

Apart from artist names, event information such as location, date, time, month and other relevant information regarding the events have also been extracted and classified best to their suitable label.

These additional information can provide an edge over the competitors in helping the company prepare for the event in departments such as marketing, ticketing, planning, prospecting, etc.

The extraction and classification of entities are done after vigourous checking with the help of confidence scores, entity recognition labels along with human intelligence.

## Part 2: Connecting the model with other Microservices!

A RESTful API using FastAPI has been developed around the entity recognition model which can integrated with other microservices on demand.
FastAPI was used because of its exceptional speed, countless functionalities and ease of use.

The solution pretty much remains the same between real-time and offline batch job predictions. As the API takes in a JSON file, the only difference between the two types will be either to take in a string or a list of strings. However, the API has been developed to address both the problems where it can be triggered to a real-time prediciton as well as batch jobs on demand, only a matter of how the pipeline is integrated. More information regarding the input batch files will be helpful to optimise the solution.

## Part 3: Other teams!

The approach taken to develop this model was to maximise information and minimise redundant words. But language is tricky and it can be hard for humans as well, let alone machines. However, care was taken to address this problem and emphasize our aim to maximise information. This was done through:

* Checking entities based on their confidence score through the ranges 90-100%, 90-60%.
* For each of the confidence interval, numerous checks were placed to ensure correct recognition and classification.
* As the confidence scores dipped, the number of checks increased to balance the quality.
* Each of the checks have undergone vigourous testing to understand the behaviour of their funtionality.

The detailed description of the tests are given in the test folder of this repository. The results of the tests are tabularized below:

| Tests    | General | PER    | LOC    | ORG    | MISC  | DATE   |
|----------|---------|--------|--------|--------|-------|--------|
| Accuracy | 83.14%  | 91.67% | 63.12% | 79.19% | 80.1% | 72.22% |

Finally, the overall accuracy for the model was calculated as 76.7%.
It has to be taken into account that accuracy for this model is calculated based on its capability to recognise and classify entities.

As for the recognition capability of the model, the accuracy was calculated as 97.32%.
Classification of entities into their respective label is tricky due to the nuances involved with language.
Nevertheless, with human assistance and constant data collection, both the accuracies can be improved.

### Approaching other teams!

A containerized version of this API using Docker is made available to the other development teams for integrating with the production line.
The docker image can be deployed in a Kubernetes cluster and used as required by the other teams namely, DevOps/MLOps team, Data integration team and Data Scientists.

### Additional data

Additional data is needed for the improvement of the model. However, the model gets better with each prediciton on its own, as it stores the artists data in its database if the artist is not present already.


## Project Implementation

The project was developed with the help of Anaconda, Jupyter Notebook and VSCode in a `python 3.9.` environment.

### Project Setup

```
# create a virtual environment
conda create -n NER python=3.9

# activate the virtual environment
conda activate NER

# install src to run scripts in src folder:
pip install -e .

# install required packages:
pip install -r requirements.txt 

```

### Running the files

```
# run save_model.py to download the weights to your local machine
python src/save_model.py

# run the api app.py
python src/app.py
```
To test the working of the API, after running the command, go to the url http://127.0.0.1:8000/docs .
Give a string for the real-time process and a list of strings for the batch process.

If you have made it this far, Thank You for reading! Good Day!