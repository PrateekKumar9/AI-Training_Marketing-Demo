# Agentic Campaign Optimization Engine

A Streamlit workshop demo that showcases an "Agent" analyzing marketing campaign data, identifying underperforming segments, rewriting ad creative, and recommending budget reallocations.

## Project Structure
- `app.py` - main Streamlit application shell
- `data/generate_data.py` - dummy marketing data generator with Excel export
- `data/marketing_data.xlsx` - exported sample campaign dataset

## Setup
1. Create a Python environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
streamlit run app.py
```

## Notes
- The data generator creates 500 rows of realistic marketing data.
- A few audience segments are intentionally skewed to appear as clear underperformers.
- This app is designed for iterative improvement throughout the workshop.
