_default:
	@echo "make"
sources:
	@echo "make sources"
	mkdir python-Updateinfo
	-mv * python-Updateinfo
	-rm -rf python-Updateinfo/htmlcov
	tar cf - * | gzip --best > python-Updateinfo.tar.gz
	mv python-Updateinfo/*.spec .
