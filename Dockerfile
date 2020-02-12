FROM ubuntu

RUN apt-get update && apt-get install haskell-platform curl python3 python3-pip libz-dev libgmp-dev -y
RUN pip3 install pyyaml
RUN curl -sSL https://get.haskellstack.org/ | sh

RUN stack update
RUN stack install fswatch
RUN echo 'extra-deps: \n - haskell-src-exts-1.20.3@sha256:83ae523bbec907a42c043de1f5bbf4c1554e7c3b898af07bb1ce6e80eaa282ec,4589 \n - hflags-0.4.3@sha256:f6b85fc7cbd170787f49225646e62d5589e5dd75abe6f26d16287e5fff3e678e,3121 \n - Glob-0.9.3@sha256:d6f8d3000651a7d72fe468f3840f59fe785dc35cfc16dc76a62821cd798f34dc,2932 \n - fswatch-0.1.0.6@sha256:56fefeb2c72f6d147dacfc864dc30089b8ee3509064e092f69ad3d548197389b,1660 \n - haskell-tools-builtin-refactorings-1.1.1.0@sha256:a532a1bf5d94ae760f64626aea34e402df05bd763ba8038a035e9186e12eb21b,16909 \n - haskell-tools-prettyprint-1.1.1.0@sha256:4178e14d94152e689fd468cd76d9bdca224277f923f2f5b958f7a2fcfc6974db,2110 \n - haskell-tools-refactor-1.1.1.0@sha256:e67268831014311576777cef548fddc16082180c8cba3640d3651cf9a195e864,5776 \n - haskell-tools-ast-1.1.1.0@sha256:b1b761c02423ef83b538ca4fab7273ce2ee46221da3192b5cca5461e9e6ce812,3928 \n - haskell-tools-backend-ghc-1.1.1.0@sha256:4fd177adcfc07f324b09008a572ace1c5340672294dece21edd420b754088ded,3165 \n - haskell-tools-rewrite-1.1.1.0@sha256:d43239b8a64af429bfebdcb1e4f58dcb32e3326b9933cdd20702431534506543,3901 \n - minisat-solver-0.1@sha256:e2ff11b1ca8c66e43f8bb2e04f21bd1b812efb94ff215d74f998c928e7e92dcd,5210 \n - portable-lines-0.1@sha256:21c3b905888a4b43f957cd8e8cdf2af00942bb161aa19a6b20db18b661de0510,1552 ' >> /root/.stack/global-project/stack.yaml

RUN stack install homplexity-0.4.4.3
RUN stack install haskell-tools-daemon haskell-tools-cli
