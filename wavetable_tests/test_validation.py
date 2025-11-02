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
        assert hasattr(any_generator, '_validate_u')
