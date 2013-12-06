



debug: 
	rm -Rf ./build/*
	rm -Rf ./dist/*
	python setup.py py2app -A

release:
	rm -Rf ./build/*
	rm -Rf ./dist/*
	python setup.py py2app
	mkdir -p Cactus_v000
	
	cp -p ./license_PyRSS2Gen.txt ./Cactus_v000/
	cp -p ./licence_feedreader.txt ./Cactus_v000/
	cp -p ./licenses_lxml.txt ./Cactus_v000/
	cp -p ./LICENSE ./Cactus_v000/
	
	# markdown README.md >README.html
	markdown_py -o html5 -f ./Cactus_v000/README.html README.md
	cp README.md  ./Cactus_v000/
	
	rm -Rf ./Cactus_v000/Cactus.app
	
	mv ./dist/Cactus.app ./Cactus_v000/

edit:
	edit Cactus*.py