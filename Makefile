install:
	pip install -r requirements.txt

run:
	. deploy/local-env && cd src && streamlit run app.py
