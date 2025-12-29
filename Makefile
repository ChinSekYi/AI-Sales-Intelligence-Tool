install:
	pip install -r requirements.txt

format:
	black .
	isort .

run-fetch:
	python3 -m src.get_news

run-app:
	streamlit run app.py

