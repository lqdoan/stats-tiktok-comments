# CITE: https://pypi.org/project/py-vncorenlp/0.0.2/

# Automatically download VnCoreNLP components from the original repository
# and save them in some local working folder
import py_vncorenlp

py_vncorenlp.download_model(save_dir='D:\Desktop\Python\project')

# # Load VnCoreNLP from the local working folder that contains both `VnCoreNLP-1.2.jar` and `models` 
# model = py_vncorenlp.VnCoreNLP(save_dir='/absolute/path/to/vncorenlp')
# # Equivalent to: model = py_vncorenlp.VnCoreNLP(annotators=["wseg", "pos", "ner", "parse"], save_dir='/absolute/path/to/vncorenlp')

# # Annotate a raw corpus
# model.annotate_file(input_file="/absolute/path/to/input/file", output_file="/absolute/path/to/output/file")

# # Annotate a raw text
# model.print_out(model.annotate_text("Ông Nguyễn Khắc Chúc  đang làm việc tại Đại học Quốc gia Hà Nội. Bà Lan, vợ ông Chúc, cũng làm việc tại đây."))


# if __name__ == '__main__':
    