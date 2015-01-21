



debug: 
	# build the app in debug mode
	rm -Rf ./build/*
	rm -Rf ./dist/*
	python setup.py py2app -A

release:
	# build the app in release mode
	rm -Rf ./build/*
	rm -Rf ./dist/*
	python setup.py py2app
	mkdir -p Cactus_v000
	
	# copy the additional licenses
	cp -p ./license_PyRSS2Gen.txt ./Cactus_v000/
	cp -p ./licence_feedreader.txt ./Cactus_v000/
	cp -p ./licenses_lxml.txt ./Cactus_v000/
	cp -p ./LICENSE ./Cactus_v000/
	
	# create a readable html from markdown
	
	# markdown README.md >README.html
	# markdown_py -o html5 -f ./Cactus_v000/README.html README.md
	# DO NOT USE mmd !! It's a wrapper that kills the reported options
	# mmd -o ./Cactus_v000/README.html README.md
	multimarkdown -o ./Cactus_v000/README.html README.md

	cp README.md  ./Cactus_v000/
	
	rm -Rf ./Cactus_v000/Cactus.app
	
	mv ./dist/Cactus.app ./Cactus_v000/
	
	# move the release folder to the binary archive
	mv Cactus_v000 ../Cactus-opml-Outliner-binaries/

edit:
	edit Cactus*.py Makefile setup.py
