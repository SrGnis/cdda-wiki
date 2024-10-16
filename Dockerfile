FROM ruby:2.3

RUN git clone https://github.com/ShiftaDeband/wayback-machine-downloader /wayback_machine_downloader

ENTRYPOINT [ "ruby", "/wayback_machine_downloader/bin/wayback_machine_downloader" ]
