git clone https://github.com/UrosMatijas/FBQATest.git
cd <repo-folder>

# ako zelite venv
python -m venv menv
# Linux/macOS
source menv/bin/activate
# Windows
menv\Scripts\activate

pip install -r requirements.txt
playwright install
pytest -q

# UrosMatijasevicQAFBTest2.pdf je Zadatak 2 - manuelni deo

