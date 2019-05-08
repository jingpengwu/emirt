#include <pybind11/pybind11.h>
#define FORCE_IMPORT_ARRAY
#include "seg.hpp"

namespace py = pybind11;

PYBIND11_MODULE(emirt, m){
    xt::import_numpy();
    m.doc() = R"pbdoc(
        emirt
        ---------

        .. currentmodule:: emirt

        .. autosummary::
            :toctree: _generate

            expand_segment
    )pbdoc";

    m.def("expand_segment", &expand_segment, R"pbdoc(
        Expand segment to shrink the boundary gap
    )pbdoc");

#ifdef VERSION_INFO
    m.attr("__version__") = VERSION_INFO;
#else
    m.attr("__version__") = "dev";
#endif
}
