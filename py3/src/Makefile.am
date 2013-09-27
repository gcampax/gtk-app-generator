NULL =

nodist_bin_SCRIPTS = $(PACKAGE_TARNAME)
nodist_pkgdata_SCRIPTS = $(PACKAGE_NAME)

EXTRA_SCRIPTS = @PACKAGE_NAME@ @PACKAGE_TARNAME@

pydir = $(pkgdatadir)
dist_py_PYTHON = \
	main.py		\
	package.py	\
	util.py		\
	window.py	\
	$(NULL)

$(PACKAGE_TARNAME): $(PACKAGE_TARNAME).in
	$(AM_V_GEN) sed \
		-e "s|[@]PYTHON@|$(PYTHON)|g" \
		-e "s|[@]PACKAGE_NAME@|$(PACKAGE_NAME)|g" \
		-e "s|[@]PACKAGE_VERSION@|$(PACKAGE_VERSION)|g" \
		-e "s|[@]prefix@|$(prefix)|g" \
		-e "s|[@]libdir@|$(libdir)|g" \
		-e "s|[@]pkgdatadir@|$(pkgdatadir)|g" \
		$< > $@
	@chmod +x $@

$(PACKAGE_NAME): $(PACKAGE_NAME).in
	$(AM_V_GEN) sed \
		-e "s|[@]PYTHON@|$(PYTHON)|g" \
		-e "s|[@]PACKAGE_NAME@|$(PACKAGE_NAME)|g" \
		-e "s|[@]PACKAGE_VERSION@|$(PACKAGE_VERSION)|g" \
		-e "s|[@]prefix@|$(prefix)|g" \
		-e "s|[@]libdir@|$(libdir)|g" \
		-e "s|[@]pkgdatadir@|$(pkgdatadir)|g" \
		$< > $@
	@chmod +x $@

EXTRA_DIST = $(PACKAGE_NAME).in $(PACKAGE_TARNAME).in
CLEANFILES = $(PACKAGE_NAME) $(PACKAGE_TARNAME)

-include $(top_srcdir)/git.mk
