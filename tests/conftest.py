import pytest
from tests.windows_compat import install


install()


@pytest.fixture(autouse=True)
def hardened_direct_mode(request):
    if "direct_vm" not in request.fixturenames:
        yield
        return
    direct_vm = request.getfixturevalue("direct_vm")
    direct_vm.check_pickling = True
    direct_vm.strict_mocks = True
    yield

