test-app-%: %
	rm -fR $@
	./gtk-app-generator.py \
		-o $(dir $@) \
		-B $(notdir $@) \
		-N "Test app" \
		--summary "This application does nothing" \
		--url http://www.test.com \
		-T $* \
		com.test.Test.$*
	cd $@ && \
	./autogen.sh --prefix=/opt/gnome --libdir=/opt/gnome/lib64 && \
	make && \
	make distcheck && \
	make rpm

LANGUAGES = js py3 vala
SUBDIRS = $(foreach lang,$(LANGUAGES),test-app-$(lang))

test: $(SUBDIRS)

clean:
	rm -fR $(SUBDIRS)

.PHONY: test
