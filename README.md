# fbc_curation

## Installation

Create virtual environment
```bash
pip install virtualenv virtualenvwrapper
mkvirtualenv fbc_curation --python=python3.7
```

Install python dependencies which are listed in `requirements.txt`
```
pip install -r requirements.txt
```

## Testing
To run the tests use
```
pytest
```

## Examples
To run the examples use
```
python examples.py
```

## Curation files
To create FBC curation for a new model use:
```
python fbc_curation.py --model ./models/e_coli_core.xml --out ./results 
```
This creates the FBC curation files for the model in the output folder.


