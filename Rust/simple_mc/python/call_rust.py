import ctypes
import json

lib = ctypes.CDLL("target/release/libsimple_mc.dylib")

# we don't want ctypes to automatically convert anything to a Python string,
#   as the Rust library owns that memory, and is responsible for
#   releasing it

lib.read_corpus_file.argtypes = [ctypes.c_char_p]
lib.read_corpus_file.restype = ctypes.c_void_p

lib.ext_generate_sentence.argtypes = [ctypes.c_void_p]
lib.ext_generate_sentence.restype = ctypes.c_void_p

# release really expects the char * from above, but we'll call it a void *
lib.release_str.argtypes = [ctypes.c_void_p]


class MarkovGenerator:
    pointer = None
    def __init__(self, fname):
        self.pointer = lib.read_corpus_file( fname )
    def sentence(self):
        p = lib.ext_generate_sentence( self.pointer )
        return ctypes.cast(p, ctypes.c_char_p).value


g = MarkovGenerator("/Users/khervold/Documents/code/Twist-PyCon-2017/Rust/corpus")
print g.sentence()