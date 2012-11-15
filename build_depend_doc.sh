sudo apt-get install python-ply
sudo apt-get install doxygen
export PYTHONPATH=$PYTHONPATH:$path/epsilon
doxygen Doxyfile
cd docs/
pdflatex report.tex
