import pytest

class TestGroupA:
    def test_one(self, class_resource, module_resource, session_resource):
        print("Running TestGroupA.test_one2")

    def test_two(self, class_resource, module_resource, session_resource):
        print("Running TestGroupA.test_two2")


class TestGroupB:
    def test_three(self, class_resource, module_resource, session_resource):
        print("Running TestGroupB.test_three2")

class TestGroupC:
    def test_four(self, class_resource, module_resource, session_resource):
        print("Running TestGroupC.test_four2")

class TestGroupD:
    def test_five(self, class_resource, module_resource, session_resource):
        print("Running TestGroupD.test_five2")