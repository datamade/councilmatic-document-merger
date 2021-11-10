SHELL := /bin/bash
ATTACHMENTS := $(shell python scripts/download_attachments.py)

define decrypt
$(shell pdfinfo $(1) | grep "Encrypted:      yes" > /dev/null 2>&1 &&
	qpdf --decrypt $(1) --replace-input)
endef

clean :
	find attachments -type f -not -name .gitkeep -delete
	find merged -type f -not -name .gitkeep -delete

upload_% : merged/%.pdf
	aws s3 cp $< s3://$$S3_BUCKET_NAME --acl public-read

merged/%.pdf : $(addsuffix .pdf,$(basename $(ATTACHMENTS)))
	$(foreach attachment,$^,$(call decrypt,$(attachment)))
	pdfunite $^ $@

attachments/%.pdf : attachments/%.xlsx
	unoconv -f pdf $<

attachments/%.pdf : attachments/%.doc
	unoconv -f pdf $<

attachments/%.pdf : attachments/%.docx
	unoconv -f pdf $<

attachments/%.pdf : attachments/%.ppt
	unoconv -f pdf $<

attachments/%.pdf : attachments/%.pptx
	unoconv -f pdf $<

attachments/%.pdf : attachments/%.rtf
	unoconv -f pdf $<
