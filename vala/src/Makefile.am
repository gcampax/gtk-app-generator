bin_SCRIPTS = @PACKAGE_TARNAME@

programdir = $(prefix)/lib/$(PACKAGE_NAME)
program_PROGRAMS = @PACKAGE_NAME@

@PACKAGE_AM_NAME@_SOURCES = \
	main.vala \
	window.vala \
	util.vala \
	package.vala \
	config.vapi
nodist_@PACKAGE_AM_NAME@_SOURCES = \
	$(top_builddir)/data/@PACKAGE_NAME@.data.c

@PACKAGE_AM_NAME@_VALAFLAGS = \
        --target-glib=2.38 \
	--pkg gtk+-3.0 \
	--pkg gdk-3.0 \
	--pkg gdk-pixbuf-2.0 \
        --gresources=$(top_builddir)/data/@PACKAGE_NAME@.data.gresource.xml
@PACKAGE_AM_NAME@_CPPFLAGS = \
	-DPREFIX=\"$(prefix)\" \
	-DLIBDIR=\"$(libdir)\" \
	-DDATADIR=\"$(datadir)\" \
	$(DEPS_CFLAGS)
@PACKAGE_AM_NAME@_LDFLAGS = $(DEPS_LIBS)

-include $(top_srcdir)/git.mk
