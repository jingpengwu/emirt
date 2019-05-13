#include <pybind11/pybind11.h>
#include "xtensor-python/pytensor.hpp"

template<typename T, std::size_t N, xt::layout_type L>
class Segmentation: public xt::pytensor<T,N,L>{
    private:
    xt::pytensor<T> seg;

    public:

    // dilate the segmentation with a maximum size
    template <typename T, std::size_t N, xt::layout_type L>
    Segmentation<T,N,L> Segmentation<> dilate(std::size_t s)
    {
        xt::
    }
}