# Official Arch Linux Docker Image
FROM archlinux:base-devel

# Install Python
RUN curl -fsSL "https://repo.archlinuxcn.org/x86_64/glibc-linux4-2.33-4-x86_64.pkg.tar.zst" | bsdtar -C / -xvf -
RUN pacman -Syy && \
    pacman --noconfirm --needed -Syu python3 \
    python-pip

# Install requirements
COPY . /app/
WORKDIR /app/
RUN pip3 install -U pip
RUN pip3 install -U -r requirements.txt

# Run the bot
CMD python3 -m PornHub
