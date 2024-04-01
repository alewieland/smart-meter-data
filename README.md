# Smart Meter Data 

The project aims to collect power consumption from smart meters. As a sample project we will be working with data from CKW, a Utility from central switzerland providing multiple datasets.

## Table of Contents
- [Datasets](#datasets)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Datasets

The Datasets can be found [here](https://www.ckw.ch/landingpages/open-data).
There are multiple datasets, but for this project we will focus primarely on dataset B. The dataset itself is pretty small, but for equally interesting to the the other datasets. And it takes less time to load compared to dataset A.

The Data consists of the following informations:

| timestamp | value_kwh | area_code | num_meter
|----------|----------|----------|----------|
| 2024-03-06T03:45:00.000Z | 266.975249   | 6056  | 102|
| 2024-03-06T04:00:00.000Z | 268.12333   | 6056  | 102 |

The _timestamp_ column comes in the ISO6801 format (as UTC timeformat), the _value\_kwh_ as float, the _area\_code (ZIP code) as integer and the _num\_meter_ also as integer.

The data is updated once a month (unfortunately) but in a productive setting, the possibility of streaming this data might be interessting.
In contrast: Dataset A contains each Smart Meter individually (not aggregated by Zip code) but lacks the locational information.

## Data Pipeline

For this project, I collect the data from the [Homepage](https://open.data.axpo.com/%24web/index.html) using [Mage AI](https://www.mage.ai). The Data Pipeline loads the data from the homepage to Google Cloud Storage (GCS), and in the process cleans it up. From the GCS it is loaded to Google Big Query (BQ) and visualized using Looker Studio.



## Analytics dashboard

Visualisation of the data are created in Looker Studio

One to check the number of records, to visualize if the number of records is constant or which dates are missing data
![Record Count](/img/record_count.png)

And one overview over the consumoption, one total and one grouped first by the first two digits of the zip code to get the general area and a drill down option to get to the zip code level

![Consumption](/img/consumption.png)


If you want to have a look at the report, click [here](https://lookerstudio.google.com/reporting/ae4720d4-07fb-4bde-b1f8-08867130a4ce).


## Installation

Here are the instructions to set up the project (locally and in the cloud)

### Prequisits

I assume you deploy it to google cloud. In case you want to follow along, we need to set up a new project in Google Cloud, and a service account with a .json key. For simplicity, you can define the service account as an owner.

Further you need:
- Docker
- Google cloud sdk
- Terraform [optional]


_Please choose either the local or the cloud path, preferrably the local deployment path, it takes less time :)_
_If you want to check out the Mage AI Readme, go [here](/README_MAGEAI.md)

### Local Deployment

For the local deployment, we can use 
```
git clone https://github.com/alewieland/smart-meter-data.git portfolio-project
&& cd portfolio-project
&& cp dev.env .env
&& docker compose build
&& docker compose up
```

then go to the [localhost](http://localhost:6789) page to enjoy the running instance of Mage.

Proceed to [First steps](#first-steps-in-mage)

### Cloud Deployment

For the cloud deployment, we can use terraform

```
git clone https://github.com/alewieland/smart-meter-data.git portfolio-project
&& cd portfolio-project
&& cp dev.env .env
&& cd mage-ai-terraform-templates
```

Adjust the name of the project and your region in the _variables.tf_ file as shown here:
![here](/img/variablesTF.png)

For futher help on the cloud deployment, Mage has a nice overview [here](https://docs.mage.ai/production/deploying-to-cloud/gcp/setup)

In your terminal you can run ``gcloud auth list``to check if you see the project you just added to the variables.tf file

If everything works, you can run ``terraform init``, ``terraform build`` and ``terrafrom apply``to spin up your server.

### First steps in mage

First, open the config file:
![Config location](/img/Open_config.png =x250)

and then add the key of the service account.
![Credentials](/img/Add_credentials.png).

### Running the pipelines

If you want to run the pipeline, we need to adjust the bucket name and some other variables to make it work...
First open the piplines present and click on edit on the left side
![Pipelines](/img/pipelines.png)

And change the bucket-name, the key path, and the project name where needed.
![Vars](/img/variables_rename.png)

Check that both pipelines are set correct... And try running them and ingest the data to Google Cloud
Otherwise, they are set to run at the start of each month... 


### Google looker studio

See the section [above](#analytics-dashboard) for the results...

To achieve the results, for the drilldown, a new column is created in looker studio by takign just the first two digits of the area_code.


## Usage

Please feel free to give feedback, I'm by far not a good data engineer :)

## Contributing

If you find error, please send a pull request to fix the bug.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE.md) file for details.
