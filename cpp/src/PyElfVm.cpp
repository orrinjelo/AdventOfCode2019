#include <boost/python.hpp>
#include <boost/python/numpy.hpp>

namespace py = boost::python;
namespace np = py::numpy;

#include "vm.h"

class pyVM
{
    public:
        pyVM(int memSize)
        {
            vm_ = new VM(memSize);
        }
        pyVM(PyObject* inputCallback, PyObject* outputCallback, int memSize)
        {
            vm_ = new VM(
                [&inputCallback](std::string s) -> int {
                    return py::call<int>(inputCallback, boost::ref(s));
                    // return 0;
                },
                [&outputCallback](big_int &i) -> void {
                    py::call<void>(outputCallback, i);
                },
                memSize
            );
        };
        ~pyVM()
        {
            delete vm_;
        };

        void loadIntCode(py::list l)
        {
            std::vector<big_int> v(len(l));
            for (int entry=0; entry<len(l); ++entry)
            {
                v[entry] = py::extract<big_int>(l[entry]);
            }
            vm_->loadIntCode(v);
        };

        void execute()
        {
            vm_->execute();
        };

        void reset()
        {
            vm_->reset();
        };

        void terminate()
        {
            vm_->terminate();
        };

    private:
        VM* vm_;
};

BOOST_PYTHON_MODULE(PyElfVm)
{
    // Specify that this module is actually a package.
    py::object package = py::scope();
    package.attr("__path__") = "PyElfVm";
    Py_Initialize();
    np::initialize();

    py::class_<pyVM>("ElfVm", py::init<int>())
        .def( py::init<PyObject*, PyObject*, int>() )
        .def( "load_int_code",   &pyVM::loadIntCode )
        .def( "execute",         &pyVM::execute     )
        .def( "reset",           &pyVM::reset       )
        .def( "terminate",       &pyVM::terminate   )
    ;

}