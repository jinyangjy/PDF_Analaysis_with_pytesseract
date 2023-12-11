<h1>Analysing multiple files with Tesseract-OCR</h1>



<h2>Development of the Parallel process to analyse multiple files</h2>
<p align="center">
<img  width = "450"
src = "https://github.com/jinyangjy/PDF_Analaysis_with_pytesseract/assets/107976566/34658e65-853e-48d2-82dd-378688980a64)">
</p>
For each PDF file, a seperate temporary directory is created, and the PDF is converted into a list of image files. The image processing function are then mapped to the pool of worker processes, while using the "pool.map" function from python's multiprocessing library. This will allow multiple PDF files to be processed concurrently, with each worker process handling a different PDF file 1, 2, and 3. The pool of workers will be responsible to process the image processing functions in parallel. Once all PDF Files have been processsed, the pool is closed.
