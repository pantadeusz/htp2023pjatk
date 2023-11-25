# How it was done

## Research - available sources

Reading and understanding provided data an links to the resources. After carefull investigation and because of the language barrier, the decision was made to base the demo on the data that was provided.

The focus was on the data about water quality ```Analyser tilførsel til Hålandsvatnet 2023```. There was also an idea to integrate the weather data to the mix, but it was postponed. Next version will include more data and will be more robust.

There was also work done on understanding the domain, for example, what does "TotN" mean.

## Data preparation

The data was prepared to be used in AI DNN model. The process was done for both tables, but the data with dates was more useful.

The preparation was both manual and automatic. The tables had to be transposed. Rows corresponds to the dates of measurements. Columns are for locations and data types.

## Model creation

The model was created using TensorFlow in Python. In the future it is possible to make it in C++ for better performance.

The model is relatively simple - sequential with 3 layers. In the imput, there are three rows of data, and the output is one row, so it is classical approach to the time series analysis.

## Problems solved

There were some usual obstacles that can be seen in data analysis, especially the missing data. It was solved by taking average between previous and next measurements. The columns with unsufficient data are omitted (in the code, there is ```exclude_places=set(['5b', '5c'])`` parameter that selects columns to skip).

## Problems unsolved

There is not enough data to create good predictive model, however we have plan for adressing this problem in case of initial success of the project.

