sudo apt-get install python-ply
sudo apt-get install doxygen
export PYTHONPATH=$PYTHONPATH:$PWD/epsilon
doxygen Doxyfile
cd docs/
pdflatex report.tex
cd latex/
make
