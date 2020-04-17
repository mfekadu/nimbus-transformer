#!/bin/bash

# echo $(python3 --version)

function remove_py_filenames() {
  python3 -c "import re; import sys; print(re.sub(r'\s\w*\/?\w*\.py\s', '', sys.stdin.read()), end='')"
}

function print_from_stdin() {
  python3 -c "import sys; \
              print( \
                sys.stdin.read(), \
                end='' \
              )"
}

function print_bytes_from_stdin() {
  # 'Â'
  python3 -c "import sys; print(sys.stdin.buffer.read(), end='')"
}

function extract_first_64_characters() {
  python3 -c "import sys; print(sys.stdin.read()[:64], end='')"
}

function python36_sha256_from_stdin() {
  python3 -c "import sys; \
              import hashlib; \
              sys.stdin.flush(); \
              print( \
                hashlib.sha256( \
                  sys.stdin.buffer.read() \
                ).hexdigest(), \
                end='' \
              )"
}

# # shasum
# # -a, --algorithm   1 (default), 224, 256, 384, 512, 512224, 512256
# # -U, --UNIVERSAL   read in Universal Newlines mode
# #                       produces same digest on Windows/Unix/Mac

# sha256="shasum -a 256 -U"
sha256="python36_sha256_from_stdin"
safe_echo="echo -n"

# To avoid having to change this checksum.sh script in the future
# We greedily read all python files nested byup to 3 directories
file_contents=$(cat *.py */*.py */*/*.py */*/*/*.py 2>/dev/null)
# file_contents="hi"
# echo $file_contents
# sha256('hi')=='8f434346648f6b96df89dda901c5176b10a6d83961dd3c1ac88b59b2dc327aa4'

shasum_of_py_files=$($safe_echo $file_contents | $sha256)
# echo "shasum_of_py_files: " $shasum_of_py_files

# https://unix.stackexchange.com/a/464023
long_sha_string=$($safe_echo $shasum_of_py_files | extract_first_64_characters)

$safe_echo $long_sha_string

# echo "long_sha_string: " $long_sha_string

# shasum_of_shas=$($safe_echo $long_sha_string | $sha256)

# echo "shasum_of_shas: " $shasum_of_shas

# $safe_echo $shasum_of_shas | extract_first_64_characters
