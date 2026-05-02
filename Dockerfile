FROM archlinux:latest

RUN pacman -Syu --noconfirm --needed \
        git \
        python python-build python-installer \
        python-hatch python-hatch-vcs \
    && pacman -Scc --noconfirm

RUN git config --system --add safe.directory '*'

WORKDIR /workspace
CMD ["bash"]
