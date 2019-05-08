#include <pybind11/pybind11.h>
#include "xtensor-python/pytensor.hpp"

template<typename T>
class Segmentation{
    private:
    xt::pytensor<T> seg;
}