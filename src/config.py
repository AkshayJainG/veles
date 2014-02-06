"""
Created on May 28, 2013

Global configuration variables.

@author: Kazantsev Alexey <a.kazantsev@samsung.com>
"""


import numpy
import error
import os


global sconfig
global _sconfig_empty


class Config(object):
    """Config service class.
    """
    def __getattr__(self, name):
        return _sconfig_empty


# : Global config
sconfig = Config()

# : Default config value
_sconfig_empty = Config()


def getConfig(value, default_value=None):
    """Gets value from global config.
    """
    if(value == _sconfig_empty):
        return default_value
    return value


# : Supported float types as OpenCL => numpy dictionary.
dtypes = {"float": numpy.float32, "double": numpy.float64,
          "float2": numpy.complex64, "double2": numpy.complex128}

# : Complex type
# c_dtype = "float"  # for real single precision numbers
c_dtype = "double"  # for real numbers
# c_dtype = "double2"  # for complex numbers
# c_dtype = "double4"  # for quad numbers (not implemented)

# : Complex type to real type mapping
dtype_map = {"float": "float", "double": "double",
             "float2": "float", "double2": "double"}

# : Real type
dtype = dtype_map[c_dtype]

# : CL defines
cl_defines = {"float":      {"dtype": "float",
                             "c_dtype": "float",
                             "sizeof_dtype": 4,
                             "sizeof_c_dtype": 4},
              "double":     {"dtype": "double",
                             "c_dtype": "double",
                             "sizeof_dtype": 8,
                             "sizeof_c_dtype": 8},
              "float2":     {"dtype": "float",
                             "c_dtype": "float2",
                             "sizeof_dtype": 4,
                             "sizeof_c_dtype": 8},
              "double2":    {"dtype": "double",
                             "c_dtype": "double2",
                             "sizeof_dtype": 8,
                             "sizeof_c_dtype": 16}}

# : Supported int types as OpenCL => numpy dictionary.
itypes = {"char": numpy.int8, "short": numpy.int16, "int": numpy.int32,
          "long": numpy.int64,
          "uchar": numpy.uint8, "ushort": numpy.uint16, "uint": numpy.uint32,
          "ulong": numpy.uint64}


# : Allowable types for automatic conversion for use in OpenCL
# (automatic conversion implemeted in formats.py).
convert_map = {numpy.float32: numpy.float64, numpy.float64: numpy.float32,
               numpy.complex64: numpy.complex128,
               numpy.complex128: numpy.complex64}


# : Map between numpy types and opencl.
def numpy_dtype_to_opencl(dtype):
    if dtype == numpy.float32:
        return "float"
    if dtype == numpy.float64:
        return "double"
    if dtype == numpy.complex64:
        return "float2"
    if dtype == numpy.complex128:
        return "double2"
    if dtype == numpy.int8:
        return "char"
    if dtype == numpy.int16:
        return "short"
    if dtype == numpy.int32:
        return "int"
    if dtype == numpy.int64:
        return "long"
    if dtype == numpy.uint8:
        return "uchar"
    if dtype == numpy.uint16:
        return "ushort"
    if dtype == numpy.uint32:
        return "uint"
    if dtype == numpy.uint64:
        return "ulong"
    raise error.ErrNotExists()


# Directories

# : Directory with config.py itself
this_dir = os.path.dirname(__file__)
if not this_dir:
    this_dir = "."

# : Directory for cache
cache_dir = os.path.join(this_dir, "../cache")
try:
    os.mkdir(cache_dir)
except OSError:
    pass

# : Directory for OpenCL source files
ocl_dirs = os.environ.get("VELES_OPENCL_DIRS", "").split(":") + \
           [os.path.join(this_dir, "../ocl")]

# : Directory where to save snapshots
snapshot_dir = os.path.join(this_dir, "../snapshots")
try:
    os.mkdir(snapshot_dir)
except OSError:
    pass

# : Directory where functional tests large datasets reside
test_dataset_root = "/data/veles"


# : Disabled plotters or not (for benchmarking purposes)
plotters_disabled = False

# : If plotters.py is in server mode
plotters_in_server_mode = False

# : If the program has been run in slave mode
is_slave = False


# : Test opencl device for optimal BLOCK_SIZE or not
test_known_device = False
test_unknown_device = True


# : For debugging purposes
unit_test = False


def get_itype_from_size(size, signed=True):
    """Get integer type from size.
    """
    if signed:
        if size < 128:
            return "char"
        if size < 32768:
            return "short"
        if size < 2147483648:
            return "int"
        return "long"
    if size < 256:
        return "uchar"
    if size < 65536:
        return "ushort"
    if size < 4294967296:
        return "uint"
    return "ulong"
