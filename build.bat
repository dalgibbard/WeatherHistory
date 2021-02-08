python -m pip install -U nuitka
#python -m nuitka --mingw64 --show-progress --standalone --plugin-enable=numpy weatherhistory.py
python -m nuitka --mingw64 --show-progress --plugin-enable=numpy --onefile --windows-company-name=FingAZ --windows-product-name=TemperatureHistory --windows-product-version=0.1.0 weatherhistory.py
