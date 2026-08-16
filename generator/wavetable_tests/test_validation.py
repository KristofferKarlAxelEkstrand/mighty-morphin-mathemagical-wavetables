"""
Tests for input validation in wavetable generators.
"""

import numpy as np
import pytest

from wavetable_synthesis.core.base_generator import BaseGenerator


class TestInputValidation:
    """Test input validation for generator parameters."""

    def test_validate_u_valid_range(self):
        """Test that valid u values pass validation."""
        # Test valid boundary values
        BaseGenerator._validate_u(0.0)
        BaseGenerator._validate_u(1.0)

        # Test valid middle values
        BaseGenerator._validate_u(0.5)
        BaseGenerator._validate_u(0.25)
        BaseGenerator._validate_u(0.75)

    def test_validate_u_invalid_negative(self):
        """Test that negative u values raise ValueError."""
        with pytest.raises(ValueError, match="must be in range"):
            BaseGenerator._validate_u(-0.1)

        with pytest.raises(ValueError, match="must be in range"):
            BaseGenerator._validate_u(-1.0)

    def test_validate_u_invalid_above_one(self):
        """Test that u values above 1.0 raise ValueError."""
        with pytest.raises(ValueError, match="must be in range"):
            BaseGenerator._validate_u(1.1)

        with pytest.raises(ValueError, match="must be in range"):
            BaseGenerator._validate_u(2.0)

    def test_validate_u_extreme_values(self):
        """Test validation with extreme values."""
        with pytest.raises(ValueError, match="must be in range"):
            BaseGenerator._validate_u(-100.0)

        with pytest.raises(ValueError, match="must be in range"):
            BaseGenerator._validate_u(100.0)

    def test_generator_with_validation(self, any_generator):
        """Test that generators can use validation in their generate methods."""
        # This tests that the validation method is available to generators
        theta = np.linspace(0, 2 * np.pi, 1024)

        # Valid values should work
        result = any_generator.generate(theta, 0.5)
        assert isinstance(result, np.ndarray)

        # Test that generators could use validation if they choose to
        # (though not all generators currently do)
        assert hasattr(any_generator, "_validate_u")


class TestMetadataValidation:
    """Test validation for generator metadata."""

    def test_validate_info_valid_metadata(self):
        """Test that valid metadata passes validation."""
        valid_info = {
            "name": "test_generator",
            "id": "test_generator",
            "description": "A test generator",
            "author": "Test Author",
            "tags": ["test", "example"],
            "collections": ["testing"],
            "keywords": ["test", "keyword"],
            "free": True,
        }
        # Should not raise any exception
        BaseGenerator.validate_info(valid_info)

    def test_validate_info_missing_fields(self):
        """Test that missing required fields raise ValueError."""
        incomplete_info = {
            "name": "test_generator",
            "id": "test_generator",
            # Missing other required fields
        }
        with pytest.raises(ValueError, match="Missing required fields"):
            BaseGenerator.validate_info(incomplete_info)

    def test_validate_info_empty_name(self):
        """Test that empty name raises ValueError."""
        info = {
            "name": "",
            "id": "test_generator",
            "description": "A test generator",
            "author": "Test Author",
            "tags": [],
            "collections": [],
            "keywords": [],
            "free": True,
        }
        with pytest.raises(ValueError, match="name.*non-empty"):
            BaseGenerator.validate_info(info)

    def test_validate_info_wrong_types(self):
        """Test that incorrect field types raise ValueError."""
        # Test with tags as string instead of list
        info = {
            "name": "test_generator",
            "id": "test_generator",
            "description": "A test generator",
            "author": "Test Author",
            "tags": "not a list",  # Wrong type
            "collections": [],
            "keywords": [],
            "free": True,
        }
        with pytest.raises(ValueError, match="tags.*list"):
            BaseGenerator.validate_info(info)

    def test_validate_info_wrong_free_type(self):
        """Test that non-boolean free field raises ValueError."""
        info = {
            "name": "test_generator",
            "id": "test_generator",
            "description": "A test generator",
            "author": "Test Author",
            "tags": [],
            "collections": [],
            "keywords": [],
            "free": "yes",  # Wrong type
        }
        with pytest.raises(ValueError, match="free.*boolean"):
            BaseGenerator.validate_info(info)

    def test_registered_generators_have_valid_metadata(self, any_generator):
        """Test that all registered generators have valid metadata."""
        info = any_generator.get_info()
        # Should not raise any exception
        BaseGenerator.validate_info(info)
