import ctypes
import argparse

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
    last_sent = None
    def __init__(self, fname):
        self.pointer = lib.read_corpus_file( fname )
    def sentence(self):
        if self.last_sent is not None:
            lib.release_str(self.last_sent)
        self.last_sent = lib.ext_generate_sentence( self.pointer )
        return ctypes.cast(self.last_sent, ctypes.c_char_p).value


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('sentence_count', type=int)
    parser.add_argument('fname')
    args = parser.parse_args()

    g = MarkovGenerator(args.fname)
    for _ in xrange(args.sentence_count):
        print g.sentence()
