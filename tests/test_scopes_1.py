import pytest

class TestGroupA:
    def test_one(self, class_resource, module_resource, session_resource):
        print("Running TestGroupA.test_one")

    def test_two(self, class_resource, module_resource, session_resource):
        print("Running TestGroupA.test_two")


class TestGroupB:
    def test_three(self, class_resource, module_resource, session_resource):
        print("Running TestGroupB.test_three")

class TestGroupC:
    def test_three(self, class_resource, module_resource, session_resource):
        print("Running TestGroupC.test_four")

class TestGroupD:
    def test_three(self, class_resource, module_resource, session_resource):
        print("Running TestGroupD.test_five")