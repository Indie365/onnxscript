# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
# --------------------------------------------------------------------------

import unittest

import onnxscript.testing
from onnxscript import script
from onnxscript.onnx_opset import opset15 as op
from onnxscript.onnx_types import FLOAT
from onnxscript.tests.common import testutils


class TypeAnnotationTest(testutils.TestBase):
    def test_type_annotation(self):
        """Test type annotations."""

        @script()
        def static_shape(A: FLOAT[100], B: FLOAT[100]) -> FLOAT[100]:
            C = op.Add(A, B)
            return C

        static_shape_txt = """
            static_shape (float[100] A, float[100] B) => (float[100] C) {
                C = Add (A, B)
            }
        """
        onnxscript.testing.assert_isomorphic_graph(static_shape, static_shape_txt)

        @script()
        def symbolic_shape(A: FLOAT["N"], B: FLOAT["N"]) -> FLOAT["N"]:  # noqa: F821
            C = op.Add(A, B)
            return C

        symbolic_shape_txt = """
            symbolic_shape (float[N] A, float[N] B) => (float[N] C) {
                C = Add (A, B)
            }
        """
        onnxscript.testing.assert_isomorphic_graph(symbolic_shape, symbolic_shape_txt)

        @script()
        def tensor_scalar(A: FLOAT["N"], B: FLOAT) -> FLOAT["N"]:  # noqa: F821
            C = op.Add(A, B)
            return C

        tensor_scalar_txt = """
            tensor_scalar (float[N] A, float B) => (float[N] C) {
                C = Add (A, B)
            }
        """
        onnxscript.testing.assert_isomorphic_graph(tensor_scalar, tensor_scalar_txt)

        @script()
        def unknown_rank(A: FLOAT[...], B: FLOAT[...]) -> FLOAT[...]:
            C = op.Add(A, B)
            return C

        unknown_rank_txt = """
            unknown_rank (float[] A, float[] B) => (float[] C) {
                C = Add (A, B)
            }
        """
        onnxscript.testing.assert_isomorphic_graph(unknown_rank, unknown_rank_txt)

        with self.assertRaises(ValueError):
            FLOAT[10][20]  # Invalid usage. pylint: disable=pointless-statement

    def test_type_annotation_with_bool_type_for_attribute(self):
        @script()
        def bool_type_for_attribute(self: FLOAT[...], sorted: bool) -> FLOAT[...]:
            out = op.Unique(self, sorted=sorted)
            return out

        bool_type_for_attribute_txt = """
            <
                domain: "this",
                opset_import: ["": 15]
            >
            bool_type_for_attribute <sorted>(self) => (out) {
                out = Unique <sorted: int = @sorted> (self)
            }

        """
        onnxscript.testing.assert_isomorphic_function(
            bool_type_for_attribute, bool_type_for_attribute_txt
        )


class UtilityFunctionsTest(unittest.TestCase):
    def test_pytype_to_input_strings(self):
        pass

if __name__ == "__main__":
    unittest.main()
